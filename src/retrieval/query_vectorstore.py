#Here, lets teste just the retrieval part to see if the system finds the right excerpts

# Import the Chroma vector store
from langchain_chroma import Chroma

# Import the local embedding model from Ollama
from langchain_ollama import OllamaEmbeddings

# Import the Document class so we can rebuild parent documents
from langchain_core.documents import Document


def load_vectorstore(persist_directory="data/vectorstore"):
    """
    Load the existing vector store from disk.
    """

    # Use the same embedding model used to build the vector store
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Load the persisted Chroma database
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

    # Search the vector store using semantic similarity
    results = vectorstore.similarity_search(question, k=k)

    return results


def group_chunks_by_parent(child_chunks):
    """
    Group retrieved child chunks by parent_id.

    Returns a dictionary:
    {
        parent_id: [chunk1, chunk2, ...]
    }
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

    For now, this function combines the child chunks belonging to the same parent.
    Later, this can be upgraded to retrieve full stored parent documents if needed.

    Returns a list of reconstructed parent documents.
    """

    parent_documents = []

    for parent_id, chunks in grouped_chunks.items():
        # Use metadata from the first chunk as representative metadata
        metadata = chunks[0].metadata.copy()

        # Combine all child chunk texts belonging to the same parent
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


def query_vectorstore(question, k=5):
    """
    Full parent-child retrieval pipeline:
    1. retrieve relevant child chunks
    2. group them by parent
    3. reconstruct parent context
    """

    child_chunks = retrieve_relevant_child_chunks(question, k=k)
    grouped = group_chunks_by_parent(child_chunks)
    parent_documents = reconstruct_parent_context(grouped)

    return child_chunks, parent_documents


if __name__ == "__main__":
    """
    Test block:
    - ask a question
    - retrieve relevant child chunks
    - reconstruct parent-level context
    - print both results
    """

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

    print(f"\nNumber of reconstructed parent documents: {len(parent_documents)}\n")

    for i, parent in enumerate(parent_documents, start=1):
        print(f"--- Parent document {i} ---")
        print("Metadata:")
        print(parent.metadata)
        print("\nContent preview:")
        print(parent.page_content[:1000])
        print("\n")