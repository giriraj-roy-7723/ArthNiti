import asyncio

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.government_official_request import GovernmentOfficialUpdateRequest,GovernmentOfficialResponse
from src.schema.government_officials import GovernmentOfficial

from src.utils.translator_utils import translate_entry


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

MULTILINGUAL_FIELDS = [
    "designation",
    "agency_name",
    "agency_address",
    "agency_city",
    "agency_state",
    "agency_country",
]


def get_source_language(
    official: GovernmentOfficial,
    target_language: str,
) -> str | None:
    """
    Find a language that already exists in the database.

    English is NOT assumed to exist.
    """

    available_languages = set()

    for field in MULTILINGUAL_FIELDS:
        value = getattr(official, field, None) or {}

        if isinstance(value, dict):
            available_languages.update(value.keys())

    # Prefer a language different from the requested language
    for language in available_languages:
        if language != target_language:
            return language

    # If the requested language is the only available language
    if target_language in available_languages:
        return target_language

    return None


async def update_government_official(
    data: GovernmentOfficialUpdateRequest,
    language: str,
    user_id: str,
    db: AsyncSession,
) -> GovernmentOfficial:

    lang_code = LANG_NORMALIZER.get(language.strip().lower())

    if not lang_code:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}",
        )

    # Get existing government official profile
    result = await db.execute(
        select(GovernmentOfficial).where(GovernmentOfficial.user_id == user_id)
    )

    official = result.scalar_one_or_none()

    if not official:
        raise HTTPException(
            status_code=404,
            detail="Government official profile not found",
        )

    # ---------------------------------------------------------
    # Multilingual fields
    # ---------------------------------------------------------

    multilingual_fields = [
        "designation",
        "agency_name",
        "agency_address",
        "agency_city",
        "agency_state",
        "agency_country",
    ]

    multilingual_updates = {
        "designation": data.designation,
        "agency_name": data.agency_name,
        "agency_address": data.agency_address,
        "agency_city": data.agency_city,
        "agency_state": data.agency_state,
        "agency_country": data.agency_country,
    }

    has_multilingual_update = any(
        value is not None for value in multilingual_updates.values()
    )

    if has_multilingual_update:
        # -----------------------------------------------------
        # Find currently stored language
        # -----------------------------------------------------

        source_language = None

        for field in multilingual_fields:
            value = getattr(official, field, None) or {}

            if isinstance(value, dict) and value:
                source_language = next(iter(value.keys()))
                break

        if not source_language:
            raise HTTPException(
                status_code=400,
                detail="No existing language available for translation",
            )

        # -----------------------------------------------------
        # Build complete profile in target language
        # -----------------------------------------------------

        if source_language == lang_code:
            # Already in requested language.
            # Copy ALL existing values first so that a PATCH
            # of one field does not remove the other fields.

            translated_entry = {}

            for field in multilingual_fields:
                value = getattr(official, field, None) or {}

                if isinstance(value, dict):
                    existing_value = value.get(source_language)

                    if existing_value is not None:
                        translated_entry[field] = existing_value

        else:
            # Different language.
            # Translate the complete existing profile.

            source_entry = {}

            for field in multilingual_fields:
                value = getattr(official, field, None) or {}

                if isinstance(value, dict):
                    existing_value = value.get(source_language)

                    if existing_value is not None:
                        source_entry[field] = existing_value

            if not source_entry:
                raise HTTPException(
                    status_code=400,
                    detail="No government official data available for translation",
                )

            translated_entry = await asyncio.to_thread(
                translate_entry,
                entry=source_entry,
                target_language=lang_code,
                source_language=source_language,
            )

        # -----------------------------------------------------
        # Override ONLY the fields supplied in PATCH
        # -----------------------------------------------------

        for field, value in multilingual_updates.items():
            if value is not None:
                translated_entry[field] = value

        # -----------------------------------------------------
        # Store ONLY the requested language
        # -----------------------------------------------------

        for field in multilingual_fields:
            value = translated_entry.get(field)

            if value is not None:
                setattr(
                    official,
                    field,
                    {lang_code: value},
                )

    # ---------------------------------------------------------
    # Non-translated fields
    # ---------------------------------------------------------

    if data.agency_type is not None:
        official.agency_type = data.agency_type

    if data.agency_pincode is not None:
        official.agency_pincode = data.agency_pincode

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    try:
        await db.commit()
        await db.refresh(official)

    except IntegrityError:
        await db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Unable to update government official profile",
        )

    return GovernmentOfficialResponse(
        id=official.id,
        user_id=official.user_id,
        designation=(official.designation or {}).get(lang_code, ""),
        agency_name=(official.agency_name or {}).get(lang_code, ""),
        agency_address=(official.agency_address or {}).get(lang_code),
        agency_city=(official.agency_city or {}).get(lang_code),
        agency_state=(official.agency_state or {}).get(lang_code),
        agency_country=(official.agency_country or {}).get(lang_code),
        agency_type=official.agency_type,
        agency_pincode=official.agency_pincode,
        created_at=official.created_at,
    )

async def get_government_official(
    user_id: str,
    language: str,
    db: AsyncSession,
) -> GovernmentOfficial:

    lang_code = LANG_NORMALIZER.get(language.strip().lower())

    if not lang_code:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}",
        )

    # Get existing government official profile
    result = await db.execute(
        select(GovernmentOfficial).where(GovernmentOfficial.user_id == user_id)
    )

    official = result.scalar_one_or_none()

    if not official:
        raise HTTPException(
            status_code=404,
            detail="Government official profile not found",
        )

    # ---------------------------------------------------------
    # Check whether ALL multilingual fields have the
    # requested language
    # ---------------------------------------------------------

    translation_missing = any(
        lang_code not in (getattr(official, field, None) or {})
        for field in MULTILINGUAL_FIELDS
    )

    # ---------------------------------------------------------
    # Translate if ANY field is missing
    # ---------------------------------------------------------

    if translation_missing:
        # Find a language that already exists in the database
        source_language = get_source_language(
            official=official,
            target_language=lang_code,
        )

        if not source_language:
            raise HTTPException(
                status_code=400,
                detail="No source language available for translation",
            )

        # Get all fields from the selected source language
        source_entry = {}

        for field in MULTILINGUAL_FIELDS:
            value = getattr(official, field, None) or {}

            source_value = value.get(source_language)

            if source_value is not None:
                source_entry[field] = source_value

        if not source_entry:
            raise HTTPException(
                status_code=400,
                detail="No government official data available for translation",
            )

        # -----------------------------------------------------
        # Translate all fields in ONE call
        # -----------------------------------------------------

        translated_entry = await asyncio.to_thread(
            translate_entry,
            entry=source_entry,
            target_language=lang_code,
            source_language=source_language,
        )

        # -----------------------------------------------------
        # Store translations
        # -----------------------------------------------------

        for field in MULTILINGUAL_FIELDS:
            translated_value = translated_entry.get(field)

            if translated_value is None:
                continue

            current_value = getattr(official, field, None) or {}

            updated_value = dict(current_value)
            updated_value[lang_code] = translated_value

            setattr(
                official,
                field,
                updated_value,
            )

        try:
            await db.commit()
            await db.refresh(official)

        except IntegrityError:
            await db.rollback()

            raise HTTPException(
                status_code=400,
                detail="Unable to save translated government official profile",
            )

    return GovernmentOfficialResponse(
        id=official.id,
        user_id=official.user_id,
        designation=(official.designation or {}).get(lang_code, ""),
        agency_name=(official.agency_name or {}).get(lang_code),
        agency_address=(official.agency_address or {}).get(lang_code),
        agency_city=(official.agency_city or {}).get(lang_code),
        agency_state=(official.agency_state or {}).get(lang_code),
        agency_country=(official.agency_country or {}).get(lang_code),
        agency_type=official.agency_type,
        agency_pincode=official.agency_pincode,
        created_at=official.created_at,
    )
