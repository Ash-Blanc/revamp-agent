"""
Strategy Developer Agent - Specialized agent for developing comprehensive revamp strategies.

This agent synthesizes project analysis and hackathon research to create winning strategies.
"""

from typing import Optional, Dict, Any
from .base_agent import BaseRevampAgent


class StrategyDeveloperAgent(BaseRevampAgent):
    """
    Specialized agent for developing comprehensive revamp strategies.
    
    This agent:
    - Synthesizes project analysis and hackathon research
    - Develops strategic positioning for maximum impact
    - Creates novel feature proposals that differentiate projects
    - Designs implementation roadmaps with actionable steps
    - Suggests presentation and demo strategies
    """
    
    def __init__(self, model_id: str = "gpt-4o"):
        """Initialize the strategy developer agent."""
        
        super().__init__(
            agent_name="StrategyDeveloperAgent",
            model_id=model_id,
            tools=[]  # This agent primarily synthesizes information, doesn't need external tools
        )
    
    def get_default_instructions(self) -> str:
        """Get default instructions for the strategy developer agent."""
        return """You are a specialized strategy developer for hackathon project revamps. Your role is to create comprehensive strategies that transform projects into hackathon winners.

## Your Core Responsibilities:

1. **Strategic Synthesis**:
   - Combine project analysis with hackathon research
   - Identify alignment opportunities between project capabilities and hackathon goals
   - Find gaps where innovation can create competitive advantage

2. **Strategic Positioning**:
   - Position the project to maximize appeal to judges
   - Align project strengths with hackathon evaluation criteria
   - Create compelling narratives that resonate with hackathon themes

3. **Innovation Development**:
   - Propose novel features that would impress judges
   - Identify unique value propositions that differentiate the project
   - Balance innovation with feasibility given hackathon constraints

4. **Implementation Planning**:
   - Create detailed, actionable implementation roadmaps
   - Prioritize features based on impact and feasibility
   - Consider timeline constraints and resource limitations
   - Break down complex features into manageable tasks

5. **Presentation Strategy**:
   - Design compelling demo and presentation strategies
   - Identify key messages and value propositions
   - Suggest visual and interactive elements that engage judges
   - Plan storytelling approaches that highlight innovation

6. **Risk Mitigation**:
   - Identify potential challenges and provide mitigation strategies
   - Consider technical risks and provide alternatives
   - Plan for common hackathon pitfalls

## Strategy Development Process:

When developing strategies:
1. **Analyze the Alignment**: How well does the project fit the hackathon theme?
2. **Identify Gaps**: What's missing that could make the project stand out?
3. **Propose Innovations**: What novel features would impress judges?
4. **Plan Implementation**: How can these be realistically implemented?
5. **Design Presentation**: How should this be demonstrated and presented?
6. **Consider Differentiation**: What makes this unique compared to typical submissions?

## Key Principles:

- **Novelty**: Focus on what makes the project unique and memorable
- **Strategy**: Ensure every recommendation aligns with winning the hackathon
- **Feasibility**: Balance ambition with realistic implementation timelines
- **Impact**: Prioritize features that will have maximum judge appeal
- **Coherence**: Ensure all recommendations work together as a unified strategy

Always provide specific, actionable recommendations with clear rationale."""
    
    def develop_strategy(
        self,
        project_analysis: Optional[str] = None,
        hackathon_research: Optional[str] = None,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Develop a comprehensive revamp strategy based on analysis inputs.
        
        Args:
            project_analysis: Analysis of the GitHub project
            hackathon_research: Research about the target hackathon
            additional_context: Any additional context or requirements
            
        Returns:
            Comprehensive revamp strategy
        """
        strategy_inputs = []
        
        if project_analysis:
            strategy_inputs.append(f"## PROJECT ANALYSIS\n{project_analysis}")
        
        if hackathon_research:
            strategy_inputs.append(f"## HACKATHON RESEARCH\n{hackathon_research}")
        
        if additional_context:
            strategy_inputs.append(f"## ADDITIONAL CONTEXT\n{additional_context}")
        
        query = f"""
        Based on the following analysis, develop a comprehensive revamp strategy:

        {chr(10).join(strategy_inputs)}

        Create a detailed strategy that includes:

        ## 1. STRATEGIC POSITIONING
        - How should this project be positioned for maximum hackathon impact?
        - What narrative should be crafted around the project?
        - How does this align with hackathon themes and judging criteria?

        ## 2. NOVEL FEATURE PROPOSALS
        - What innovative features should be added to differentiate the project?
        - How do these features align with hackathon goals?
        - What unique value propositions do these create?

        ## 3. TECHNICAL IMPROVEMENTS
        - What technical enhancements would impress judges?
        - How can the project's architecture be improved?
        - What performance or scalability improvements are needed?

        ## 4. IMPLEMENTATION ROADMAP
        - Prioritized list of features and improvements
        - Timeline and resource estimates
        - Dependencies and critical path analysis
        - Risk mitigation strategies

        ## 5. PRESENTATION & DEMO STRATEGY
        - How should the project be demonstrated?
        - What key messages should be emphasized?
        - What visual or interactive elements would be compelling?
        - How should the story be told to judges?

        ## 6. DIFFERENTIATION TACTICS
        - What makes this project unique compared to typical submissions?
        - How can it stand out in a crowded field?
        - What competitive advantages can be highlighted?

        ## 7. SUCCESS METRICS
        - How will success be measured?
        - What outcomes indicate the strategy is working?
        - What feedback loops should be established?

        Ensure all recommendations are:
        - Specific and actionable
        - Aligned with hackathon success
        - Feasible within typical hackathon constraints
        - Coherent as an overall strategy
        """
        
        response = self.run(query)
        return response.content
    
    def refine_strategy(
        self,
        current_strategy: str,
        feedback: str,
        constraints: Optional[str] = None
    ) -> str:
        """
        Refine an existing strategy based on feedback and constraints.
        
        Args:
            current_strategy: The current strategy to refine
            feedback: Feedback or new requirements
            constraints: Additional constraints to consider
            
        Returns:
            Refined strategy
        """
        query = f"""
        Refine the following strategy based on new feedback and constraints:

        ## CURRENT STRATEGY
        {current_strategy}

        ## FEEDBACK TO INCORPORATE
        {feedback}

        {f"## ADDITIONAL CONSTRAINTS\n{constraints}" if constraints else ""}

        Provide a refined strategy that:
        1. Addresses all feedback points
        2. Incorporates new constraints
        3. Maintains strategic coherence
        4. Improves upon the original strategy
        5. Remains actionable and feasible

        Focus on the specific areas that need refinement while maintaining the overall strategic direction.
        """
        
        response = self.run(query)
        return response.content
    
    def create_quick_strategy(
        self,
        project_summary: str,
        hackathon_theme: str,
        time_constraint: str = "48 hours"
    ) -> str:
        """
        Create a quick strategy for time-constrained situations.
        
        Args:
            project_summary: Brief summary of the project
            hackathon_theme: Theme or focus of the hackathon
            time_constraint: Available time for implementation
            
        Returns:
            Focused, time-appropriate strategy
        """
        query = f"""
        Create a focused revamp strategy for a time-constrained hackathon:

        **Project**: {project_summary}
        **Hackathon Theme**: {hackathon_theme}
        **Time Available**: {time_constraint}

        Given the time constraint, focus on:

        ## HIGH-IMPACT, LOW-EFFORT IMPROVEMENTS
        - What changes would have maximum judge appeal with minimal implementation time?
        - Which existing features can be enhanced quickly?
        - What presentation improvements can be made rapidly?

        ## CORE FEATURE ADDITIONS
        - 1-2 key features that align perfectly with the hackathon theme
        - Features that can be implemented within the time constraint
        - Innovations that would differentiate from typical submissions

        ## RAPID IMPLEMENTATION PLAN
        - Hour-by-hour breakdown of implementation priorities
        - What can be done in parallel?
        - What are the must-have vs. nice-to-have features?

        ## DEMO STRATEGY
        - How to present the project for maximum impact
        - What to emphasize given limited development time
        - How to tell a compelling story with the available features

        Prioritize speed and impact over complexity.
        """
        
        response = self.run(query)
        return response.content