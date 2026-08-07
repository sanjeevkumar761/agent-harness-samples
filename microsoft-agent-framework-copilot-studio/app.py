# Copyright (c) Microsoft. All rights reserved.
"""Copilot Studio x Microsoft Agent Framework - Web Chat (Streamlit).

A polished browser chat UI that talks to a published Microsoft Copilot Studio
agent through the Microsoft Agent Framework. Run it with:

    streamlit run app.py

The first message triggers an interactive Entra sign-in (a browser tab opens on
the machine running Streamlit). Configuration is read from .env - see the sidebar
for the live connection details.
"""

from __future__ import annotations

import asyncio
import os
import time

import streamlit as st
from agent_framework.microsoft import CopilotStudioAgent
from dotenv import load_dotenv
from microsoft_agents.copilotstudio.client.power_platform_environment import (
    PowerPlatformEnvironment,
)

load_dotenv()

# --------------------------------------------------------------------------- #
# Page setup
# --------------------------------------------------------------------------- #
st.set_page_config(
    page_title="Copilot Studio x Agent Framework",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

EXAMPLE_PROMPTS = [
    "What is the capital of France?",
    "What can you help me with?",
    "Summarize what you do in one sentence.",
]


# --------------------------------------------------------------------------- #
# Agent lifecycle (created once per browser session, cached in session_state)
# --------------------------------------------------------------------------- #
def get_agent() -> CopilotStudioAgent:
    """Create the agent once and reuse it across Streamlit reruns."""
    if "agent" not in st.session_state:
        st.session_state.agent = CopilotStudioAgent()
        st.session_state.chat_session = st.session_state.agent.create_session()
    return st.session_state.agent


def new_conversation() -> None:
    """Start a fresh conversation (new session + cleared transcript)."""
    if "agent" in st.session_state:
        st.session_state.chat_session = st.session_state.agent.create_session()
    st.session_state.messages = []
    st.session_state.last_latency = None


def ask_agent(prompt: str) -> str:
    """Send one turn to the agent and return its reply text."""
    agent = get_agent()
    session = st.session_state.chat_session
    result = asyncio.run(agent.run(prompt, session=session))
    _capture_call(agent, session, prompt)
    return result.text


def _capture_call(agent: CopilotStudioAgent, session, prompt: str) -> None:
    """Record the real backend call details for the 'API & backend call' panel."""
    conversation_id = session.service_session_id
    conversation_id = conversation_id if isinstance(conversation_id, str) else None
    try:
        url = PowerPlatformEnvironment.get_copilot_studio_connection_url(
            settings=agent.client.settings,
            conversation_id=conversation_id,
        )
    except Exception:  # noqa: BLE001 - display-only; never block the chat
        url = "<built by CopilotClient at call time>"
    st.session_state.last_call = {
        "prompt": prompt,
        "conversation_id": conversation_id or "(assigned on first turn)",
        "url": url,
    }


# --------------------------------------------------------------------------- #
# Session state defaults
# --------------------------------------------------------------------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_latency" not in st.session_state:
    st.session_state.last_latency = None


# --------------------------------------------------------------------------- #
# Sidebar - connection details & controls
# --------------------------------------------------------------------------- #
def mask(value: str | None) -> str:
    if not value:
        return "—"
    return value if len(value) <= 8 else f"{value[:4]}…{value[-4:]}"


with st.sidebar:
    st.title("🤖 Connection")
    st.caption("Microsoft Agent Framework → Copilot Studio (Direct-to-Engine)")

    connected = "agent" in st.session_state
    st.markdown(
        f"**Status:** {'🟢 Connected' if connected else '⚪ Not connected yet'}"
    )

    st.divider()
    st.subheader("Configuration")
    st.markdown(
        f"""
- **Environment:** `{mask(os.getenv("COPILOTSTUDIOAGENT__ENVIRONMENTID"))}`
- **Agent (schema):** `{os.getenv("COPILOTSTUDIOAGENT__SCHEMANAME", "—")}`
- **Tenant:** `{mask(os.getenv("COPILOTSTUDIOAGENT__TENANTID"))}`
- **App (client) ID:** `{mask(os.getenv("COPILOTSTUDIOAGENT__AGENTAPPID"))}`
"""
    )

    if st.session_state.last_latency is not None:
        st.divider()
        st.metric("Last response", f"{st.session_state.last_latency:.2f} s")

    st.divider()
    st.button("🔄 New conversation", use_container_width=True, on_click=new_conversation)


# --------------------------------------------------------------------------- #
# Main - header & transcript
# --------------------------------------------------------------------------- #
st.title("Copilot Studio × Agent Framework")
st.caption(
    "A live chat with a published Copilot Studio agent, invoked from the "
    "Microsoft Agent Framework."
)

# --------------------------------------------------------------------------- #
# API & backend call panel - shows exactly how the UI reaches the agent
# --------------------------------------------------------------------------- #
with st.expander("🔌 API & backend call — how the UI talks to the agent", expanded=False):
    st.markdown("**1 · UI → Microsoft Agent Framework** (Python API this app calls)")
    st.code(
        "from agent_framework.microsoft import CopilotStudioAgent\n"
        "\n"
        "agent = CopilotStudioAgent()          # reads COPILOTSTUDIOAGENT__* env vars\n"
        "session = agent.create_session()      # holds multi-turn conversation state\n"
        "\n"
        "# one chat turn (async):\n"
        "response = await agent.run(\n"
        "    user_text,            # str | ChatMessage | list[...]\n"
        "    session=session,      # AgentSession — carries conversation context\n"
        "    stream=False,         # False → final AgentResponse; True → AgentResponseUpdate stream\n"
        ")\n"
        "reply = response.text     # the agent's answer as text/markdown",
        language="python",
    )

    st.markdown(
        "**2 · Agent Framework → Copilot Studio** (Direct-to-Engine HTTP call, "
        "made for you by `CopilotClient`)"
    )
    last = st.session_state.get("last_call")
    url = last["url"] if last else "<POST URL built from environment + schema + conversation id>"
    conv = last["conversation_id"] if last else "(assigned on first turn)"
    body_text = (last["prompt"] if last else "What is the capital of France?").replace('"', '\\"')
    st.code(
        f"POST {url}\n"
        "Authorization: Bearer <Entra access token>   # aud = https://api.powerplatform.com\n"
        "Content-Type: application/json\n"
        "Accept: text/event-stream                    # SSE stream of Activity objects\n"
        "\n"
        "{\n"
        '  "activity": {\n'
        '    "type": "message",\n'
        f'    "text": "{body_text}",\n'
        f'    "conversation": {{ "id": "{conv}" }}\n'
        "  }\n"
        "}",
        language="http",
    )
    st.caption(
        "Call stack:  `agent.run()`  →  `CopilotClient.ask_question()`  →  "
        "`POST` (SSE)  →  PPAPI gateway (validates the JWT + tenant)  →  "
        "Direct-to-Engine  →  published agent.  The reply streams back as "
        "`Activity` objects, which the Agent Framework maps to `AgentResponse.text`."
    )
    if last is None:
        st.info("Send a message to populate this panel with the real, live values.")

# Render the transcript so far.
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# Example-prompt buttons (only before the first message).
if not st.session_state.messages:
    st.write("Try one of these:")
    cols = st.columns(len(EXAMPLE_PROMPTS))
    for col, example in zip(cols, EXAMPLE_PROMPTS):
        if col.button(example, use_container_width=True):
            st.session_state.pending_prompt = example
            st.rerun()


# --------------------------------------------------------------------------- #
# Handle input (chat box or a clicked example)
# --------------------------------------------------------------------------- #
prompt = st.chat_input("Ask the Copilot Studio agent…")
if "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Signing in / contacting the agent…"):
            try:
                started = time.perf_counter()
                reply = ask_agent(prompt)
                st.session_state.last_latency = time.perf_counter() - started
            except Exception as exc:  # noqa: BLE001 - surface any error to the user
                reply = f"⚠️ **Error:** {exc}"
                st.session_state.last_latency = None
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
