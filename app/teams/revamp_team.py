"""
Specialized team for hackathon project revamp tasks.
"""

from typing import Dict, Any, Optional
from .base_team import BaseTeam
from ..core.agent_factory import AgentFactory
from ..agents.project_analyzer import ProjectAnalyzer
from ..agents.hackathon_researcher import HackathonResearcher
from ..agents.strategy_agent import StrategyAgent

class RevampTeam(BaseTeam):
    """
    A team of specialized agents for the hackathon project revamp process.
    """
    
    def __init__(self):
        # Create specialized agents using the factory
        factory = AgentFactory()
        
        self.project_analyzer = factory.create_project_analyzer()
        self.hackathon_researcher = factory.create_hackathon_researcher()
        self.strategy_agent = factory.create_strategy_agent()
        
        agents = [
            self.project_analyzer,
            self.hackathon_researcher,
            self.strategy_agent
        ]
        
        instructions = """You are a team of specialized agents working together to transform open-source GitHub projects into hackathon-winning solutions.
        
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
        
        super().__init__(agents, instructions)
    
    def execute(
        self,
        github_url: Optional[str] = None,
        hackathon_url: Optional[str] = None,
        hackathon_context: Optional[str] = None,
        search_topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute the complete revamp process using team collaboration.
        
        Args:
            github_url: GitHub repository URL
            hackathon_url: Hackathon website URL
            hackathon_context: Additional hackathon context
            search_topic: Topic for discovery
            
        Returns:
            Dictionary with team execution results
        """
        results = {
            "project_analysis": None,
            "hackathon_research": None,
            "strategy": None,
            "success": False
        }
        
        try:
            # Step 1: Project Analysis (if GitHub URL provided)
            if github_url:
                results["project_analysis"] = self.project_analyzer.analyze_project(github_url)
            
            # Step 2: Hackathon Research (if hackathon URL provided)
            if hackathon_url:
                results["hackathon_research"] = self.hackathon_researcher.research_hackathon(hackathon_url)
            elif search_topic and github_url:
                # Find relevant hackathons for the project
                results["hackathon_research"] = self.hackathon_researcher.find_relevant_hackathons(
                    project_topic=search_topic
                )
            
            # Step 3: Strategy Development
            results["strategy"] = self.strategy_agent.create_revamp_strategy(
                github_url=github_url,
                hackathon_url=hackathon_url,
                hackathon_context=hackathon_context,
                search_topic=search_topic
            )
            
            results["success"] = True
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def analyze_project_only(self, github_url: str) -> str:
        """Analyze a project using the project analyzer."""
        return self.project_analyzer.analyze_project(github_url)
    
    def research_hackathon_only(self, hackathon_url: str) -> str:
        """Research a hackathon using the hackathon researcher."""
        return self.hackathon_researcher.research_hackathon(hackathon_url)
    
    def create_strategy_only(
        self,
        github_url: Optional[str] = None,
        hackathon_url: Optional[str] = None,
        hackathon_context: Optional[str] = None,
        search_topic: Optional[str] = None
    ) -> str:
        """Create a strategy using the strategy agent."""
        return self.strategy_agent.create_revamp_strategy(
            github_url=github_url,
            hackathon_url=hackathon_url,
            hackathon_context=hackathon_context,
            search_topic=search_topic
        )