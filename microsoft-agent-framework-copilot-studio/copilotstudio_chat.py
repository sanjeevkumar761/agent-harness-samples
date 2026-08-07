# Copyright (c) Microsoft. All rights reserved.
"""Copilot Studio Agent — Interactive Chat.

A small terminal chat loop (REPL) that streams responses from a Microsoft
Copilot Studio agent through the Microsoft Agent Framework. This is the best
script to run for a live demo: type a message, watch the agent stream back a
reply, and keep the conversation going with full multi-turn context.

Authentication uses an interactive user sign-in (a browser opens on first run).
The ``COPILOTSTUDIOAGENT__AGENTAPPID`` must therefore be a standard public-client
Entra App Registration (with 'Allow public client flows' enabled and a
http://localhost redirect URI) — not a Copilot Studio agent identity / blueprint,
which Entra blocks from interactive flows (AADSTS82018).

A conversation *thread* is created once and reused for every turn so the agent
remembers what was said earlier in the session.

Commands inside the chat:
    exit / quit / :q   End the session.
    reset              Start a fresh conversation thread.

Required environment variables (see .env.example):
    COPILOTSTUDIOAGENT__ENVIRONMENTID - Environment ID where your agent is deployed
    COPILOTSTUDIOAGENT__SCHEMANAME    - Agent identifier / schema name
    COPILOTSTUDIOAGENT__AGENTAPPID    - Public-client App Registration client ID
    COPILOTSTUDIOAGENT__TENANTID      - Tenant ID
"""

import asyncio

from agent_framework.microsoft import CopilotStudioAgent
from dotenv import load_dotenv

# Load COPILOTSTUDIOAGENT__* values from a local .env file, if present.
load_dotenv()

EXIT_COMMANDS = {"exit", "quit", ":q"}
BANNER = r"""
+------------------------------------------------------------+
|   Copilot Studio  x  Microsoft Agent Framework  (chat)     |
|                                                            |
|   Type a message and press Enter.                          |
|   'reset' clears the conversation, 'exit' ends it.         |
+------------------------------------------------------------+
"""


async def stream_reply(agent: CopilotStudioAgent, session, user_input: str) -> None:
    """Get a single agent reply and print it within the given session.

    Uses a non-streaming call: classic Copilot Studio agents deliver their answer
    as a final ``message`` activity rather than incremental ``typing`` activities,
    so streaming mode can yield no text for them.
    """
    result = await agent.run(user_input, session=session)
    print(f"Agent: {result.text}\n")


async def main() -> None:
    print(BANNER)

    agent = CopilotStudioAgent()
    session = agent.create_session()

    while True:
        try:
            user_input = input("You:   ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in EXIT_COMMANDS:
            print("Goodbye!")
            break

        if user_input.lower() == "reset":
            session = agent.create_session()
            print("(Conversation reset.)\n")
            continue

        try:
            await stream_reply(agent, session, user_input)
        except Exception as exc:  # noqa: BLE001 - surface any runtime error to the user
            print(f"\n[error] {exc}\n")


if __name__ == "__main__":
    asyncio.run(main())
