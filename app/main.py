"""
Main entry point for the Hackathon Project Revamp Agent.

This agent specializes in transforming open-source GitHub projects into
hackathon-winning solutions through strategic analysis, research, and innovation.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

try:
    from .core.agent_factory import AgentFactory
    from .teams.revamp_team import RevampTeam
    from .workflows.revamp_workflow import RevampWorkflow
    from .memory_storage import get_memory_manager
    from .session_manager import get_session_manager, SessionStatus
    from .core.exceptions import RevampError, ConfigurationError
except ImportError:
    # Handle relative import for direct execution
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from app.core.agent_factory import AgentFactory
    from app.teams.revamp_team import RevampTeam
    from app.workflows.revamp_workflow import RevampWorkflow
    from app.memory_storage import get_memory_manager
    from app.session_manager import get_session_manager, SessionStatus
    from app.core.exceptions import RevampError, ConfigurationError

# Load environment variables
load_dotenv(os.path.join(os.getcwd(), ".env"))
load_dotenv()

# Initialize managers
memory_manager = get_memory_manager()
session_manager = get_session_manager()

# Initialize factory for creating agents
agent_factory = AgentFactory()

# Create default instances for backward compatibility
_default_team = None
_default_workflow = None

def get_default_team() -> RevampTeam:
    """Get or create the default revamp team."""
    global _default_team
    if _default_team is None:
        _default_team = RevampTeam()
    return _default_team

def get_default_workflow() -> RevampWorkflow:
    """Get or create the default revamp workflow."""
    global _default_workflow
    if _default_workflow is None:
        _default_workflow = RevampWorkflow()
    return _default_workflow


def revamp_project(
    github_url: Optional[str] = None,
    hackathon_url: Optional[str] = None,
    hackathon_context: Optional[str] = None,
    search_order: str = "projects_first",
    search_topic: Optional[str] = None,
    use_team: bool = False
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
        use_team: Whether to use team-based approach (default: False, uses single agent)
    
    Returns:
        Comprehensive revamp strategy and recommendations
    
    Note: If neither github_url nor hackathon_url is provided, the agent will use discovery tools
    to find relevant options based on search_topic or general ongoing hackathons/projects.
    """
    try:
        # Validate inputs
        from .utils.validation import validate_inputs
        validated = validate_inputs(
            github_url=github_url,
            hackathon_url=hackathon_url,
            hackathon_context=hackathon_context,
            search_topic=search_topic,
            search_order=search_order
        )
        
        # Print warnings if any
        if validated.get("warnings"):
            for warning in validated["warnings"]:
                print(f"Warning: {warning}")
        
        if use_team:
            # Use team-based approach
            team = get_default_team()
            return team.create_strategy_only(
                github_url=github_url,
                hackathon_url=hackathon_url,
                hackathon_context=hackathon_context,
                search_topic=search_topic
            )
        else:
            # Use single agent approach
            strategy_agent = agent_factory.create_strategy_agent()
            return strategy_agent.create_revamp_strategy(
                github_url=github_url,
                hackathon_url=hackathon_url,
                hackathon_context=hackathon_context,
                search_order=search_order,
                search_topic=search_topic
            )
    except Exception as e:
        raise RevampError(f"Failed to create revamp strategy: {str(e)}")


def revamp_and_implement(
    github_url: Optional[str] = None,
    hackathon_url: Optional[str] = None,
    hackathon_context: Optional[str] = None,
    search_order: str = "projects_first",
    search_topic: Optional[str] = None,
    implement_changes: bool = False,
    fork_repo: bool = False,
    branch_name: str = "hackathon-revamp",
    use_workflow: bool = True
) -> Dict[str, Any]:
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
        use_workflow: Whether to use workflow-based approach (default: True)
    
    Returns:
        Dictionary with:
        - strategy: The revamp strategy text
        - implementation: Implementation summary (if implement_changes=True)
        - repo_name: Repository name used for implementation
        - execution_summary: Workflow execution details (if use_workflow=True)
    """
    try:
        # Validate inputs
        from .utils.validation import validate_inputs, validate_implementation_inputs
        
        validated = validate_inputs(
            github_url=github_url,
            hackathon_url=hackathon_url,
            hackathon_context=hackathon_context,
            search_topic=search_topic,
            search_order=search_order
        )
        
        impl_validated = validate_implementation_inputs(
            github_url=github_url,
            implement_changes=implement_changes,
            fork_repo=fork_repo,
            branch_name=branch_name
        )
        
        # Print warnings if any
        all_warnings = validated.get("warnings", []) + impl_validated.get("warnings", [])
        for warning in all_warnings:
            print(f"Warning: {warning}")
        
        if use_workflow:
            # Use workflow-based approach
            workflow = RevampWorkflow(include_coding_agent=implement_changes)
            result = workflow.execute(
                github_url=github_url,
                hackathon_url=hackathon_url,
                hackathon_context=hackathon_context,
                search_topic=search_topic,
                implement_changes=implement_changes,
                fork_repo=fork_repo,
                branch_name=branch_name
            )
            
            # Add repo name from validation
            if validated.get("github_repo_name"):
                result["repo_name"] = validated["github_repo_name"]
            
            return result
        else:
            # Use legacy approach for backward compatibility
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
                "repo_name": validated.get("github_repo_name")
            }
            
            # Step 2: Implement changes if requested
            if implement_changes:
                coding_agent = agent_factory.create_coding_agent()
                
                repo_name = validated.get("github_repo_name")
                if not repo_name:
                    result["implementation"] = "Repository name required for implementation. Please provide github_url."
                    return result
                
                if fork_repo:
                    implementation = coding_agent.fork_and_implement(
                        original_repo=repo_name,
                        revamp_strategy=strategy,
                        branch_name=branch_name
                    )
                else:
                    implementation = coding_agent.implement_strategy(
                        repo_name=repo_name,
                        revamp_strategy=strategy,
                        branch_name=branch_name
                    )
                
                result["implementation"] = implementation
            
            return result
            
    except Exception as e:
        raise RevampError(f"Failed to execute revamp workflow: {str(e)}")


# Convenience functions for specific use cases
def analyze_project_only(github_url: str) -> str:
    """Analyze a GitHub project only."""
    project_analyzer = agent_factory.create_project_analyzer()
    return project_analyzer.analyze_project(github_url)


def research_hackathon_only(hackathon_url: str) -> str:
    """Research a hackathon only."""
    hackathon_researcher = agent_factory.create_hackathon_researcher()
    return hackathon_researcher.research_hackathon(hackathon_url)


def create_strategy_with_team(
    github_url: Optional[str] = None,
    hackathon_url: Optional[str] = None,
    hackathon_context: Optional[str] = None,
    search_topic: Optional[str] = None
) -> Dict[str, Any]:
    """Create strategy using team collaboration."""
    team = get_default_team()
    return team.execute(
        github_url=github_url,
        hackathon_url=hackathon_url,
        hackathon_context=hackathon_context,
        search_topic=search_topic
    )


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