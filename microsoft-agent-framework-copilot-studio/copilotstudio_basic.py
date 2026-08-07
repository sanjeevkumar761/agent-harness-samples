# Copyright (c) Microsoft. All rights reserved.
"""Copilot Studio Agent — Basic Example.

The simplest way to call a Microsoft Copilot Studio agent from the Microsoft
Agent Framework. ``CopilotStudioAgent`` reads its connection settings from
environment variables, so all you need is ``agent.run(...)``.

This sample shows both a non-streaming response (the full answer at once) and a
streaming response (tokens as they are generated).

Required environment variables (see .env.example):
    COPILOTSTUDIOAGENT__ENVIRONMENTID - Environment ID where your agent is deployed
    COPILOTSTUDIOAGENT__SCHEMANAME    - Agent identifier / schema name
    COPILOTSTUDIOAGENT__AGENTAPPID    - App Registration client ID
    COPILOTSTUDIOAGENT__TENANTID      - Tenant ID
"""

import asyncio

from agent_framework.microsoft import CopilotStudioAgent
from dotenv import load_dotenv

# Load COPILOTSTUDIOAGENT__* values from a local .env file, if present.
load_dotenv()


async def non_streaming_example() -> None:
    """Get the complete result in a single call."""
    print("=== Non-streaming Response Example ===")

    agent = CopilotStudioAgent()

    query = "What is the capital of France?"
    print(f"User:  {query}")
    result = await agent.run(query)
    print(f"Agent: {result}\n")


async def streaming_example() -> None:
    """Print the response incrementally as the agent produces it."""
    print("=== Streaming Response Example ===")

    agent = CopilotStudioAgent()

    query = "What is the capital of Spain?"
    print(f"User:  {query}")
    print("Agent: ", end="", flush=True)
    async for chunk in agent.run(query, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print("\n")


async def main() -> None:
    await non_streaming_example()
    await streaming_example()


if __name__ == "__main__":
    asyncio.run(main())
