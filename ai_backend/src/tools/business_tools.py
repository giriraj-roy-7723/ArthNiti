import asyncio
import os
from fastapi import HTTPException
from typing import Literal, Optional

from langchain_core.tools import tool
from tavily import TavilyClient

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.schema.financial_analysis import FinancialAnalysis
from src.schema.business_profile import BusinessProfile
from src.schema.business_analysis import BusinessAnalysis
from src.schema.business import (
    Business,
    BusinessStatus,
)
from src.schema.chat import ChatSession

# Geocoding & localization utilities used in update controller
from src.utils.translator_utils import translate_entry
from src.utils.geo_utils import get_coordinates

from src.services.business_report_search import (
    search_business_report as report_vector_search,
)
from src.services.scheme_embedding import generate_embedding
from src.services.scheme_search import search_similar_schemes



LANG_NORMALIZER = {
    "english": "en",
    "en": "en",
    "eng": "en",
    "bengali": "bn",
    "bng": "bn",
    "bn": "bn",
    "hindi": "hi",
    "hin": "hi",
    "hi": "hi",
}


def normalize_language(language: str) -> str:
    language = language.lower().strip()

    lang_code = LANG_NORMALIZER.get(language)

    if not lang_code:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}",
        )

    return lang_code


def get_en(field) -> str:
    """Safely extract the English string from a JSONB column or fallback to string."""
    if isinstance(field, dict):
        return field.get("en", "")
    return str(field or "")


def get_business_agent_tools(db: AsyncSession, business_id: str, user_id: str) -> list:
    """
    Constructs and returns LangChain tools pre-bound to the authenticated
    user_id, business_id, and active database AsyncSession.
    """

    @tool
    async def get_business_details() -> dict:
        """
        Retrieves the core profile and registration details of the current business.
        Use this tool to inspect basic business metadata: business name, category,
        description, initial margin capital, geographic address, GPS coordinates, and status.
        """
        stmt = select(Business).where(Business.id == business_id).limit(1)
        result = await db.execute(stmt)
        business = result.scalar_one_or_none()

        if not business:
            return {"error": "Business record not found."}

        return {
            "business_id": business.id,
            "business_name": get_en(business.business_name),
            "category": get_en(business.category),
            "margin_capital": business.margin_capital,
            "description": get_en(business.description),
            "location": {
                "village": get_en(business.village),
                "district": get_en(business.district),
                "city": get_en(business.city),
                "state": get_en(business.state),
                "country": get_en(business.country),
                "pincode": business.pincode,
                "latitude": business.latitude,
                "longitude": business.longitude,
            },
            "status": business.status.value
            if hasattr(business.status, "value")
            else business.status,
            "created_at": business.created_at.isoformat()
            if business.created_at
            else None,
        }

    @tool
    async def update_business_details(
        name: Optional[str] = None,
        description: Optional[str] = None,
        village: Optional[str] = None,
        district: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        pincode: Optional[str] = None,
        margin_capital: Optional[float] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        language: str = "en",
    ) -> dict:
        """
        DATABASE MUTATION TOOL: Updates metadata, location, margin capital, and coordinates
        for the current business. Automatically translates text fields and updates GPS coordinates.

        CRITICAL: Never execute this tool without explicit user confirmation of the fields to change.

        Args:
            name: New business name.
            description: Detailed business description or model.
            village: Village/Locality name.
            district: District name.
            city: City or town name.
            state: State or province.
            country: Country name.
            pincode: Postal/PIN code.
            margin_capital: Updated initial capital/investment amount.
            latitude: Specific GPS latitude coordinate (optional).
            longitude: Specific GPS longitude coordinate (optional).
            language: Language code of the provided inputs (default 'en').
        """
        try:
            lang_code = normalize_language(language)

            # 1. Fetch business record
            stmt = select(Business).where(
                Business.id == business_id,
                Business.owner_id == user_id,
            )
            result = await db.execute(stmt)
            business = result.scalar_one_or_none()

            if not business:
                return {"error": "Business not found or access denied."}

            # 2. Extract and update multilingual fields
            multilingual_inputs = {
                "business_name": name,
                "description": description,
                "village": village,
                "district": district,
                "city": city,
                "state": state,
                "country": country,
            }

            updated_multilingual_fields = {
                k: v.strip()
                for k, v in multilingual_inputs.items()
                if v is not None and v.strip() != ""
            }

            if updated_multilingual_fields:
                for field, new_val in updated_multilingual_fields.items():
                    setattr(business, field, {lang_code: new_val})

                await db.flush()

                # Re-translate to other supported locales
                all_other_languages = {"en", "bn", "hi"} - {lang_code}
                source_entry = {k: v for k, v in updated_multilingual_fields.items()}

                for target_lang in all_other_languages:
                    try:
                        translated_entry = await asyncio.to_thread(
                            translate_entry,
                            entry=source_entry,
                            target_language=target_lang,
                            source_language=lang_code,
                        )

                        for field, trans_val in (translated_entry or {}).items():
                            if trans_val is not None:
                                current_dict = dict(
                                    getattr(business, field, None) or {}
                                )
                                current_dict[target_lang] = trans_val
                                setattr(business, field, current_dict)
                    except Exception as exc:
                        print(f"Translation warning for {target_lang}: {exc}")

                await db.flush()

            # 3. Handle GPS Coordinates & Geocoding
            location_fields_touched = any(
                k in updated_multilingual_fields
                for k in ["city", "district", "state", "country"]
            )

            if latitude is not None and longitude is not None:
                business.latitude = latitude
                business.longitude = longitude
            elif location_fields_touched or (
                business.latitude is None and business.longitude is None
            ):
                city_val = (business.city or {}).get(lang_code) or ""
                district_val = (business.district or {}).get(lang_code) or ""
                state_val = (business.state or {}).get(lang_code) or ""
                country_val = (business.country or {}).get(lang_code) or ""

                location_parts = [city_val, district_val, state_val, country_val]
                location_str = ", ".join(
                    part.strip() for part in location_parts if part and part.strip()
                )

                if location_str:
                    try:
                        lat, lon = await asyncio.to_thread(
                            get_coordinates, location_str
                        )
                        business.latitude = lat
                        business.longitude = lon
                    except Exception as exc:
                        print(f"Geocoding warning: {exc}")

            # 4. Handle Non-multilingual Scalars
            if margin_capital is not None:
                business.margin_capital = margin_capital

            if pincode is not None:
                business.pincode = pincode.strip() if pincode else None

            # 5. Commit changes
            await db.commit()
            await db.refresh(business)

            return {
                "success": True,
                "message": "Business details updated successfully.",
                "business_id": business.id,
                "business_name": get_en(business.business_name),
                "margin_capital": business.margin_capital,
                "latitude": business.latitude,
                "longitude": business.longitude,
                "updated_fields": list(updated_multilingual_fields.keys())
                + (
                    [
                        k
                        for k, v in [
                            ("margin_capital", margin_capital),
                            ("pincode", pincode),
                            ("coordinates", latitude or longitude),
                        ]
                        if v is not None
                    ]
                ),
            }

        except IntegrityError as e:
            await db.rollback()
            return {"error": f"Database integrity error updating details: {str(e)}"}
        except Exception as e:
            await db.rollback()
            return {"error": f"Failed to update business details: {str(e)}"}

    @tool
    async def update_business_status(
        new_status: Literal["pending", "active", "closed"],
        language: str = "en",
    ) -> dict:
        """
        DATABASE MUTATION TOOL: Updates the lifecycle or operational status of the current business.
        CRITICAL: Never run this tool without explicit user permission and confirmation.

        Args:
            new_status: The target status value to apply to the business.
            language: The target language code for localization checks (defaults to 'en').
        """
        try:
            stmt = select(Business).where(
                Business.id == business_id,
                Business.owner_id == user_id,
            )
            result = await db.execute(stmt)
            business = result.scalar_one_or_none()

            if not business:
                return {"error": "Business not found or access denied."}

            old_status = (
                business.status.value
                if hasattr(business.status, "value")
                else str(business.status)
            )

            target_status = (
                BusinessStatus[new_status]
                if hasattr(BusinessStatus, new_status)
                else new_status
            )
            business.status = target_status

            await db.flush()
            await db.commit()
            await db.refresh(business)

            updated_status_str = (
                business.status.value
                if hasattr(business.status, "value")
                else str(business.status)
            )

            return {
                "success": True,
                "message": f"Business status successfully updated from '{old_status}' to '{updated_status_str}'.",
                "business_id": business.id,
                "new_status": updated_status_str,
            }

        except IntegrityError as e:
            await db.rollback()
            return {"error": f"Database integrity error updating status: {str(e)}"}
        except Exception as e:
            await db.rollback()
            return {"error": f"Failed to update business status: {str(e)}"}

    @tool
    async def get_all_other_user_businesses() -> list[dict] | dict:
        """
        Retrieves an overview of all other businesses registered by this user,
        excluding the currently selected business.
        """
        stmt = (
            select(Business)
            .where(Business.owner_id == user_id, Business.id != business_id)
            .order_by(Business.created_at.desc())
        )
        result = await db.execute(stmt)
        records = result.scalars().all()

        if not records:
            return {"message": "No other businesses found for this user."}

        return [
            {
                "business_id": b.id,
                "business_name": get_en(b.business_name),
                "category": get_en(b.category),
                "status": b.status.value if hasattr(b.status, "value") else b.status,
                "city": get_en(b.city),
                "state": get_en(b.state),
                "created_at": b.created_at.isoformat() if b.created_at else None,
            }
            for b in records
        ]

    @tool
    async def get_previous_chat_session_summaries(limit: int = 5) -> list[dict] | dict:
        """
        Retrieves concise historical summaries of past chat sessions for this specific business.
        """
        stmt = (
            select(ChatSession)
            .where(
                ChatSession.business_id == business_id,
                ChatSession.summary.isnot(None),
            )
            .order_by(ChatSession.updated_at.desc())
            .limit(limit)
        )
        result = await db.execute(stmt)
        sessions = result.scalars().all()

        if not sessions:
            return {
                "message": "No previous chat session summaries available for this business."
            }

        return [
            {
                "session_id": s.id,
                "title": getattr(s, "title", None),
                "summary": s.summary,
                "key_topics": getattr(s, "key_topics", None),
                "updated_at": s.updated_at.isoformat() if s.updated_at else None,
            }
            for s in sessions
        ]

    @tool
    async def get_feasibility_evidence_payloads(
        payload_type: Literal[
            "all",
            "population",
            "competitors",
            "market_price",
            "supply_chain",
            "transportation",
            "seasonality",
        ] = "all",
    ) -> dict:
        """
        Retrieves raw underlying evidence JSON datasets from the latest Feasibility Analysis.
        """
        stmt = (
            select(BusinessAnalysis)
            .where(BusinessAnalysis.business_id == business_id)
            .order_by(BusinessAnalysis.version.desc())
            .limit(1)
        )
        result = await db.execute(stmt)
        analysis = result.scalar_one_or_none()

        if not analysis:
            return {"error": "No feasibility analysis found for this business."}

        evidence_store = {
            "population": analysis.population_payload,
            "competitors": analysis.competitor_payload,
            "market_price": analysis.market_price_payload,
            "supply_chain": analysis.supply_chain_payload,
            "transportation": analysis.transportation_payload,
            "seasonality": analysis.seasonality_payload,
        }

        if payload_type != "all":
            payload = evidence_store.get(payload_type)
            if payload is None:
                return {"message": f"No data recorded for '{payload_type}'."}
            return {
                "version": analysis.version,
                "radius_km": analysis.radius_km,
                "payload_type": payload,
            }

        return {
            "version": analysis.version,
            "radius_km": analysis.radius_km,
            "coordinates": {
                "latitude": analysis.latitude,
                "longitude": analysis.longitude,
            },
            "evidence": evidence_store,
        }

    @tool
    async def get_financial_analysis() -> dict:
        """
        Retrieves the latest financial calculation data and plan for this business.
        """
        stmt = (
            select(FinancialAnalysis)
            .where(FinancialAnalysis.business_id == business_id)
            .order_by(FinancialAnalysis.version.desc())
            .limit(1)
        )
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()

        if not record:
            return {"error": "No financial analysis found for this business."}

        return {
            "version": record.version,
            "input_payload": record.input_payload,
            "estimation_payload": record.estimation_payload,
            "financial_plan_payload": record.financial_plan_payload,
            "ai_analysis": record.ai_analysis,
        }

    @tool
    async def get_business_profile() -> dict:
        """
        Retrieves the business profile, qualification details, and pre-calculated
        recommended government schemes.
        """
        stmt = (
            select(BusinessProfile)
            .where(BusinessProfile.business_id == business_id)
            .limit(1)
        )
        result = await db.execute(stmt)
        profile = result.scalar_one_or_none()

        if not profile:
            return {"error": "No business profile found."}

        return {
            "business_profile": profile.business_profile,
            "eligibility_profile": profile.eligibility_profile,
            "recommended_schemes": profile.recommended_schemes,
        }

    @tool
    async def search_business_report(query: str) -> list[dict] | dict:
        """
        Performs semantic vector search across the 13 narrative sections of the user's
        Feasibility Report.
        """
        try:
            query_embedding = generate_embedding(query)
            chunks = await report_vector_search(
                db=db,
                business_id=business_id,
                query_embedding=query_embedding,
                limit=5,
            )
            if not chunks:
                return {"message": "No relevant report sections found for this query."}
            return chunks
        except Exception as e:
            return {"error": f"Failed to search report: {str(e)}"}

    @tool
    async def search_government_schemes(query: str) -> list[dict] | dict:
        """
        Searches the broader government schemes database via vector similarity.
        """
        try:
            query_embedding = generate_embedding(query)
            schemes = await search_similar_schemes(
                db=db,
                query_embedding=query_embedding,
                limit=5,
            )
            if not schemes:
                return {"message": "No matching government schemes found."}
            return schemes
        except Exception as e:
            return {"error": f"Failed to query government schemes: {str(e)}"}

    @tool
    def web_search(query: str) -> list[dict] | dict:
        """
        Searches the live web via Tavily for time-sensitive, regulatory, or live data.
        """
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return {"error": "TAVILY_API_KEY is not configured."}

        try:
            client = TavilyClient(api_key=api_key)
            response = client.search(
                query=query,
                search_depth="basic",
                max_results=4,
            )
            return response.get("results", [])
        except Exception as e:
            return {"error": f"Web search failed: {str(e)}"}

    return [
        get_business_details,
        update_business_details,  # Newly added
        update_business_status,
        get_all_other_user_businesses,
        get_previous_chat_session_summaries,
        get_business_profile,
        search_business_report,
        get_feasibility_evidence_payloads,
        get_financial_analysis,
        search_government_schemes,
        web_search,
    ]
