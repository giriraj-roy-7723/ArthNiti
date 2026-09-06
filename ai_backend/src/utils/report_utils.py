import re

def parse_report_sections(markdown_text: str) -> list[dict]:
    """
    Splits the Markdown report into sections based on '## X. Title' headers.
    """
    pattern = re.compile(r"^##\s+(\d+)\.\s+(.*?)$", re.MULTILINE)
    matches = list(pattern.finditer(markdown_text))

    sections = []
    for i, match in enumerate(matches):
        section_number = int(match.group(1))
        section_title = match.group(2).strip()

        start_idx = match.end()
        end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(markdown_text)

        content = markdown_text[start_idx:end_idx].strip()
        # Remove markdown horizontal rules and extra whitespace
        content = re.sub(r"^---+\s*", "", content, flags=re.MULTILINE).strip()

        if content:
            sections.append(
                {"number": section_number, "title": section_title, "content": content}
            )

    return sections


def split_text_recursively(
    text: str, max_chars: int = 1500, overlap: int = 150
) -> list[str]:
    """
    Recursively splits large text sections into chunks matching embedding token limits.
    1500 characters safely fits within the 512 token limit of BGE-small.
    """
    if len(text) <= max_chars:
        return [text]

    separators = ["\n\n", "\n", ". ", ", ", " "]
    for sep in separators:
        if sep in text:
            splits = text.split(sep)
            chunks = []
            current_chunk = ""

            for split in splits:
                if len(current_chunk) + len(split) + len(sep) <= max_chars:
                    current_chunk += split + sep
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = split + sep

            if current_chunk:
                chunks.append(current_chunk.strip())

            # Verify if this separator successfully reduced chunk sizes
            if all(len(c) <= max_chars for c in chunks if c):
                return [c for c in chunks if c]

    # Hard fallback if no natural separators exist
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars - overlap)]
