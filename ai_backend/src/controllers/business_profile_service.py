import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schema.business import Business
from src.schema.business_analysis import BusinessAnalysis
from src.schema.business_profile import BusinessProfile
from src.schema.government_schemes import GovernmentScheme
from src.schema.scheme_embedding import SchemeEmbedding

from src.utils.ai_utils import get_gemini_client
from src.config.config import GEMINI_MODEL_NAME
from src.services.scheme_embedding import generate_embedding
from src.utils.translator_utils import Translator

client = get_gemini_client()


def build_business_context(
    business: Business, analysis: BusinessAnalysis
) -> dict[str, Any]:
    return {
        "business": {
            "business_id": business.id,
            "business_name": getattr(business, "business_name", None),
            "category": getattr(business, "category", None),
            "description": getattr(business, "description", None),
            "state": getattr(business, "state", None),
            "district": getattr(business, "district", None),
            "block": getattr(business, "block", None),
            "village": getattr(business, "village", None),
            "status": getattr(business, "status", None),
        },
        "analysis": {
            "population": getattr(analysis, "population_payload", None),
            "competitors": getattr(analysis, "competitor_payload", None),
            "market_price": getattr(analysis, "market_price_payload", None),
            "supply_chain": getattr(analysis, "supply_chain_payload", None),
        },
    }


def build_embedding_text(
    business_profile: dict[str, Any], eligibility_profile: dict[str, Any]
) -> str:
    return (
        "Business Profile:\n"
        f"{json.dumps(business_profile, ensure_ascii=False, indent=2)}\n\n"
        "Eligibility Profile:\n"
        f"{json.dumps(eligibility_profile, ensure_ascii=False, indent=2)}"
    )


async def generate_profile_with_gemini(context: dict) -> dict:
    prompt = f"""
You are a business profiling system. Create a structured business profile from the supplied context.
Focus on business sector, stage, financial needs, risks, and potential government support categories.
Return ONLY valid JSON matching this structure:
{{
  "business_type": "", "sector": "", "sub_sector": "", "business_stage": "",
  "financial_needs": [], "risks": [], "support_categories": [], "scheme_search_keywords": []
}}
Context: {json.dumps(context, ensure_ascii=False, indent=2)}
"""
    if hasattr(client, "aio"):
        response = await client.aio.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
    else:
        response = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
    return json.loads(response.text)


async def search_similar_schemes_async(
    db: AsyncSession, query_embedding: list[float], limit: int = 10
):
    distance = SchemeEmbedding.embedding.cosine_distance(query_embedding)
    similarity = (1 - distance).label("similarity")

    stmt = (
        select(GovernmentScheme, similarity)
        .join(SchemeEmbedding, SchemeEmbedding.scheme_id == GovernmentScheme.id)
        .order_by(distance)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.all()


async def process_profile_and_recommendations(
    db: AsyncSession,
    business_id: str,
    eligibility_data: dict[str, Any],
    target_language: str = "en",
    limit: int = 10,
):
    # 1. Fetch Business & Analysis
    business = (
        (await db.execute(select(Business).where(Business.id == business_id)))
        .scalars()
        .first()
    )
    if not business:
        raise ValueError("Business not found")

    analysis = (
        (
            await db.execute(
                select(BusinessAnalysis)
                .where(BusinessAnalysis.business_id == business_id)
                .order_by(BusinessAnalysis.version.desc())
            )
        )
        .scalars()
        .first()
    )

    if not analysis:
        raise ValueError("No business analysis found for this business")

    # 2. Generate AI Profile & Combine with Eligibility
    context = build_business_context(business, analysis)
    ai_business_profile = await generate_profile_with_gemini(context)

    eligibility_profile = {
        "state": getattr(business, "state", None),
        "business_type": getattr(business, "category", None),
        "business_stage": getattr(business, "status", None),
        **eligibility_data,
    }

    embedding_text = build_embedding_text(ai_business_profile, eligibility_profile)

    # 3. Generate Embedding & Search Schemes
    query_vector = generate_embedding(embedding_text)
    raw_results = await search_similar_schemes_async(db, query_vector, limit)

    english_schemes = []
    for scheme, similarity_score in raw_results:
        english_schemes.append(
            {
                "scheme_id": scheme.id,
                "name": scheme.scheme_name,
                "description": getattr(scheme, "details", None),
                "benefits": getattr(scheme, "benefits", None),
                "eligibility_criteria": getattr(scheme, "eligibility", None),
                "similarity_score": round(float(similarity_score), 4),
            }
        )

    # 4. Translate Schemes (if applicable)
    translated_schemes = None
    if target_language.lower() not in ["en", "english"]:
        try:
            translator = Translator()
            translated_schemes = translator.translate_json(
                english_schemes, target_language=target_language
            )
        except Exception as e:
            pass

    # 5. Upsert directly into BusinessProfile table
    existing_profile = (
        (
            await db.execute(
                select(BusinessProfile).where(
                    BusinessProfile.business_id == business_id
                )
            )
        )
        .scalars()
        .first()
    )

    if existing_profile:
        existing_profile.analysis_id = analysis.id
        existing_profile.business_profile = ai_business_profile
        existing_profile.eligibility_profile = eligibility_profile
        existing_profile.embedding_text = embedding_text
        existing_profile.target_language = target_language
        existing_profile.recommended_schemes = english_schemes
        existing_profile.translated_schemes = translated_schemes
    else:
        new_profile = BusinessProfile(
            business_id=business_id,
            analysis_id=analysis.id,
            business_profile=ai_business_profile,
            eligibility_profile=eligibility_profile,
            embedding_text=embedding_text,
            target_language=target_language,
            recommended_schemes=english_schemes,
            translated_schemes=translated_schemes,
        )
        db.add(new_profile)

    await db.commit()

    return {
        "analysis_id": analysis.id,
        "business_profile": ai_business_profile,
        "eligibility_profile": eligibility_profile,
        "original_english_schemes": english_schemes,
        "translated_schemes": translated_schemes,
    }
