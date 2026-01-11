"""
Extended GitHub tools with fork functionality.
"""

from agno.tools.github import GithubTools
from agno.tools import tool
import json


class ExtendedGithubTools(GithubTools):
    """Extended GitHub tools with additional functionality like forking."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add fork tool to the tools list
        if hasattr(self, '_tools'):
            self._tools.append(self.fork_repository)
        else:
            # If tools are stored differently, we'll need to check
            pass
    
    @tool
    def fork_repository(self, repo_name: str, organization: str = None) -> str:
        """
        Fork a repository to the authenticated user's account or an organization.
        
        Args:
            repo_name: Full name of the repository to fork (e.g., 'owner/repo')
            organization: Optional organization name to fork to. If None, forks to user account.
        
        Returns:
            JSON string with fork information or error message.
        """
        try:
            repo = self.g.get_repo(repo_name)
            
            # Fork the repository
            if organization:
                org = self.g.get_organization(organization)
                forked_repo = org.create_fork(repo)
            else:
                # Fork to user account
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
            return json.dumps({"error": f"Failed to fork repository: {str(e)}"}, indent=2)