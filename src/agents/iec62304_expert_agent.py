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
[Section {section_id} - {section_title}]
Pages: {page_start} to {page_end}

{doc.page_content}
"""
        context_parts.append(context_part)

    return "\n\n".join(context_parts)


def generate_answer(question, context):
    """
    Generate an answer using only the retrieved IEC 62304 context.
    """

    llm = OllamaLLM(model="llama3.2:1b")

    prompt = prompt = f"""
You are an expert assistant specialized in IEC 62304.

You MUST follow ALL rules strictly.

Rules:
1. Use ONLY the provided context.
2. Do NOT use external knowledge.
3. If the answer is not in the context, reply EXACTLY:
"I could not find this information in the provided context."

4. You MUST always cite BOTH Section ID and Page Number.
Use EXACTLY this format:
(Section X.X, Page Y)

5. Your answer MUST follow this structure:

- Start with:
"According to IEC 62304 (Section X.X, Page Y):"

- Then provide a bullet-point list of requirements.

- Each bullet point MUST end with a citation:
(Section X.X, Page Y)

6. Do NOT write malformed references (e.g., "Ic e6.1").
7. Do NOT omit the page number.

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
    """

    child_chunks, parent_documents = query_vectorstore(question, k=5)

    context = build_context(parent_documents)

    answer = generate_answer(question, context)

    return answer


if __name__ == "__main__":
    #Example question 
    question = "What does IEC 62304 say about software maintenance?"

    print(f"Question: {question}\n")

    answer = ask_iec62304(question)

    print("Answer:\n")
    print(answer)