from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schema.government_schemes import GovernmentScheme
from src.schema.scheme_embedding import SchemeEmbedding


async def search_similar_schemes(
    db: AsyncSession,
    query_embedding: list[float],
    limit: int = 5,
    category: str | None = None,
    level: str | None = None,
) -> list[dict]:
    """
    Searches government schemes using cosine distance against pgvector embeddings.
    Allows optional category/level pre-filtering.
    """
    distance = SchemeEmbedding.embedding.cosine_distance(query_embedding)
    similarity = (1 - distance).label("similarity")

    stmt = select(
        GovernmentScheme.id,
        GovernmentScheme.scheme_name,
        GovernmentScheme.scheme_category,
        GovernmentScheme.level,
        GovernmentScheme.details,
        GovernmentScheme.benefits,
        GovernmentScheme.eligibility,
        GovernmentScheme.application,
        GovernmentScheme.documents,
        similarity,
    ).join(
        SchemeEmbedding,
        SchemeEmbedding.scheme_id == GovernmentScheme.id,
    )

    if category:
        stmt = stmt.where(GovernmentScheme.scheme_category.ilike(f"%{category}%"))
    if level:
        stmt = stmt.where(GovernmentScheme.level.ilike(f"%{level}%"))

    stmt = stmt.order_by(distance).limit(limit)

    result = await db.execute(stmt)
    rows = result.all()

    return [
        {
            "scheme_id": row.id,
            "scheme_name": row.scheme_name,
            "category": row.scheme_category,
            "level": row.level,
            "details": row.details,
            "benefits": row.benefits,
            "eligibility": row.eligibility,
            "application": row.application,
            "documents": row.documents,
            "similarity": round(float(row.similarity), 4),
        }
        for row in rows
    ]