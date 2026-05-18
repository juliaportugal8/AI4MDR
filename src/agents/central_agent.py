from langchain_ollama import OllamaLLM

from src.agents.iec62304_expert_agent import ask_iec62304
from src.agents.evaluation_agent import run_evaluation
from src.ingestion.load_pdf import load_pdf
from src.ingestion.parse_sections import parse_sections


PDF_PATH = "data/raw/IEC_62304_2006_en_fr_.pdf"

# Memory to store the last question and answer
conversation_memory = {
    "last_question": None,
    "last_answer": None,
}


def classify_message(user_message):
    """
    Simple deterministic routing.

    Since this assistant is specialized in IEC 62304:
    - simple conversation -> chitchat
    - document structure questions -> structure
    - evaluation request -> evaluate
    - everything else -> IEC 62304 expert agent
    """

    q = user_message.lower().strip()

    # Reject very short or meaningless input
    words = [w for w in q.split() if len(w) > 1]
    if len(q) < 4 or len(words) == 0:
        return "chitchat"

    chitchat_terms = [
        "hello",
        "hi",
        "hey",
        "thank you",
        "thanks",
        "obrigada",
        "obrigado",
    ]

    if any(term in q for term in chitchat_terms):
        has_question = "?" in user_message or any(
            word in q for word in ["how", "what", "when", "where", "why", "which", "define", "explain", "list"]
        )
        if not has_question:
            return "chitchat"

    structure_terms = [
        "how many sections",
        "number of sections",
        "list sections",
        "list the sections",
        "extracted sections",
        "document structure",
        "how is the document organized",
    ]

    if any(term in q for term in structure_terms):
        return "structure"

    compare_terms = [
        "compara a resposta",
        "compare the answer",
        "compare your answer",
        "compare the answer",
        "how accurate was",
        "evaluate your answer",
        "avalia a resposta",
    ]

    if any(term in q for term in compare_terms):
        return "evaluate"

    return "iec62304"


def answer_chitchat(user_message):
    """
    Answer normal conversational messages.
    """

    llm = OllamaLLM(model="mistral")

    prompt = f"""
You are a helpful assistant.
Respond briefly and naturally.

User message:
{user_message}

Answer:
"""

    return llm.invoke(prompt).strip()


def answer_structure_question(user_message):
    """
    Answer questions about the extracted structure of IEC 62304.
    """

    docs = load_pdf(PDF_PATH)
    sections = parse_sections(docs)

    # Group by top-level section
    top_level = {}
    for doc in sections:
        section_id = doc.metadata.get("section_id", "")
        top = section_id.split(".")[0]
        if top not in top_level:
            top_level[top] = []
        top_level[top].append(
            f"  {section_id} - {doc.metadata.get('section_title')}"
        )

    structure_lines = []
    for top, subsections in sorted(top_level.items(), key=lambda x: int(x[0])):
        structure_lines.append(f"Section {top}:")
        structure_lines.extend(subsections)

    llm = OllamaLLM(model="mistral")

    prompt = f"""
You are answering a question about the structure of IEC 62304.

The document has {len(top_level)} top-level sections (1 through {max(int(k) for k in top_level.keys())}).
It has {len(sections)} subsections in total.

Structure:
{chr(10).join(structure_lines)}

User question:
{user_message}

Answer clearly. Distinguish between top-level sections and subsections if relevant.
Do not invent sections.
"""

    return llm.invoke(prompt).strip()


def central_agent(user_message):
    """
    Main routing function. Classifies the message and calls the appropriate handler.
    """

    label = classify_message(user_message)

    if label == "evaluate":
        if conversation_memory["last_question"] is None:
            return {"answer": "No previous answer to evaluate. Please ask a question first.", "sources": [], "route": "evaluate"}
        report = run_evaluation(
            conversation_memory["last_question"],
            conversation_memory["last_answer"]
        )
        return {"answer": report, "sources": [], "route": "evaluate"}

    if label == "chitchat":
        return {"answer": answer_chitchat(user_message), "sources": [], "route": "chitchat"}

    if label == "structure":
        answer = answer_structure_question(user_message)
        conversation_memory["last_question"] = user_message
        conversation_memory["last_answer"] = answer
        return {"answer": answer, "sources": [], "route": "structure"}

    if label == "iec62304":
        answer, sources = ask_iec62304(user_message)
        conversation_memory["last_question"] = user_message
        conversation_memory["last_answer"] = answer
        return {"answer": answer, "sources": sources, "route": "iec62304"}


def run_chat():
    """
    Interactive terminal chat.
    """

    print("Hello. How can I help you?\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() in ["exit", "quit", "q"]:
            print("Goodbye.")
            break

        if not user_message:
            print("Please write a question.")
            continue

        result = central_agent(user_message)

        print("\nAssistant:")
        print(result["answer"])
        print()


if __name__ == "__main__":
    run_chat()
    