import logging
from typing import Any

from src.utils.translator_utils import Translator

logger = logging.getLogger(__name__)

SUPPORTED_REPORT_LANGUAGES = {
    "english": "en",
    "hindi": "hi",
    "bengali": "bn",
}


class ReportTranslationError(Exception):
    """Raised when feasibility report translation fails."""

    pass


def translate_feasibility_report(
    report_markdown: str,
    raw_evidence: dict[str, Any],
    target_language: str,
) -> dict[str, Any]:
    """
    Translate the feasibility report and all evidence.

    English remains the canonical/original version.
    Hindi and Bengali are generated only when requested.
    """

    language = target_language.strip().lower()

    if language not in SUPPORTED_REPORT_LANGUAGES:
        raise ReportTranslationError(
            f"Unsupported language: {target_language}. "
            f"Supported languages: "
            f"{', '.join(SUPPORTED_REPORT_LANGUAGES.keys())}"
        )

    if language == "english":
        return {
            "language": "english",
            "report_markdown": report_markdown,
            "raw_evidence": raw_evidence,
        }

    target_language_code = SUPPORTED_REPORT_LANGUAGES[language]

    translator = Translator()

    try:
        logger.info(
            "[TRANSLATION] Translating report to %s",
            language,
        )

        translated_report = translator.translate(
            text=report_markdown,
            target_language=target_language_code,
        )

        translated_evidence = translator.translate_json(
            data=raw_evidence,
            target_language=target_language_code,
        )

        logger.info(
            "[TRANSLATION] Translation completed successfully: %s",
            language,
        )

        return {
            "language": language,
            "report_markdown": translated_report,
            "raw_evidence": translated_evidence,
        }

    except Exception as exc:
        logger.exception(
            "[TRANSLATION] Failed to translate report to %s",
            language,
        )

        raise ReportTranslationError(
            f"Failed to translate feasibility report: {exc}"
        ) from exc