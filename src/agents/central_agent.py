from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

from src.agents.iec62304_expert_agent import ask_iec62304


@tool
def iec62304_expert_tool(question: str) -> str:
    """
    Use this tool to answer questions about IEC 62304, medical device software,
    software lifecycle processes, software maintenance, risk management,
    configuration management, testing, release, and problem resolution.
    """
    return ask_iec62304(question)


def create_central_agent():
    """
    Create the central AI4MDR agent.

    The central agent can:
    - answer normal conversational messages directly
    - call the IEC 62304 expert tool when needed
    - refuse questions outside its current scope
    """

    model = ChatOllama(model="llama3.2:1b")

    system_prompt = """
You are the AI4MDR central assistant.

You are a helpful AI assistant, but your technical knowledge is currently limited to IEC 62304
and medical device software regulation.

You have access to one specialist tool:
- iec62304_expert_tool

Use the IEC 62304 expert tool ONLY when the user asks about:
- IEC 62304
- medical device software
- software lifecycle processes
- software development
- software maintenance
- software risk management
- software configuration management
- software testing
- software release
- software problem resolution
- regulatory evidence for medical device software

For normal conversation, such as greetings, thanks, or short social messages, respond naturally yourself.
Do not call the tool for greetings or casual conversation.

If the user asks something outside your current scope, politely say that you cannot answer it at the moment
and that you can currently help with IEC 62304-related questions.

Do not invent IEC 62304 content yourself. For IEC 62304 questions, use the tool.
"""

    agent = create_agent(
        model=model,
        tools=[iec62304_expert_tool],
        system_prompt=system_prompt,
    )

    return agent


def get_last_ai_message(response):
    """
    Extract the final assistant message from the agent response.
    """

    messages = response.get("messages", [])

    if not messages:
        return "I could not generate a response."

    last_message = messages[-1]

    if hasattr(last_message, "content"):
        return last_message.content

    return str(last_message)


def run_chat():
    """
    Interactive terminal chat.
    """

    agent = create_central_agent()
    conversation_history = []

    print("Hello. How can I help you?\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() in ["exit", "quit", "q"]:
            print("Goodbye.")
            break

        if not user_message:
            print("Please write a question.")
            continue

        conversation_history.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        response = agent.invoke(
            {
                "messages": conversation_history
            }
        )

        answer = get_last_ai_message(response)

        print("\nAssistant:")
        print(answer)
        print()

        conversation_history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )


if __name__ == "__main__":
    run_chat()
    