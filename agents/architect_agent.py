"""
Test Architect Agent - Creates comprehensive test plans and strategies.
"""

from typing import Dict, Optional
from .base_agent import BaseAgent
from .agent_prompts import get_agent_prompt
from loguru import logger
import json


class ArchitectAgent(BaseAgent):
    """Test Architect Agent that creates test plans and strategies."""
    
    def __init__(self):
        super().__init__(
            name="Test Architect",
            role="Create comprehensive test plans and testing strategies",
            temperature=0.7
        )
    
    def get_system_prompt(self) -> str:
        """Get system prompt for architect."""
        return get_agent_prompt('architect')
    
    def execute_task(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Execute test architecture task.
        
        Args:
            task: Task dictionary
            context: Optional context
            
        Returns:
            Task result
        """
        task_type = task.get('type', 'create_test_plan')
        
        if task_type == 'create_test_plan':
            return self.create_test_plan(task, context)
        elif task_type == 'define_strategy':
            return self.define_test_strategy(task, context)
        elif task_type == 'analyze_coverage':
            return self.analyze_test_coverage(task, context)
        else:
            return self.create_test_plan(task, context)
    
    def create_test_plan(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Create comprehensive test plan.
        
        Args:
            task: Task parameters
            context: Code analysis and documentation context
            
        Returns:
            Test plan
        """
        logger.info("Creating comprehensive test plan...")
        
        prompt = f"""
Create a comprehensive test plan for the software project based on the following information:

{context}

The test plan should include:

1. TEST PLAN OVERVIEW
   - Project/Application name
   - Test plan version
   - Purpose and objectives
   - Scope (what will be tested and what won't)

2. TEST APPROACH
   - Testing methodology (Agile, Waterfall, hybrid)
   - Test levels (Unit, Integration, System, Acceptance)
   - Test types required for each component

3. BACKEND TESTING STRATEGY
   a) API Testing:
      - REST API endpoints to test
      - Authentication/Authorization testing
      - Request/Response validation
      - Error handling scenarios
      - Performance testing requirements
   
   b) Database Testing:
      - Database schema validation
      - CRUD operations testing
      - Data integrity checks
      - Query performance testing
      - Migration testing
   
   c) CLI Testing:
      - Command-line interface testing
      - Input validation
      - Output verification
      - Error handling

4. FRONTEND TESTING STRATEGY
   a) GUI Testing:
      - User interface components
      - User workflows and scenarios
      - Cross-browser testing
      - Responsive design testing
      - Accessibility testing
   
   b) Component Testing:
      - Individual component testing
      - Component integration
      - State management

5. INTEGRATION TESTING
   - Backend-Frontend integration points
   - Third-party integrations
   - API contract testing
   - Data flow validation

6. END-TO-END TESTING
   - Critical user journeys
   - Business workflow scenarios
   - Cross-component interactions

7. NON-FUNCTIONAL TESTING
   - Performance testing
   - Security testing
   - Load/Stress testing
   - Compatibility testing

8. TEST ENVIRONMENT
   - Environment setup requirements
   - Test data requirements
   - Tools and frameworks needed

9. RISK ANALYSIS
   - High-risk areas
   - Mitigation strategies
   - Contingency plans

10. TIMELINE AND MILESTONES
    - Test planning phase
    - Test case development phase
    - Automation development phase
    - Test execution phase
    - Reporting phase

11. RESOURCE ALLOCATION
    - Agent assignments
    - Effort estimates
    - Dependencies

12. ENTRY AND EXIT CRITERIA
    - When to start testing
    - When testing is complete
    - Quality gates

13. DELIVERABLES
    - Test cases
    - Automation scripts
    - Test reports
    - Documentation

Format the output as a well-structured markdown document that can be directly saved as a test plan.
"""
        
        response = self.generate_response(prompt, context=context)
        
        test_plan = {
            'test_plan_document': response,
            'version': '1.0',
            'status': 'draft',
            'created_by': self.name
        }
        
        self.log_activity("Test plan created", {'length': len(response)})
        return test_plan
    
    def define_test_strategy(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Define detailed test strategy.
        
        Args:
            task: Task parameters
            context: Context
            
        Returns:
            Test strategy
        """
        logger.info("Defining test strategy...")
        
        component = task.get('component', 'all')
        
        prompt = f"""
Define a detailed test strategy for: {component}

Context:
{context}

Provide:
1. Component-specific testing approach
2. Test case categories and priorities
3. Tools and frameworks to use
4. Automation strategy
5. Test data strategy
6. Reporting requirements
7. Success criteria

Be specific and technical with examples where appropriate.
"""
        
        response = self.generate_response(prompt, context=context)
        
        strategy = {
            'component': component,
            'strategy_document': response,
            'created_by': self.name
        }
        
        self.log_activity("Test strategy defined", {'component': component})
        return strategy
    
    def analyze_test_coverage(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Analyze test coverage requirements.
        
        Args:
            task: Task parameters
            context: Context with code analysis
            
        Returns:
            Coverage analysis
        """
        logger.info("Analyzing test coverage requirements...")
        
        prompt = f"""
Based on the code analysis, determine the test coverage requirements:

{context}

Provide:
1. Code coverage targets (percentage for unit, integration, e2e)
2. Critical paths that must be covered
3. High-risk areas requiring extensive testing
4. Coverage gaps and how to address them
5. Coverage measurement strategy
6. Tools for coverage analysis

Format as structured analysis with specific recommendations.
"""
        
        response = self.generate_response(prompt, context=context)
        
        coverage = {
            'coverage_analysis': response,
            'created_by': self.name
        }
        
        self.log_activity("Coverage analysis completed")
        return coverage
    
    def revise_test_plan(self, original_plan: str, feedback: str, context: Optional[str] = None) -> Dict:
        """
        Revise test plan based on feedback.
        
        Args:
            original_plan: Original test plan
            feedback: Feedback from critic
            context: Additional context
            
        Returns:
            Revised test plan
        """
        logger.info("Revising test plan based on feedback...")
        
        prompt = f"""
Original Test Plan:
{original_plan}

Feedback from Test Architect Critic:
{feedback}

Additional Context:
{context}

Revise the test plan by:
1. Addressing all critical feedback points
2. Incorporating suggestions
3. Filling identified gaps
4. Improving clarity where needed
5. Adding missing sections

Provide the complete revised test plan in the same format.
"""
        
        response = self.generate_response(prompt)
        
        revised_plan = {
            'test_plan_document': response,
            'version': '2.0',
            'status': 'revised',
            'changes': 'Incorporated feedback from architect critic',
            'created_by': self.name
        }
        
        self.log_activity("Test plan revised based on feedback")
        return revised_plan
