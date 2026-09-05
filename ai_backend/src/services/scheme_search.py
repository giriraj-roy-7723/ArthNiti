# src/services/scheme_search.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.schema.government_schemes import GovernmentScheme
from src.schema.scheme_embedding import SchemeEmbedding


def search_similar_schemes(
    session: Session,
    query_embedding: list[float],
    limit: int = 10,
):
    distance = SchemeEmbedding.embedding.cosine_distance(query_embedding)

    similarity = (1 - distance).label("similarity")

    stmt = (
        select(
            GovernmentScheme,
            similarity,
        )
        .join(
            SchemeEmbedding,
            SchemeEmbedding.scheme_id == GovernmentScheme.id,
        )
        .order_by(distance)
        .limit(limit)
    )

    return session.execute(stmt).all()
