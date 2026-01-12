"""
Session Management System for the Revamp Agent.

This module provides session management capabilities using Agno's AgentSession.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from agno.agent import AgentSession, Message
from .memory_storage import get_memory_manager


class SessionStatus(Enum):
    """Enumeration of possible session statuses."""
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class SessionManager:
    """
    Manages agent sessions using Agno's AgentSession for tracking conversations
    and maintaining context across multiple interactions.
    """
    
    def __init__(self):
        """Initialize the session manager."""
        self.memory_manager = get_memory_manager()
        self.active_sessions = {}
    
    def create_session(self, session_id: Optional[str] = None, user_id: Optional[str] = None) -> str:
        """
        Create a new session.
        
        Args:
            session_id: Optional session ID (auto-generated if not provided)
            user_id: Optional user identifier
            
        Returns:
            Session ID
        """
        agent_session = self.memory_manager.create_agent_session(session_id)
        session_id = agent_session.session_id
        
        # Store session metadata
        session_data = {
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": SessionStatus.ACTIVE,
            "user_id": user_id,
            "history": [],
            "agent_session": agent_session
        }
        
        self.active_sessions[session_id] = session_data
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session data.
        
        Args:
            session_id: Session ID to retrieve
            
        Returns:
            Session data dictionary or None if not found
        """
        return self.active_sessions.get(session_id)
    
    def add_message_to_session(self, session_id: str, role: str, content: str) -> bool:
        """
        Add a message to the session history.
        
        Args:
            session_id: Session ID to add message to
            role: Role of the message ('user', 'assistant', 'system')
            content: Content of the message
            
        Returns:
            True if successful, False otherwise
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return False
        
        # Create message object
        message = Message(role=role, content=content)
        
        # Add to session history
        session_data["history"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        session_data["updated_at"] = datetime.now().isoformat()
        
        # Add to agent session as well
        try:
            agent_session = session_data["agent_session"]
            agent_session.add_message(message)
        except Exception:
            pass  # Continue even if agent session update fails
        
        return True
    
    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get the message history for a session.
        
        Args:
            session_id: Session ID to retrieve history for
            
        Returns:
            List of messages in the session history
        """
        session_data = self.get_session(session_id)
        if session_data:
            return session_data.get("history", [])
        return []
    
    def update_session_status(self, session_id: str, status: SessionStatus) -> bool:
        """
        Update session status.
        
        Args:
            session_id: Session ID to update
            status: New status for the session
            
        Returns:
            True if successful, False otherwise
        """
        session_data = self.get_session(session_id)
        if not session_data:
            return False
        
        session_data["status"] = status
        session_data["updated_at"] = datetime.now().isoformat()
        return True
    
    def end_session(self, session_id: str, status: SessionStatus = SessionStatus.COMPLETED) -> bool:
        """
        End a session with a specific status.
        
        Args:
            session_id: Session ID to end
            status: Status to set for the session (default: COMPLETED)
            
        Returns:
            True if successful, False otherwise
        """
        success = self.update_session_status(session_id, status)
        if success:
            # Move from active to completed (we could store in a separate completed sessions dict)
            session_data = self.active_sessions.pop(session_id, None)
            return session_data is not None
        return False
    
    def list_active_sessions(self) -> List[str]:
        """
        List all active session IDs.
        
        Returns:
            List of active session IDs
        """
        return list(self.active_sessions.keys())


# Global session manager instance
session_manager = SessionManager()


def get_session_manager() -> SessionManager:
    """
    Get the global session manager instance.
    
    Returns:
        SessionManager instance
    """
    return session_manager