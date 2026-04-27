from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from src.ingestion.load_pdf import load_pdf
from src.ingestion.parse_sections import parse_sections
from src.ingestion.chunking import chunk_parent_documents


def build_vectorstore(pdf_path, persist_directory="data/vectorstore"):
     """
    Build a vector store from the IEC 62304 PDF using the parent-child approach.

    Steps:
    1. Load the PDF as page-level documents
    2. Parse the English parent sections
    3. Split parent sections into child chunks
    4. Embed the child chunks
    5. Store them in Chroma
    """
    # Load the PDF as page-level documents 
     docs = load_pdf(pdf_path)

    # parse section- level parent documents
     parent_sections = parse_sections(docs)

     #split parent sections into child chunks
     child_chunks = chunk_parent_documents(parent_sections)

     #create the embedding model
     embeddings = OllamaEmbeddings(model="nomic-embed-text")

     #Build and persist the vector store using the child chunks
     vectorstore = Chroma.from_documents(
          documents=child_chunks,
          embedding=embeddings,
          persist_directory=persist_directory
     )

     return vectorstore, parent_sections, child_chunks
if __name__ == "__main__":
     """
      Test block:
    - build the vector store from the parent-child pipeline
    - print summary information
    """
     pdf_path = "data/raw/IEC_62304_2006_en_fr_.pdf"

     print("Loading PDF and building parent-child vector store...")
     vectorstore, parent_sections, child_chunks = build_vectorstore(pdf_path)
     print("Vector store created successfully.\n")
     print(f"Total parent sections: {len(parent_sections)}")
     print(f"Total child chunks stored in vector store: {len(child_chunks)}")
     print("Saved in: data/vectorstore")
    


  