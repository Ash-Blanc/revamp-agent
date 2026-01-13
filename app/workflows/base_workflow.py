"""
Base workflow class for structured agent processes.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from agno.workflow import Workflow
from ..core.base_agent import BaseRevampAgent

class BaseWorkflow(ABC):
    """
    Base class for agent workflows with common process management.
    """
    
    def __init__(self, agents: List[BaseRevampAgent]):
        """
        Initialize the workflow.
        
        Args:
            agents: List of agents to use in the workflow
        """
        self.agents = agents
        self.workflow = Workflow()
        self.execution_history = []
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the workflow.
        
        Returns:
            Dictionary with execution results
        """
        pass
    
    def log_step(self, step_name: str, result: Any, success: bool = True):
        """Log a workflow step."""
        self.execution_history.append({
            "step": step_name,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "result": result if success else None,
            "error": result if not success else None
        })
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get a summary of the workflow execution."""
        total_steps = len(self.execution_history)
        successful_steps = sum(1 for step in self.execution_history if step["success"])
        
        return {
            "total_steps": total_steps,
            "successful_steps": successful_steps,
            "success_rate": successful_steps / total_steps if total_steps > 0 else 0,
            "execution_time": self._calculate_execution_time(),
            "history": self.execution_history
        }
    
    def _calculate_execution_time(self) -> Optional[float]:
        """Calculate total execution time."""
        if len(self.execution_history) < 2:
            return None
        
        start_time = datetime.fromisoformat(self.execution_history[0]["timestamp"])
        end_time = datetime.fromisoformat(self.execution_history[-1]["timestamp"])
        
        return (end_time - start_time).total_seconds()
    
    def get_agent_by_type(self, agent_type: type) -> Optional[BaseRevampAgent]:
        """Get an agent by its type."""
        for agent in self.agents:
            if isinstance(agent, agent_type):
                return agent
        return None