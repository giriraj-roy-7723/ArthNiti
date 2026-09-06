import os
from typing import Literal

from langchain_core.tools import tool
from tavily import TavilyClient

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schema.financial_analysis import FinancialAnalysis
from src.schema.business_profile import BusinessProfile
from src.schema.business_analysis import BusinessAnalysis
from src.schema.business import Business
from src.schema.enterpreneur import Enterpreneur
from src.schema.user import User

from src.services.business_report_search import (
    search_business_report as report_vector_search,
)
from src.services.scheme_embedding import generate_embedding
from src.services.scheme_search import search_similar_schemes


def get_business_agent_tools(db: AsyncSession, business_id: str) -> list:
    """
    Constructs and returns LangChain tools pre-bound to the authenticated
    user's business_id and active database AsyncSession.
    """

    @tool
    async def get_business_details() -> dict:
        """
        Retrieves the core profile and registration details of the business.
        Use this tool to inspect basic business metadata: business name, category,
        description, initial margin capital, geographic address (village, district,
        city, state, country, pincode), GPS coordinates, and current status.
        """
        stmt = select(Business).where(Business.id == business_id).limit(1)
        result = await db.execute(stmt)
        business = result.scalar_one_or_none()

        if not business:
            return {"error": "Business record not found."}

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
            "created_at": business.created_at.isoformat()
            if business.created_at
            else None,
        }

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
        Use this when exact numerical metrics or specific raw evidence are needed:
        - 'population': WorldPop / UN DESA demographic data, radius density, household counts.
        - 'competitors': OpenStreetMap competitor names, proximity distances, and density counts.
        - 'market_price': Agmarknet/DOCA commodity price statistics (min, max, median, mean).
        - 'supply_chain': Pillar scores and distance to livestock farms, abattoirs, cold chains.
        - 'transportation': OSRM route distances, detour factors, travel times, and vehicle OPEX models.
        - 'seasonality': Monthly rainfall, monsoon risk index, temperature, production/price indices.
        - 'all': Returns all available evidence payloads.

        Args:
            payload_type: The category of raw evidence to retrieve. Defaults to 'all'.
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
                payload_type: payload,
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
        Use this tool when answering questions about financial projections, EMIs,
        startup capital, loan requirements, estimated profits, cashflow, or break-even.
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
        Use this tool FIRST when the user asks which schemes they are eligible for,
        or when general business profile characteristics are required.
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
        Feasibility Report (covering SWOT, business model recommendations, synthesized risks, etc.).

        Args:
            query: The specific topic or question to search within the narrative report.
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
        Only use this if the user's pre-matched schemes in `get_business_profile`
        do not contain the necessary information or if exploring alternative subsidies.

        Args:
            query: The scheme type, sector, or specific support requirement.
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
        Searches the live web via Tavily.
        Use this tool ONLY when:
        1. Checking time-sensitive or live data (current bank interest rates, active deadlines).
        2. Verifying recent regulatory or policy shifts.
        3. Stored database tools return no relevant information.

        Args:
            query: The search query string.
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
        get_business_profile,
        search_business_report,
        get_feasibility_evidence_payloads,
        get_financial_analysis,
        search_government_schemes,
        web_search,
    ]
