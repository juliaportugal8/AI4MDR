# Purpose of this file: Import PDF pages and group them into section-level parent documents.

import re
from typing import List, Optional, Tuple

from langchain_core.documents import Document

from src.ingestion.load_pdf import load_pdf


def keep_english_pages(documents: List[Document]) -> List[Document]:
    """
    Keep only the English pages from the main normative body of IEC 62304.

    For this bilingual PDF:
    - French and English pages alternate
    - English pages are generally odd page labels
    - the main normative body is approximately from page 17 to page 67
    """

    english_docs = []

    for doc in documents:
        page_index = doc.metadata.get("page")
        page_label = doc.metadata.get("page_label")

        if page_label is not None:
            try:
                label = int(page_label)

                if label < 17 or label > 67:
                    continue

                if label % 2 == 1:
                    english_docs.append(doc)

                continue

            except ValueError:
                pass

        if page_index is not None:
            human_page = page_index + 1

            if human_page < 17 or human_page > 67:
                continue

            if human_page % 2 == 1:
                english_docs.append(doc)

    return english_docs


def normalize_line(line: str) -> str:
    """
    Normalize spacing.
    """

    line = line.replace("\u00a0", " ")
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def is_toc_or_noise_line(line: str) -> bool:
    """
    Detect lines that should not be used as section headings or content.
    """

    if not line:
        return True

    if "...." in line:
        return True

    noise_patterns = [
        "Licensed to",
        "Single user licence only",
        "ISO Store Order",
        "Downloaded:",
        "Customer Feedback Form",
    ]

    if any(pattern in line for pattern in noise_patterns):
        return True

    if "IEC:2006" in line and len(line) < 50:
        return True

    return False


def looks_like_table_heading(line: str) -> bool:
    """
    Detect lines that look like table rows accidentally parsed as section headings.
    """

    table_patterns = [
        "Yes/No",
        "Class A",
        "Class B",
        "Class C",
        "All requirements",
        "Related clause",
        "ISO 14971",
        "ISO 13485",
        "ISO/IEC 12207",
        "Table ",
        "Figure ",
    ]

    if any(pattern in line for pattern in table_patterns):
        return True

    if re.search(r"\bX\s+X\b", line):
        return True

    if len(re.findall(r"\b\d+\b", line)) > 5:
        return True

    return False


def is_valid_section_title(line: str) -> bool:
    """
    Validate whether a detected X.Y heading is likely to be a real section heading.
    """

    line = normalize_line(line)

    if is_toc_or_noise_line(line):
        return False

    if looks_like_table_heading(line):
        return False

    if not re.match(r"^\d+\.\d+\s+", line):
        return False

    if len(line.split()) > 18:
        return False

    return True


def is_section_heading(line: str) -> bool:
    """
    Detect X.Y headings used as parent documents.

    Examples:
    - 1.1 * Purpose
    - 5.1 * Software development planning
    - 6.2 * Problem and modification analysis
    """

    line = normalize_line(line)

    if not is_valid_section_title(line):
        return False

    pattern = r"^\d+\.\d+\s+\*?\s*[A-Z].+"

    return re.match(pattern, line) is not None


def is_top_level_heading(line: str) -> bool:
    """
    Detect top-level headings like:
    - 1 Scope
    - 5 Software development PROCESS
    - 6 Software maintenance PROCESS

    These act as boundaries, but are not saved as parent documents.
    """

    line = normalize_line(line)

    if is_toc_or_noise_line(line):
        return False

    if looks_like_table_heading(line):
        return False

    if len(line) < 8:
        return False

    if re.match(r"^\d+\.\d+", line):
        return False

    pattern = r"^\d+\s+\*?\s*[A-Z].+"

    return re.match(pattern, line) is not None


def extract_section_id_and_title(line: str) -> Tuple[str, str]:
    """
    Extract section id and title.

    Example:
    "6.2 * Problem and modification analysis"
    -> ("6.2", "Problem and modification analysis")
    """

    line = normalize_line(line)

    match = re.match(r"^(\d+\.\d+)\s+\*?\s*(.+)", line)

    if match:
        section_id = match.group(1).strip()
        section_title = match.group(2).strip()
        return section_id, section_title

    return "unknown", line


def safe_page_label(page_label) -> Optional[int]:
    """
    Convert PDF page_label metadata into an integer when possible.
    """

    if page_label is None:
        return None

    try:
        return int(page_label)
    except ValueError:
        return None


def make_parent_document(
    section_id: str,
    section_title: str,
    section_text: List[str],
    page_start: Optional[int],
    page_end: Optional[int],
    page_label_start: Optional[int],
    page_label_end: Optional[int],
    source: Optional[str],
) -> Document:
    """
    Build a LangChain Document representing one parent section.
    """

    return Document(
        page_content="\n".join(section_text),
        metadata={
            "parent_id": section_id,
            "section_id": section_id,
            "section_title": section_title,
            "page_start": page_start,
            "page_end": page_end,
            "page_label_start": page_label_start,
            "page_label_end": page_label_end,
            "source": source,
            "standard": "IEC 62304",
            "language": "en",
            "document_part": "main_normative_body",
            "document_type": "standard_section",
        },
    )


def parse_sections(documents: List[Document]) -> List[Document]:
    """
    Convert page-level documents into section-level parent documents.

    Strategy:
    - keep only English pages from the main normative body
    - use X.Y headings as parent documents
    - use X headings as boundaries
    - avoid treating table rows as section headings
    """

    english_docs = keep_english_pages(documents)
    sections = []

    current_section_id = None
    current_section_title = None
    current_section_text = []

    current_page_start = None
    current_page_end = None
    current_page_label_start = None
    current_page_label_end = None
    current_source = None

    for doc in english_docs:
        page_text = doc.page_content
        page_index = doc.metadata.get("page")
        page_label = safe_page_label(doc.metadata.get("page_label"))
        source = doc.metadata.get("source")

        lines = page_text.splitlines()

        for raw_line in lines:
            line = normalize_line(raw_line)

            if not line:
                continue

            if is_toc_or_noise_line(line):
                continue

            if is_section_heading(line):
                if current_section_id is not None and current_section_text:
                    sections.append(
                        make_parent_document(
                            current_section_id,
                            current_section_title,
                            current_section_text,
                            current_page_start,
                            current_page_end,
                            current_page_label_start,
                            current_page_label_end,
                            current_source,
                        )
                    )

                current_section_id, current_section_title = extract_section_id_and_title(line)
                current_section_text = [line]

                current_page_start = page_index
                current_page_end = page_index
                current_page_label_start = page_label
                current_page_label_end = page_label
                current_source = source

            elif is_top_level_heading(line):
                if current_section_id is not None and current_section_text:
                    sections.append(
                        make_parent_document(
                            current_section_id,
                            current_section_title,
                            current_section_text,
                            current_page_start,
                            current_page_end,
                            current_page_label_start,
                            current_page_label_end,
                            current_source,
                        )
                    )

                current_section_id = None
                current_section_title = None
                current_section_text = []

                current_page_start = None
                current_page_end = None
                current_page_label_start = None
                current_page_label_end = None
                current_source = None

            else:
                if current_section_id is not None:
                    current_section_text.append(line)
                    current_page_end = page_index
                    current_page_label_end = page_label

    if current_section_id is not None and current_section_text:
        sections.append(
            make_parent_document(
                current_section_id,
                current_section_title,
                current_section_text,
                current_page_start,
                current_page_end,
                current_page_label_start,
                current_page_label_end,
                current_source,
            )
        )

    return sections


if __name__ == "__main__":
    pdf_path = "data/raw/IEC_62304_2006_en_fr_.pdf"

    print("Loading PDF...")
    docs = load_pdf(pdf_path)

    print("Parsing English section-level parent documents...")
    sections = parse_sections(docs)

    print(f"Total page-level documents: {len(docs)}")
    print(f"Total parsed parent sections: {len(sections)}\n")

    if sections:
        print("First parent section metadata:")
        print(sections[0].metadata)

        print("\nFirst parent section content preview:\n")
        print(sections[0].page_content[:1200])

        print("\nSample section titles:\n")
        for section in sections[:15]:
            print(
                f"{section.metadata.get('section_id')} - "
                f"{section.metadata.get('section_title')} "
                f"(pages {section.metadata.get('page_label_start')} "
                f"to {section.metadata.get('page_label_end')})"
            )

        print("\nLast section titles:\n")
        for section in sections[-10:]:
            print(
                f"{section.metadata.get('section_id')} - "
                f"{section.metadata.get('section_title')} "
                f"(pages {section.metadata.get('page_label_start')} "
                f"to {section.metadata.get('page_label_end')})"
            )