"""
Main entry point for the Hackathon Project Revamp Agent.

This agent specializes in transforming open-source GitHub projects into
hackathon-winning solutions through strategic analysis, research, and innovation.
"""

import os
from dotenv import load_dotenv
import langwatch
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.firecrawl import FirecrawlTools
from agno.tools.file import FileTools
from agno.tools.local_file_system import LocalFileSystemTools
try:
    from app.tools import HackathonDiscoveryTools
    from app.memory_storage import get_memory_manager
    from app.session_manager import get_session_manager, SessionStatus
    from app.teams_workflows import get_revamp_team, get_revamp_workflow
except ImportError:
    # Handle relative import for direct execution
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from app.tools import HackathonDiscoveryTools
    from app.memory_storage import get_memory_manager
    from app.session_manager import get_session_manager, SessionStatus
    from app.teams_workflows import get_revamp_team, get_revamp_workflow

# Load environment variables
# Try to load from current working directory first (for CLI usage)
load_dotenv(os.path.join(os.getcwd(), ".env"))
# Also try default loading (system env vars or local .env if script is run directly)
load_dotenv()

# Initialize LangWatch
langwatch.setup(
    api_key=os.getenv("LANGWATCH_API_KEY"),
)

# Get the prompt from LangWatch
prompt = langwatch.prompts.get("hackathon_revamp_agent")

# Initialize memory and session managers
memory_manager = get_memory_manager()
session_manager = get_session_manager()

# Initialize tools
tools = [
    DuckDuckGoTools(),
    HackathonDiscoveryTools(),  # Custom tools for discovering hackathons and projects
    FileTools(),
    LocalFileSystemTools(),
]
if os.getenv("FIRECRAWL_API_KEY"):
    tools.append(FirecrawlTools())

# Create the agent with memory integration
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions=prompt.prompt if prompt else "You are a helpful assistant.",
    tools=tools,
    markdown=True,
)


def revamp_project(
    github_url: str = None,
    hackathon_url: str = None,
    hackathon_context: str = None,
    search_order: str = "projects_first",
    search_topic: str = None
) -> str:
    """
    Revamp an open-source GitHub project for a specific hackathon.
    
    If URLs are not provided, the agent will automatically discover relevant options.
    
    Args:
        github_url: URL of the GitHub repository to revamp (optional)
        hackathon_url: URL of the hackathon website to analyze (optional)
        hackathon_context: Additional description of the hackathon theme, judging criteria, etc. (optional)
        search_order: Order of discovery when both URLs are missing. Options:
            - "projects_first": Find GitHub projects first, then find hackathons for them (default)
            - "hackathons_first": Find hackathons first, then find projects for them
        search_topic: Topic/theme to guide discovery when URLs are not provided (optional)
    
    Returns:
        Comprehensive revamp strategy and recommendations
    
    Note: If neither github_url nor hackathon_url is provided, the agent will use discovery tools
    to find relevant options based on search_topic or general ongoing hackathons/projects.
    """
    # Build the query based on what's provided
    query_parts = []
    needs_discovery = []
    
    if github_url:
        query_parts.append(f"GitHub Project: {github_url}")
    else:
        needs_discovery.append("github_project")
    
    if hackathon_url:
        query_parts.append(f"Hackathon Website: {hackathon_url}")
        query_parts.append(
            "Please scrape and analyze the hackathon website to understand: "
            "themes, judging criteria, prizes, deadlines, requirements, and any specific focus areas."
        )
    else:
        needs_discovery.append("hackathon")
    
    if hackathon_context:
        query_parts.append(f"Additional Hackathon Context: {hackathon_context}")
    
    # Build discovery instructions
    discovery_instructions = []
    
    if needs_discovery:
        if len(needs_discovery) == 2:
            # Both are missing - use search_order
            if search_order == "hackathons_first":
                discovery_instructions.append(
                    "1. First, use the find_ongoing_hackathons tool to discover relevant, ongoing hackathons. "
                    f"{'Focus on: ' + search_topic if search_topic else 'Look for popular and relevant hackathons'}."
                )
                discovery_instructions.append(
                    "2. Then, for each discovered hackathon, use find_projects_for_hackathon to find GitHub projects "
                    "that would be a good fit for that hackathon's theme."
                )
                discovery_instructions.append(
                    "3. Present the discovered options and select the best matches for revamp strategy."
                )
            else:  # projects_first (default)
                discovery_instructions.append(
                    "1. First, use the find_relevant_github_projects tool to discover relevant GitHub projects. "
                    f"{'Focus on topic: ' + search_topic if search_topic else 'Look for interesting open-source projects'}."
                )
                discovery_instructions.append(
                    "2. Then, for each discovered project, use find_hackathons_for_project to find hackathons "
                    "that would be a good fit for that project's topic/tech stack."
                )
                discovery_instructions.append(
                    "3. Present the discovered options and select the best matches for revamp strategy."
                )
        elif "github_project" in needs_discovery:
            discovery_instructions.append(
                "Use the find_relevant_github_projects tool to discover relevant GitHub projects. "
                f"{'Focus on topic: ' + search_topic if search_topic else 'Look for projects that align with the hackathon theme'}."
            )
        elif "hackathon" in needs_discovery:
            discovery_instructions.append(
                "Use the find_ongoing_hackathons tool to discover relevant, ongoing hackathons. "
                f"{'Focus on: ' + search_topic if search_topic else 'Look for hackathons that align with the project'}."
            )
    
    query = f"""
    Analyze the provided information and create a winning hackathon revamp strategy:
    
    {chr(10).join(query_parts) if query_parts else 'No specific URLs provided - discovery mode activated.'}
    
    {chr(10).join(discovery_instructions) if discovery_instructions else ''}
    
    Please provide:
    1. Project analysis (if GitHub URL provided or discovered: structure, features, tech stack, strengths/weaknesses)
    2. Hackathon analysis (if hackathon URL provided or discovered: themes, criteria, requirements, focus areas)
    3. Strategic positioning that aligns the project with hackathon goals
    4. Novel feature proposals that differentiate the project
    5. Comprehensive revamp plan with actionable steps
    6. Demo and presentation recommendations
    7. Differentiation tactics
    
    Focus on novelty, strategy, and research-backed enhancements.
    Use web scraping tools (Firecrawl) to gather detailed information from hackathon websites when URLs are provided.
    Use discovery tools (find_ongoing_hackathons, find_relevant_github_projects, etc.) when URLs are not provided.
    """
    
    response = agent.run(query)
    return response.content


def revamp_and_implement(
    github_url: str = None,
    hackathon_url: str = None,
    hackathon_context: str = None,
    search_order: str = "projects_first",
    search_topic: str = None,
    implement_changes: bool = False,
    fork_repo: bool = False,
    branch_name: str = "hackathon-revamp"
) -> dict:
    """
    Complete revamp workflow: strategy + optional implementation.
    
    This function:
    1. Creates a revamp strategy (using revamp_project)
    2. Optionally implements the changes via coding agent
    
    Args:
        github_url: URL of the GitHub repository to revamp (optional)
        hackathon_url: URL of the hackathon website to analyze (optional)
        hackathon_context: Additional description of the hackathon theme, etc. (optional)
        search_order: Order of discovery when both URLs are missing
        search_topic: Topic/theme to guide discovery (optional)
        implement_changes: If True, implement the strategy via coding agent (default: False)
        fork_repo: If True, fork the repository before implementing (default: False)
        branch_name: Name of the branch for changes (default: 'hackathon-revamp')
    
    Returns:
        Dictionary with:
        - strategy: The revamp strategy text
        - implementation: Implementation summary (if implement_changes=True)
        - repo_name: Repository name used for implementation
    """
    # Step 1: Generate revamp strategy
    strategy = revamp_project(
        github_url=github_url,
        hackathon_url=hackathon_url,
        hackathon_context=hackathon_context,
        search_order=search_order,
        search_topic=search_topic
    )
    
    result = {
        "strategy": strategy,
        "implementation": None,
        "repo_name": None
    }
    
    # Step 2: Implement changes if requested
    if implement_changes:
        try:
            from app.coding_agent import implement_revamp_strategy, fork_and_revamp
            
            # Extract repo name from github_url if provided
            repo_name = None
            if github_url:
                # Extract owner/repo from URL
                import re
                match = re.search(r'github\.com/([^/]+/[^/]+)', github_url)
                if match:
                    repo_name = match.group(1)
            
            if not repo_name:
                # Try to extract from strategy or ask user
                result["implementation"] = "Repository name required for implementation. Please provide github_url or repo_name."
                return result
            
            if fork_repo:
                # Fork and implement
                implementation = fork_and_revamp(
                    original_repo=repo_name,
                    revamp_strategy=strategy,
                    branch_name=branch_name
                )
            else:
                # Implement directly (user must have write access or work on their fork)
                implementation = implement_revamp_strategy(
                    repo_name=repo_name,
                    revamp_strategy=strategy,
                    branch_name=branch_name
                )
            
            result["implementation"] = implementation
            result["repo_name"] = repo_name
            
        except ImportError as e:
            result["implementation"] = f"Error importing coding agent: {e}"
        except Exception as e:
            result["implementation"] = f"Error during implementation: {e}"
    
    return result


def main():
    """Main entry point for the agent."""
    print("🚀 Hackathon Project Revamp Agent")
    print("=" * 50)
    print()
    print("This agent helps transform open-source projects into hackathon winners!")
    print()
    print("Example usage:")
    print("  from app.main import revamp_project, revamp_and_implement")
    print()
    print("  # Strategy only:")
    print("  result = revamp_project(")
    print("      github_url='https://github.com/user/repo',")
    print("      hackathon_url='https://hackathon-website.com'")
    print("  )")
    print()
    print("  # Strategy + Implementation (with forking):")
    print("  result = revamp_and_implement(")
    print("      github_url='https://github.com/user/repo',")
    print("      hackathon_url='https://hackathon-website.com',")
    print("      implement_changes=True,")
    print("      fork_repo=True")
    print("  )")
    print()
    print("  # Auto-discover and implement:")
    print("  result = revamp_and_implement(")
    print("      search_topic='AI',")
    print("      implement_changes=True")
    print("  )")
    print()
    print("Agent is ready! Use the revamp_project() function to get started.")


if __name__ == "__main__":
    main()