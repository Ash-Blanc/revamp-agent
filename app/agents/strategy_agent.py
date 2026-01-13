"""
Strategy agent for creating revamp strategies.
"""

from typing import List, Optional
from ..core.base_agent import BaseRevampAgent

class StrategyAgent(BaseRevampAgent):
    """
    Agent specialized in creating comprehensive revamp strategies.
    """
    
    def __init__(self, tools: Optional[List] = None):
        super().__init__(
            model_id="gpt-4o",
            temperature=0.7,
            tools=tools,
            prompt_name="hackathon_revamp_agent"
        )
    
    def get_default_instructions(self) -> str:
        return """You are an expert hackathon strategist and open-source project revamp specialist. Your mission is to transform existing open-source GitHub projects into hackathon-winning solutions.

## Your Core Capabilities:

1. **Project Analysis**: Deeply analyze GitHub repositories to understand:
   - Codebase structure, architecture, and technical stack
   - Current features and functionality
   - Strengths and weaknesses
   - Technical debt and improvement opportunities

2. **Hackathon Research & Strategy**: 
   - Scrape and analyze hackathon websites to extract themes, judging criteria, and priorities
   - Discover ongoing hackathons when URLs are not provided using discovery tools
   - Understand specific requirements, deadlines, and constraints
   - Research current trends in hackathon-winning projects
   - Identify what makes projects stand out to judges
   - Develop strategic positioning for maximum impact

3. **Innovation & Novelty**: 
   - Propose creative, novel features that differentiate the project
   - Combine existing functionality with innovative enhancements
   - Focus on unique value propositions that judges will remember
   - Balance feasibility with ambition

4. **Comprehensive Revamp Planning**:
   - Create detailed revamp strategies with actionable steps
   - Prioritize features based on hackathon impact
   - Suggest technical improvements and optimizations
   - Provide presentation and demo strategies

Always focus on:
- **Novelty**: What makes this revamp unique and memorable?
- **Strategy**: How does this position the project to win?
- **Research**: What do winning hackathon projects typically have?
- **Feasibility**: Can this be realistically implemented for the hackathon?

Be thorough, creative, and strategic in your analysis and recommendations."""
    
    def create_revamp_strategy(
        self,
        github_url: Optional[str] = None,
        hackathon_url: Optional[str] = None,
        hackathon_context: Optional[str] = None,
        search_order: str = "projects_first",
        search_topic: Optional[str] = None
    ) -> str:
        """
        Create a comprehensive revamp strategy.
        
        Args:
            github_url: GitHub repository URL
            hackathon_url: Hackathon website URL
            hackathon_context: Additional hackathon context
            search_order: Discovery order ("projects_first" or "hackathons_first")
            search_topic: Topic for discovery
            
        Returns:
            Comprehensive revamp strategy
        """
        # Build the query based on what's provided
        query_parts = []
        needs_discovery = []
        
        if github_url:
            query_parts.append(f"GitHub Project: {github_url}")
        else:
            needs_discovery.append("github_project")
        
        if hackathon_url:
            query_parts.append(f"Hackathon Website: {hackathon_url}")
            query_parts.append(
                "Please scrape and analyze the hackathon website to understand: "
                "themes, judging criteria, prizes, deadlines, requirements, and any specific focus areas."
            )
        else:
            needs_discovery.append("hackathon")
        
        if hackathon_context:
            query_parts.append(f"Additional Hackathon Context: {hackathon_context}")
        
        # Build discovery instructions
        discovery_instructions = []
        
        if needs_discovery:
            if len(needs_discovery) == 2:
                # Both are missing - use search_order
                if search_order == "hackathons_first":
                    discovery_instructions.append(
                        "1. First, use the find_ongoing_hackathons tool to discover relevant, ongoing hackathons. "
                        f"{'Focus on: ' + search_topic if search_topic else 'Look for popular and relevant hackathons'}."
                    )
                    discovery_instructions.append(
                        "2. Then, for each discovered hackathon, use find_projects_for_hackathon to find GitHub projects "
                        "that would be a good fit for that hackathon's theme."
                    )
                else:  # projects_first (default)
                    discovery_instructions.append(
                        "1. First, use the find_relevant_github_projects tool to discover relevant GitHub projects. "
                        f"{'Focus on topic: ' + search_topic if search_topic else 'Look for interesting open-source projects'}."
                    )
                    discovery_instructions.append(
                        "2. Then, for each discovered project, use find_hackathons_for_project to find hackathons "
                        "that would be a good fit for that project's topic/tech stack."
                    )
                discovery_instructions.append(
                    "3. Present the discovered options and select the best matches for revamp strategy."
                )
            elif "github_project" in needs_discovery:
                discovery_instructions.append(
                    "Use the find_relevant_github_projects tool to discover relevant GitHub projects. "
                    f"{'Focus on topic: ' + search_topic if search_topic else 'Look for projects that align with the hackathon theme'}."
                )
            elif "hackathon" in needs_discovery:
                discovery_instructions.append(
                    "Use the find_ongoing_hackathons tool to discover relevant, ongoing hackathons. "
                    f"{'Focus on: ' + search_topic if search_topic else 'Look for hackathons that align with the project'}."
                )
        
        query = f"""
        Analyze the provided information and create a winning hackathon revamp strategy:
        
        {chr(10).join(query_parts) if query_parts else 'No specific URLs provided - discovery mode activated.'}
        
        {chr(10).join(discovery_instructions) if discovery_instructions else ''}
        
        Please provide:
        1. Project analysis (if GitHub URL provided or discovered: structure, features, tech stack, strengths/weaknesses)
        2. Hackathon analysis (if hackathon URL provided or discovered: themes, criteria, requirements, focus areas)
        3. Strategic positioning that aligns the project with hackathon goals
        4. Novel feature proposals that differentiate the project
        5. Comprehensive revamp plan with actionable steps
        6. Demo and presentation recommendations
        7. Differentiation tactics
        
        Focus on novelty, strategy, and research-backed enhancements.
        Use web scraping tools (Firecrawl) to gather detailed information from hackathon websites when URLs are provided.
        Use discovery tools (find_ongoing_hackathons, find_relevant_github_projects, etc.) when URLs are not provided.
        """
        
        return self.run(query)