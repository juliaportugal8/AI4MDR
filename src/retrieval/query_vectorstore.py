#Here, lets teste just the retrieval part to see if the system finds the right excerpts

# Here, let's test just the retrieval part to see if the system finds the right excerpts

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document


def load_vectorstore(persist_directory="data/vectorstore"):
    """
    Load the existing vector store from disk.
    """

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    return vectorstore


def retrieve_relevant_child_chunks(question, k=5):
    """
    Retrieve the k most relevant child chunks for a given question.
    """

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search(question, k=k)

    return results


def group_chunks_by_parent(child_chunks):
    """
    Group retrieved child chunks by parent_id.
    """

    grouped = {}

    for chunk in child_chunks:
        parent_id = chunk.metadata.get("parent_id", "unknown")

        if parent_id not in grouped:
            grouped[parent_id] = []

        grouped[parent_id].append(chunk)

    return grouped


def reconstruct_parent_context(grouped_chunks):
    """
    Reconstruct parent-level context from retrieved child chunks.
    """

    parent_documents = []

    for parent_id, chunks in grouped_chunks.items():
        metadata = chunks[0].metadata.copy()

        combined_text = "\n\n".join(chunk.page_content for chunk in chunks)

        parent_doc = Document(
            page_content=combined_text,
            metadata={
                "parent_id": metadata.get("parent_id"),
                "section_id": metadata.get("section_id"),
                "section_title": metadata.get("section_title"),
                "page_start": metadata.get("page_start"),
                "page_end": metadata.get("page_end"),
                "page_label_start": metadata.get("page_label_start"),
                "page_label_end": metadata.get("page_label_end"),
                "source": metadata.get("source"),
                "language": metadata.get("language"),
                "reconstructed_from_children": True,
            },
        )

        parent_documents.append(parent_doc)

    return parent_documents


def select_top_parent_documents(parent_documents, max_parents=2):
    """
    Keep only the top N parent documents.

    Assumes that earlier documents are more relevant.
    """

    return parent_documents[:max_parents]


def query_vectorstore(question, k=5):
    """
    Full parent-child retrieval pipeline:
    1. retrieve relevant child chunks
    2. group them by parent
    3. reconstruct parent context
    4. select top parent documents
    """

    child_chunks = retrieve_relevant_child_chunks(question, k=k)
    grouped = group_chunks_by_parent(child_chunks)
    parent_documents = reconstruct_parent_context(grouped)

    top_parents = select_top_parent_documents(parent_documents)

    return child_chunks, top_parents


if __name__ == "__main__":
    question = "What does IEC 62304 say about software maintenance?"

    print(f"Question: {question}\n")

    child_chunks, parent_documents = query_vectorstore(question, k=5)

    print(f"Number of retrieved child chunks: {len(child_chunks)}\n")

    for i, chunk in enumerate(child_chunks, start=1):
        print(f"--- Child chunk {i} ---")
        print("Metadata:")
        print(chunk.metadata)
        print("\nContent preview:")
        print(chunk.page_content[:500])
        print("\n")

    print(f"\nNumber of selected parent documents: {len(parent_documents)}\n")

    for i, parent in enumerate(parent_documents, start=1):
        print(f"--- Parent document {i} ---")
        print("Metadata:")
        print(parent.metadata)
        print("\nContent preview:")
        print(parent.page_content[:1000])
        print("\n")