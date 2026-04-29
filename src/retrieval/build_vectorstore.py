# Purpose of this file:
# Build or load a persistent Chroma vector store for IEC 62304 child chunks.
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from src.ingestion.load_pdf import load_pdf
from src.ingestion.parse_sections import parse_sections
from src.ingestion.chunking import chunk_parent_documents


def build_vectorstore(pdf_path, persist_directory="data/vectorstore"):
    """
    Build a vector store from the IEC 62304 PDF using section-based child chunks.
    """

    docs = load_pdf(pdf_path)

    parent_sections = parse_sections(docs)

    child_chunks = chunk_parent_documents(parent_sections)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = Chroma.from_documents(
        documents=child_chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    return vectorstore, parent_sections, child_chunks


if __name__ == "__main__":
    pdf_path = "data/raw/IEC_62304_2006_en_fr_.pdf"

    print("Loading PDF and building vector store...")
    vectorstore, parent_sections, child_chunks = build_vectorstore(pdf_path)

    print("Vector store created successfully.\n")
    print(f"Total parent sections: {len(parent_sections)}")
    print(f"Total child chunks stored in vector store: {len(child_chunks)}")
    print("Saved in: data/vectorstore")