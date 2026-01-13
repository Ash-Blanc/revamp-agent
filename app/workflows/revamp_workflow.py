"""
Structured workflow for the hackathon project revamp process.
"""

from typing import Dict, Any, Optional
from .base_workflow import BaseWorkflow
from ..core.agent_factory import AgentFactory
from ..agents.project_analyzer import ProjectAnalyzer
from ..agents.hackathon_researcher import HackathonResearcher
from ..agents.strategy_agent import StrategyAgent
from ..agents.coding_agent import CodingAgent

class RevampWorkflow(BaseWorkflow):
    """
    A structured workflow for the hackathon project revamp process.
    """
    
    def __init__(self, include_coding_agent: bool = False):
        """
        Initialize the revamp workflow.
        
        Args:
            include_coding_agent: Whether to include the coding agent for implementation
        """
        factory = AgentFactory()
        
        agents = [
            factory.create_project_analyzer(),
            factory.create_hackathon_researcher(),
            factory.create_strategy_agent()
        ]
        
        if include_coding_agent:
            agents.append(factory.create_coding_agent())
        
        super().__init__(agents)
        
        self.include_coding = include_coding_agent
    
    def execute(
        self,
        github_url: Optional[str] = None,
        hackathon_url: Optional[str] = None,
        hackathon_context: Optional[str] = None,
        search_topic: Optional[str] = None,
        implement_changes: bool = False,
        fork_repo: bool = False,
        branch_name: str = "hackathon-revamp"
    ) -> Dict[str, Any]:
        """
        Execute the complete revamp workflow.
        
        Args:
            github_url: GitHub repository URL
            hackathon_url: Hackathon website URL
            hackathon_context: Additional hackathon context
            search_topic: Topic for discovery
            implement_changes: Whether to implement code changes
            fork_repo: Whether to fork the repository
            branch_name: Branch name for changes
            
        Returns:
            Dictionary with workflow results
        """
        results = {
            "workflow_start_time": self.execution_history[0]["timestamp"] if self.execution_history else None,
            "project_analysis": None,
            "hackathon_research": None,
            "strategy": None,
            "implementation": None,
            "success": False
        }
        
        try:
            # Step 1: Project Analysis
            if github_url:
                self.log_step("workflow_start", "Starting revamp workflow")
                
                project_analyzer = self.get_agent_by_type(ProjectAnalyzer)
                if project_analyzer:
                    project_analysis = project_analyzer.analyze_project(github_url)
                    results["project_analysis"] = project_analysis
                    self.log_step("project_analysis", project_analysis)
            
            # Step 2: Hackathon Research
            if hackathon_url:
                hackathon_researcher = self.get_agent_by_type(HackathonResearcher)
                if hackathon_researcher:
                    hackathon_research = hackathon_researcher.research_hackathon(hackathon_url)
                    results["hackathon_research"] = hackathon_research
                    self.log_step("hackathon_research", hackathon_research)
            elif search_topic and github_url:
                hackathon_researcher = self.get_agent_by_type(HackathonResearcher)
                if hackathon_researcher:
                    hackathon_research = hackathon_researcher.find_relevant_hackathons(
                        project_topic=search_topic
                    )
                    results["hackathon_research"] = hackathon_research
                    self.log_step("hackathon_discovery", hackathon_research)
            
            # Step 3: Strategy Development
            strategy_agent = self.get_agent_by_type(StrategyAgent)
            if strategy_agent:
                strategy = strategy_agent.create_revamp_strategy(
                    github_url=github_url,
                    hackathon_url=hackathon_url,
                    hackathon_context=hackathon_context,
                    search_topic=search_topic
                )
                results["strategy"] = strategy
                self.log_step("strategy_development", strategy)
            
            # Step 4: Implementation (if requested and coding agent available)
            if implement_changes and self.include_coding:
                coding_agent = self.get_agent_by_type(CodingAgent)
                if coding_agent and github_url:
                    # Extract repo name from URL
                    import re
                    match = re.search(r'github\.com/([^/]+/[^/]+)', github_url)
                    if match:
                        repo_name = match.group(1)
                        
                        if fork_repo:
                            implementation = coding_agent.fork_and_implement(
                                original_repo=repo_name,
                                revamp_strategy=strategy,
                                branch_name=branch_name
                            )
                        else:
                            implementation = coding_agent.implement_strategy(
                                repo_name=repo_name,
                                revamp_strategy=strategy,
                                branch_name=branch_name
                            )
                        
                        results["implementation"] = implementation
                        self.log_step("implementation", implementation)
            
            results["success"] = True
            self.log_step("workflow_complete", "Workflow completed successfully")
            
        except Exception as e:
            error_msg = str(e)
            results["error"] = error_msg
            self.log_step("workflow_error", error_msg, success=False)
        
        # Add execution summary
        results["execution_summary"] = self.get_execution_summary()
        
        return results
    
    def execute_strategy_only(
        self,
        github_url: Optional[str] = None,
        hackathon_url: Optional[str] = None,
        hackathon_context: Optional[str] = None,
        search_topic: Optional[str] = None
    ) -> str:
        """
        Execute only the strategy development part of the workflow.
        
        Returns:
            Strategy string
        """
        result = self.execute(
            github_url=github_url,
            hackathon_url=hackathon_url,
            hackathon_context=hackathon_context,
            search_topic=search_topic,
            implement_changes=False
        )
        
        return result.get("strategy", "")
    
    def execute_with_implementation(
        self,
        github_url: str,
        hackathon_url: Optional[str] = None,
        hackathon_context: Optional[str] = None,
        search_topic: Optional[str] = None,
        fork_repo: bool = True,
        branch_name: str = "hackathon-revamp"
    ) -> Dict[str, Any]:
        """
        Execute the workflow with code implementation.
        
        Returns:
            Complete workflow results including implementation
        """
        return self.execute(
            github_url=github_url,
            hackathon_url=hackathon_url,
            hackathon_context=hackathon_context,
            search_topic=search_topic,
            implement_changes=True,
            fork_repo=fork_repo,
            branch_name=branch_name
        )