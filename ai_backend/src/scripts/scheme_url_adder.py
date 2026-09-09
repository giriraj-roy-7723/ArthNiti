import asyncio
import os
import re
import time
from urllib.parse import urlparse

from google import genai
from google.genai import types
from sqlalchemy import text

from src.config.database import AsyncSessionLocal, engine


# ============================================================
# CONFIG
# ============================================================

MODEL_NAME = "gemini-3.5-flash-lite"

# Test with 10 first.
# Change to None after confirming the results.
LIMIT = None

REQUEST_DELAY = 1.0

# Number of rows committed at a time.
COMMIT_EVERY = 10


# ============================================================
# GEMINI CLIENT
# ============================================================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=GEMINI_API_KEY)


# ============================================================
# DATABASE
# ============================================================


async def ensure_columns():
    """
    Add the URL-related columns if they don't already exist.
    """

    async with engine.begin() as conn:
        await conn.execute(
            text(
                """
                ALTER TABLE government_schemes
                ADD COLUMN IF NOT EXISTS scheme_url TEXT;
                """
            )
        )

        await conn.execute(
            text(
                """
                ALTER TABLE government_schemes
                ADD COLUMN IF NOT EXISTS scheme_url_source TEXT;
                """
            )
        )

        await conn.execute(
            text(
                """
                ALTER TABLE government_schemes
                ADD COLUMN IF NOT EXISTS scheme_url_confidence TEXT;
                """
            )
        )

        await conn.execute(
            text(
                """
                ALTER TABLE government_schemes
                ADD COLUMN IF NOT EXISTS scheme_url_status TEXT;
                """
            )
        )


# ============================================================
# URL HELPERS
# ============================================================


def normalize_url(url):
    if not url:
        return ""

    url = str(url).strip()

    # Remove common punctuation surrounding URLs.
    url = url.strip(" \t\r\n.,;:()[]{}<>\"'")

    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def is_valid_url(url):
    if not url:
        return False

    try:
        parsed = urlparse(url)

        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

    except Exception:
        return False


def extract_urls(text):
    if not text:
        return []

    # URLs appearing in Gemini's textual response.
    pattern = r"https?://[^\s<>\"]+"

    matches = re.findall(
        pattern,
        text,
        flags=re.IGNORECASE,
    )

    urls = []

    for match in matches:
        url = normalize_url(match)

        if url and is_valid_url(url) and url not in urls:
            urls.append(url)

    return urls


# ============================================================
# EXISTING APPLICATION FIELD
# ============================================================


def extract_existing_url(application):
    """
    Your CSV/database already has an `application` field.

    If it already contains a URL, use it before doing
    an expensive Gemini search.
    """

    urls = extract_urls(application)

    if urls:
        return urls[0]

    return ""


# ============================================================
# GEMINI + GOOGLE SEARCH
# ============================================================


def find_application_url(
    scheme_name,
    slug,
    details,
    benefits,
    eligibility,
    application,
):
    """
    Use Gemini's Google Search grounding to find the
    actual application destination.
    """

    prompt = f"""
You are researching an Indian government scheme.

Your task is to find the OFFICIAL ONLINE APPLICATION
URL for this exact scheme.

SCHEME NAME:
{scheme_name}

SCHEME SLUG:
{slug}

DETAILS:
{details[:4000]}

BENEFITS:
{benefits[:3000]}

ELIGIBILITY:
{eligibility[:3000]}

APPLICATION INSTRUCTIONS FROM OUR DATABASE:
{application[:5000]}

------------------------------------------------------------

SEARCH REQUIREMENTS:

Search the web for this exact scheme.

First identify the official scheme page/source.

Then determine whether the scheme has an online application
process.

If an online application exists, find the ACTUAL URL where
the applicant starts the application/registration process.

Prefer:

- Official Government of India websites
- Official State Government websites
- Official Ministry/Department websites
- Official government implementing-agency websites
- The official myScheme page when it identifies the
  application destination

IMPORTANT:

Do NOT invent URLs.

Do NOT construct a URL from the scheme name or slug.

Do NOT return a Google search URL.

Do NOT return a news website.

Do NOT return a blog.

Do NOT return a private article.

Do NOT return a generic government homepage unless that
homepage is genuinely where the application starts.

If myScheme only provides scheme information and points
to another official portal, return the actual application
portal if you can identify it.

If the scheme is offline and applicants must visit an office,
return NO_URL.

The URL must be supported by the web search evidence.

------------------------------------------------------------

RETURN EXACTLY:

APPLICATION_URL:
<actual URL>

SOURCE_URL:
<official source URL>

CONFIDENCE:
HIGH

or:

APPLICATION_URL:
NO_URL

SOURCE_URL:
<best official source URL>

CONFIDENCE:
LOW

Do not guess.
"""

    try:
        google_search_tool = types.Tool(google_search=types.GoogleSearch())

        config = types.GenerateContentConfig(
            tools=[google_search_tool],
            temperature=0,
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=config,
        )

        response_text = response.text or ""

        # ----------------------------------------------------
        # 1. Try to extract explicit APPLICATION_URL.
        # ----------------------------------------------------

        application_match = re.search(
            r"APPLICATION_URL:\s*(https?://\S+)",
            response_text,
            flags=re.IGNORECASE,
        )

        application_url = ""

        if application_match:
            application_url = normalize_url(application_match.group(1))

        # ----------------------------------------------------
        # Explicit NO_URL
        # ----------------------------------------------------

        if re.search(
            r"APPLICATION_URL:\s*NO_URL",
            response_text,
            flags=re.IGNORECASE,
        ):
            application_url = ""

        # ----------------------------------------------------
        # 2. Extract explicit SOURCE_URL.
        # ----------------------------------------------------

        source_match = re.search(
            r"SOURCE_URL:\s*(https?://\S+)",
            response_text,
            flags=re.IGNORECASE,
        )

        source_url = ""

        if source_match:
            source_url = normalize_url(source_match.group(1))

        # ----------------------------------------------------
        # 3. Read grounding metadata.
        #
        # These are URLs actually returned by Google Search
        # grounding rather than URLs we invented.
        # ----------------------------------------------------

        grounded_urls = []

        try:
            candidate = response.candidates[0]

            metadata = getattr(
                candidate,
                "grounding_metadata",
                None,
            )

            if metadata:
                chunks = getattr(
                    metadata,
                    "grounding_chunks",
                    [],
                )

                for chunk in chunks:
                    web_chunk = getattr(
                        chunk,
                        "web",
                        None,
                    )

                    if not web_chunk:
                        continue

                    uri = getattr(
                        web_chunk,
                        "uri",
                        None,
                    )

                    if not uri:
                        continue

                    uri = normalize_url(uri)

                    if is_valid_url(uri) and uri not in grounded_urls:
                        grounded_urls.append(uri)

        except Exception as exc:
            print(f"  Grounding metadata warning: {exc}")

        # ----------------------------------------------------
        # 4. If Gemini explicitly gave a URL, use it.
        # ----------------------------------------------------

        if application_url and is_valid_url(application_url):
            return {
                "application_url": application_url,
                "source_url": source_url or application_url,
                "confidence": "HIGH",
                "response": response_text,
            }

        # ----------------------------------------------------
        # 5. We do NOT blindly select the first grounded URL.
        #
        # If Gemini couldn't identify an application URL,
        # don't turn an arbitrary search result into one.
        # ----------------------------------------------------

        return {
            "application_url": "",
            "source_url": source_url,
            "confidence": "LOW",
            "response": response_text,
            "grounded_urls": grounded_urls,
        }

    except Exception as exc:
        print(f"  Gemini search error: {exc}")

        return {
            "application_url": "",
            "source_url": "",
            "confidence": "ERROR",
            "response": str(exc),
            "grounded_urls": [],
        }


# ============================================================
# PROCESS ONE DATABASE ROW
# ============================================================


def process_scheme(row):
    scheme_id = row.id
    scheme_name = row.scheme_name
    slug = row.slug or ""

    details = row.details or ""
    benefits = row.benefits or ""
    eligibility = row.eligibility or ""
    application = row.application or ""

    print()
    print("=" * 100)
    print(f"ID:      {scheme_id}")
    print(f"SCHEME:  {scheme_name}")
    print(f"SLUG:    {slug}")
    print("=" * 100)

    # --------------------------------------------------------
    # First use URL already present in application field.
    # --------------------------------------------------------

    existing_url = extract_existing_url(application)

    if existing_url:
        print(f"Existing URL found: {existing_url}")

        return {
            "application_url": existing_url,
            "source_url": existing_url,
            "confidence": "EXISTING_DATA",
            "status": "FOUND",
            "response": "",
        }

    # --------------------------------------------------------
    # Otherwise use Gemini + Google Search.
    # --------------------------------------------------------

    print("No existing URL. Searching web...")

    result = find_application_url(
        scheme_name=scheme_name,
        slug=slug,
        details=details,
        benefits=benefits,
        eligibility=eligibility,
        application=application,
    )

    application_url = result.get(
        "application_url",
        "",
    )

    source_url = result.get(
        "source_url",
        "",
    )

    confidence = result.get(
        "confidence",
        "LOW",
    )

    response_text = result.get(
        "response",
        "",
    )

    if application_url:
        print(f"FOUND APPLICATION URL:")
        print(f"  {application_url}")

        print(f"CONFIDENCE: {confidence}")

        status = "FOUND"

    else:
        print("No application URL identified.")

        if source_url:
            print(f"SOURCE: {source_url}")

        status = "NOT_FOUND"

    return {
        "application_url": application_url,
        "source_url": source_url,
        "confidence": confidence,
        "status": status,
        "response": response_text,
    }


# ============================================================
# MAIN DATABASE PROCESS
# ============================================================


async def enrich_scheme_urls():

    await ensure_columns()

    async with AsyncSessionLocal() as session:
        # ----------------------------------------------------
        # Fetch schemes.
        #
        # Only process rows that have not already been
        # successfully processed.
        # ----------------------------------------------------

        query = text(
            """
            SELECT
                id,
                scheme_name,
                slug,
                details,
                benefits,
                eligibility,
                application
            FROM government_schemes
            WHERE id >= 875
                AND (scheme_url IS NULL OR TRIM(scheme_url) = '')
            ORDER BY id
            """
        )

        if LIMIT is not None:
            query = text(
                """
                SELECT
                    id,
                    scheme_name,
                    slug,
                    details,
                    benefits,
                    eligibility,
                    application
                FROM government_schemes
                WHERE id >= 875
                    AND (scheme_url IS NULL OR TRIM(scheme_url) = '')
                ORDER BY id
                LIMIT :limit
                """
            )

            result = await session.execute(
                query,
                {
                    "limit": LIMIT,
                },
            )

        else:
            result = await session.execute(query)

        rows = result.fetchall()

        print()
        print("=" * 100)
        print("GOVERNMENT SCHEME URL ENRICHMENT")
        print("=" * 100)
        print(f"Rows to process: {len(rows)}")

        found_count = 0
        not_found_count = 0

        # ----------------------------------------------------
        # Process rows.
        # ----------------------------------------------------

        for index, row in enumerate(rows, start=1):
            result = process_scheme(row)

            application_url = result["application_url"]

            source_url = result["source_url"]

            confidence = result["confidence"]

            status = result["status"]

            # ------------------------------------------------
            # Update database.
            # ------------------------------------------------

            await session.execute(
                text(
                    """
                    UPDATE government_schemes
                    SET
                        scheme_url = :scheme_url,
                        scheme_url_source = :source_url,
                        scheme_url_confidence = :confidence,
                        scheme_url_status = :status
                    WHERE id = :id
                    """
                ),
                {
                    "scheme_url": application_url or None,
                    "source_url": source_url or None,
                    "confidence": confidence,
                    "status": status,
                    "id": row.id,
                },
            )

            if application_url:
                found_count += 1
            else:
                not_found_count += 1

            # ------------------------------------------------
            # Commit periodically.
            # ------------------------------------------------

            if index % COMMIT_EVERY == 0:
                await session.commit()

                print()
                print(f"COMMITTED: {index}/{len(rows)}")
                print(f"FOUND: {found_count}")
                print(f"NOT FOUND: {not_found_count}")

            time.sleep(REQUEST_DELAY)

        # ----------------------------------------------------
        # Final commit.
        # ----------------------------------------------------

        await session.commit()

        print()
        print("=" * 100)
        print("COMPLETED")
        print("=" * 100)

        print(f"Processed : {len(rows)}")

        print(f"Found     : {found_count}")

        print(f"Not found : {not_found_count}")


# ============================================================
# ENTRY POINT
# ============================================================


async def main():

    try:
        await enrich_scheme_urls()

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
