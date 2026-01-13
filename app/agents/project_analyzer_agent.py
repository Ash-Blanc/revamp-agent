"""
Project Analyzer Agent - Specialized agent for analyzing GitHub projects.

This agent focuses on understanding project structure, technology stack,
and identifying improvement opportunities.
"""

import os
from typing import Optional, List
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.firecrawl import FirecrawlTools
from agno.tools.file import FileTools
from agno.tools.local_file_system import LocalFileSystemTools
from .base_agent import BaseRevampAgent


class ProjectAnalyzerAgent(BaseRevampAgent):
    """
    Specialized agent for analyzing GitHub projects.
    
    This agent:
    - Examines repository structure and architecture
    - Identifies technology stack and dependencies
    - Assesses current features and functionality
    - Highlights strengths and weaknesses
    - Identifies potential improvement areas
    """
    
    def __init__(self, model_id: str = "gpt-4o"):
        """Initialize the project analyzer agent."""
        
        tools = [DuckDuckGoTools(), FileTools(), LocalFileSystemTools()]
        if os.getenv("FIRECRAWL_API_KEY"):
            tools.append(FirecrawlTools())
        
        super().__init__(
            agent_name="ProjectAnalyzerAgent",
            model_id=model_id,
            tools=tools
        )
    
    def get_default_instructions(self) -> str:
        """Get default instructions for the project analyzer agent."""
        return """You are a specialized GitHub project analyzer. Your role is to deeply analyze GitHub repositories to understand:

1. **Codebase Structure & Architecture**:
   - Repository organization and folder structure
   - Main modules and components
   - Architecture patterns used (MVC, microservices, etc.)
   - Code organization and separation of concerns

2. **Technology Stack & Dependencies**:
   - Programming languages used
   - Frameworks and libraries
   - Build tools and package managers
   - Database and storage solutions
   - External APIs and services

3. **Current Features & Functionality**:
   - Core features and capabilities
   - User interface and experience
   - API endpoints and integrations
   - Performance characteristics
   - Security implementations

4. **Strengths & Weaknesses Assessment**:
   - Well-implemented features
   - Code quality and maintainability
   - Documentation quality
   - Test coverage
   - Areas needing improvement

5. **Improvement Opportunities**:
   - Technical debt identification
   - Performance optimization potential
   - Feature enhancement possibilities
   - Modernization opportunities
   - Security improvements

When analyzing projects:
- Examine the repository structure thoroughly
- Read key files (README, package.json, requirements.txt, etc.)
- Identify the main technologies and frameworks
- Assess the project's current state and maturity
- Look for patterns and architectural decisions
- Note any obvious issues or improvement areas
- Consider scalability and maintainability aspects

Use available tools to gather comprehensive information about the repository."""
    
    def analyze_project(self, github_url: str) -> str:
        """
        Analyze a GitHub project comprehensively.
        
        Args:
            github_url: URL of the GitHub repository to analyze
            
        Returns:
            Detailed project analysis
        """
        query = f"""
        Analyze the GitHub repository at {github_url}. Provide a comprehensive analysis covering:

        1. **Repository Overview**:
           - Project name and description
           - Main purpose and target audience
           - Repository statistics (stars, forks, issues)

        2. **Codebase Structure**:
           - Folder and file organization
           - Main modules and components
           - Architecture patterns identified

        3. **Technology Stack**:
           - Programming languages (with percentages if available)
           - Frameworks and libraries used
           - Build tools and dependencies
           - Database and storage solutions

        4. **Features & Functionality**:
           - Core features and capabilities
           - User interface type (web, mobile, CLI, etc.)
           - API endpoints or integrations
           - Notable functionality

        5. **Code Quality Assessment**:
           - Code organization and structure
           - Documentation quality
           - Test coverage (if visible)
           - Code style and consistency

        6. **Strengths**:
           - Well-implemented aspects
           - Notable features or innovations
           - Good practices observed

        7. **Areas for Improvement**:
           - Technical debt or issues identified
           - Missing features or functionality
           - Performance optimization opportunities
           - Modernization possibilities

        8. **Hackathon Potential**:
           - How suitable is this project for hackathon enhancement?
           - What types of hackathons would this project fit?
           - What novel features could be added?

        Use web search and file reading tools to gather comprehensive information.
        """
        
        response = self.run(query)
        return response.content
    
    def quick_analysis(self, github_url: str) -> str:
        """
        Perform a quick analysis focusing on key aspects.
        
        Args:
            github_url: URL of the GitHub repository to analyze
            
        Returns:
            Concise project analysis
        """
        query = f"""
        Perform a quick analysis of the GitHub repository at {github_url}. Focus on:

        1. **Tech Stack**: Main languages, frameworks, and tools
        2. **Core Features**: What does this project do?
        3. **Architecture**: How is the code organized?
        4. **Strengths**: What's working well?
        5. **Improvement Areas**: What could be enhanced?
        6. **Hackathon Fit**: What hackathon themes would this project suit?

        Provide a concise but informative analysis.
        """
        
        response = self.run(query)
        return response.content