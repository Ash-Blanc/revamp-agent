"""
Coding Agent for implementing revamp strategies.

This agent specializes in:
- Reading and understanding codebases
- Making code changes based on revamp strategies
- Creating branches and commits
- Managing GitHub repositories
"""

import os
from dotenv import load_dotenv
import langwatch
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.github import GithubTools
from agno.tools.models.morph import MorphTools
from agno.tools.shell import ShellTools
from agno.tools.file import FileTools
from agno.tools.local_file_system import LocalFileSystemTools
from agno.tools.sleep import SleepTools

# Import model providers
try:
    from agno.models.cerebras import Cerebras
    CEREBRAS_AVAILABLE = True
except ImportError:
    CEREBRAS_AVAILABLE = False

try:
    from agno.models.mistral import MistralChat
    MISTRAL_AVAILABLE = True
except ImportError:
    MISTRAL_AVAILABLE = False

try:
    from agno.models.openrouter import OpenRouter
    OPENROUTER_AVAILABLE = True
except ImportError:
    OPENROUTER_AVAILABLE = False

try:
    from app.github_tools_extended import ExtendedGithubTools
    USE_EXTENDED_TOOLS = True
except ImportError:
    USE_EXTENDED_TOOLS = False

# Load environment variables
# Try to load from current working directory first (for CLI usage)
load_dotenv(os.path.join(os.getcwd(), ".env"))
# Also try default loading (system env vars or local .env if script is run directly)
load_dotenv()

# Initialize LangWatch
langwatch.setup(
    api_key=os.getenv("LANGWATCH_API_KEY"),
)

# Get coding agent prompt
try:
    prompt = langwatch.prompts.get("coding_agent")
except:
    prompt = None


def get_coding_model():
    """
    Get the coding model with fallback logic:
    1. Primary: Cerebras
    2. Fallback 1: Mistral
    3. Fallback 2: OpenRouter
    
    Returns:
        Model instance
    """
    # Try Cerebras first (primary)
    if CEREBRAS_AVAILABLE and os.getenv("CEREBRAS_API_KEY"):
        try:
            return Cerebras(id="llama-4-scout-17b-16e-instruct")
        except Exception as e:
            print(f"Warning: Could not initialize Cerebras model: {e}")
    
    # Fallback to Mistral
    if MISTRAL_AVAILABLE and os.getenv("MISTRAL_API_KEY"):
        try:
            return MistralChat(id="mistral-large-latest")
        except Exception as e:
            print(f"Warning: Could not initialize Mistral model: {e}")
    
    # Fallback to OpenRouter
    if OPENROUTER_AVAILABLE and os.getenv("OPENROUTER_API_KEY"):
        try:
            return OpenRouter(id="anthropic/claude-3.5-sonnet")
        except Exception as e:
            print(f"Warning: Could not initialize OpenRouter model: {e}")
    
    # Final fallback to OpenAI
    print("Warning: No preferred coding models available, falling back to OpenAI")
    return OpenAIChat(id="gpt-4o")

# Initialize tools
tools = []

# Add local system tools
tools.append(ShellTools())
tools.append(FileTools())
tools.append(LocalFileSystemTools())
tools.append(SleepTools())

# Add GitHub tools if API key is available
if os.getenv("GITHUB_ACCESS_TOKEN"):
    if USE_EXTENDED_TOOLS:
        tools.append(ExtendedGithubTools())
    else:
        tools.append(GithubTools())

# Add MorphTools for code editing if API key is available
if os.getenv("MORPH_API_KEY"):
    try:
        tools.append(MorphTools())
    except Exception as e:
        print(f"Warning: Could not initialize MorphTools: {e}")

# Get the coding model with fallback
coding_model = get_coding_model()

# Create the coding agent
coding_agent = Agent(
    model=coding_model,
    instructions=prompt.prompt if prompt else """You are an expert software engineer specializing in code refactoring and enhancement.

Your capabilities:
1. **Code Analysis**: Read and understand codebases, architecture, and patterns
2. **Code Modification**: Make precise code changes, refactoring, and enhancements
3. **File Management**: Create, update, and delete files as needed (both local and remote)
4. **Git Operations**: Work with branches, commits, and pull requests via GitHub API
5. **System Operations**: Run shell commands and manage local files

When making changes:
- Follow existing code style and patterns
- Write clean, maintainable code
- Add appropriate comments and documentation
- Ensure changes are incremental and testable
- Use GitHub tools to read files before modifying them
- Create branches for your changes
- Make atomic commits with clear messages
- Use local tools (Shell, File) when working on local projects

Always read the current file content before modifying it to preserve existing functionality.""",
    tools=tools,
    markdown=True,
)


def implement_revamp_strategy(
    repo_name: str,
    revamp_strategy: str,
    branch_name: str = "hackathon-revamp",
    base_branch: str = "main"
) -> str:
    """
    Implement a revamp strategy by making code changes to a repository.
    
    Args:
        repo_name: Full repository name (e.g., 'owner/repo')
        revamp_strategy: The revamp strategy and plan to implement
        branch_name: Name of the branch to create for changes (default: 'hackathon-revamp')
        base_branch: Base branch to create from (default: 'main')
    
    Returns:
        Summary of changes made
    """
    query = f"""
    Implement the following revamp strategy for repository {repo_name}:
    
    {revamp_strategy}
    
    Steps to follow:
    1. First, explore the repository structure using get_directory_content to understand the codebase
    2. Read key files to understand the current implementation
    3. Create a new branch '{branch_name}' from '{base_branch}' using create_branch
    4. Make the necessary code changes based on the revamp strategy:
       - **For code editing**: Prefer using MorphTools edit_file for AI-powered, precise edits:
         a. Use get_file_content to read the file from GitHub
         b. Save content to a temporary local file
         c. Use MorphTools edit_file with clear instructions and code edits
         d. Read the edited file and use update_file to commit back to GitHub
       - **For new files**: Use create_file directly
       - **For deletions**: Use delete_file
       - **Fallback**: If MorphTools is not available, use update_file directly
    5. Make incremental, logical commits with clear messages
    6. Provide a summary of all changes made
    
    Focus on:
    - Implementing the novel features proposed in the strategy
    - Making technical improvements
    - Enhancing code quality and maintainability
    - Following the project's existing patterns and style
    """
    
    response = coding_agent.run(query)
    return response.content


def fork_and_revamp(
    original_repo: str,
    revamp_strategy: str,
    fork_name: str = None,
    branch_name: str = "hackathon-revamp"
) -> str:
    """
    Fork a repository and implement revamp strategy.
    
    Note: GitHub API doesn't support forking via API directly in all cases.
    This function will guide the user or use alternative approaches.
    
    Args:
        original_repo: Full name of the original repository (e.g., 'owner/repo')
        revamp_strategy: The revamp strategy to implement
        fork_name: Name for the forked repository (optional, defaults to original name)
        branch_name: Name of the branch for changes
    
    Returns:
        Summary of fork and changes
    """
    # Note: GitHub API forking requires special permissions and may not work for all repos
    # Alternative: User should fork manually, then we work on their fork
    
    query = f"""
    The user wants to fork repository {original_repo} and implement a revamp strategy.
    
    IMPORTANT: 
    - First, try to fork the repository using fork_repository tool if available
    - If forking succeeds, use the forked repository name for all operations
    - If forking fails or tool is not available, guide the user to:
      1. Manually fork {original_repo} on GitHub
      2. Provide the forked repository name (their_username/repo_name)
    
    Once we have the repository:
    1. Create a branch '{branch_name}' 
    2. Implement the following revamp strategy:
    
    {revamp_strategy}
    
    Make all necessary code changes following the same process as implement_revamp_strategy.
    """
    
    response = coding_agent.run(query)
    return response.content