"""
Project analyzer agent for analyzing GitHub repositories.
"""

from typing import List, Optional
from ..core.base_agent import BaseRevampAgent

class ProjectAnalyzer(BaseRevampAgent):
    """
    Agent specialized in analyzing GitHub projects.
    """
    
    def __init__(self, tools: Optional[List] = None):
        super().__init__(
            model_id="gpt-4o",
            temperature=0.3,  # Lower temperature for more consistent analysis
            tools=tools
        )
    
    def get_default_instructions(self) -> str:
        return """You are a specialized GitHub project analyzer. Your role is to deeply analyze GitHub repositories to understand:
        
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
        
        Use available tools to gather information about the repository. You can access both GitHub repositories and local files."""
    
    def analyze_project(self, github_url: str) -> str:
        """
        Analyze a GitHub project comprehensively.
        
        Args:
            github_url: URL of the GitHub repository
            
        Returns:
            Detailed project analysis
        """
        query = f"""
        Analyze the GitHub repository at {github_url}. Provide detailed analysis of:
        
        1. **Repository Structure**: 
           - Main directories and their purposes
           - Key files and their roles
           - Overall organization and architecture
        
        2. **Technology Stack**:
           - Programming languages used
           - Frameworks and libraries
           - Dependencies and package managers
           - Build tools and configuration
        
        3. **Current Features**:
           - Main functionality provided
           - Key components and modules
           - User-facing features
           - API endpoints or interfaces
        
        4. **Code Quality Assessment**:
           - Code organization and structure
           - Documentation quality
           - Testing coverage and approach
           - Code style and consistency
        
        5. **Strengths**:
           - What the project does well
           - Unique or innovative aspects
           - Technical advantages
           - Community engagement
        
        6. **Areas for Improvement**:
           - Technical debt or issues
           - Missing features or functionality
           - Performance bottlenecks
           - User experience improvements
           - Documentation gaps
        
        7. **Enhancement Opportunities**:
           - Potential new features
           - Technology upgrades
           - Architecture improvements
           - Integration possibilities
        
        Use GitHub tools to explore the repository structure, read key files, and understand the codebase.
        """
        
        return self.run(query)