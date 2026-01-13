"""
Base team class for agent orchestration.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from agno.team import Team
from ..core.base_agent import BaseRevampAgent

class BaseTeam(ABC):
    """
    Base class for agent teams with common orchestration functionality.
    """
    
    def __init__(self, agents: List[BaseRevampAgent], instructions: str):
        """
        Initialize the team.
        
        Args:
            agents: List of agents in the team
            instructions: Team-level instructions
        """
        self.agents = agents
        self.instructions = instructions
        
        # Convert BaseRevampAgent instances to Agno Agent instances for Team
        agno_agents = [agent.agent for agent in agents]
        
        self.team = Team(
            members=agno_agents,
            instructions=instructions
        )
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the team's main task.
        
        Returns:
            Dictionary with execution results
        """
        pass
    
    def add_agent(self, agent: BaseRevampAgent):
        """Add an agent to the team."""
        self.agents.append(agent)
        # Recreate team with new agent
        agno_agents = [agent.agent for agent in self.agents]
        self.team = Team(
            members=agno_agents,
            instructions=self.instructions
        )
    
    def get_agent_by_type(self, agent_type: type) -> Optional[BaseRevampAgent]:
        """Get an agent by its type."""
        for agent in self.agents:
            if isinstance(agent, agent_type):
                return agent
        return None