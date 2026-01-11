"""
Custom Agno tools for the Hackathon Project Revamp Agent.

These tools help discover relevant hackathons and GitHub projects when URLs are not provided.
"""

from agno.tools import Toolkit, tool
from agno.tools.duckduckgo import DuckDuckGoTools
from typing import List, Dict, Optional
import re
import json


class HackathonDiscoveryTools(Toolkit):
    """
    Tools for discovering ongoing hackathons and relevant GitHub projects.
    """
    
    def __init__(self):
        super().__init__(name="hackathon_discovery")
        self.ddg = DuckDuckGoTools()
    
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
        search_query = f"{query} site:devpost.com OR site:hackathon.com OR site:mlh.io"
        
        # Use DuckDuckGo to search
        results_json = self.ddg.duckduckgo_search(query=search_query, max_results=max_results * 2)
        results = json.loads(results_json) if isinstance(results_json, str) else results_json
        
        hackathons = []
        seen_urls = set()
        
        # Extract hackathon information from search results
        if results and isinstance(results, list):
            for result in results[:max_results * 2]:
                if isinstance(result, dict):
                    title = result.get("title", "")
                    url = result.get("href", result.get("url", ""))
                    body = result.get("body", result.get("snippet", ""))
                    
                    # Filter for hackathon-related results
                    if url and url not in seen_urls:
                        # Check if it looks like a hackathon URL
                        if any(domain in url.lower() for domain in ["devpost", "hackathon", "mlh.io", "hack"]):
                            # Try to extract deadline/date from body
                            deadline_match = re.search(r'(\w+\s+\d{1,2},?\s+\d{4})|(deadline|ends|closes).*?(\w+\s+\d{1,2})', body, re.IGNORECASE)
                            deadline = deadline_match.group(0) if deadline_match else None
                            
                            hackathons.append({
                                "name": title,
                                "url": url,
                                "description": body[:200] if body else "",
                                "deadline": deadline
                            })
                            seen_urls.add(url)
                            
                            if len(hackathons) >= max_results:
                                break
        
        # If we didn't find enough, try a broader search
        if len(hackathons) < max_results:
            broader_query = f"hackathons open registration 2024 2025"
            broader_results_json = self.ddg.duckduckgo_search(query=broader_query, max_results=max_results)
            broader_results = json.loads(broader_results_json) if isinstance(broader_results_json, str) else broader_results_json
            
            if broader_results and isinstance(broader_results, list):
                for result in broader_results:
                    if isinstance(result, dict):
                        url = result.get("href", result.get("url", ""))
                        if url and url not in seen_urls:
                            if any(domain in url.lower() for domain in ["devpost", "hackathon", "mlh.io", "hack"]):
                                hackathons.append({
                                    "name": result.get("title", "Hackathon"),
                                    "url": url,
                                    "description": result.get("body", result.get("snippet", ""))[:200],
                                    "deadline": None
                                })
                                seen_urls.add(url)
                                
                                if len(hackathons) >= max_results:
                                    break
        
        return hackathons[:max_results]
    
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
        # Build search query
        if language:
            search_query = f"{topic} {language} site:github.com"
        else:
            search_query = f"{topic} site:github.com"
        
        # Use DuckDuckGo to search
        results_json = self.ddg.duckduckgo_search(query=search_query, max_results=max_results * 2)
        results = json.loads(results_json) if isinstance(results_json, str) else results_json
        
        projects = []
        seen_urls = set()
        
        # Extract GitHub project information
        if results and isinstance(results, list):
            for result in results[:max_results * 2]:
                if isinstance(result, dict):
                    url = result.get("href", result.get("url", ""))
                    
                    # Filter for GitHub URLs
                    if url and "github.com" in url and url not in seen_urls:
                        # Extract repo name from URL
                        repo_match = re.search(r'github\.com/([^/]+/[^/]+)', url)
                        if repo_match:
                            repo_name = repo_match.group(1)
                            
                            projects.append({
                                "name": result.get("title", repo_name),
                                "url": url,
                                "description": result.get("body", result.get("snippet", ""))[:200],
                                "stars": None  # Would need GitHub API for accurate stars
                            })
                            seen_urls.add(url)
                            
                            if len(projects) >= max_results:
                                break
        
        return projects[:max_results]
    
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