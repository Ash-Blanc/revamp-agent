"""
Coding agent for implementing revamp strategies.
"""

from typing import List, Optional, Any
from ..core.base_agent import BaseRevampAgent

class CodingAgent(BaseRevampAgent):
    """
    Agent specialized in implementing code changes based on revamp strategies.
    """
    
    def __init__(self, model: Any = None, tools: Optional[List] = None):
        # Use provided model or default
        if model:
            self.custom_model = model
        
        super().__init__(
            tools=tools,
            prompt_name="coding_agent"
        )
        
        # Override agent creation to use custom model if provided
        if hasattr(self, 'custom_model'):
            from agno.agent import Agent
            instructions = self.prompt.prompt if self.prompt else self.get_default_instructions()
            self.agent = Agent(
                model=self.custom_model,
                instructions=instructions,
                tools=self.tools,
                markdown=True,
            )
    
    def get_default_instructions(self) -> str:
        return """You are an expert software engineer specializing in code refactoring and enhancement.

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

Always read the current file content before modifying it to preserve existing functionality."""
    
    def implement_strategy(
        self,
        repo_name: str,
        revamp_strategy: str,
        branch_name: str = "hackathon-revamp",
        base_branch: str = "main"
    ) -> str:
        """
        Implement a revamp strategy by making code changes.
        
        Args:
            repo_name: Full repository name (e.g., 'owner/repo')
            revamp_strategy: The revamp strategy to implement
            branch_name: Name of the branch to create
            base_branch: Base branch to create from
            
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
        
        return self.run(query)
    
    def fork_and_implement(
        self,
        original_repo: str,
        revamp_strategy: str,
        fork_name: Optional[str] = None,
        branch_name: str = "hackathon-revamp"
    ) -> str:
        """
        Fork a repository and implement revamp strategy.
        
        Args:
            original_repo: Full name of the original repository
            revamp_strategy: The revamp strategy to implement
            fork_name: Name for the forked repository (optional)
            branch_name: Name of the branch for changes
            
        Returns:
            Summary of fork and changes
        """
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
        
        Make all necessary code changes following the same process as implement_strategy.
        """
        
        return self.run(query)