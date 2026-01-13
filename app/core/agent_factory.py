"""
Factory for creating different types of agents.
"""

import os
from typing import Optional, List, Dict, Any
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.firecrawl import FirecrawlTools
from agno.tools.file import FileTools
from agno.tools.local_file_system import LocalFileSystemTools
from agno.tools.github import GithubTools

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

from .base_agent import BaseRevampAgent
from .exceptions import ConfigurationError

class AgentFactory:
    """
    Factory for creating different types of revamp agents.
    """
    
    @staticmethod
    def get_available_tools() -> Dict[str, Any]:
        """Get all available tools based on API keys."""
        tools = {
            "duckduckgo": DuckDuckGoTools(),
            "file": FileTools(),
            "local_file_system": LocalFileSystemTools(),
        }
        
        # Add optional tools based on API keys
        if os.getenv("FIRECRAWL_API_KEY"):
            tools["firecrawl"] = FirecrawlTools()
        
        if os.getenv("GITHUB_ACCESS_TOKEN"):
            tools["github"] = GithubTools()
        
        return tools
    
    @staticmethod
    def get_coding_model():
        """
        Get the best available coding model with fallback logic.
        
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
        
        # Final fallback to OpenAI
        from agno.models.openai import OpenAIChat
        return OpenAIChat(id="gpt-4o")
    
    @classmethod
    def create_strategy_agent(cls, tools: Optional[List] = None) -> BaseRevampAgent:
        """Create a strategy agent for revamp planning."""
        from ..agents.strategy_agent import StrategyAgent
        
        if tools is None:
            available_tools = cls.get_available_tools()
            tools = [
                available_tools["duckduckgo"],
                available_tools["file"],
                available_tools["local_file_system"]
            ]
            
            # Add discovery tools
            from ..tools import HackathonDiscoveryTools
            tools.append(HackathonDiscoveryTools())
            
            # Add optional tools
            if "firecrawl" in available_tools:
                tools.append(available_tools["firecrawl"])
        
        return StrategyAgent(tools=tools)
    
    @classmethod
    def create_coding_agent(cls, tools: Optional[List] = None) -> BaseRevampAgent:
        """Create a coding agent for implementation."""
        from ..agents.coding_agent import CodingAgent
        
        if tools is None:
            available_tools = cls.get_available_tools()
            tools = [
                available_tools["file"],
                available_tools["local_file_system"]
            ]
            
            # Add GitHub tools if available
            if "github" in available_tools:
                tools.append(available_tools["github"])
        
        model = cls.get_coding_model()
        return CodingAgent(model=model, tools=tools)
    
    @classmethod
    def create_project_analyzer(cls) -> BaseRevampAgent:
        """Create a project analyzer agent."""
        from ..agents.project_analyzer import ProjectAnalyzer
        
        available_tools = cls.get_available_tools()
        tools = [
            available_tools["duckduckgo"],
            available_tools["file"],
            available_tools["local_file_system"]
        ]
        
        if "github" in available_tools:
            tools.append(available_tools["github"])
        
        return ProjectAnalyzer(tools=tools)
    
    @classmethod
    def create_hackathon_researcher(cls) -> BaseRevampAgent:
        """Create a hackathon researcher agent."""
        from ..agents.hackathon_researcher import HackathonResearcher
        
        available_tools = cls.get_available_tools()
        tools = [available_tools["duckduckgo"]]
        
        if "firecrawl" in available_tools:
            tools.append(available_tools["firecrawl"])
        
        return HackathonResearcher(tools=tools)