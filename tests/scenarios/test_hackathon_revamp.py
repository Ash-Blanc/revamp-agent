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

# Import scenario when available
try:
    from scenario import Scenario, on
    SCENARIO_AVAILABLE = True
except ImportError:
    SCENARIO_AVAILABLE = False
    pytestmark = pytest.mark.skip(reason="scenario package not installed. Install it to run scenario tests.")


if SCENARIO_AVAILABLE:
    from app.main import revamp_project

    @Scenario
    def test_basic_hackathon_revamp():
        """
        Test that the agent can analyze a GitHub project and provide
        a comprehensive revamp strategy for a hackathon.
        
        This test validates:
        - Project analysis capabilities
        - Hackathon strategy development
        - Novel feature proposals
        - Actionable recommendations
        """
        github_url = "https://github.com/octocat/Hello-World"
        hackathon_context = "AI/ML hackathon focusing on innovation and social impact"
        
        result = revamp_project(github_url=github_url, hackathon_context=hackathon_context)
        
        # Judge criteria: The response should be comprehensive and strategic
        # Using judge instead of regex/word matching as per best practices
        on(result).should(
            "contain a project analysis section",
            "contain hackathon strategy recommendations", 
            "propose novel features or improvements",
            "provide actionable revamp steps",
            "demonstrate understanding of hackathon context",
            "be comprehensive and well-structured"
        )
        
        # Deterministic checks for things we can verify programmatically
        assert len(result) > 500, "Response should be comprehensive (at least 500 characters)"
        
        # Check that key concepts are present (deterministic)
        result_lower = result.lower()
        has_project_ref = "project" in result_lower or "repository" in result_lower or "github" in result_lower
        has_strategy_ref = "hackathon" in result_lower or "strategy" in result_lower or "revamp" in result_lower
        
        assert has_project_ref, "Should reference the project being analyzed"
        assert has_strategy_ref, "Should provide hackathon strategy or revamp recommendations"

    @Scenario
    def test_hackathon_website_analysis():
        """
        Test that the agent can scrape and analyze hackathon websites
        to extract themes, criteria, and requirements.
        
        This test validates:
        - Web scraping capabilities via Firecrawl
        - Hackathon website analysis
        - Extraction of themes, criteria, and requirements
        - Strategic recommendations based on scraped data
        """
        hackathon_url = "https://example-hackathon.com"
        
        result = revamp_project(hackathon_url=hackathon_url)
        
        # Judge criteria: The response should demonstrate understanding of hackathon details
        on(result).should(
            "demonstrate understanding of hackathon themes or criteria",
            "contain strategic recommendations based on hackathon information",
            "reference information from the hackathon website",
            "provide actionable revamp suggestions",
            "be comprehensive and well-structured"
        )
        
        # Deterministic checks
        assert len(result) > 500, "Response should be comprehensive (at least 500 characters)"
        
        result_lower = result.lower()
        has_hackathon_ref = "hackathon" in result_lower or "theme" in result_lower or "criteria" in result_lower
        assert has_hackathon_ref, "Should reference hackathon information"

    @Scenario
    def test_combined_github_and_hackathon_analysis():
        """
        Test that the agent can analyze both a GitHub project and hackathon website
        to create a comprehensive revamp strategy.
        
        This test validates:
        - Combined project and hackathon analysis
        - Strategic alignment between project and hackathon goals
        - Comprehensive revamp planning
        """
        github_url = "https://github.com/octocat/Hello-World"
        hackathon_url = "https://example-hackathon.com"
        
        result = revamp_project(
            github_url=github_url,
            hackathon_url=hackathon_url
        )
        
        # Judge criteria: The response should integrate both analyses
        on(result).should(
            "contain project analysis",
            "contain hackathon analysis or references to hackathon information",
            "demonstrate strategic alignment between project and hackathon goals",
            "propose features that align with hackathon themes",
            "provide comprehensive revamp recommendations",
            "be well-structured and actionable"
        )
        
        # Deterministic checks
        assert len(result) > 500, "Response should be comprehensive (at least 500 characters)"
        
        result_lower = result.lower()
        has_project = "project" in result_lower or "repository" in result_lower or "github" in result_lower
        has_hackathon = "hackathon" in result_lower or "theme" in result_lower
        
        assert has_project, "Should reference the project"
        assert has_hackathon, "Should reference hackathon information"

    @Scenario
    def test_auto_discover_hackathons():
        """
        Test that the agent can automatically discover hackathons when hackathon_url is not provided.
        
        This test validates:
        - Discovery tool usage
        - Finding ongoing hackathons
        - Presenting discovered options
        """
        github_url = "https://github.com/octocat/Hello-World"
        
        result = revamp_project(github_url=github_url, search_topic="AI")
        
        # Judge criteria: The response should demonstrate discovery and selection
        on(result).should(
            "demonstrate understanding of hackathon themes or criteria",
            "contain strategic recommendations",
            "reference discovered hackathons or provide hackathon analysis",
            "be comprehensive and actionable"
        )
        
        # Deterministic checks
        assert len(result) > 500, "Response should be comprehensive"
        result_lower = result.lower()
        has_hackathon_ref = "hackathon" in result_lower or "theme" in result_lower
        assert has_hackathon_ref, "Should reference hackathon information"

    @Scenario
    def test_auto_discover_projects_and_hackathons():
        """
        Test that the agent can automatically discover both projects and hackathons when neither URL is provided.
        
        This test validates:
        - Discovery of both projects and hackathons
        - Following search_order parameter
        - Matching projects with hackathons
        """
        result = revamp_project(
            search_order="projects_first",
            search_topic="web3"
        )
        
        # Judge criteria: The response should demonstrate discovery of both
        on(result).should(
            "demonstrate discovery of GitHub projects",
            "demonstrate discovery of hackathons",
            "show strategic matching between projects and hackathons",
            "provide comprehensive revamp recommendations",
            "be well-structured and actionable"
        )
        
        # Deterministic checks
        assert len(result) > 500, "Response should be comprehensive"
        result_lower = result.lower()
        has_project = "project" in result_lower or "repository" in result_lower or "github" in result_lower
        has_hackathon = "hackathon" in result_lower or "theme" in result_lower
        
        assert has_project, "Should reference discovered projects"
        assert has_hackathon, "Should reference discovered hackathons"

    @Scenario
    def test_coding_agent_integration():
        """
        Test that the coding agent can be used to implement revamp strategies.
        
        This test validates:
        - Coding agent can be imported and initialized
        - Implementation functions are available
        - Integration with revamp workflow
        """
        from app.coding_agent import coding_agent, implement_revamp_strategy
        
        # Test that coding agent is available
        assert coding_agent is not None, "Coding agent should be initialized"
        
        # Test that implementation function exists
        assert callable(implement_revamp_strategy), "implement_revamp_strategy should be callable"
        
        # Note: Actual implementation test would require GitHub access token
        # and would make real changes to repositories, so we skip that in automated tests