import asyncio
import json
from fastapi import APIRouter, Depends, HTTPException, Query
from enum import Enum

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.config.database import get_db
from src.middlewares.role import require_enterpreneur
from src.schema.business import Business
from src.schema.business_analysis import BusinessAnalysis
from src.schema.business_profile import BusinessProfile
from src.schema.business_profile_translation import BusinessProfileTranslation
from src.schema.business_report_chunk import BusinessReportChunk
from src.schema.chat import ChatMessage, ChatMessageTranslation, ChatSession
from src.schema.enterpreneur import Enterpreneur
from src.schema.financial_analysis import FinancialAnalysis
from src.schema.finance_translation import FinancialAnalysisTranslation
from src.schema.report_translations import ReportLanguage, ReportTranslation

from src.controllers.translator_service import translate_feasibility_report
from src.controllers.business_profile_service import (
    create_profile_translation,
    normalize_language,
)
from src.controllers.finance_service import create_financial_translation
from src.utils.translator_utils import Translator

router = APIRouter()


def resolve_lang_code(language: str) -> str:
    lang = language.strip().lower()
    if lang in ["bn", "ben", "bengali"]:
        return "bn"
    if lang in ["hi", "hin", "hindi"]:
        return "hi"
    if lang in ["ta", "tam", "tamil"]:
        return "ta"
    if lang in ["te", "tel", "telugu"]:
        return "te"
    return "en"


import logging

logger = logging.getLogger(__name__)


def get_localized(field, lang_code: str) -> tuple[str, bool]:
    """
    Safely extract a localized string from a JSONB field.
    Returns a tuple of (localized_text, was_modified_flag).
    """
    if not field:
        return "", False

    if isinstance(field, str):
        try:
            parsed = json.loads(field)
            if isinstance(parsed, dict):
                field = parsed
            else:
                return field, False
        except Exception:
            return field, False

    if isinstance(field, dict):
        mapping = {
            "en": ["en", "english"],
            "hi": ["hi", "hindi", "hin"],
            "bn": ["bn", "bengali", "ben"],
            "ta": ["ta", "tamil", "tam"],
            "te": ["te", "telugu", "tel"],
        }

        variants = mapping.get(lang_code, [lang_code])
        for v in variants:
            if v in field and field[v] and str(field[v]).strip():
                return str(field[v]).strip(), False

        # Find base text to translate from (preferably English)
        base_text = ""
        for fallback in ["en", "english", "hi", "bn"]:
            if fallback in field and field[fallback] and str(field[fallback]).strip():
                base_text = str(field[fallback]).strip()
                break

        if not base_text and field:
            for val in field.values():
                if val and str(val).strip():
                    base_text = str(val).strip()
                    break

        # Translate on-the-fly if missing
        if base_text and lang_code != "en":
            try:
                translator = Translator()
                translated = translator.translate(
                    text=base_text,
                    source_language="en",
                    target_language=lang_code,
                )
                if translated and translated.strip():
                    field[lang_code] = translated.strip()
                    return translated.strip(), True
            except Exception as e:
                logger.error(f"On-the-fly translation failed for {lang_code}: {e}")
                return base_text, False

        return base_text, False

    return str(field or "").strip(), False


async def get_owned_business(
    business_id: str,
    entrepreneur: Enterpreneur,
    db: AsyncSession,
) -> Business:
    result = await db.execute(
        select(Business).where(
            Business.id == business_id,
            Business.owner_id == entrepreneur.user_id,
        )
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found.")
    return business


async def get_latest_analysis(
    business_id: str,
    db: AsyncSession,
) -> BusinessAnalysis:
    result = await db.execute(
        select(BusinessAnalysis)
        .where(BusinessAnalysis.business_id == business_id)
        .order_by(BusinessAnalysis.version.desc())
        .limit(1)
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="No feasibility report found for this business.",
        )
    return analysis


@router.get("/businesses/{business_id}")
async def get_business(
    business_id: str,
    language: str = Query("en"),
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    business = await get_owned_business(business_id, entrepreneur, db)
    lang_code = resolve_lang_code(language)

    # Helper to extract English/base value
    def get_source_value(field):
        if not field:
            return ""

        if isinstance(field, str):
            try:
                parsed = json.loads(field)
                if isinstance(parsed, dict):
                    field = parsed
                else:
                    return field.strip()
            except Exception:
                return field.strip()

        if isinstance(field, dict):
            for key in ["en", "english"]:
                value = field.get(key)
                if value and str(value).strip():
                    return str(value).strip()

            # Fallback to any existing value
            for value in field.values():
                if value and str(value).strip():
                    return str(value).strip()

        return str(field or "").strip()

    # Translate a JSONB field and return the updated value + whether DB changed
    def translate_field(field):
        if not field:
            return "", field, False

        # Convert JSON string into dict if possible
        if isinstance(field, str):
            try:
                parsed = json.loads(field)
                if isinstance(parsed, dict):
                    field = parsed
                else:
                    # Existing DB value is plain text
                    source = field.strip()

                    if lang_code == "en":
                        return source, field, False

                    translated = translator.translate(
                        text=source,
                        source_language="en",
                        target_language=lang_code,
                    )

                    if translated and translated.strip():
                        new_field = {
                            "en": source,
                            lang_code: translated.strip(),
                        }
                        return translated.strip(), new_field, True

                    return source, field, False
            except Exception:
                source = field.strip()

                if lang_code == "en":
                    return source, field, False

                try:
                    translated = translator.translate(
                        text=source,
                        source_language="en",
                        target_language=lang_code,
                    )

                    if translated and translated.strip():
                        new_field = {
                            "en": source,
                            lang_code: translated.strip(),
                        }
                        return translated.strip(), new_field, True

                except Exception as e:
                    logger.error(f"Translation failed for {lang_code}: {e}")

                return source, field, False

        # JSONB/dict field
        if isinstance(field, dict):
            # Requested language already exists
            existing = field.get(lang_code)

            if existing and str(existing).strip():
                return str(existing).strip(), field, False

            source = get_source_value(field)

            if not source:
                return "", field, False

            if lang_code == "en":
                return source, field, False

            try:
                translated = translator.translate(
                    text=source,
                    source_language="en",
                    target_language=lang_code,
                )

                if translated and translated.strip():
                    translated = translated.strip()

                    # Create a NEW dictionary so SQLAlchemy detects
                    # the JSONB modification.
                    updated_field = dict(field)
                    updated_field[lang_code] = translated

                    return translated, updated_field, True

            except Exception as e:
                logger.error(f"Business field translation failed ({lang_code}): {e}")

            return source, field, False

        return str(field).strip(), field, False

    translator = Translator()

    # Keep original values
    business_name, new_business_name, changed_name = translate_field(
        business.business_name
    )
    category, new_category, changed_category = translate_field(business.category)
    description, new_description, changed_description = translate_field(
        business.description
    )
    village, new_village, changed_village = translate_field(business.village)
    district, new_district, changed_district = translate_field(business.district)
    city, new_city, changed_city = translate_field(business.city)
    state, new_state, changed_state = translate_field(business.state)
    country, new_country, changed_country = translate_field(business.country)

    # Persist newly generated translations
    if changed_name:
        business.business_name = new_business_name

    if changed_category:
        business.category = new_category

    if changed_description:
        business.description = new_description

    if changed_village:
        business.village = new_village

    if changed_district:
        business.district = new_district

    if changed_city:
        business.city = new_city

    if changed_state:
        business.state = new_state

    if changed_country:
        business.country = new_country

    has_changes = any(
        [
            changed_name,
            changed_category,
            changed_description,
            changed_village,
            changed_district,
            changed_city,
            changed_state,
            changed_country,
        ]
    )

    if has_changes:
        db.add(business)
        await db.commit()
        await db.refresh(business)

    return {
        "business_id": business.id,
        "business_name": business_name,
        "category": category,
        "margin_capital": business.margin_capital,
        "description": description,
        "location": {
            "village": village,
            "district": district,
            "city": city,
            "state": state,
            "country": country,
            "pincode": business.pincode,
            "latitude": business.latitude,
            "longitude": business.longitude,
        },
        "status": (
            business.status.value
            if hasattr(business.status, "value")
            else business.status
        ),
        "created_at": (
            business.created_at.isoformat() if business.created_at else None
        ),
        "updated_at": (
            business.updated_at.isoformat() if business.updated_at else None
        ),
    }


@router.get("/businesses/{business_id}/report")
async def get_business_report(
    business_id: str,
    language: str = Query("english"),
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    await get_owned_business(business_id, entrepreneur, db)
    analysis = await get_latest_analysis(business_id, db)
    requested_language = language.strip().lower()

    evidence = {
        "population": analysis.population_payload,
        "competitors": analysis.competitor_payload,
        "market_price": analysis.market_price_payload,
        "supply_chain": analysis.supply_chain_payload,
        "transportation": analysis.transportation_payload,
        "seasonality": analysis.seasonality_payload,
    }

    if requested_language in ["en", "english"]:
        return {
            "analysis_id": analysis.id,
            "version": analysis.version,
            "language": "english",
            "report_markdown": analysis.report_markdown,
            "raw_evidence": evidence,
        }

    try:
        report_language = ReportLanguage(requested_language)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Supported languages: english, hindi, bengali.",
        ) from exc

    translation_result = await db.execute(
        select(ReportTranslation).where(
            ReportTranslation.report_id == analysis.id,
            ReportTranslation.language == report_language,
        )
    )
    translation = translation_result.scalar_one_or_none()

    if not translation:
        try:
            translated_result = await asyncio.to_thread(
                translate_feasibility_report,
                report_markdown=analysis.report_markdown,
                raw_evidence=evidence,
                target_language=requested_language,
            )
            translated_evidence = translated_result["raw_evidence"]
            translation = ReportTranslation(
                report_id=analysis.id,
                language=report_language,
                content=translated_result["report_markdown"],
                population_payload=translated_evidence.get("population"),
                competitor_payload=translated_evidence.get("competitors"),
                market_price_payload=translated_evidence.get("market_price"),
                supply_chain_payload=translated_evidence.get("supply_chain"),
                transportation_payload=translated_evidence.get("transportation"),
                seasonality_payload=translated_evidence.get("seasonality"),
            )
            db.add(translation)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to translate report: {str(e)}"
            )

    if not translation.content:
        try:
            translated_result = await asyncio.to_thread(
                translate_feasibility_report,
                report_markdown=analysis.report_markdown,
                raw_evidence=evidence,
                target_language=requested_language,
            )

            translated_evidence = translated_result["raw_evidence"]

            # Update existing translation
            translation = await db.scalar(
                select(ReportTranslation).where(
                    ReportTranslation.report_id == analysis.id,
                    ReportTranslation.language == report_language,
                )
            )

            if not translation:
                raise HTTPException(
                    status_code=404,
                    detail="Translation record not found",
                )

            translation.content = translated_result["report_markdown"]
            translation.population_payload = translated_evidence.get("population")
            translation.competitor_payload = translated_evidence.get("competitors")
            translation.market_price_payload = translated_evidence.get("market_price")
            translation.supply_chain_payload = translated_evidence.get("supply_chain")
            translation.transportation_payload = translated_evidence.get(
                "transportation"
            )
            translation.seasonality_payload = translated_evidence.get("seasonality")

            await db.commit()
            await db.refresh(translation)

        except HTTPException:
            await db.rollback()
            raise

        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to translate report: {str(e)}",
            )

    return {
        "analysis_id": analysis.id,
        "version": analysis.version,
        "language": requested_language,
        "report_markdown": translation.content,
        # "raw_evidence": {
        #     "population": translation.population_payload,
        #     "competitors": translation.competitor_payload,
        #     "market_price": translation.market_price_payload,
        #     "supply_chain": translation.supply_chain_payload,
        #     "transportation": translation.transportation_payload,
        #     "seasonality": translation.seasonality_payload,
        # },
    }


class ReportPayloadType(str, Enum):
    all = "all"
    population = "population"
    competitors = "competitors"
    market_price = "market_price"
    supply_chain = "supply_chain"
    transportation = "transportation"
    seasonality = "seasonality"


@router.get("/businesses/{business_id}/report/evidence")
async def get_report_evidence(
    business_id: str,
    language: str = Query("en"),
    payload_type: ReportPayloadType = Query(ReportPayloadType.all),
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    await get_owned_business(business_id, entrepreneur, db)
    analysis = await get_latest_analysis(business_id, db)

    # Resolve requested language safely
    lang_input = language.strip().lower()

    lang_code_map = {
        "en": "en",
        "english": "en",
        "eng": "en",
        "hi": "hi",
        "hin": "hi",
        "hindi": "hi",
        "bn": "bn",
        "ben": "bn",
        "bengali": "bn",
    }
    lang_code = lang_code_map.get(lang_input, "en")

    report_lang_map = {"hi": ReportLanguage.hindi, "bn": ReportLanguage.bengali}

    evidence = {
        "population": analysis.population_payload,
        "competitors": analysis.competitor_payload,
        "market_price": analysis.market_price_payload,
        "supply_chain": analysis.supply_chain_payload,
        "transportation": analysis.transportation_payload,
        "seasonality": analysis.seasonality_payload,
    }
    translation_fields = {
        "population": "population_payload",
        "competitors": "competitor_payload",
        "market_price": "market_price_payload",
        "supply_chain": "supply_chain_payload",
        "transportation": "transportation_payload",
        "seasonality": "seasonality_payload",
    }

    if payload_type != "all" and payload_type not in evidence:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported payload_type: {payload_type}",
        )

    # 1. Return Original English Evidence (No translation needed)
    if lang_code == "en":
        if payload_type != "all":
            return {
                "analysis_id": analysis.id,
                "version": analysis.version,
                "language": "en",
                "payload_type": payload_type,
                "payload": evidence[payload_type],
            }

        return {
            "analysis_id": analysis.id,
            "version": analysis.version,
            "language": "en",
            "radius_km": analysis.radius_km,
            "coordinates": {
                "latitude": analysis.latitude,
                "longitude": analysis.longitude,
            },
            "evidence": evidence,
        }

    # 2. Handle Translations using ReportTranslation Table
    target_enum = report_lang_map.get(lang_code)
    if not target_enum:
        raise HTTPException(
            status_code=400, detail="Language not supported for report evidence."
        )

    # Check if a translation record already exists for this report & language
    result = await db.execute(
        select(ReportTranslation).where(
            ReportTranslation.report_id == analysis.id,
            ReportTranslation.language == target_enum,
        )
    )
    translation = result.scalar_one_or_none()

    # Create empty translation record if none exists
    if not translation:
        translation = ReportTranslation(report_id=analysis.id, language=target_enum)
        db.add(translation)

    translator = Translator()

    async def translate_payload(payload):
        """Recursively translates nested JSON values into a pure target-language structure."""
        if not payload:
            return payload
        if isinstance(payload, dict):
            return {k: await translate_payload(v) for k, v in payload.items()}
        if isinstance(payload, list):
            return [await translate_payload(v) for v in payload]
        if isinstance(payload, str) and payload.strip():
            try:
                translated_text = await asyncio.to_thread(
                    translator.translate,
                    text=payload.strip(),
                    source_language="en",
                    target_language=lang_code,
                )
                return translated_text.strip() if translated_text else payload
            except Exception as e:
                logger.error(f"Evidence translation failed for {lang_code}: {e}")
                return payload
        return payload

    # 3. Translate and return only the requested payload
    if payload_type != "all":
        translation_field = translation_fields[payload_type]
        current_payload = getattr(translation, translation_field)

        if not current_payload and evidence[payload_type]:
            current_payload = await translate_payload(evidence[payload_type])
            setattr(translation, translation_field, current_payload)
            await db.commit()
            await db.refresh(translation)

        return {
            "analysis_id": analysis.id,
            "version": analysis.version,
            "language": lang_input,
            "payload_type": payload_type,
            "payload": current_payload,
        }

    # 4. Translate and return all missing evidence payloads
    updated = False
    translated_evidence = {}

    for key, orig_payload in evidence.items():
        translation_field = translation_fields[key]
        current_payload = getattr(translation, translation_field)

        if not current_payload and orig_payload:
            current_payload = await translate_payload(orig_payload)
            setattr(translation, translation_field, current_payload)
            updated = True

        translated_evidence[key] = current_payload

    if updated:
        await db.commit()
        await db.refresh(translation)

    return {
        "analysis_id": analysis.id,
        "version": analysis.version,
        "language": lang_input,
        "radius_km": analysis.radius_km,
        "coordinates": {
            "latitude": analysis.latitude,
            "longitude": analysis.longitude,
        },
        "evidence": translated_evidence,
    }


# @router.get("/businesses/{business_id}/report/chunks")
# async def get_report_chunks(
#     business_id: str,
#     entrepreneur: Enterpreneur = Depends(require_enterpreneur),
#     db: AsyncSession = Depends(get_db),
# ):
#     await get_owned_business(business_id, entrepreneur, db)
#     analysis = await get_latest_analysis(business_id, db)
#     result = await db.execute(
#         select(BusinessReportChunk)
#         .where(BusinessReportChunk.business_analysis_id == analysis.id)
#         .order_by(
#             BusinessReportChunk.section_number,
#             BusinessReportChunk.chunk_index,
#         )
#     )
#     chunks = result.scalars().all()
#     return {
#         "analysis_id": analysis.id,
#         "version": analysis.version,
#         "chunks": [
#             {
#                 "chunk_id": chunk.id,
#                 "section_number": chunk.section_number,
#                 "section_title": chunk.section_title,
#                 "chunk_index": chunk.chunk_index,
#                 "content": chunk.content,
#                 "embedding_text": chunk.embedding_text,
#             }
#             for chunk in chunks
#         ],
#     }


@router.get("/businesses/{business_id}/government-schemes")
async def get_government_schemes_profile(
    business_id: str,
    language: str = Query("en"),
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    await get_owned_business(business_id, entrepreneur, db)
    profile_result = await db.execute(
        select(BusinessProfile).where(BusinessProfile.business_id == business_id)
    )
    profile = profile_result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="No business profile found.")

    language_name = normalize_language(language)
    if language_name == "english":
        return {
            "business_id": business_id,
            "analysis_id": profile.analysis_id,
            "language": "english",
            "business_profile": profile.business_profile,
            "eligibility_profile": profile.eligibility_profile,
            "recommended_schemes": profile.recommended_schemes or [],
        }

    translation_result = await db.execute(
        select(BusinessProfileTranslation).where(
            BusinessProfileTranslation.business_profile_id == profile.id,
            BusinessProfileTranslation.language == language_name,
        )
    )
    translation = translation_result.scalar_one_or_none()

    if not translation:
        try:
            translation = await create_profile_translation(db, profile, language_name)
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to translate schemes: {str(e)}"
            )

    return {
        "business_id": business_id,
        "analysis_id": profile.analysis_id,
        "language": language_name,
        "business_profile": translation.business_profile,
        "eligibility_profile": profile.eligibility_profile,
        "recommended_schemes": translation.recommended_schemes or [],
    }


@router.get("/businesses/{business_id}/finance")
async def get_financial_analysis(
    business_id: str,
    language: str = Query("en"),
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    await get_owned_business(business_id, entrepreneur, db)
    result = await db.execute(
        select(FinancialAnalysis)
        .where(FinancialAnalysis.business_id == business_id)
        .order_by(FinancialAnalysis.version.desc())
        .limit(1)
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="No financial analysis found for this business.",
        )

    lang_code = resolve_lang_code(language)
    response = {
        "financial_analysis_id": analysis.id,
        "version": analysis.version,
        "language": "en",
        "input_payload": analysis.input_payload,
        "estimation_payload": analysis.estimation_payload,
        "financial_plan_payload": analysis.financial_plan_payload,
        "ai_analysis": analysis.ai_analysis,
    }

    if lang_code == "en":
        return response

    translation_result = await db.execute(
        select(FinancialAnalysisTranslation).where(
            FinancialAnalysisTranslation.financial_analysis_id == analysis.id,
            FinancialAnalysisTranslation.language == language,
        )
    )
    translation = translation_result.scalar_one_or_none()

    if not translation:
        try:
            translation = await create_financial_translation(db, analysis, lang_code)
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to translate finance plan: {str(e)}"
            )

    response["language"] = lang_code
    response["ai_analysis"] = translation.ai_analysis
    response["translation_id"] = translation.id
    return response


@router.get("/businesses/{business_id}/chat/sessions")
async def get_chat_sessions(
    business_id: str,
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    await get_owned_business(business_id, entrepreneur, db)
    result = await db.execute(
        select(ChatSession)
        .where(
            ChatSession.business_id == business_id,
            ChatSession.user_id == entrepreneur.user_id,
        )
        .order_by(ChatSession.created_at.desc())
    )
    sessions = result.scalars().all()
    return {
        "business_id": business_id,
        "sessions": [
            {
                "session_id": session.id,
                "created_at": session.created_at.isoformat()
                if session.created_at
                else None,
            }
            for session in sessions
        ],
    }


@router.get("/businesses/{business_id}/chat/sessions/{session_id}")
async def get_chat_session(
    business_id: str,
    session_id: str,
    language: str = Query("en"),
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    await get_owned_business(business_id, entrepreneur, db)

    session_result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.business_id == business_id,
            ChatSession.user_id == entrepreneur.user_id,
        )
    )
    session = session_result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found.")

    messages_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session.id)
        .options(selectinload(ChatMessage.translations))
        .order_by(ChatMessage.created_at.asc())
    )
    messages = messages_result.scalars().all()

    lang_code = resolve_lang_code(language)
    translator = Translator() if lang_code != "en" else None

    response_messages = []

    for msg in messages:
        target_content = msg.content

        if lang_code != "en":
            translation_record = next(
                (t for t in msg.translations if t.language == lang_code), None
            )

            if translation_record:
                target_content = translation_record.content
            else:
                try:
                    target_content = await asyncio.to_thread(
                        translator.translate,
                        text=msg.content,
                        source_language="en",
                        target_language=lang_code,
                    )
                    new_translation = ChatMessageTranslation(
                        message_id=msg.id, language=lang_code, content=target_content
                    )
                    db.add(new_translation)
                except Exception:
                    target_content = msg.content

        response_messages.append(
            {
                "message_id": msg.id,
                "role": msg.role,
                "content": target_content,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
            }
        )

    await db.commit()

    return {
        "business_id": business_id,
        "session_id": session.id,
        "language": lang_code,
        "created_at": session.created_at.isoformat() if session.created_at else None,
        "messages": response_messages,
    }
