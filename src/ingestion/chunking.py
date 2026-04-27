# This tool divides parent documents into smaller overlapping child chunks

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.ingestion.load_pdf import load_pdf
from src.ingestion.parse_sections import parse_sections


def chunk_parent_documents(parent_documents, chunk_size=800, chunk_overlap=150):
    """
    Split parent section documents into smaller child chunks.

    Parameters:
    - parent_documents: list of section-level parent documents
    - chunk_size: maximum size of each child chunk
    - chunk_overlap: overlap between consecutive child chunks

    Returns:
    - A list of child chunks
    """

    # Create the text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # Split the parent documents into smaller child chunks
    child_chunks = splitter.split_documents(parent_documents)

    # Add metadata to mark these as child chunks
    for chunk in child_chunks:
        chunk.metadata["chunk_type"] = "child"

    return child_chunks


if __name__ == "__main__":
    """
    Test block:
    - load PDF
    - parse section-level parent documents
    - split parents into child chunks
    - print examples
    """

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