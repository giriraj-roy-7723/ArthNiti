import logging
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.config.config import GEMINI_MODEL_NAME

logger = logging.getLogger(__name__)


class CategoryOutput(BaseModel):
    category: str = Field(
        description="The normalized standard business industry category in English or the provided language."
    )


async def normalize_and_validate_category(
    business_name: str,
    provided_category: str,
    description: str | None = None,
) -> str:
    """
    Validates and standardizes the user-provided category using the business name
    and description to prevent classification and downstream pipeline mismatches.
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL_NAME,
            temperature=0.0,
        ).with_structured_output(CategoryOutput)

        prompt = (
            "You are an expert business classification assistant.\n"
            f"- Business Name: {business_name}\n"
            f"- User-selected Category: {provided_category}\n"
            f"- Description: {description or 'N/A'}\n\n"
            "Task: Determine the most precise standard commercial industry/category for this business.\n"
            "- If the user-selected category is accurate and specific, keep it.\n"
            "- If it is vague, mismatched, misspelled, or contradicted by the name/description, correct it.\n"
        )

        result: CategoryOutput = await llm.ainvoke(
            [
                SystemMessage(
                    content="You normalize business industry categories accurately and concisely."
                ),
                HumanMessage(content=prompt),
            ]
        )

        return result.category.strip() or provided_category

    except Exception as e:
        logger.warning(
            f"Failed to normalize category, falling back to original '{provided_category}': {e}"
        )

        return provided_category
