# Copyright (c) Microsoft. All rights reserved.
"""Copilot Studio Agent — Explicit Settings.

A production-style configuration of ``CopilotStudioAgent``. Instead of relying on
the framework to wire everything up from environment variables, this sample
acquires an access token manually and builds an explicit ``ConnectionSettings`` /
``CopilotClient``. Use this pattern when you need control over the cloud, the
agent type, or the underlying HTTP session (for example, larger read buffers for
big connector payloads).

Two approaches are shown:
    1. Manual token + ConnectionSettings + CopilotClient.
    2. CopilotStudioAgent with all parameters passed explicitly.

Required environment variables (see .env.example):
    COPILOTSTUDIOAGENT__ENVIRONMENTID - Environment ID where your agent is deployed
    COPILOTSTUDIOAGENT__SCHEMANAME    - Agent identifier / schema name
    COPILOTSTUDIOAGENT__AGENTAPPID    - App Registration client ID
    COPILOTSTUDIOAGENT__TENANTID      - Tenant ID
"""

import asyncio
import os

from agent_framework.microsoft import CopilotStudioAgent, acquire_token
from dotenv import load_dotenv
from microsoft_agents.copilotstudio.client import (
    AgentType,
    ConnectionSettings,
    CopilotClient,
    PowerPlatformCloud,
)

# Load COPILOTSTUDIOAGENT__* values from a local .env file, if present.
load_dotenv()


async def example_with_connection_settings() -> None:
    """Build the client explicitly with a manually acquired token."""
    print("=== Copilot Studio Agent with Connection Settings ===")

    environment_id = os.environ["COPILOTSTUDIOAGENT__ENVIRONMENTID"]
    agent_identifier = os.environ["COPILOTSTUDIOAGENT__SCHEMANAME"]
    client_id = os.environ["COPILOTSTUDIOAGENT__AGENTAPPID"]
    tenant_id = os.environ["COPILOTSTUDIOAGENT__TENANTID"]

    # Acquire an access token (interactive sign-in on first run, cached after).
    token = acquire_token(
        client_id=client_id,
        tenant_id=tenant_id,
    )

    settings = ConnectionSettings(
        environment_id=environment_id,
        agent_identifier=agent_identifier,
        cloud=PowerPlatformCloud.PROD,  # e.g. PROD, GOV, HIGH, ...
        copilot_agent_type=AgentType.PUBLISHED,  # or AgentType.PREBUILT
        custom_power_platform_cloud=None,  # optional custom cloud endpoint
        # Raise aiohttp's per-line buffer above the 512 KB default so large
        # Copilot Studio activities don't raise LineTooLong.
        client_session_settings={"read_bufsize": 1024 * 1024},
    )

    client = CopilotClient(settings=settings, token=token)
    agent = CopilotStudioAgent(client=client)

    query = "What is the capital of Italy?"
    print(f"User:  {query}")
    result = await agent.run(query)
    print(f"Agent: {result}\n")


async def example_with_explicit_parameters() -> None:
    """Let the agent build the client, but pass every parameter explicitly."""
    print("=== Copilot Studio Agent with All Explicit Parameters ===")

    environment_id = os.environ["COPILOTSTUDIOAGENT__ENVIRONMENTID"]
    agent_identifier = os.environ["COPILOTSTUDIOAGENT__SCHEMANAME"]
    client_id = os.environ["COPILOTSTUDIOAGENT__AGENTAPPID"]
    tenant_id = os.environ["COPILOTSTUDIOAGENT__TENANTID"]

    agent = CopilotStudioAgent(
        environment_id=environment_id,
        agent_identifier=agent_identifier,
        client_id=client_id,
        tenant_id=tenant_id,
        cloud=PowerPlatformCloud.PROD,
        agent_type=AgentType.PUBLISHED,
    )

    query = "What is the capital of Japan?"
    print(f"User:  {query}")
    result = await agent.run(query)
    print(f"Agent: {result}\n")


async def main() -> None:
    await example_with_connection_settings()
    await example_with_explicit_parameters()


if __name__ == "__main__":
    asyncio.run(main())
