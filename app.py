import streamlit as st
import sys
import os
import json
import uuid
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agents.central_agent import central_agent
from src.agents.evaluation_agent import run_evaluation

CONVERSATIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "conversations")
os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

st.set_page_config(
    page_title="AI4MDR",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Background */
    .stApp {
        background-color: #EBF5F7;
    }

    /* Reduce side padding of main content area */
    .main .block-container {
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        padding-top: 0 !important;
        margin-top: -7rem !important;
        max-width: 100% !important;
    }

    /* Hide default streamlit header and toolbar */
    header[data-testid="stHeader"] {
        background-color: transparent;
    }
    div[data-testid="stToolbar"] {
        display: none;
    }
    #MainMenu {
        display: none;
    }
    footer {
        display: none;
    }

    /* Header banner */
    .ai4mdr-header {
        background: linear-gradient(135deg, #1A6B7A 0%, #2E8FA3 100%);
        padding: 36px 32px;
        border-radius: 12px;
        margin-bottom: 24px;
        margin-top: -6rem;
        box-shadow: 0 4px 12px rgba(26, 107, 122, 0.25);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .ai4mdr-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0 0 6px 0;
        letter-spacing: 0.5px;
    }
    .ai4mdr-subtitle {
        font-size: 0.88rem;
        color: #C8E8EF;
        margin: 0;
        font-style: italic;
    }

    /* Remove default white box from all messages */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-bottom: 10px !important;
        align-items: center !important;
        gap: 6px !important;
    }

    /* User message - flip to right, items packed to the right */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse;
        justify-content: flex-start;
    }

    /* Force zero margin on direct children of user message */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) > * {
        margin: 0 !important;
        flex-shrink: 0 !important;
    }

    /* Force zero margin on direct children of assistant message */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) > * {
        margin: 0 !important;
        flex-shrink: 0 !important;
    }

    /* User message bubble - teal */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) > div:not([data-testid="stChatMessageAvatarUser"]) {
        background-color: #1A6B7A !important;
        color: #FFFFFF !important;
        border-radius: 18px 4px 18px 18px !important;
        padding: 10px 16px !important;
        max-width: 78% !important;
        width: fit-content !important;
        min-width: 0 !important;
    }

    /* Remove ALL inner spacing inside user bubble */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) > div:not([data-testid="stChatMessageAvatarUser"]) * {
        padding: 0 !important;
        margin: 0 !important;
        color: #FFFFFF !important;
        line-height: 1.4 !important;
    }

    /* Assistant message - no bubble, text flows naturally */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) > div:not([data-testid="stChatMessageAvatarAssistant"]) {
        background-color: transparent !important;
        border: none !important;
        padding: 4px 12px !important;
        max-width: 90% !important;
        min-width: 0 !important;
    }

    /* User avatar - small, subtle dark red */
    div[data-testid="stChatMessageAvatarUser"] {
        background-color: #7B2020 !important;
        border-radius: 50% !important;
        min-width: 28px !important;
        width: 28px !important;
        height: 28px !important;
        flex-shrink: 0 !important;
        margin: 0 !important;
    }

    /* Assistant avatar - small, subtle teal */
    div[data-testid="stChatMessageAvatarAssistant"] {
        background-color: #2E8FA3 !important;
        border-radius: 50% !important;
        min-width: 28px !important;
        width: 28px !important;
        height: 28px !important;
        flex-shrink: 0 !important;
    }

    /* Scale avatar icons to fit */
    div[data-testid="stChatMessageAvatarUser"] svg,
    div[data-testid="stChatMessageAvatarAssistant"] svg {
        width: 16px !important;
        height: 16px !important;
    }

    /* Sources box */
    .sources-box {
        background-color: #D6EEF3;
        border-left: 4px solid #2E8FA3;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin-top: 10px;
    }
    .sources-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #1A6B7A;
        margin-bottom: 7px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .source-chip {
        display: inline-block;
        background-color: #2E8FA3;
        color: #FFFFFF;
        padding: 3px 10px;
        border-radius: 14px;
        font-size: 0.75rem;
        margin: 2px 3px 2px 0;
        font-weight: 500;
    }

    /* Evaluation box */
    .eval-box {
        background-color: #FFFFFF;
        border: 2px solid #2E8FA3;
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 10px;
    }
    .eval-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #1A6B7A;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Compare button */
    div[data-testid="stButton"] > button {
        background-color: #1A6B7A;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 8px 18px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 6px;
        transition: background-color 0.2s;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #2E8FA3;
        color: #FFFFFF;
    }

    /* Chat input bar background */
    div[data-testid="stBottom"] {
        background-color: #EBF5F7 !important;
        border-top: 1px solid #C8E8EE !important;
    }
    div[data-testid="stBottom"] > div {
        background-color: #EBF5F7 !important;
    }
    /* Remove corner decorations */
    div[data-testid="stChatInput"] span {
        display: none !important;
    }
    /* Chat input box */
    div[data-testid="stChatInput"] textarea {
        background-color: #FFFFFF !important;
        color: #2C3E50 !important;
        border-color: #2E8FA3 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: #1A6B7A !important;
        box-shadow: 0 0 0 2px rgba(26,107,122,0.2) !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #7FB5C0 !important;
    }
    /* Submit button (arrow) */
    div[data-testid="stChatInput"] button {
        background-color: #1A6B7A !important;
        border-color: #1A6B7A !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background-color: #2E8FA3 !important;
        border-color: #2E8FA3 !important;
    }
    /* Override focus ring on input container */
    div[data-testid="stChatInput"] > div {
        background-color: #FFFFFF !important;
        border-color: #1A6B7A !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #2E8FA3 !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Conversation persistence ──────────────────────────────────────────────────

def list_conversations():
    files = sorted(
        [f for f in os.listdir(CONVERSATIONS_DIR) if f.endswith(".json")],
        key=lambda f: os.path.getmtime(os.path.join(CONVERSATIONS_DIR, f)),
        reverse=True,
    )
    conversations = []
    for fname in files:
        path = os.path.join(CONVERSATIONS_DIR, fname)
        try:
            with open(path, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            conversations.append({
                "id": data.get("id", fname.replace(".json", "")),
                "title": data.get("title", "Untitled"),
                "timestamp": data.get("timestamp", ""),
                "filename": fname,
            })
        except Exception:
            pass
    return conversations


def save_conversation(conv_id, messages):
    if not messages:
        return
    user_msgs = [m for m in messages if m["role"] == "user"]
    title = user_msgs[0]["content"][:60] if user_msgs else "Untitled"
    data = {
        "id": conv_id,
        "title": title,
        "timestamp": datetime.now().isoformat(),
        "messages": messages,
    }
    path = os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json")
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def load_conversation(conv_id):
    path = os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    return data.get("messages", [])


# ── Session state ─────────────────────────────────────────────────────────────
if "conv_id" not in st.session_state:
    st.session_state.conv_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_iec_question" not in st.session_state:
    st.session_state.last_iec_question = None
if "last_iec_answer" not in st.session_state:
    st.session_state.last_iec_answer = None
if "show_compare" not in st.session_state:
    st.session_state.show_compare = False
if "evaluation_result" not in st.session_state:
    st.session_state.evaluation_result = None


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #1A6B7A;
        }
        section[data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }
        /* New conversation button */
        section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
            background-color: rgba(255,255,255,0.15) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255,255,255,0.35) !important;
            border-radius: 8px !important;
            width: 100% !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            margin-bottom: 4px !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
            background-color: rgba(255,255,255,0.25) !important;
        }
        .sidebar-logo {
            font-size: 1.4rem;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
        }
        .sidebar-tagline {
            font-size: 0.75rem;
            color: #C8E8EF;
            font-style: italic;
            margin-bottom: 18px;
        }
        .about-box {
            background-color: rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 12px 14px;
            margin-bottom: 16px;
        }
        .about-text {
            font-size: 0.8rem;
            color: #D8F0F5;
            line-height: 1.55;
        }
        .about-text b {
            color: #FFFFFF !important;
        }
        .sidebar-divider {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.2);
            margin: 14px 0 12px 0;
        }
        .history-label {
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #A8D8E0;
            margin-bottom: 8px;
        }
        .conv-item {
            background-color: rgba(255,255,255,0.08);
            border-radius: 6px;
            padding: 8px 10px;
            margin-bottom: 5px;
            cursor: pointer;
            transition: background-color 0.15s;
        }
        .conv-item:hover {
            background-color: rgba(255,255,255,0.18);
        }
        .conv-item-active {
            background-color: rgba(255,255,255,0.22) !important;
            border-left: 3px solid #FFFFFF;
            padding-left: 7px;
        }
        .conv-title {
            font-size: 0.82rem;
            color: #FFFFFF;
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .conv-date {
            font-size: 0.7rem;
            color: #A8D8E0;
            margin-top: 1px;
        }
        .no-history {
            font-size: 0.78rem;
            color: #A8D8E0;
            font-style: italic;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-logo">AI4MDR</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Agentic AI for Medical Device Regulation</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="about-box">
        <div class="about-text">
            <b>AI4MDR</b> is an AI assistant specialized in <b>IEC 62304</b> — the international standard for medical device software development.<br><br>
            Ask about software life cycle processes, safety classification, risk management, documentation requirements, or any clause of the standard.<br><br>
            Answers are grounded exclusively in the IEC 62304 document using Retrieval-Augmented Generation (RAG).
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("+ New conversation"):
        if st.session_state.messages:
            save_conversation(st.session_state.conv_id, st.session_state.messages)
        st.session_state.conv_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.last_iec_question = None
        st.session_state.last_iec_answer = None
        st.session_state.show_compare = False
        st.session_state.evaluation_result = None
        st.rerun()

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="history-label">Conversation history</div>', unsafe_allow_html=True)

    conversations = list_conversations()

    if not conversations:
        st.markdown('<div class="no-history">No previous conversations yet.</div>', unsafe_allow_html=True)
    else:
        for conv in conversations:
            is_active = conv["id"] == st.session_state.conv_id
            try:
                dt = datetime.fromisoformat(conv["timestamp"])
                date_str = dt.strftime("%b %d, %Y")
            except Exception:
                date_str = ""

            label = conv["title"] if len(conv["title"]) <= 36 else conv["title"][:34] + "…"

            if is_active:
                st.markdown(
                    f'<div class="conv-item conv-item-active">'
                    f'<div class="conv-title">{label}</div>'
                    f'<div class="conv-date">{date_str}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                if st.button(f"{label}\n{date_str}", key=f"conv_{conv['id']}"):
                    if st.session_state.messages:
                        save_conversation(st.session_state.conv_id, st.session_state.messages)
                    loaded = load_conversation(conv["id"])
                    st.session_state.conv_id = conv["id"]
                    st.session_state.messages = loaded
                    st.session_state.last_iec_question = None
                    st.session_state.last_iec_answer = None
                    st.session_state.show_compare = False
                    st.session_state.evaluation_result = None
                    st.rerun()


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ai4mdr-header">
    <div class="ai4mdr-title">AI4MDR</div>
    <div class="ai4mdr-subtitle">Agentic AI for Medical Device Regulation Certification</div>
</div>
""", unsafe_allow_html=True)


def render_sources(sources):
    if not sources:
        return
    chips = "".join(
        f'<span class="source-chip">Clause {s["section_id"]} — {s["section_title"]}</span>'
        for s in sources
    )
    st.markdown(
        f'<div class="sources-box">'
        f'<div class="sources-label">Sources — IEC 62304</div>'
        f'{chips}'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            render_sources(msg["sources"])
        if msg.get("evaluation"):
            st.markdown(
                f'<div class="eval-box">'
                f'<div class="eval-label">Evaluation Report</div>'
                f'{msg["evaluation"]}'
                f'</div>',
                unsafe_allow_html=True,
            )

# ── Compare button (shown after last iec62304 answer) ─────────────────────────
if st.session_state.show_compare:
    if st.button("Compare with reference answer"):
        with st.spinner("Evaluating answer..."):
            eval_result = run_evaluation(
                st.session_state.last_iec_question,
                st.session_state.last_iec_answer,
            )
        st.session_state.evaluation_result = eval_result
        for msg in reversed(st.session_state.messages):
            if msg["role"] == "assistant" and msg.get("sources") is not None:
                msg["evaluation"] = eval_result
                break
        st.session_state.show_compare = False
        save_conversation(st.session_state.conv_id, st.session_state.messages)
        st.rerun()

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question about Software Medical Device..."):
    st.session_state.show_compare = False
    st.session_state.evaluation_result = None

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = central_agent(prompt)

        answer = result["answer"]
        sources = result["sources"]
        route = result["route"]

        st.markdown(answer)
        if sources:
            render_sources(sources)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources if sources else None,
    })

    save_conversation(st.session_state.conv_id, st.session_state.messages)

    if route == "iec62304" and sources:
        st.session_state.last_iec_question = prompt
        st.session_state.last_iec_answer = answer
        st.session_state.show_compare = True

    st.rerun()
