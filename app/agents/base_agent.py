"""
Base agent class for all Revamp Agent implementations.

This provides common functionality and interfaces for all agents in the system.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import langwatch
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Load environment variables
load_dotenv()

# Initialize LangWatch
langwatch.setup(
    api_key=os.getenv("LANGWATCH_API_KEY"),
)


class BaseRevampAgent(Agent, ABC):
    """
    Base class for all Revamp Agent implementations.
    
    Provides common functionality like:
    - Environment setup
    - LangWatch integration
    - Common tools initialization
    - Standardized configuration
    """
    
    def __init__(
        self,
        agent_name: str,
        model_id: str = "gpt-4o",
        instructions: Optional[str] = None,
        prompt_name: Optional[str] = None,
        tools: Optional[List] = None,
        **kwargs
    ):
        """
        Initialize the base agent.
        
        Args:
            agent_name: Name of the agent for identification
            model_id: Model ID to use (default: gpt-4o)
            instructions: Direct instructions string
            prompt_name: Name of LangWatch prompt to use
            tools: List of tools to provide to the agent
            **kwargs: Additional arguments passed to Agent
        """
        self.agent_name = agent_name
        
        # Get instructions from prompt or use provided
        final_instructions = instructions
        if prompt_name:
            try:
                prompt = langwatch.prompts.get(prompt_name)
                final_instructions = prompt.prompt if prompt else instructions
            except Exception:
                # Fallback to provided instructions if prompt fetch fails
                pass
        
        # Initialize with default model if not specified
        model = kwargs.pop('model', OpenAIChat(id=model_id))
        
        super().__init__(
            model=model,
            instructions=final_instructions or self.get_default_instructions(),
            tools=tools or [],
            markdown=True,
            **kwargs
        )
    
    @abstractmethod
    def get_default_instructions(self) -> str:
        """
        Get default instructions for this agent type.
        
        Returns:
            Default instruction string
        """
        pass
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about this agent.
        
        Returns:
            Dictionary with agent metadata
        """
        return {
            "name": self.agent_name,
            "type": self.__class__.__name__,
            "model": str(self.model),
            "tools": [tool.__class__.__name__ for tool in self.tools] if self.tools else [],
        }
    
    def run_with_context(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Run the agent with additional context.
        
        Args:
            query: The main query/task
            context: Additional context dictionary
            
        Returns:
            Agent response content
        """
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            full_query = f"Context:\n{context_str}\n\nTask:\n{query}"
        else:
            full_query = query
        
        response = self.run(full_query)
        return response.content