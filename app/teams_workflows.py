"""
Agentic Teams and Workflows for the Revamp Agent.

This module implements specialized teams of agents and structured workflows
using Agno's Team and Workflow classes.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.workflow import Workflow
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.firecrawl import FirecrawlTools
from .tools import HackathonDiscoveryTools
from .memory_storage import get_memory_manager
from .session_manager import get_session_manager


class ProjectAnalyzerAgent(Agent):
    """
    Specialized agent for analyzing GitHub projects.
    """
    
    def __init__(self):
        # Get the project analysis prompt
        instructions = """You are a specialized GitHub project analyzer. Your role is to deeply analyze GitHub repositories to understand:
        
        1. Codebase structure and architecture
        2. Technology stack and dependencies
        3. Current features and functionality
        4. Strengths and weaknesses
        5. Potential improvement areas
        6. Code quality and maintainability
        
        When analyzing projects:
        - Examine the repository structure
        - Identify the main technologies used
        - Assess the project's current state
        - Highlight key components and modules
        - Identify potential areas for enhancement
        - Note any technical debt or improvement opportunities
        
        Use available tools to gather information about the repository."""
        
        super().__init__(
            model=OpenAIChat(id="gpt-4o"),
            instructions=instructions,
            tools=[DuckDuckGoTools(), FirecrawlTools()] if FirecrawlTools and __import__('os').environ.get("FIRECRAWL_API_KEY") else [DuckDuckGoTools()],
            markdown=True,
        )


class HackathonResearcherAgent(Agent):
    """
    Specialized agent for researching hackathons.
    """
    
    def __init__(self):
        instructions = """You are a specialized hackathon researcher. Your role is to analyze hackathon websites and information to understand:
        
        1. Hackathon themes and focus areas
        2. Judging criteria and evaluation metrics
        3. Prizes and awards offered
        4. Timeline and important deadlines
        5. Requirements and constraints
        6. Sponsor information and priorities
        7. Previous winning projects and patterns
        
        When researching hackathons:
        - Extract key information about themes and requirements
        - Identify what judges typically look for
        - Note any special tracks or categories
        - Gather information about sponsors and their interests
        - Research previous winners and successful patterns
        - Look for differentiation opportunities
        
        Use web scraping tools to gather comprehensive information from hackathon websites."""
        
        super().__init__(
            model=OpenAIChat(id="gpt-4o"),
            instructions=instructions,
            tools=[DuckDuckGoTools(), FirecrawlTools()] if FirecrawlTools and __import__('os').environ.get("FIRECRAWL_API_KEY") else [DuckDuckGoTools()],
            markdown=True,
        )


class StrategyDeveloperAgent(Agent):
    """
    Specialized agent for developing revamp strategies.
    """
    
    def __init__(self):
        instructions = """You are a specialized strategy developer for hackathon project revamps. Your role is to create comprehensive strategies that:
        
        1. Align project capabilities with hackathon goals
        2. Identify novel features that would impress judges
        3. Develop differentiation tactics
        4. Create implementation roadmaps
        5. Suggest presentation and demo strategies
        6. Consider feasibility and timeline constraints
        
        When developing strategies:
        - Focus on novelty and innovation
        - Consider the hackathon's specific requirements
        - Think about what would make the project memorable
        - Balance ambition with feasibility
        - Create actionable implementation steps
        - Consider presentation and demo aspects
        
        Synthesize information from project analysis and hackathon research to create winning strategies."""
        
        super().__init__(
            model=OpenAIChat(id="gpt-4o"),
            instructions=instructions,
            tools=[],
            markdown=True,
        )


class RevampTeam(Team):
    """
    A team of specialized agents for the hackathon project revamp process.
    """
    
    def __init__(self):
        # Create specialized agents
        self.project_analyzer = ProjectAnalyzerAgent()
        self.hackathon_researcher = HackathonResearcherAgent()
        self.strategy_developer = StrategyDeveloperAgent()
        
        # Initialize the team with the agents
        agents = [
            self.project_analyzer,
            self.hackathon_researcher,
            self.strategy_developer
        ]
        
        # Define team instructions
        team_instructions = """You are a team of specialized agents working together to transform open-source GitHub projects into hackathon-winning solutions.
        
        The team consists of:
        1. Project Analyzer: Analyzes GitHub repositories for structure, tech stack, features, and improvement opportunities
        2. Hackathon Researcher: Researches hackathon requirements, themes, judging criteria, and winning patterns
        3. Strategy Developer: Creates comprehensive revamp strategies that align projects with hackathon goals
        
        Work collaboratively to:
        - Analyze the provided GitHub project
        - Research the target hackathon
        - Develop a winning strategy
        - Deliver a complete solution ready for the hackathon
        
        Share information between agents as needed to achieve the best outcome."""
        
        super().__init__(
            members=agents,
            instructions=team_instructions
        )


class RevampWorkflow(Workflow):
    """
    A structured workflow for the hackathon project revamp process.
    """
    
    def __init__(self):
        super().__init__()
        self.project_analyzer = ProjectAnalyzerAgent()
        self.hackathon_researcher = HackathonResearcherAgent()
        self.strategy_developer = StrategyDeveloperAgent()
        self.session_manager = get_session_manager()
        self.memory_manager = get_memory_manager()
        
    def run_workflow(
        self,
        github_url: Optional[str] = None,
        hackathon_url: Optional[str] = None,
        hackathon_context: Optional[str] = None,
        search_topic: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute the complete revamp workflow.
        
        Args:
            github_url: URL of the GitHub repository to revamp
            hackathon_url: URL of the hackathon website to analyze
            hackathon_context: Additional context about the hackathon
            search_topic: Topic for discovery if URLs are not provided
            session_id: Session ID to track the workflow
            
        Returns:
            Dictionary with workflow results
        """
        results = {
            "workflow_start_time": datetime.now().isoformat(),
            "project_analysis": None,
            "hackathon_research": None,
            "strategy": None,
            "workflow_end_time": None,
            "success": False
        }
        
        try:
            # Add to session if provided
            if session_id:
                self.session_manager.add_message_to_session(
                    session_id, "system", "Starting revamp workflow"
                )
            
            # Step 1: Project Analysis
            if github_url:
                project_query = f"Analyze the GitHub repository at {github_url}. Provide detailed analysis of codebase structure, technology stack, current features, strengths, weaknesses, and improvement opportunities."
                
                if session_id:
                    self.session_manager.add_message_to_session(
                        session_id, "system", f"Analyzing project: {github_url}"
                    )
                
                project_analysis = self.project_analyzer.run(project_query)
                results["project_analysis"] = project_analysis.content
                
                if session_id:
                    self.session_manager.add_message_to_session(
                        session_id, "assistant", f"Project Analysis:\n{project_analysis.content}"
                    )
            
            # Step 2: Hackathon Research
            if hackathon_url:
                hackathon_query = f"Research the hackathon at {hackathon_url}. Extract information about themes, judging criteria, prizes, deadlines, requirements, and sponsor interests."
                
                if session_id:
                    self.session_manager.add_message_to_session(
                        session_id, "system", f"Researching hackathon: {hackathon_url}"
                    )
                
                hackathon_research = self.hackathon_researcher.run(hackathon_query)
                results["hackathon_research"] = hackathon_research.content
                
                if session_id:
                    self.session_manager.add_message_to_session(
                        session_id, "assistant", f"Hackathon Research:\n{hackathon_research.content}"
                    )
            
            # Step 3: Strategy Development
            strategy_query_parts = ["Develop a comprehensive revamp strategy based on the analysis:"]
            
            if results["project_analysis"]:
                strategy_query_parts.append(f"PROJECT ANALYSIS:\n{results['project_analysis']}")
            
            if results["hackathon_research"]:
                strategy_query_parts.append(f"HACKATHON RESEARCH:\n{results['hackathon_research']}")
            
            if hackathon_context:
                strategy_query_parts.append(f"ADDITIONAL CONTEXT:\n{hackathon_context}")
            
            strategy_query_parts.append("""
            Create a strategy that:
            1. Aligns the project with hackathon goals
            2. Identifies novel features that would impress judges
            3. Develops differentiation tactics
            4. Provides an implementation roadmap
            5. Suggests presentation and demo strategies
            """)
            
            strategy_query = "\n\n".join(strategy_query_parts)
            
            if session_id:
                self.session_manager.add_message_to_session(
                    session_id, "system", "Developing revamp strategy"
                )
            
            strategy_result = self.strategy_developer.run(strategy_query)
            results["strategy"] = strategy_result.content
            
            if session_id:
                self.session_manager.add_message_to_session(
                    session_id, "assistant", f"Revamp Strategy:\n{strategy_result.content}"
                )
            
            results["success"] = True
            
        except Exception as e:
            results["error"] = str(e)
            if session_id:
                self.session_manager.add_message_to_session(
                    session_id, "system", f"Workflow failed with error: {str(e)}"
                )
        
        results["workflow_end_time"] = datetime.now().isoformat()
        
        if session_id:
            self.session_manager.add_message_to_session(
                session_id, "system", "Workflow completed"
            )
        
        return results


# Global instances
revamp_team = RevampTeam()
revamp_workflow = RevampWorkflow()


def get_revamp_team() -> RevampTeam:
    """
    Get the global revamp team instance.
    
    Returns:
        RevampTeam instance
    """
    return revamp_team


def get_revamp_workflow() -> RevampWorkflow:
    """
    Get the global revamp workflow instance.
    
    Returns:
        RevampWorkflow instance
    """
    return revamp_workflow