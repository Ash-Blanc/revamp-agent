"""
Scenario tests for the Hackathon Project Revamp Agent.

These tests validate end-to-end agent behavior using Scenario.
Follow the Agent Testing Pyramid: use Scenario for end-to-end agentic tests.
Always access Scenario docs through the LangWatch MCP.
"""

import os
import pytest
from dotenv import load_dotenv

# Load environment variables for tests
load_dotenv()

def test_basic_revamp_functionality():
    """Test basic revamp functionality without external dependencies."""
    from app.main import revamp_project
    
    # Test with minimal input
    result = revamp_project(
        hackathon_context="AI hackathon focusing on healthcare solutions",
        search_topic="healthcare AI"
    )
    
    # Basic validation
    assert result is not None
    assert len(result) > 100  # Should be a substantial response
    assert "strategy" in result.lower() or "revamp" in result.lower()

def test_discovery_tools():
    """Test the discovery tools functionality."""
    from app.tools import HackathonDiscoveryTools
    
    tools = HackathonDiscoveryTools()
    
    # Test hackathon discovery
    hackathons = tools.find_ongoing_hackathons("AI hackathon", max_results=2)
    assert isinstance(hackathons, list)
    
    # Test project discovery
    projects = tools.find_relevant_github_projects("AI", max_results=2)
    assert isinstance(projects, list)

def test_cli_commands():
    """Test CLI command structure."""
    import subprocess
    
    # Test help command
    result = subprocess.run(["uv", "run", "revamp", "--help"], 
                          capture_output=True, text=True)
    assert result.returncode == 0
    assert "revamp" in result.stdout.lower()

@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OpenAI API key required")
def test_full_revamp_with_api():
    """Test full revamp functionality with API keys."""
    from app.main import revamp_project
    
    result = revamp_project(
        github_url="https://github.com/microsoft/vscode",
        hackathon_context="Developer tools hackathon"
    )
    
    assert result is not None
    assert len(result) > 200
    # Should contain strategic elements
    assert any(word in result.lower() for word in ["strategy", "feature", "improvement", "hackathon"])

def test_session_management():
    """Test session management functionality."""
    from app.session_manager import get_session_manager, SessionStatus
    
    manager = get_session_manager()
    
    # Create session
    session_id = manager.create_session(user_id="test_user")
    assert session_id is not None
    
    # Add message
    success = manager.add_message_to_session(session_id, "user", "Test message")
    assert success
    
    # Get history
    history = manager.get_session_history(session_id)
    assert len(history) == 1
    assert history[0]["content"] == "Test message"
    
    # End session
    success = manager.end_session(session_id)
    assert success

def test_memory_storage():
    """Test memory storage functionality."""
    from app.memory_storage import get_memory_manager
    
    manager = get_memory_manager()
    
    # Store and retrieve memory
    success = manager.store_user_memory("test_user", "test_key", "test_value")
    assert success
    
    value = manager.retrieve_user_memory("test_user", "test_key")
    assert value == "test_value"

# TODO: Add Scenario tests when langwatch-scenario is properly configured
# Refer to LangWatch MCP for correct Scenario API usage

"""
Example of what Scenario tests should look like (when properly configured):

@scenario
def test_end_to_end_revamp_scenario():
    # Test complete user journey
    # 1. User provides GitHub URL and hackathon URL
    # 2. Agent analyzes both
    # 3. Agent provides comprehensive strategy
    # 4. Strategy includes novel features and implementation plan
    pass

@scenario  
def test_discovery_mode_scenario():
    # Test discovery functionality
    # 1. User provides only a topic
    # 2. Agent discovers relevant projects and hackathons
    # 3. Agent selects best matches
    # 4. Agent provides strategy for the match
    pass
"""
