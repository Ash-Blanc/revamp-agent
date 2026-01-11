"""
AgentOS setup for the Hackathon Project Revamp Agent.

This module sets up the AgentOS runtime for production deployment.
AgentOS provides a FastAPI application that can be served locally or in the cloud.
"""

import os
from dotenv import load_dotenv
import langwatch
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.firecrawl import FirecrawlTools
from agno.os import AgentOS

# Load environment variables
load_dotenv()

# Initialize LangWatch
langwatch.setup(
    api_key=os.getenv("LANGWATCH_API_KEY"),
)

# Get the prompt from LangWatch
prompt = langwatch.prompts.get("hackathon_revamp_agent")

# Initialize tools
tools = [
    DuckDuckGoTools(),
]
try:
    from app.tools import HackathonDiscoveryTools
    tools.append(HackathonDiscoveryTools())
except ImportError:
    pass

if os.getenv("FIRECRAWL_API_KEY"):
    tools.append(FirecrawlTools())

# Create the agent
hackathon_revamp_agent = Agent(
    name="Revamp Agent",
    model="mistral:mistral-small-latest",
    instructions=prompt.prompt if prompt else "You are a helpful assistant.",
    tools=tools,
    markdown=True,
)

# Setup AgentOS
agent_os = AgentOS(
    description="AI agent that transforms open-source GitHub projects into hackathon-winning solutions through strategic analysis, research, and innovation",
    agents=[hackathon_revamp_agent],
)

# Get the FastAPI app
app = agent_os.get_app()


def serve():
    """Serve the AgentOS application."""
    agent_os.serve(app="app.os:app")


if __name__ == "__main__":
    serve()
