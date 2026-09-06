from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.middlewares.role import require_enterpreneur
from src.schema.business import Business
from src.schema.business_analysis import BusinessAnalysis
from src.schema.business_profile import BusinessProfile
from src.schema.business_profile_translation import BusinessProfileTranslation
from src.schema.business_report_chunk import BusinessReportChunk
from src.schema.chat import ChatMessage, ChatSession
from src.schema.enterpreneur import Enterpreneur
from src.schema.financial_analysis import FinancialAnalysis
from src.schema.finance_translation import FinancialAnalysisTranslation
from src.schema.report_translations import ReportLanguage, ReportTranslation

router = APIRouter()


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
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    business = await get_owned_business(business_id, entrepreneur, db)
    return {
        "business_id": business.id,
        "business_name": business.business_name,
        "category": business.category,
        "margin_capital": business.margin_capital,
        "description": business.description,
        "location": {
            "village": business.village,
            "district": business.district,
            "city": business.city,
            "state": business.state,
            "country": business.country,
            "pincode": business.pincode,
            "latitude": business.latitude,
            "longitude": business.longitude,
        },
        "status": business.status.value
        if hasattr(business.status, "value")
        else business.status,
        "created_at": business.created_at.isoformat() if business.created_at else None,
        "updated_at": business.updated_at.isoformat() if business.updated_at else None,
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

    if requested_language == "english":
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
        raise HTTPException(
            status_code=404,
            detail="Requested report translation not found.",
        )

    return {
        "analysis_id": analysis.id,
        "version": analysis.version,
        "language": requested_language,
        "report_markdown": translation.content,
        "raw_evidence": {
            "population": translation.population_payload,
            "competitors": translation.competitor_payload,
            "market_price": translation.market_price_payload,
            "supply_chain": translation.supply_chain_payload,
            "transportation": translation.transportation_payload,
            "seasonality": translation.seasonality_payload,
        },
    }


@router.get("/businesses/{business_id}/report/evidence")
async def get_report_evidence(
    business_id: str,
    payload_type: str = Query("all"),
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    await get_owned_business(business_id, entrepreneur, db)
    analysis = await get_latest_analysis(business_id, db)
    evidence = {
        "population": analysis.population_payload,
        "competitors": analysis.competitor_payload,
        "market_price": analysis.market_price_payload,
        "supply_chain": analysis.supply_chain_payload,
        "transportation": analysis.transportation_payload,
        "seasonality": analysis.seasonality_payload,
    }

    if payload_type != "all":
        if payload_type not in evidence:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported payload_type: {payload_type}",
            )
        return {
            "analysis_id": analysis.id,
            "version": analysis.version,
            "payload_type": payload_type,
            "payload": evidence[payload_type],
        }

    return {
        "analysis_id": analysis.id,
        "version": analysis.version,
        "radius_km": analysis.radius_km,
        "coordinates": {
            "latitude": analysis.latitude,
            "longitude": analysis.longitude,
        },
        "evidence": evidence,
    }


@router.get("/businesses/{business_id}/report/chunks")
async def get_report_chunks(
    business_id: str,
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    await get_owned_business(business_id, entrepreneur, db)
    analysis = await get_latest_analysis(business_id, db)
    result = await db.execute(
        select(BusinessReportChunk)
        .where(BusinessReportChunk.business_analysis_id == analysis.id)
        .order_by(
            BusinessReportChunk.section_number,
            BusinessReportChunk.chunk_index,
        )
    )
    chunks = result.scalars().all()
    return {
        "analysis_id": analysis.id,
        "version": analysis.version,
        "chunks": [
            {
                "chunk_id": chunk.id,
                "section_number": chunk.section_number,
                "section_title": chunk.section_title,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "embedding_text": chunk.embedding_text,
            }
            for chunk in chunks
        ],
    }


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

    requested_language = language.strip().lower()
    if requested_language in {"en", "english"}:
        return {
            "business_id": business_id,
            "analysis_id": profile.analysis_id,
            "language": "en",
            "business_profile": profile.business_profile,
            "eligibility_profile": profile.eligibility_profile,
            "recommended_schemes": profile.recommended_schemes or [],
        }

    language_aliases = {
        "hi": "hindi",
        "hindi": "hindi",
        "bn": "bengali",
        "bengali": "bengali",
        "ta": "tamil",
        "tamil": "tamil",
        "te": "telugu",
        "telugu": "telugu",
    }
    normalized_language = language_aliases.get(requested_language)
    if not normalized_language:
        raise HTTPException(status_code=400, detail="Unsupported language.")

    translation_result = await db.execute(
        select(BusinessProfileTranslation).where(
            BusinessProfileTranslation.business_profile_id == profile.id,
            BusinessProfileTranslation.language == normalized_language,
        )
    )
    translation = translation_result.scalar_one_or_none()
    if not translation:
        raise HTTPException(
            status_code=404,
            detail="Requested government-scheme translation not found.",
        )

    return {
        "business_id": business_id,
        "analysis_id": profile.analysis_id,
        "language": normalized_language,
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

    requested_language = language.strip().lower()
    response = {
        "financial_analysis_id": analysis.id,
        "version": analysis.version,
        "language": "en",
        "input_payload": analysis.input_payload,
        "estimation_payload": analysis.estimation_payload,
        "financial_plan_payload": analysis.financial_plan_payload,
        "ai_analysis": analysis.ai_analysis,
    }

    if requested_language in {"en", "english"}:
        return response

    language_aliases = {
        "hi": "hindi",
        "hindi": "hindi",
        "bn": "bengali",
        "bengali": "bengali",
    }
    normalized_language = language_aliases.get(requested_language)
    if not normalized_language:
        raise HTTPException(status_code=400, detail="Unsupported language.")

    translation_result = await db.execute(
        select(FinancialAnalysisTranslation).where(
            FinancialAnalysisTranslation.financial_analysis_id == analysis.id,
            FinancialAnalysisTranslation.language == normalized_language,
        )
    )
    translation = translation_result.scalar_one_or_none()
    if not translation:
        raise HTTPException(
            status_code=404,
            detail="Requested financial translation not found.",
        )

    response["language"] = normalized_language
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
        .order_by(ChatMessage.created_at.asc())
    )
    messages = messages_result.scalars().all()
    return {
        "business_id": business_id,
        "session_id": session.id,
        "created_at": session.created_at.isoformat() if session.created_at else None,
        "messages": [
            {
                "message_id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at.isoformat()
                if message.created_at
                else None,
            }
            for message in messages
        ],
    }
