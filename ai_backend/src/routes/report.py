from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.controllers.report_service import generate_feasibility_report
from src.controllers.business_report_persistence_service import save_business_analysis
from src.middlewares.role import require_enterpreneur
from src.schema.business import Business, BusinessStatus
from src.schema.enterpreneur import Enterpreneur
from src.models.report import ReportRequest, ReportResponse

router = APIRouter()


@router.post(
    "/generate",
    response_model=ReportResponse,
)
async def generate_report(
    request: ReportRequest,
    entrepreneur: Enterpreneur = Depends(require_enterpreneur),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a pending business, generate its feasibility analysis,
    persist the analysis, and return the result.
    """

    # ========================================================
    # Create business
    # ========================================================

    business = Business(
        owner_id=entrepreneur.user_id,
        business_name=request.business_name,
        category=request.business_type,
        margin_capital=request.margin_capital,
        description=request.business_description,
        village=request.village,
        district=request.district,
        city=request.city,
        state=request.state,
        country=request.country,
        pincode=request.pincode,
        latitude=0.0,
        longitude=0.0,
        status=BusinessStatus.pending,
    )

    db.add(business)
    await db.flush()

    # ========================================================
    # Generate report
    # ========================================================

    try:
        result = generate_feasibility_report(
            business_name=request.business_name,
            business_type=request.business_type,
            business_description=request.business_description,
            country=request.country,
            state=request.state,
            district=request.district,
            city=request.city,
            village=request.village,
            pincode=request.pincode,
            margin_capital=request.margin_capital,
            radius_km=request.radius_km,
            language=request.language,
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    # ========================================================
    # Get coordinates from generated population response
    # ========================================================

    latitude = result.get("analysis_latitude")
    longitude = result.get("analysis_longitude")

    if latitude is not None and longitude is not None:
        business.latitude = latitude
        business.longitude = longitude

    # ========================================================
    # Persist analysis
    # ========================================================

    try:
        analysis = await save_business_analysis(
            db=db,
            business_id=business.id,
            result=result,
            radius_km=request.radius_km,
            latitude=latitude,
            longitude=longitude,
        )

        # Business has successfully received an analysis.
        await db.commit()
        await db.refresh(analysis)

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save analysis: {str(e)}",
        )

    # ========================================================
    # Response
    # ========================================================

    return ReportResponse(
        status="success",
        # report=result,
        analysis_id=analysis.id,
        version=analysis.version,
        language=result["language"],
        report_markdown=result["report_markdown"],
        raw_evidence=result["raw_evidence"],
    )
