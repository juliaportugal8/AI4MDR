# Purpose of this file:
# Build or load a persistent Chroma vector store for IEC 62304 child chunks.
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import shutil
import os

from src.ingestion.load_pdf import load_pdf
from src.ingestion.parse_sections import parse_sections
from src.ingestion.chunking import chunk_parent_documents


def build_vectorstore(pdf_path, persist_directory="data/vectorstore"):
    """
    Build a vector store from the IEC 62304 PDF using the parent-child approach.
    Always deletes the existing vectorstore before rebuilding to avoid duplicates.
    """

    # Always delete existing vectorstore to avoid duplicates
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
        print(f"Deleted existing vectorstore at {persist_directory}")

    # Load the PDF as page-level documents
    docs = load_pdf(pdf_path)

    # Parse section-level parent documents
    parent_sections = parse_sections(docs)

    # Split parent sections into child chunks
    child_chunks = chunk_parent_documents(parent_sections)

    # Enrich chunks that have 'unknown' section_title
    # by extracting the title from the first line of content
    for chunk in child_chunks:
        if chunk.metadata.get("section_title") == "unknown":
            first_line = chunk.page_content.strip().splitlines()
            # First line is the section number, second line is the term
            if len(first_line) >= 2:
                chunk.metadata["section_title"] = first_line[1].strip()

    # Create the embedding model
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Build and persist the vector store using the child chunks
    vectorstore = Chroma.from_documents(
        documents=child_chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    return vectorstore, parent_sections, child_chunks


if __name__ == "__main__":
    pdf_path = "data/raw/IEC_62304_2006_en_fr_.pdf"

    print("Loading PDF and building parent-child vector store...")
    vectorstore, parent_sections, child_chunks = build_vectorstore(pdf_path)
    print("Vector store created successfully.\n")
    print(f"Total parent sections: {len(parent_sections)}")
    print(f"Total child chunks stored in vector store: {len(child_chunks)}")
    print("Saved in: data/vectorstore")