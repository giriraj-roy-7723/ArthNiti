import asyncio
from fastapi import HTTPException, status

from sqlalchemy import select,func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.schema.user import User
from src.schema.business import Business, BusinessStatus
from src.models.business_request import BusinessCreateRequest, BusinessResponse, BusinessOwnerContactResponse

from src.utils.translator_utils import translate_entry
from src.utils.geo_utils import get_coordinates
from src.utils.business_category_verifier import normalize_and_validate_category

from src.services.distance_service import ensure_user_coordinates,calculate_haversine_distance


MULTILINGUAL_BUSINESS_FIELDS = [
    "business_name",
    "category",
    "description",
    "village",
    "district",
    "city",
    "state",
    "country",
]

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


def get_available_source_language(
    business: Business,
    target_language: str,
) -> str | None:
    """
    Find a language that already exists in the database.

    We prefer:
    1. A language different from target_language
    2. Otherwise target_language itself

    This avoids hardcoding English as the source language.
    """

    available_languages = set()

    for field in MULTILINGUAL_BUSINESS_FIELDS:
        value = getattr(business, field, None) or {}

        if isinstance(value, dict):
            available_languages.update(value.keys())

    # Prefer another language as the translation source
    for lang in available_languages:
        if lang != target_language:
            return lang

    # If only target language exists, return it
    if target_language in available_languages:
        return target_language

    return None


async def ensure_business_language(
    business: Business,
    target_language: str,
    db: AsyncSession,
):
    """
    Make sure every multilingual business field has the requested language.

    If even one field is missing the requested language, translate ALL
    multilingual fields using a language already available in the DB.
    """

    # Check whether all fields already contain the requested language
    all_translated = True

    for field in MULTILINGUAL_BUSINESS_FIELDS:
        value = getattr(business, field, None) or {}

        if not value or target_language not in value:
            all_translated = False
            break

    if all_translated:
        return

    # Find a source language that actually exists in the DB
    source_language = get_available_source_language(
        business,
        target_language,
    )

    if not source_language:
        raise HTTPException(
            status_code=400,
            detail="No source language is available for business translation.",
        )

    # Build the source entry using ONLY the selected source language
    source_entry = {}

    for field in MULTILINGUAL_BUSINESS_FIELDS:
        value = getattr(business, field, None) or {}

        source_entry[field] = value.get(source_language)

    # Remove fields that don't have a value in the source language
    source_entry = {
        key: value for key, value in source_entry.items() if value is not None
    }

    if not source_entry:
        raise HTTPException(
            status_code=400,
            detail="No translatable business data is available.",
        )

    # Translate all fields in one Gemini call
    translated_entry = await asyncio.to_thread(
        translate_entry,
        entry=source_entry,
        target_language=target_language,
        source_language=source_language,
    )

    # Store the translated values in JSONB
    for field in MULTILINGUAL_BUSINESS_FIELDS:
        translated_value = translated_entry.get(field)

        if translated_value is None:
            continue

        current_value = getattr(business, field, None) or {}

        # Create a new dict so SQLAlchemy/JSONB detects the change
        updated_value = dict(current_value)
        updated_value[target_language] = translated_value

        setattr(
            business,
            field,
            updated_value,
        )

    await db.flush()


async def create_business(
    data: BusinessCreateRequest,
    owner_id: str,
    language: str,
    db: AsyncSession,
) -> Business:

    lang_code = normalize_language(language)

    # ---------------------------------------------------------
    # Get coordinates if not provided
    # ---------------------------------------------------------

    latitude = data.latitude
    longitude = data.longitude

    if latitude is None or longitude is None:
        location_parts = [
            data.city,
            data.district,
            data.state,
            data.country,
        ]

        location = ", ".join(
            part.strip() for part in location_parts if part and part.strip()
        )

        if not location:
            raise HTTPException(
                status_code=400,
                detail="Unable to determine location for geocoding",
            )

        try:
            latitude, longitude = await asyncio.to_thread(
                get_coordinates,
                location,
            )

        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc

        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Unable to geocode business location",
            ) from exc

    # ---------------------------------------------------------
    # Create business
    # ---------------------------------------------------------
    validated_category = await normalize_and_validate_category(
        business_name=data.business_name,
        provided_category=data.category,
        description=data.description,
    )

    business = Business(
        owner_id=owner_id,
        business_name={lang_code: data.business_name},
        category={lang_code: validated_category},
        description=({lang_code: data.description} if data.description else {}),
        village=({lang_code: data.village} if data.village else {}),
        district={lang_code: data.district},
        city=({lang_code: data.city} if data.city else {}),
        state={lang_code: data.state},
        country={lang_code: data.country},
        margin_capital=data.margin_capital,
        pincode=data.pincode,
        latitude=latitude,
        longitude=longitude,
        status=BusinessStatus.pending,
    )

    db.add(business)

    try:
        await db.commit()
        await db.refresh(business)

    except IntegrityError:
        await db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Unable to create business",
        )

    return BusinessResponse(
        id=business.id,
        owner_id=business.owner_id,
        business_name=(business.business_name or {}).get(lang_code, ""),
        category=(business.category or {}).get(lang_code, ""),
        description=(business.description or {}).get(lang_code),
        village=(business.village or {}).get(lang_code),
        district=(business.district or {}).get(lang_code, ""),
        city=(business.city or {}).get(lang_code),
        state=(business.state or {}).get(lang_code, ""),
        country=(business.country or {}).get(lang_code, ""),
        margin_capital=business.margin_capital,
        pincode=business.pincode,
        latitude=business.latitude,
        longitude=business.longitude,
        status=business.status,
        created_at=business.created_at,
        updated_at=business.updated_at,
    )


def get_business_source_language(
    business: Business,
    target_language: str,
) -> str | None:
    """
    Find any language already available in the business data.

    English is NOT assumed to exist.
    """

    available_languages = set()

    for field in MULTILINGUAL_BUSINESS_FIELDS:
        value = getattr(business, field, None) or {}

        if isinstance(value, dict):
            available_languages.update(value.keys())

    # Prefer a language different from the requested language
    for language in available_languages:
        if language != target_language:
            return language

    # Fallback if only the requested language exists
    if target_language in available_languages:
        return target_language

    return None


async def get_business(
    business_id: str,
    language: str,
    owner_id: str,
    db: AsyncSession,
) -> BusinessResponse:

    lang_code = normalize_language(language)

    result = await db.execute(
        select(Business).where(
            Business.id == business_id,
            Business.owner_id == owner_id,
        )
    )

    business = result.scalar_one_or_none()

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found",
        )

    # ---------------------------------------------------------
    # Check whether ALL fields already have the requested language
    # ---------------------------------------------------------

    translation_missing = False

    for field in MULTILINGUAL_BUSINESS_FIELDS:
        value = getattr(business, field, None) or {}

        if lang_code not in value:
            translation_missing = True
            break

    # ---------------------------------------------------------
    # Translate if ANY field is missing
    # ---------------------------------------------------------

    if translation_missing:
        source_language = get_business_source_language(
            business=business,
            target_language=lang_code,
        )

        if not source_language:
            raise HTTPException(
                status_code=400,
                detail="No source language available for business translation.",
            )

        source_entry = {}

        for field in MULTILINGUAL_BUSINESS_FIELDS:
            value = getattr(business, field, None) or {}

            source_value = value.get(source_language)

            if source_value is not None:
                source_entry[field] = source_value

        if not source_entry:
            raise HTTPException(
                status_code=400,
                detail="No business data available for translation.",
            )

        translated_entry = await asyncio.to_thread(
            translate_entry,
            entry=source_entry,
            target_language=lang_code,
            source_language=source_language,
        )

        # -----------------------------------------------------
        # Store translated values
        # -----------------------------------------------------

        for field in MULTILINGUAL_BUSINESS_FIELDS:
            translated_value = translated_entry.get(field)

            if translated_value is None:
                continue

            current_value = getattr(business, field, None) or {}

            updated_value = dict(current_value)

            updated_value[lang_code] = translated_value

            setattr(
                business,
                field,
                updated_value,
            )

        await db.commit()
        await db.refresh(business)

    # ---------------------------------------------------------
    # Build response using requested language
    # ---------------------------------------------------------

    return BusinessResponse(
        id=business.id,
        owner_id=business.owner_id,
        business_name=(business.business_name or {}).get(lang_code, ""),
        category=(business.category or {}).get(lang_code, ""),
        description=(business.description or {}).get(lang_code),
        village=(business.village or {}).get(lang_code),
        district=(business.district or {}).get(lang_code, ""),
        city=(business.city or {}).get(lang_code),
        state=(business.state or {}).get(lang_code, ""),
        country=(business.country or {}).get(lang_code, ""),
        margin_capital=business.margin_capital,
        pincode=business.pincode,
        latitude=business.latitude,
        longitude=business.longitude,
        status=business.status,
        created_at=business.created_at,
        updated_at=business.updated_at,
    )


async def get_my_business_ids(
    user_id: str,
    db: AsyncSession,
) -> list[str]:

    print("USER ID FROM TOKEN:", user_id)

    result = await db.execute(select(Business).where(Business.owner_id == user_id))

    businesses = result.scalars().all()

    print("BUSINESSES FOUND:", businesses)

    return [str(business.id) for business in businesses]


async def mark_business_state(
    user_id: str,
    business_id: str,
    state: BusinessStatus,
    language: str,
    db: AsyncSession,
) -> BusinessResponse:
    lang_code = normalize_language(language)

    result = await db.execute(
        select(Business).where(
            Business.id == business_id,
            Business.owner_id == user_id,
        )
    )

    business = result.scalar_one_or_none()

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found",
        )

    business.status = state

    try:
        # Flush status changes before running translation checks
        await db.flush()

        # Ensure all multilingual fields are translated to the target language
        await ensure_business_language(
            business=business,
            target_language=lang_code,
            db=db,
        )

        await db.commit()
        await db.refresh(business)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Unable to update business status",
        )

    return BusinessResponse(
        id=business.id,
        owner_id=business.owner_id,
        business_name=(business.business_name or {}).get(lang_code, ""),
        category=(business.category or {}).get(lang_code, ""),
        description=(business.description or {}).get(lang_code),
        village=(business.village or {}).get(lang_code),
        district=(business.district or {}).get(lang_code, ""),
        city=(business.city or {}).get(lang_code),
        state=(business.state or {}).get(lang_code, ""),
        country=(business.country or {}).get(lang_code, ""),
        margin_capital=business.margin_capital,
        pincode=business.pincode,
        latitude=business.latitude,
        longitude=business.longitude,
        status=business.status,
        created_at=business.created_at,
        updated_at=business.updated_at,
    )


def _build_business_response(business: Business, lang_code: str) -> BusinessResponse:
    return BusinessResponse(
        id=business.id,
        owner_id=business.owner_id,
        business_name=(business.business_name or {}).get(lang_code, ""),
        category=(business.category or {}).get(lang_code, ""),
        description=(business.description or {}).get(lang_code),
        village=(business.village or {}).get(lang_code),
        district=(business.district or {}).get(lang_code, ""),
        city=(business.city or {}).get(lang_code),
        state=(business.state or {}).get(lang_code, ""),
        country=(business.country or {}).get(lang_code, ""),
        margin_capital=business.margin_capital,
        pincode=business.pincode,
        latitude=business.latitude,
        longitude=business.longitude,
        status=business.status,
        created_at=business.created_at,
        updated_at=business.updated_at,
    )



async def search_businesses(
    db: AsyncSession,
    user_id: str,
    language: str,
    name: str | None = None,
    category: str | None = None,
    status: BusinessStatus | None = None,
    village: str | None = None,
    district: str | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    pincode: str | None = None,
) -> list[BusinessResponse]:
    lang_code = normalize_language(language)
    user_lat, user_lon = await ensure_user_coordinates(user_id=user_id, db=db)

    filters = [Business.owner_id == user_id]

    if name:
        filters.append(
            func.lower(Business.business_name["en"].astext) == name.strip().lower()
        )
    if category:
        filters.append(
            func.lower(Business.category["en"].astext) == category.strip().lower()
        )
    if status:
        filters.append(Business.status == status)
    if village:
        filters.append(
            func.lower(Business.village["en"].astext) == village.strip().lower()
        )
    if district:
        filters.append(
            func.lower(Business.district["en"].astext) == district.strip().lower()
        )
    if city:
        filters.append(func.lower(Business.city["en"].astext) == city.strip().lower())
    if state:
        filters.append(func.lower(Business.state["en"].astext) == state.strip().lower())
    if country:
        filters.append(
            func.lower(Business.country["en"].astext) == country.strip().lower()
        )
    if pincode:
        filters.append(func.lower(Business.pincode) == pincode.strip().lower())

    if not filters:
        raise HTTPException(
            status_code=400,
            detail="At least one search filter is required",
        )

    result = await db.execute(select(Business).where(*filters))
    businesses = result.scalars().all()

    sorted_entries: list[tuple[float, BusinessResponse]] = []

    for business in businesses:
        await ensure_business_language(
            business=business,
            target_language=lang_code,
            db=db,
        )

        distance = (
            calculate_haversine_distance(
                user_lat, user_lon, business.latitude, business.longitude
            )
            if business.latitude is not None and business.longitude is not None
            else float("inf")
        )

        sorted_entries.append((distance, _build_business_response(business, lang_code)))

    await db.commit()
    sorted_entries.sort(key=lambda item: item[0])
    return [item[1] for item in sorted_entries]


async def search_other_businesses(
    db: AsyncSession,
    language: str,
    user_id: str | None = None,
    name: str | None = None,
    category: str | None = None,
    status: BusinessStatus | None = None,
    village: str | None = None,
    district: str | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    pincode: str | None = None,
) -> list[BusinessResponse]:
    lang_code = normalize_language(language)

    # 1. Resolve user coordinates if user_id is provided
    user_lat: float | None = None
    user_lon: float | None = None

    if user_id:
        try:
            user_lat, user_lon = await ensure_user_coordinates(user_id=user_id, db=db)
        except HTTPException:
            user_lat, user_lon = None, None

    # 2. Build query filters
    filters = []

    # Only filter out the user's businesses if user_id is given
    if user_id:
        filters.append(Business.owner_id != user_id)

    if name:
        filters.append(
            func.lower(Business.business_name["en"].astext) == name.strip().lower()
        )
    if category:
        filters.append(
            func.lower(Business.category["en"].astext) == category.strip().lower()
        )
    if status:
        filters.append(Business.status == status)
    if village:
        filters.append(
            func.lower(Business.village["en"].astext) == village.strip().lower()
        )
    if district:
        filters.append(
            func.lower(Business.district["en"].astext) == district.strip().lower()
        )
    if city:
        filters.append(func.lower(Business.city["en"].astext) == city.strip().lower())
    if state:
        filters.append(func.lower(Business.state["en"].astext) == state.strip().lower())
    if country:
        filters.append(
            func.lower(Business.country["en"].astext) == country.strip().lower()
        )
    if pincode:
        filters.append(func.lower(Business.pincode) == pincode.strip().lower())

    if not filters:
        raise HTTPException(
            status_code=400,
            detail="At least one search filter is required",
        )

    # 3. Query records
    query = select(Business).where(*filters)

    # If coordinates are missing, sort by newest creation date
    if user_lat is None or user_lon is None:
        query = query.order_by(Business.created_at.desc())

    result = await db.execute(query)
    businesses = result.scalars().all()

    # 4. Translation and response building
    if user_lat is not None and user_lon is not None:
        sorted_entries: list[tuple[float, BusinessResponse]] = []

        for business in businesses:
            await ensure_business_language(
                business=business,
                target_language=lang_code,
                db=db,
            )

            distance = (
                calculate_haversine_distance(
                    user_lat, user_lon, business.latitude, business.longitude
                )
                if business.latitude is not None and business.longitude is not None
                else float("inf")
            )

            sorted_entries.append(
                (distance, _build_business_response(business, lang_code))
            )

        await db.commit()
        sorted_entries.sort(key=lambda item: item[0])
        return [item[1] for item in sorted_entries]

    # Fallback response for unauthenticated / non-localized requests
    responses = []
    for business in businesses:
        await ensure_business_language(
            business=business,
            target_language=lang_code,
            db=db,
        )
        responses.append(_build_business_response(business, lang_code))

    await db.commit()
    return responses


async def get_active_businesses(
    language: str,
    db: AsyncSession,
    user_id: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[BusinessResponse]:
    """
    Fetches active businesses and ensures translations.

    - If user_id is provided and coordinates are resolved:
      returns businesses sorted by proximity to the user.
    - If user_id is None, user is not found, or coordinates cannot be resolved:
      returns businesses ordered normally by creation date (newest first).
    """
    lang_code = normalize_language(language)

    # 1. Try to get user coordinates if user_id is supplied
    user_lat: float | None = None
    user_lon: float | None = None

    if user_id:
        try:
            user_lat, user_lon = await ensure_user_coordinates(user_id=user_id, db=db)
        except HTTPException:
            # User profile not found, address invalid, or geocoding failed: fallback gracefully
            user_lat, user_lon = None, None

    # 2. Case A: Location is available -> Fetch all active, compute distance, sort & paginate
    if user_lat is not None and user_lon is not None:
        query = select(Business).where(Business.status == BusinessStatus.active)
        result = await db.execute(query)
        businesses = result.scalars().all()

        sorted_entries: list[tuple[float, BusinessResponse]] = []

        for business in businesses:
            await ensure_business_language(
                business=business,
                target_language=lang_code,
                db=db,
            )

            distance = (
                calculate_haversine_distance(
                    user_lat, user_lon, business.latitude, business.longitude
                )
                if business.latitude is not None and business.longitude is not None
                else float("inf")
            )

            sorted_entries.append(
                (distance, _build_business_response(business, lang_code))
            )

        await db.commit()

        # Sort globally by proximity and slice
        sorted_entries.sort(key=lambda item: item[0])
        paginated_entries = sorted_entries[offset : offset + limit]

        return [item[1] for item in paginated_entries]

    # 3. Case B: Fallback (no user_id or coordinates) -> Standard DB pagination ordered by created_at
    query = (
        select(Business)
        .where(Business.status == BusinessStatus.active)
        .order_by(Business.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    result = await db.execute(query)
    businesses = result.scalars().all()

    responses = []
    for business in businesses:
        await ensure_business_language(
            business=business,
            target_language=lang_code,
            db=db,
        )
        responses.append(_build_business_response(business, lang_code))

    await db.commit()

    return responses

async def get_business_owner_contact(
    business_id: str,
    db: AsyncSession,
) -> BusinessOwnerContactResponse:
    # Query Business and join User by owner_id
    query = (
        select(Business, User)
        .join(User, Business.owner_id == User.user_id)
        .where(Business.id == business_id)
    )

    result = await db.execute(query)
    record = result.first()

    if not record:
        # Check if the business exists without a user, or doesn't exist at all
        business_check = await db.scalar(
            select(Business.id).where(Business.id == business_id)
        )
        if not business_check:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner contact details not found",
        )

    business, owner = record

    return BusinessOwnerContactResponse(
        business_id=str(business.id),
        owner_id=str(owner.user_id),
        owner_name=getattr(owner, "full_name", getattr(owner, "name", None)),
        email=getattr(owner, "email", None),
        phone_number=getattr(owner, "phone_number", getattr(owner, "phone", None)),
    )