"""
Memory Storage Implementation for the Revamp Agent.

This module provides persistent memory capabilities using Agno's built-in memory management.
"""

from typing import Optional, Dict, Any
from agno.memory.manager import MemoryManager, UserMemory
from agno.agent import AgentSession


class PersistentMemoryManager:
    """
    Manages persistent memory for the revamp agent using Agno's built-in capabilities.
    """
    
    def __init__(self):
        """Initialize the memory manager with Agno's MemoryManager."""
        self.memory_manager = MemoryManager()
    
    def store_user_memory(self, user_id: str, key: str, value: Any) -> bool:
        """
        Store memory associated with a user.
        
        Args:
            user_id: Unique identifier for the user
            key: Memory key
            value: Value to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user_memory = UserMemory(user_id=user_id)
            user_memory.set(key, value)
            self.memory_manager.save(user_memory)
            return True
        except Exception:
            return False
    
    def retrieve_user_memory(self, user_id: str, key: str) -> Optional[Any]:
        """
        Retrieve memory associated with a user.
        
        Args:
            user_id: Unique identifier for the user
            key: Memory key to retrieve
            
        Returns:
            Stored value or None if not found
        """
        try:
            user_memory = UserMemory(user_id=user_id)
            return user_memory.get(key)
        except Exception:
            return None
    
    def create_agent_session(self, session_id: Optional[str] = None) -> AgentSession:
        """
        Create a new agent session for tracking interactions.
        
        Args:
            session_id: Optional session ID (auto-generated if not provided)
            
        Returns:
            AgentSession instance
        """
        if session_id:
            return AgentSession(session_id=session_id)
        else:
            return AgentSession()
    
    def get_memory_summary(self, user_id: str) -> Dict[str, Any]:
        """
        Get a summary of user memory.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Dictionary with memory summary
        """
        try:
            user_memory = UserMemory(user_id=user_id)
            return user_memory.to_dict()
        except Exception:
            return {}


# Global memory manager instance
memory_manager = PersistentMemoryManager()


def get_memory_manager() -> PersistentMemoryManager:
    """
    Get the global memory manager instance.
    
    Returns:
        PersistentMemoryManager instance
    """
    return memory_manager