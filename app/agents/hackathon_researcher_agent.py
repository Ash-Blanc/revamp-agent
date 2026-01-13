"""
Hackathon Researcher Agent - Specialized agent for researching hackathons.

This agent focuses on understanding hackathon requirements, themes, judging criteria,
and identifying winning patterns.
"""

import os
from typing import Optional, List
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.firecrawl import FirecrawlTools
from .base_agent import BaseRevampAgent


class HackathonResearcherAgent(BaseRevampAgent):
    """
    Specialized agent for researching hackathons and understanding their requirements.
    
    This agent:
    - Analyzes hackathon websites and documentation
    - Extracts themes, judging criteria, and requirements
    - Researches previous winners and successful patterns
    - Identifies sponsor interests and priorities
    - Understands timeline and constraints
    """
    
    def __init__(self, model_id: str = "gpt-4o"):
        """Initialize the hackathon researcher agent."""
        
        tools = [DuckDuckGoTools()]
        if os.getenv("FIRECRAWL_API_KEY"):
            tools.append(FirecrawlTools())
        
        super().__init__(
            agent_name="HackathonResearcherAgent",
            model_id=model_id,
            tools=tools
        )
    
    def get_default_instructions(self) -> str:
        """Get default instructions for the hackathon researcher agent."""
        return """You are a specialized hackathon researcher. Your role is to analyze hackathon websites and information to understand:

1. **Hackathon Themes & Focus Areas**:
   - Main themes and tracks
   - Specific problem areas to address
   - Technology focus (AI, blockchain, IoT, etc.)
   - Social impact areas (climate, healthcare, education, etc.)

2. **Judging Criteria & Evaluation Metrics**:
   - How projects will be evaluated
   - Scoring rubrics and weightings
   - What judges look for in winning projects
   - Technical vs. business vs. presentation criteria

3. **Prizes & Awards Structure**:
   - Prize categories and amounts
   - Special tracks and sponsor prizes
   - Recognition opportunities
   - What different prizes reward

4. **Timeline & Important Deadlines**:
   - Registration deadlines
   - Submission deadlines
   - Event dates and duration
   - Key milestones and checkpoints

5. **Requirements & Constraints**:
   - Eligibility requirements
   - Team size limitations
   - Technology restrictions or requirements
   - Submission format and requirements

6. **Sponsor Information & Priorities**:
   - Who are the sponsors?
   - What are their business interests?
   - What technologies do they want to see used?
   - What problems do they want solved?

7. **Previous Winners & Successful Patterns**:
   - What types of projects have won before?
   - Common characteristics of successful submissions
   - Innovation patterns and trends
   - Presentation and demo strategies that work

When researching hackathons:
- Extract comprehensive information from hackathon websites
- Look for detailed rules, guidelines, and FAQs
- Research sponsor companies and their interests
- Find information about previous editions and winners
- Identify what makes projects stand out to judges
- Note any special requirements or constraints
- Look for differentiation opportunities

Use web scraping tools to gather comprehensive information from hackathon websites and related resources."""
    
    def research_hackathon(self, hackathon_url: str) -> str:
        """
        Research a hackathon comprehensively using its website.
        
        Args:
            hackathon_url: URL of the hackathon website to research
            
        Returns:
            Detailed hackathon research report
        """
        query = f"""
        Research the hackathon at {hackathon_url} comprehensively. Extract and analyze:

        1. **Hackathon Overview**:
           - Name and organizing body
           - Event dates and location (virtual/physical)
           - Registration and submission deadlines
           - Event format and duration

        2. **Themes & Tracks**:
           - Main hackathon theme
           - Specific tracks or categories
           - Problem areas to address
           - Technology focus areas

        3. **Judging & Evaluation**:
           - Judging criteria and rubrics
           - Evaluation process and timeline
           - What judges look for
           - Scoring methodology

        4. **Prizes & Recognition**:
           - Prize structure and amounts
           - Special category prizes
           - Sponsor-specific awards
           - Non-monetary recognition

        5. **Requirements & Rules**:
           - Eligibility requirements
           - Team size and composition rules
           - Technology requirements or restrictions
           - Submission format and requirements
           - Code of conduct and guidelines

        6. **Sponsors & Partners**:
           - List of sponsors and their roles
           - Sponsor-specific challenges or prizes
           - Technologies sponsors want to see
           - Sponsor business interests

        7. **Resources & Support**:
           - Provided APIs, datasets, or tools
           - Mentorship and support available
           - Workshops or training sessions
           - Technical resources

        8. **Success Patterns**:
           - Information about previous winners (if available)
           - Common characteristics of successful projects
           - What types of innovations are valued
           - Presentation and demo best practices

        Use web scraping tools to extract detailed information from the hackathon website.
        """
        
        response = self.run(query)
        return response.content
    
    def analyze_hackathon_context(self, hackathon_context: str) -> str:
        """
        Analyze provided hackathon context and research related information.
        
        Args:
            hackathon_context: Description or context about the hackathon
            
        Returns:
            Analysis and additional research based on the context
        """
        query = f"""
        Analyze the following hackathon context and provide additional research:

        Context: {hackathon_context}

        Based on this context:

        1. **Theme Analysis**:
           - Identify the main themes and focus areas
           - Understand the problem space
           - Determine technology requirements

        2. **Research Similar Hackathons**:
           - Find similar hackathons with these themes
           - Research what types of projects typically win
           - Identify common judging criteria for this theme

        3. **Success Patterns**:
           - What innovations work well in this space?
           - What technical approaches are most valued?
           - What presentation strategies are effective?

        4. **Opportunity Identification**:
           - What gaps exist in typical solutions?
           - What novel approaches could differentiate a project?
           - What emerging technologies could be leveraged?

        5. **Strategic Recommendations**:
           - How should projects be positioned for this theme?
           - What aspects should be emphasized?
           - What common pitfalls should be avoided?

        Use web search to find additional information about similar hackathons and winning strategies.
        """
        
        response = self.run(query)
        return response.content
    
    def find_winning_patterns(self, hackathon_theme: str) -> str:
        """
        Research winning patterns for hackathons with a specific theme.
        
        Args:
            hackathon_theme: The theme or focus area of hackathons to research
            
        Returns:
            Analysis of winning patterns and strategies
        """
        query = f"""
        Research winning patterns for hackathons focused on "{hackathon_theme}". Find:

        1. **Successful Project Types**:
           - What categories of projects typically win?
           - Common technical approaches
           - Popular frameworks and technologies

        2. **Innovation Patterns**:
           - What types of innovations are most valued?
           - How do winners differentiate themselves?
           - What novel features or approaches stand out?

        3. **Technical Excellence**:
           - What technical aspects do judges prioritize?
           - How important is code quality vs. functionality?
           - What technical demonstrations are most impressive?

        4. **Presentation & Demo Strategies**:
           - How do winning teams present their projects?
           - What demo formats are most effective?
           - How do they tell their story?

        5. **Common Mistakes to Avoid**:
           - What causes projects to fail in this theme?
           - What technical pitfalls are common?
           - What presentation mistakes should be avoided?

        Use web search to find information about past hackathon winners in this theme area.
        """
        
        response = self.run(query)
        return response.content