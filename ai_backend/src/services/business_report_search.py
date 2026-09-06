from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schema.business_report_chunk import BusinessReportChunk


async def search_business_report(
    db: AsyncSession,
    business_id: str,
    query_embedding: list[float],
    limit: int = 5,
    version: int | None = None,
) -> list[dict]:
    """
    Performs cosine similarity search on the latest business report chunks.
    Filters strictly by business_id (and optionally latest version).
    """
    distance = BusinessReportChunk.embedding.cosine_distance(query_embedding)
    similarity = (1 - distance).label("similarity")

    # If version is not specified, resolve the latest version for this business
    if version is None:
        latest_version_stmt = (
            select(BusinessReportChunk.version)
            .where(BusinessReportChunk.business_id == business_id)
            .order_by(BusinessReportChunk.version.desc())
            .limit(1)
        )
        version_result = await db.execute(latest_version_stmt)
        version = version_result.scalar_one_or_none()

    stmt = select(
        BusinessReportChunk.section_number,
        BusinessReportChunk.section_title,
        BusinessReportChunk.chunk_index,
        BusinessReportChunk.content,
        similarity,
    ).where(BusinessReportChunk.business_id == business_id)

    if version is not None:
        stmt = stmt.where(BusinessReportChunk.version == version)

    stmt = stmt.order_by(distance).limit(limit)

    result = await db.execute(stmt)
    rows = result.all()

    return [
        {
            "section_number": row.section_number,
            "section_title": row.section_title,
            "chunk_index": row.chunk_index,
            "content": row.content,
            "similarity": float(row.similarity),
        }
        for row in rows
    ]
