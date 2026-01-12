"""
Discovery tools for Hackathons and GitHub projects.
"""
from typing import List, Dict, Optional, Any
import json
import re
from agno.tools import Toolkit, tool
from agno.tools.duckduckgo import DuckDuckGoTools
from app.utils.logger import logger

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
    ) -> List[Dict[str, Any]]:
        """
        Search for ongoing and upcoming hackathons on the web.
        """
        search_query = f"{query} site:devpost.com OR site:hackathon.com OR site:mlh.io"
        logger.info(f"Searching for hackathons with query: {search_query}")
        
        try:
            results_json = self.ddg.duckduckgo_search(query=search_query, max_results=max_results * 2)
            results = json.loads(results_json) if isinstance(results_json, str) else results_json
        except Exception as e:
            logger.error(f"Error searching hackathons: {e}")
            return []
        
        hackathons = []
        seen_urls = set()
        
        if results and isinstance(results, list):
            for result in results[:max_results * 2]:
                if isinstance(result, dict):
                    title = result.get("title", "")
                    url = result.get("href", result.get("url", ""))
                    body = result.get("body", result.get("snippet", ""))
                    
                    if url and url not in seen_urls:
                        if any(domain in url.lower() for domain in ["devpost", "hackathon", "mlh.io", "hack"]):
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
        
        # Fallback broader search
        if len(hackathons) < max_results:
            logger.info("Insufficient results, trying broader search.")
            broader_query = f"hackathons open registration 2024 2025"
            try:
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
            except Exception as e:
                logger.error(f"Error in broader search: {e}")

        return hackathons[:max_results]
    
    @tool
    def find_relevant_github_projects(
        self,
        topic: str,
        language: Optional[str] = None,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant GitHub projects based on a topic.
        """
        if language:
            search_query = f"{topic} {language} site:github.com"
        else:
            search_query = f"{topic} site:github.com"
            
        logger.info(f"Searching GitHub projects with query: {search_query}")
        
        try:
            results_json = self.ddg.duckduckgo_search(query=search_query, max_results=max_results * 2)
            results = json.loads(results_json) if isinstance(results_json, str) else results_json
        except Exception as e:
            logger.error(f"Error searching projects: {e}")
            return []
        
        projects = []
        seen_urls = set()
        
        if results and isinstance(results, list):
            for result in results[:max_results * 2]:
                if isinstance(result, dict):
                    url = result.get("href", result.get("url", ""))
                    
                    if url and "github.com" in url and url not in seen_urls:
                        repo_match = re.search(r'github\.com/([^/]+/[^/]+)', url)
                        if repo_match:
                            repo_name = repo_match.group(1)
                            projects.append({
                                "name": result.get("title", repo_name),
                                "url": url,
                                "description": result.get("body", result.get("snippet", ""))[:200],
                                "stars": None
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
    ) -> List[Dict[str, Any]]:
        """Find hackathons fitting a project."""
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
    ) -> List[Dict[str, Any]]:
        """Find projects fitting a hackathon."""
        if hackathon_requirements:
            query = f"{hackathon_theme} {hackathon_requirements}"
        else:
            query = hackathon_theme
        return self.find_relevant_github_projects(topic=query, max_results=max_results)
