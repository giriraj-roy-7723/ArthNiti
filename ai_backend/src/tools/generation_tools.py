from langchain_core.tools import tool
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.schema.business import Business, BusinessStatus
from src.schema.financial_analysis import FinancialAnalysis
from src.schema.business_report_chunk import BusinessReportChunk

from src.controllers.report_service import generate_feasibility_report
from src.controllers.business_report_persistence_service import save_business_analysis
from src.controllers.finance_service import (
    generate_financial_plan,
    generate_ai_analysis,
)
from src.controllers.business_profile_service import process_profile_and_recommendations

from src.services.scheme_embedding import generate_embedding
from src.utils.report_utils import parse_report_sections, split_text_recursively


def get_generation_tools(db: AsyncSession, business_id: str, user_id: str) -> list:
    """
    Constructs and returns LangChain action tools for generating analytical reports.
    These tools execute the heavy AI orchestration and persist the results to the database.
    """

    @tool
    async def generate_feasibility_report_tool(
        business_name: str,
        business_type: str,
        country: str,
        state: str,
        district: str,
        margin_capital: float,
        business_description: str = None,
        city: str = None,
        village: str = None,
        pincode: str = None,
        radius_km: float = 10.0,
    ) -> dict:
        """
        Generates the foundational Feasibility Report for the business.
        Call this tool when the user provides the required business and location details
        and explicitly wants to create or regenerate their Feasibility Analysis.

        Args:
            business_name: The name of the proposed business.
            business_type: The category or industry (e.g., 'Poultry Farm').
            country: The operating country.
            state: The operating state.
            district: The operating district.
            margin_capital: The available startup capital in local currency (must be > 0).
            business_description: Optional detailed description of the business.
            city: Optional operating city.
            village: Optional operating village.
            pincode: Optional postal code.
            radius_km: The market analysis radius (defaults to 10.0).
        """
        try:
            # 1. Fetch or Create the Business Record
            result = await db.execute(
                select(Business).where(
                    Business.id == business_id,
                    Business.owner_id == user_id,
                )
            )
            business = result.scalar_one_or_none()

            if not business:
                business = Business(
                    id=business_id,
                    owner_id=user_id,
                    business_name=business_name,
                    category=business_type,
                    margin_capital=margin_capital,
                    description=business_description,
                    village=village,
                    district=district,
                    city=city,
                    state=state,
                    country=country,
                    pincode=pincode,
                    latitude=0.0,
                    longitude=0.0,
                    status=BusinessStatus.pending,
                )
                db.add(business)
                await db.flush()

            # 2. Run the Orchestrator Pipeline
            report_result = generate_feasibility_report(
                business_name=business_name,
                business_type=business_type,
                business_description=business_description,
                country=country,
                state=state,
                district=district,
                city=city,
                village=village,
                pincode=pincode,
                margin_capital=margin_capital,
                radius_km=radius_km,
                language="english",
            )

            # 3. Update Coordinates based on Demographic Resolution
            latitude = report_result.get("analysis_latitude")
            longitude = report_result.get("analysis_longitude")

            if latitude is not None and longitude is not None:
                business.latitude = latitude
                business.longitude = longitude

            # 4. Save Analysis to Database
            analysis = await save_business_analysis(
                db=db,
                business_id=business.id,
                result=report_result,
                radius_km=radius_km,
                latitude=latitude,
                longitude=longitude,
            )
            await db.flush()

            # 5. Chunk and Vectorize the Report for RAG
            markdown_text = report_result.get(
                "original_report_markdown", report_result.get("report_markdown")
            )
            sections = parse_report_sections(markdown_text)

            chunks_to_insert = []
            for section in sections:
                text_chunks = split_text_recursively(
                    section["content"], max_chars=1500, overlap=150
                )
                for chunk_idx, chunk_text in enumerate(text_chunks):
                    embedding_text = f"Section {section['number']}: {section['title']}\n\n{chunk_text}"
                    embedding_vector = generate_embedding(embedding_text)

                    chunks_to_insert.append(
                        BusinessReportChunk(
                            business_id=business.id,
                            business_analysis_id=analysis.id,
                            version=analysis.version,
                            section_number=section["number"],
                            section_title=section["title"],
                            chunk_index=chunk_idx,
                            content=chunk_text,
                            embedding_text=embedding_text,
                            embedding=embedding_vector,
                        )
                    )

            if chunks_to_insert:
                db.add_all(chunks_to_insert)

            await db.commit()

            return {
                "status": "success",
                "message": "Feasibility Report generated and indexed successfully.",
                "analysis_id": analysis.id,
                "version": analysis.version,
            }

        except Exception as e:
            await db.rollback()
            return {"error": f"Failed to generate feasibility report: {str(e)}"}

    @tool
    async def generate_financial_plan_tool(
        margin: float,
        monthly_revenue: float,
        monthly_direct_costs: float,
        monthly_fixed_costs: float,
    ) -> dict:
        """
        Generates the Financial Plan and AI Financial Advisory for the business.
        Call this tool ONLY AFTER the Feasibility Report exists, and when the user
        provides their expected margin capital, monthly revenue, direct costs, and fixed costs.

        Args:
            margin: The initial margin/own capital invested (must be > 0).
            monthly_revenue: Expected monthly sales revenue.
            monthly_direct_costs: Expected monthly direct/variable costs (raw materials, utility usage).
            monthly_fixed_costs: Expected monthly fixed costs (rent, salaries).
        """
        try:
            plan_result = await generate_financial_plan(
                db=db,
                business_id=business_id,
                margin=margin,
                monthly_revenue=monthly_revenue,
                monthly_direct_costs=monthly_direct_costs,
                monthly_fixed_costs=monthly_fixed_costs,
            )

            ai_commentary = await generate_ai_analysis(plan_result)

            result = await db.execute(
                select(func.max(FinancialAnalysis.version)).where(
                    FinancialAnalysis.business_id == business_id
                )
            )
            latest_version = result.scalar() or 0
            next_version = latest_version + 1

            estimation_payload = {
                "input_validation": plan_result.get("input_validation"),
                "financial_estimation": plan_result.get("financial_estimation"),
                "used_values": plan_result.get("used_values"),
            }

            financial_analysis = FinancialAnalysis(
                business_id=business_id,
                business_analysis_id=plan_result.get("business_analysis_id"),
                version=next_version,
                input_payload={
                    "margin_capital": margin,
                    "monthly_revenue": monthly_revenue,
                    "monthly_direct_costs": monthly_direct_costs,
                    "monthly_fixed_costs": monthly_fixed_costs,
                },
                estimation_payload=estimation_payload,
                financial_plan_payload=plan_result,
                ai_analysis=ai_commentary,
            )

            db.add(financial_analysis)
            await db.commit()
            await db.refresh(financial_analysis)

            return {
                "status": "success",
                "message": "Financial Plan and Advisory generated and saved successfully.",
                "financial_analysis_id": financial_analysis.id,
                "version": financial_analysis.version,
            }

        except Exception as e:
            await db.rollback()
            return {"error": f"Failed to generate financial plan: {str(e)}"}

    @tool
    async def generate_government_schemes_profile_tool(
        age: int = None,
        gender: str = None,
        social_category: str = None,
        ownership_type: str = None,
        annual_income: float = None,
        annual_turnover: float = None,
        investment_amount: float = None,
        business_registration: bool = None,
        farmer_status: bool = None,
        land_ownership: bool = None,
    ) -> dict:
        """
        Generates the Business Profile and recommends matched Government Schemes based on eligibility.
        Call this tool ONLY AFTER the Feasibility Report exists. Use this when the user wants
        to find out what subsidies or schemes they are eligible for.

        All arguments are OPTIONAL. Ask the user for any details they are willing to provide
        to get better matches, but you can run it even if some are missing.

        Args:
            age: Entrepreneur's age (18 to 100).
            gender: 'male', 'female', 'other'.
            social_category: e.g., 'general', 'obc', 'sc', 'st'.
            ownership_type: e.g., 'sole proprietorship', 'partnership'.
            annual_income: Expected/current annual income.
            annual_turnover: Expected/current annual turnover.
            investment_amount: Total project investment amount.
            business_registration: True if formally registered, False otherwise.
            farmer_status: True if the user holds farmer status.
            land_ownership: True if the user owns the business land.
        """
        try:
            # Package only the provided non-None arguments to mimic model_dump(exclude_unset=True)
            eligibility_data = {
                "age": age,
                "gender": gender,
                "social_category": social_category,
                "ownership_type": ownership_type,
                "annual_income": annual_income,
                "annual_turnover": annual_turnover,
                "investment_amount": investment_amount,
                "business_registration": business_registration,
                "farmer_status": farmer_status,
                "land_ownership": land_ownership,
            }
            # Remove None values
            eligibility_data = {
                k: v for k, v in eligibility_data.items() if v is not None
            }

            result = await process_profile_and_recommendations(
                db=db,
                business_id=business_id,
                eligibility_data=eligibility_data,
                target_language="en",
                limit=10,
            )

            return {
                "status": "success",
                "message": "Business profile generated and schemes recommended successfully.",
                "analysis_id": result["analysis_id"],
                "recommended_schemes_count": len(result["original_english_schemes"]),
                "recommended_schemes": [
                    {"name": s["name"], "similarity": s["similarity_score"]}
                    for s in result["original_english_schemes"]
                ],
            }

        except ValueError as exc:
            # Usually triggered if Feasibility Analysis doesn't exist yet
            return {
                "error": f"Prerequisite missing: {str(exc)}. Please ensure the Feasibility Report is generated first."
            }
        except Exception as exc:
            await db.rollback()
            return {
                "error": f"Failed to generate profile and recommendations: {str(exc)}"
            }

    return [
        generate_feasibility_report_tool,
        generate_financial_plan_tool,
        generate_government_schemes_profile_tool,
    ]
