# This tool will open pdf, read pages, print texto
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path):
    """
    Load a PDF file and return its content as a list of documents.

    Each document corresponds to one page of the PDF and contains:
    - page_content: the text of the page
    - metadata: information such as page number and source
    """

    
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    return documents


if __name__ == "__main__":
    """
    This block runs only when the file is executed directly.
    It is used here to test if the PDF loading works correctly
    """
    pdf_path = "data/raw/IEC_62304_2006_en_fr_.pdf"

    docs = load_pdf(pdf_path)

    print(f"Total pages: {len(docs)}")
    print("\nFirst page content:\n")
    print(docs[30].page_content[:1000])

#Converts the PDF into a formal that the system can use