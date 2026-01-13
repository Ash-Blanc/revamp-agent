"""
Base agent class with common functionality.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import langwatch
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from .exceptions import ConfigurationError

# Load environment variables
load_dotenv(os.path.join(os.getcwd(), ".env"))
load_dotenv()

class BaseRevampAgent(ABC):
    """
    Base class for all revamp agents with common functionality.
    """
    
    def __init__(
        self,
        model_id: str = "gpt-4o",
        temperature: float = 0.7,
        tools: Optional[List] = None,
        prompt_name: Optional[str] = None
    ):
        """
        Initialize base agent.
        
        Args:
            model_id: Model identifier
            temperature: Model temperature
            tools: List of tools to use
            prompt_name: Name of the prompt to load from LangWatch
        """
        self.model_id = model_id
        self.temperature = temperature
        self.tools = tools or []
        self.prompt_name = prompt_name
        
        # Initialize LangWatch
        self._setup_langwatch()
        
        # Load prompt if specified
        self.prompt = self._load_prompt() if prompt_name else None
        
        # Create agent
        self.agent = self._create_agent()
    
    def _setup_langwatch(self):
        """Setup LangWatch with API key."""
        api_key = os.getenv("LANGWATCH_API_KEY")
        if not api_key:
            raise ConfigurationError("LANGWATCH_API_KEY not found in environment")
        
        langwatch.setup(api_key=api_key)
    
    def _load_prompt(self) -> Optional[Any]:
        """Load prompt from LangWatch."""
        try:
            return langwatch.prompts.get(self.prompt_name)
        except Exception as e:
            print(f"Warning: Could not load prompt '{self.prompt_name}': {e}")
            return None
    
    def _create_agent(self) -> Agent:
        """Create the Agno agent."""
        instructions = self.prompt.prompt if self.prompt else self.get_default_instructions()
        
        return Agent(
            model=OpenAIChat(id=self.model_id),
            instructions=instructions,
            tools=self.tools,
            markdown=True,
        )
    
    @abstractmethod
    def get_default_instructions(self) -> str:
        """Get default instructions if no prompt is loaded."""
        pass
    
    def run(self, query: str) -> str:
        """Run the agent with a query."""
        response = self.agent.run(query)
        return response.content
    
    def add_tool(self, tool):
        """Add a tool to the agent."""
        self.tools.append(tool)
        # Recreate agent with new tools
        self.agent = self._create_agent()
    
    def update_instructions(self, instructions: str):
        """Update agent instructions."""
        self.agent.instructions = instructions