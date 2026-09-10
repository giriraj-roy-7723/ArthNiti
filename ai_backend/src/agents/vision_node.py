import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from src.config.config import GEMINI_MODEL_NAME

logger = logging.getLogger(__name__)

vision_llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL_NAME,
    temperature=0.1,
)


async def analyze_user_image(image_source: str, user_text: str = "") -> str:
    """Directly calls Gemini to extract business insights from base64 or URL."""
    if not image_source:
        return ""

    prompt = f"""
You are a business vision analyst. The user uploaded an image with the message: "{user_text}".
Analyze this image carefully.
Describe:
- What objects, store/stall setup, equipment, or products are visible.
- The condition, cleanliness, arrangement, or stock levels.
- Notable business-related observations.
Keep it factual, concise, and focused on operational details.
"""

    try:
        response = await vision_llm.ainvoke(
            [
                HumanMessage(
                    content=[
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_source}},
                    ]
                )
            ]
        )
        content = response.content
        if isinstance(content, list):
            return "".join(b.get("text", "") for b in content if isinstance(b, dict))
        return str(content)
    except Exception as e:
        logger.exception("Failed to analyze image with vision model")
        return f"[Image uploaded, but visual extraction failed: {str(e)}]"
