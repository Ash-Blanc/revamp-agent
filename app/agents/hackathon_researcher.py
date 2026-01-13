"""
Hackathon researcher agent for analyzing hackathon requirements.
"""

from typing import List, Optional
from ..core.base_agent import BaseRevampAgent

class HackathonResearcher(BaseRevampAgent):
    """
    Agent specialized in researching hackathons and their requirements.
    """
    
    def __init__(self, tools: Optional[List] = None):
        super().__init__(
            model_id="gpt-4o",
            temperature=0.3,  # Lower temperature for more consistent research
            tools=tools
        )
    
    def get_default_instructions(self) -> str:
        return """You are a specialized hackathon researcher. Your role is to analyze hackathon websites and information to understand:
        
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
    
    def research_hackathon(self, hackathon_url: str) -> str:
        """
        Research a hackathon comprehensively.
        
        Args:
            hackathon_url: URL of the hackathon website
            
        Returns:
            Detailed hackathon research
        """
        query = f"""
        Research the hackathon at {hackathon_url}. Extract and analyze:
        
        1. **Hackathon Overview**:
           - Name and organizing body
           - Main theme or focus area
           - Target audience and participants
           - Event format (virtual, in-person, hybrid)
        
        2. **Themes and Tracks**:
           - Primary themes or challenge areas
           - Specific tracks or categories
           - Technology focus areas
           - Problem statements or challenges
        
        3. **Judging Criteria**:
           - How projects will be evaluated
           - Scoring rubrics or criteria
           - What judges look for
           - Weighting of different factors
        
        4. **Prizes and Recognition**:
           - Prize amounts and categories
           - Special awards or recognitions
           - Sponsor-specific prizes
           - Non-monetary benefits
        
        5. **Timeline and Deadlines**:
           - Registration deadlines
           - Submission deadlines
           - Event dates and schedule
           - Key milestones
        
        6. **Requirements and Rules**:
           - Eligibility criteria
           - Team size limitations
           - Technology restrictions
           - Submission requirements
           - Code of conduct
        
        7. **Sponsors and Partners**:
           - Main sponsors and their interests
           - Technology partners
           - What sponsors are looking for
           - Sponsor-specific challenges
        
        8. **Success Patterns**:
           - Previous winning projects (if available)
           - Common themes in successful submissions
           - What makes projects stand out
           - Innovation areas that impress judges
        
        Use web scraping tools (Firecrawl) to gather comprehensive information from the hackathon website.
        Also search for additional information about the hackathon, previous winners, and related events.
        """
        
        return self.run(query)
    
    def find_relevant_hackathons(self, project_topic: str, tech_stack: Optional[str] = None) -> str:
        """
        Find hackathons relevant to a project topic.
        
        Args:
            project_topic: Main topic or theme of the project
            tech_stack: Technologies used in the project
            
        Returns:
            List of relevant hackathons with analysis
        """
        query = f"""
        Find ongoing and upcoming hackathons that would be a good fit for a project with:
        - Topic/Theme: {project_topic}
        {f"- Technology Stack: {tech_stack}" if tech_stack else ""}
        
        Use the find_ongoing_hackathons tool to discover relevant hackathons.
        For each hackathon found, provide:
        1. Name and URL
        2. Why it's a good fit for the project
        3. Key themes that align
        4. Submission deadlines
        5. Prize information
        6. Strategic positioning recommendations
        
        Focus on hackathons where the project would have a competitive advantage.
        """
        
        return self.run(query)