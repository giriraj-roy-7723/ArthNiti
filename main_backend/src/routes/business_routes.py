from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.controllers.business_controller import (
    create_business,
    get_business,
    get_my_business_ids,
    mark_business_state,
    search_businesses,
    search_other_businesses,
)
from src.middlewares.auth import verify_token
from src.models.business_request import BusinessCreateRequest, BusinessResponse
from src.schema.business import BusinessStatus

router = APIRouter()


# =========================================================
# CREATE
# =========================================================


@router.post(
    "/create",
    response_model=BusinessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_business_route(
    data: BusinessCreateRequest,
    language: str = "english",
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    return await create_business(
        data=data,
        owner_id=user_id,
        language=language,
        db=db,
    )


# =========================================================
# MY BUSINESSES
# =========================================================


@router.get(
    "/my",
    response_model=list[str],
    status_code=status.HTTP_200_OK,
)
async def get_my_business_ids_route(
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    return await get_my_business_ids(
        user_id=user_id,
        db=db,
    )


# =========================================================
# SEARCH
# =========================================================


@router.get(
    "/search",
    response_model=list[BusinessResponse],
    status_code=status.HTTP_200_OK,
)
async def search_businesses_route(
    language: str = "english",
    name: str | None = None,
    category: str | None = None,
    status: BusinessStatus | None = None,
    village: str | None = None,
    district: str | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    pincode: str | None = None,
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    return await search_businesses(
        db=db,
        language=language,
        user_id=user_id,
        name=name,
        category=category,
        status=status,
        village=village,
        district=district,
        city=city,
        state=state,
        country=country,
        pincode=pincode,
    )


# =========================================================
# OTHER BUSINESSES
# =========================================================


@router.get(
    "/search/others",
    response_model=list[BusinessResponse],
    status_code=status.HTTP_200_OK,
)
async def search_other_businesses_route(
    language: str = "english",
    name: str | None = None,
    category: str | None = None,
    status: BusinessStatus | None = None,
    village: str | None = None,
    district: str | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    pincode: str | None = None,
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    return await search_other_businesses(
        db=db,
        language=language,
        name=name,
        category=category,
        status=status,
        village=village,
        district=district,
        city=city,
        state=state,
        country=country,
        user_id= user_id,
        pincode=pincode,
    )


# =========================================================
# UPDATE BUSINESS STATUS
# =========================================================


@router.patch(
    "/{business_id}/status",
    response_model=BusinessResponse,
    status_code=status.HTTP_200_OK,
)
async def mark_business_state_route(
    business_id: str,
    state: BusinessStatus,
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    return await mark_business_state(
        user_id=user_id,
        business_id=business_id,
        state=state,
        db=db,
    )


# =========================================================
# GET SINGLE BUSINESS
# =========================================================


@router.get(
    "/{business_id}",
    response_model=BusinessResponse,
    status_code=status.HTTP_200_OK,
)
async def get_business_route(
    business_id: str,
    language: str = "english",
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    return await get_business(
        business_id=business_id,
        language=language,
        owner_id=user_id,
        db=db,
    )
