# This tool divides parent documents into smaller overlapping child chunks
# Purpose of this file:
# Split section-level parent documents into smaller overlapping child chunks,
# while preserving IEC 62304 metadata for traceability.

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.ingestion.load_pdf import load_pdf
from src.ingestion.parse_sections import parse_sections


def chunk_parent_documents(parent_documents, chunk_size=800, chunk_overlap=150):
    """
    Split parent section documents into smaller child chunks.

    Each child chunk keeps the metadata from the parent section:
    - section_id
    - section_title
    - page labels
    - source
    - standard

    Additional metadata is added:
    - chunk_type
    - child_chunk_id
    - parent_id
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "; ",
            ", ",
            " ",
            "",
        ],
    )

    child_chunks = []

    for parent_doc in parent_documents:
        parent_id = parent_doc.metadata.get("parent_id", "unknown")
        section_id = parent_doc.metadata.get("section_id", "unknown")

        split_docs = splitter.split_documents([parent_doc])

        for i, chunk in enumerate(split_docs):
            chunk.metadata["chunk_type"] = "child"
            chunk.metadata["parent_id"] = parent_id
            chunk.metadata["section_id"] = section_id
            chunk.metadata["child_chunk_id"] = f"{section_id}_chunk_{i + 1}"
            chunk.metadata["chunk_index_within_parent"] = i + 1
            chunk.metadata["total_chunks_in_parent"] = len(split_docs)

            child_chunks.append(chunk)

    return child_chunks


if __name__ == "__main__":
    pdf_path = "data/raw/IEC_62304_2006_en_fr_.pdf"

    print("Loading PDF...")
    docs = load_pdf(pdf_path)

    print("Parsing parent sections...")
    parent_sections = parse_sections(docs)

    print("Creating child chunks from parent sections...")
    child_chunks = chunk_parent_documents(parent_sections)

    print(f"Total parent sections: {len(parent_sections)}")
    print(f"Total child chunks: {len(child_chunks)}\n")

    if child_chunks:
        print("First child chunk metadata:")
        print(child_chunks[0].metadata)

        print("\nFirst child chunk content preview:\n")
        print(child_chunks[0].page_content[:1000])

        print("\nSample child chunks:\n")
        for chunk in child_chunks[:10]:
            print(
                f"{chunk.metadata.get('child_chunk_id')} | "
                f"section {chunk.metadata.get('section_id')} - "
                f"{chunk.metadata.get('section_title')} | "
                f"pages {chunk.metadata.get('page_label_start')} "
                f"to {chunk.metadata.get('page_label_end')}"
            )