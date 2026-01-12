"""
Extended GitHub tools.
"""
from typing import Optional
import json
from agno.tools.github import GithubTools
from agno.tools import tool
from app.utils.logger import logger

class ExtendedGithubTools(GithubTools):
    """Extended GitHub tools with additional functionality like forking."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Manually register the fork_repository tool if not auto-discovered
        # Agno's Toolkit might need explicit tool registration depending on version
        # But @tool decorator should handle it if inspected.
    
    @tool
    def fork_repository(self, repo_name: str, organization: Optional[str] = None) -> str:
        """
        Fork a repository to the authenticated user's account or an organization.
        
        Args:
            repo_name: Full name of the repository to fork (e.g., 'owner/repo')
            organization: Optional organization name to fork to. If None, forks to user account.
        
        Returns:
            JSON string with fork information or error message.
        """
        logger.info(f"Forking repository: {repo_name} (org: {organization})")
        try:
            repo = self.g.get_repo(repo_name)
            
            if organization:
                org = self.g.get_organization(organization)
                forked_repo = org.create_fork(repo)
            else:
                user = self.g.get_user()
                forked_repo = user.create_fork(repo)
            
            fork_info = {
                "name": forked_repo.full_name,
                "url": forked_repo.html_url,
                "fork": forked_repo.fork,
                "parent": {
                    "name": repo.full_name,
                    "url": repo.html_url
                },
                "message": f"Successfully forked {repo_name} to {forked_repo.full_name}"
            }
            return json.dumps(fork_info, indent=2)
        except Exception as e:
            error_msg = f"Failed to fork repository: {str(e)}"
            logger.error(error_msg)
            return json.dumps({"error": error_msg}, indent=2)
