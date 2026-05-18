from langchain_ollama import OllamaLLM

from src.retrieval.query_vectorstore import query_vectorstore


def build_context(parent_documents):
    """
    Build the context that will be sent to the LLM.
    Each parent document includes section and page metadata.
    """

    context_parts = []

    for doc in parent_documents:
        section_id = doc.metadata.get("section_id", "unknown")
        section_title = doc.metadata.get("section_title", "unknown")
        page_start = doc.metadata.get("page_label_start", "unknown")
        page_end = doc.metadata.get("page_label_end", "unknown")

        context_part = f"""
[IEC 62304 - Section {section_id} - {section_title}]
Pages: {page_start} to {page_end}

{doc.page_content}
"""
        context_parts.append(context_part)

    return "\n\n".join(context_parts)


def generate_answer(question, context):
    """
    Generate an answer using only the retrieved IEC 62304 context.
    """

    if not context.strip():
        return "I could not find this information in the provided context."

    llm = OllamaLLM(model="mistral")

    prompt = f"""
You are an expert assistant specialized in IEC 62304.

Use ONLY the provided context.
Do NOT use external knowledge.
Do NOT invent IEC 62304 requirements.

If the answer is not in the context, reply:
"I could not find this information in the provided context."

Answer guidelines:

1. Understand the type of question:

- If the user asks for an explanation of a concept (e.g., "risk management", "software maintenance", "configuration management"):
    → Explain what the standard says about that concept.
    → Describe the relevant processes, requirements, or activities.
    → Use short paragraphs.

- If the user asks for a list (e.g., "list requirements", "what are the steps"):
    → Use bullet points.

- If the user asks a simple factual question:
    → Answer briefly in one paragraph.

2. Do NOT treat conceptual questions as structure questions.
   Do NOT list section titles unless the user explicitly asks for sections.

3. Always cite IEC 62304 when using context:
   Use format: (Section X.X, Page Y)

4. Keep answers clear and grounded in the context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response


def ask_iec62304(question):
    """
    Full IEC 62304 expert pipeline:
    - retrieve relevant parent-context documents
    - build LLM context
    - generate grounded answer
    Returns (answer, sources) where sources is a list of section dicts.
    """

    child_chunks, parent_documents = query_vectorstore(question, k=15)

    if not parent_documents:
        return "I could not find this information in the provided context.", []

    context = build_context(parent_documents)

    answer = generate_answer(question, context)

    if "could not find this information" in answer.lower():
        return answer, []

    sources = [
        {
            "section_id": doc.metadata.get("section_id", "?"),
            "section_title": doc.metadata.get("section_title", "?"),
            "page_label_start": doc.metadata.get("page_label_start", "?"),
            "page_label_end": doc.metadata.get("page_label_end", "?"),
        }
        for doc in parent_documents
    ]

    return answer, sources


if __name__ == "__main__":
    question = "What does IEC 62304 say about software maintenance?"

    print(f"Question: {question}\n")

    answer = ask_iec62304(question)

    print("Answer:\n")
    print(answer)