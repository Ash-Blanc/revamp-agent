"""
Custom Agno tools for the Hackathon Project Revamp Agent.

These tools help discover relevant hackathons and GitHub projects when URLs are not provided.
"""

from agno.tools import tool
from agno.tools.duckduckgo import DuckDuckGoTools
from typing import List, Dict, Optional
import re
import json
from .base_tool import BaseTool


class HackathonDiscoveryTools(BaseTool):
    """
    Tools for discovering ongoing hackathons and relevant GitHub projects.
    """
    
    def __init__(self):
        super().__init__(name="hackathon_discovery")
        self.ddg = DuckDuckGoTools()
    
    def get_tool_info(self) -> Dict[str, any]:
        """Get information about this tool."""
        return {
            "name": "HackathonDiscoveryTools",
            "description": "Discovers ongoing hackathons and relevant GitHub projects",
            "capabilities": [
                "find_ongoing_hackathons",
                "find_relevant_github_projects", 
                "find_hackathons_for_project",
                "find_projects_for_hackathon"
            ],
            "cache_enabled": self._cache_enabled
        }
    
    @tool
    def find_ongoing_hackathons(
        self,
        query: str = "ongoing hackathons 2024 2025",
        max_results: int = 5
    ) -> List[Dict[str, str]]:
        """
        Search for ongoing and upcoming hackathons on the web.
        
        Args:
            query: Search query for hackathons (default: "ongoing hackathons 2024 2025")
            max_results: Maximum number of hackathons to return (default: 5)
        
        Returns:
            List of dictionaries with hackathon information including:
            - name: Hackathon name
            - url: Hackathon website URL
            - description: Brief description
            - deadline: Deadline or date information if available
        """
        return self._cached_call(
            "find_ongoing_hackathons",
            self._find_hackathons_impl,
            query,
            max_results
        )
    
    def _find_hackathons_impl(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """Implementation of hackathon finding logic."""
        search_query = f"{query} site:devpost.com OR site:hackathon.com OR site:mlh.io"
        
        # Use DuckDuckGo to search
        results_json = self._safe_execute(
            self.ddg.duckduckgo_search,
            query=search_query,
            max_results=max_results * 2
        )
        
        if not results_json:
            return []
        
        results = json.loads(results_json) if isinstance(results_json, str) else results_json
        hackathons = []
        seen_urls = set()
        
        # Extract hackathon information from search results
        if results and isinstance(results, list):
            for result in results[:max_results * 2]:
                if isinstance(result, dict):
                    hackathon = self._extract_hackathon_info(result)
                    if hackathon and hackathon["url"] not in seen_urls:
                        hackathons.append(hackathon)
                        seen_urls.add(hackathon["url"])
                        
                        if len(hackathons) >= max_results:
                            break
        
        # If we didn't find enough, try a broader search
        if len(hackathons) < max_results:
            hackathons.extend(self._broader_hackathon_search(max_results - len(hackathons), seen_urls))
        
        return hackathons[:max_results]
    
    def _extract_hackathon_info(self, result: Dict) -> Optional[Dict[str, str]]:
        """Extract hackathon information from search result."""
        title = result.get("title", "")
        url = result.get("href", result.get("url", ""))
        body = result.get("body", result.get("snippet", ""))
        
        # Filter for hackathon-related results
        if url and self._is_hackathon_url(url):
            # Try to extract deadline/date from body
            deadline_match = re.search(
                r'(\w+\s+\d{1,2},?\s+\d{4})|(deadline|ends|closes).*?(\w+\s+\d{1,2})', 
                body, 
                re.IGNORECASE
            )
            deadline = deadline_match.group(0) if deadline_match else None
            
            return {
                "name": title,
                "url": url,
                "description": body[:200] if body else "",
                "deadline": deadline
            }
        
        return None
    
    def _is_hackathon_url(self, url: str) -> bool:
        """Check if URL looks like a hackathon URL."""
        hackathon_domains = ["devpost", "hackathon", "mlh.io", "hack"]
        return any(domain in url.lower() for domain in hackathon_domains)
    
    def _broader_hackathon_search(self, needed: int, seen_urls: set) -> List[Dict[str, str]]:
        """Perform broader hackathon search."""
        broader_query = "hackathons open registration 2024 2025"
        broader_results_json = self._safe_execute(
            self.ddg.duckduckgo_search,
            query=broader_query,
            max_results=needed
        )
        
        if not broader_results_json:
            return []
        
        broader_results = json.loads(broader_results_json) if isinstance(broader_results_json, str) else broader_results_json
        additional_hackathons = []
        
        if broader_results and isinstance(broader_results, list):
            for result in broader_results:
                if isinstance(result, dict):
                    url = result.get("href", result.get("url", ""))
                    if url and url not in seen_urls and self._is_hackathon_url(url):
                        additional_hackathons.append({
                            "name": result.get("title", "Hackathon"),
                            "url": url,
                            "description": result.get("body", result.get("snippet", ""))[:200],
                            "deadline": None
                        })
                        seen_urls.add(url)
                        
                        if len(additional_hackathons) >= needed:
                            break
        
        return additional_hackathons
    
    @tool
    def find_relevant_github_projects(
        self,
        topic: str,
        language: Optional[str] = None,
        max_results: int = 5
    ) -> List[Dict[str, str]]:
        """
        Search for relevant GitHub projects based on a topic.
        
        Args:
            topic: Topic or technology area to search for (e.g., "AI", "web3", "climate")
            language: Programming language filter (optional, e.g., "python", "javascript")
            max_results: Maximum number of projects to return (default: 5)
        
        Returns:
            List of dictionaries with project information including:
            - name: Project name
            - url: GitHub repository URL
            - description: Project description
            - stars: Number of stars (if available)
        """
        return self._cached_call(
            "find_relevant_github_projects",
            self._find_projects_impl,
            topic,
            language,
            max_results
        )
    
    def _find_projects_impl(self, topic: str, language: Optional[str], max_results: int) -> List[Dict[str, str]]:
        """Implementation of project finding logic."""
        # Build search query
        if language:
            search_query = f"{topic} {language} site:github.com"
        else:
            search_query = f"{topic} site:github.com"
        
        # Use DuckDuckGo to search
        results_json = self._safe_execute(
            self.ddg.duckduckgo_search,
            query=search_query,
            max_results=max_results * 2
        )
        
        if not results_json:
            return []
        
        results = json.loads(results_json) if isinstance(results_json, str) else results_json
        projects = []
        seen_urls = set()
        
        # Extract GitHub project information
        if results and isinstance(results, list):
            for result in results[:max_results * 2]:
                if isinstance(result, dict):
                    project = self._extract_project_info(result)
                    if project and project["url"] not in seen_urls:
                        projects.append(project)
                        seen_urls.add(project["url"])
                        
                        if len(projects) >= max_results:
                            break
        
        return projects[:max_results]
    
    def _extract_project_info(self, result: Dict) -> Optional[Dict[str, str]]:
        """Extract project information from search result."""
        url = result.get("href", result.get("url", ""))
        
        # Filter for GitHub URLs
        if url and "github.com" in url:
            # Extract repo name from URL
            repo_match = re.search(r'github\.com/([^/]+/[^/]+)', url)
            if repo_match:
                repo_name = repo_match.group(1)
                
                return {
                    "name": result.get("title", repo_name),
                    "url": url,
                    "description": result.get("body", result.get("snippet", ""))[:200],
                    "stars": None  # Would need GitHub API for accurate stars
                }
        
        return None
    
    @tool
    def find_hackathons_for_project(
        self,
        project_topic: str,
        project_tech_stack: Optional[str] = None,
        max_results: int = 5
    ) -> List[Dict[str, str]]:
        """
        Find hackathons that would be a good fit for a project with given topic/tech stack.
        
        Args:
            project_topic: Main topic or theme of the project (e.g., "AI", "blockchain", "healthcare")
            project_tech_stack: Technologies used (optional, e.g., "Python, React")
            max_results: Maximum number of hackathons to return (default: 5)
        
        Returns:
            List of dictionaries with hackathon information
        """
        # Build search query based on project characteristics
        if project_tech_stack:
            query = f"{project_topic} {project_tech_stack} hackathon 2024 2025"
        else:
            query = f"{project_topic} hackathon 2024 2025"
        
        return self.find_ongoing_hackathons(query=query, max_results=max_results)
    
    @tool
    def find_projects_for_hackathon(
        self,
        hackathon_theme: str,
        hackathon_requirements: Optional[str] = None,
        max_results: int = 5
    ) -> List[Dict[str, str]]:
        """
        Find GitHub projects that would be a good fit for a hackathon with given theme.
        
        Args:
            hackathon_theme: Main theme of the hackathon (e.g., "AI", "sustainability", "web3")
            hackathon_requirements: Specific requirements or tech stack (optional)
            max_results: Maximum number of projects to return (default: 5)
        
        Returns:
            List of dictionaries with project information
        """
        # Build search query based on hackathon theme
        if hackathon_requirements:
            query = f"{hackathon_theme} {hackathon_requirements}"
        else:
            query = hackathon_theme
        
        return self.find_relevant_github_projects(topic=query, max_results=max_results)