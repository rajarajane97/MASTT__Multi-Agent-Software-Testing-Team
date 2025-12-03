"""
Project Manager Agent - Coordinates all testing activities and agents.
"""

from typing import Dict, List, Optional
from .base_agent import BaseAgent
from .agent_prompts import get_agent_prompt
from loguru import logger


class ProjectManagerAgent(BaseAgent):
    """Project Manager Agent that coordinates the entire testing workflow."""
    
    def __init__(self):
        super().__init__(
            name="Project Manager",
            role="Coordinate testing activities and manage team of agents",
            temperature=0.7
        )
        self.assigned_tasks = []
        self.completed_tasks = []
        self.pending_tasks = []
    
    def get_system_prompt(self) -> str:
        """Get system prompt for project manager."""
        return get_agent_prompt('project_manager')
    
    def execute_task(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Execute project management task.
        
        Args:
            task: Task dictionary
            context: Optional context
            
        Returns:
            Task result
        """
        task_type = task.get('type', 'general')
        
        if task_type == 'plan_project':
            return self.plan_project(task, context)
        elif task_type == 'assign_tasks':
            return self.assign_tasks(task, context)
        elif task_type == 'monitor_progress':
            return self.monitor_progress(task, context)
        elif task_type == 'handle_feedback':
            return self.handle_feedback(task, context)
        else:
            return self.general_coordination(task, context)
    
    def plan_project(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Create initial project plan.
        
        Args:
            task: Task parameters
            context: Context information
            
        Returns:
            Project plan
        """
        logger.info("Creating project plan...")
        
        prompt = f"""
Based on the provided code analysis and documentation, create a comprehensive project plan for testing.

Project Information:
{context}

Create a plan that includes:
1. Project overview and objectives
2. Team structure (which agents will work on what)
3. Phase-by-phase breakdown:
   - Phase 1: Analysis and Planning
   - Phase 2: Test Case Development
   - Phase 3: Automation Framework Development
   - Phase 4: Test Implementation
   - Phase 5: Documentation and Review
4. Timeline estimates for each phase
5. Dependencies between tasks
6. Risk assessment
7. Quality checkpoints

Format the output as a structured JSON with clear sections.
"""
        
        response = self.generate_response(prompt, context=context)
        
        # Parse and structure the response
        plan = {
            'project_plan': response,
            'status': 'planned',
            'created_by': self.name
        }
        
        self.log_activity("Project plan created", {'plan_length': len(response)})
        return plan
    
    def assign_tasks(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Assign tasks to appropriate agents.
        
        Args:
            task: Task parameters
            context: Context
            
        Returns:
            Task assignments
        """
        logger.info("Assigning tasks to agents...")
        
        current_phase = task.get('phase', 'planning')
        
        prompt = f"""
Current Project Phase: {current_phase}

Context:
{context}

Based on the current phase and project status, assign tasks to the following agents:

Available Agents:
1. Architect Agent - Test planning and strategy
2. Architect Critic Agent - Review test plans
3. Test Case Writer Agent - Write test cases
4. Test Critic Agent - Review test cases
5. Automation Architect Agent - Design automation framework
6. API Automation Agent - Implement API tests
7. DB Automation Agent - Implement database tests
8. CLI Automation Agent - Implement CLI tests
9. GUI Automation Agent - Implement GUI tests
10. Documentation Agent - Create documentation

For each agent, provide:
- Task assignment
- Priority (High/Medium/Low)
- Dependencies (which agents must complete their work first)
- Expected deliverables
- Estimated effort

Format as structured JSON.
"""
        
        response = self.generate_response(prompt, context=context)
        
        assignments = {
            'phase': current_phase,
            'assignments': response,
            'assigned_by': self.name
        }
        
        self.assigned_tasks.append(assignments)
        self.log_activity("Tasks assigned", {'phase': current_phase})
        
        return assignments
    
    def monitor_progress(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Monitor progress of all agents.
        
        Args:
            task: Task parameters
            context: Context with agent outputs
            
        Returns:
            Progress report
        """
        logger.info("Monitoring project progress...")
        
        prompt = f"""
Review the current project status and agent outputs:

{context}

Provide a progress report that includes:
1. Overall project completion percentage
2. Status of each agent's tasks (Not Started/In Progress/Completed/Blocked)
3. Completed deliverables
4. Pending deliverables
5. Blockers or issues
6. Next steps and priorities
7. Quality assessment of completed work
8. Recommendations for improvement

Format as structured JSON.
"""
        
        response = self.generate_response(prompt, context=context)
        
        progress_report = {
            'timestamp': self.get_timestamp(),
            'report': response,
            'generated_by': self.name
        }
        
        self.log_activity("Progress report generated")
        return progress_report
    
    def handle_feedback(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Handle user feedback and coordinate fixes.
        
        Args:
            task: Task with feedback
            context: Context
            
        Returns:
            Action plan for addressing feedback
        """
        logger.info("Handling user feedback...")
        
        feedback = task.get('feedback', '')
        
        prompt = f"""
User has provided the following feedback:

{feedback}

Current Project Context:
{context}

Analyze the feedback and create an action plan:
1. Categorize the feedback (bug fix/enhancement/correction)
2. Identify which agents need to rework their deliverables
3. Determine the scope of changes required
4. Create a prioritized action plan
5. Estimate the effort for implementing changes
6. Identify any dependencies or risks

Provide specific, actionable steps for each affected agent.

Format as structured JSON.
"""
        
        response = self.generate_response(prompt, context=context)
        
        action_plan = {
            'original_feedback': feedback,
            'action_plan': response,
            'status': 'pending',
            'created_by': self.name
        }
        
        self.log_activity("Feedback processed and action plan created")
        return action_plan
    
    def general_coordination(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Handle general coordination tasks.
        
        Args:
            task: Task parameters
            context: Context
            
        Returns:
            Coordination result
        """
        prompt = task.get('prompt', 'Coordinate the testing team activities')
        
        response = self.generate_response(prompt, context=context)
        
        return {
            'response': response,
            'task_type': 'coordination',
            'agent': self.name
        }
    
    def generate_final_report(self, all_results: Dict) -> Dict:
        """
        Generate final project report.
        
        Args:
            all_results: All agent results
            
        Returns:
            Final report
        """
        logger.info("Generating final project report...")
        
        prompt = f"""
Generate a comprehensive final project report based on all completed work:

Project Results:
{all_results}

The report should include:
1. Executive Summary
2. Project Objectives and Completion Status
3. Deliverables Summary:
   - Test Plan
   - Test Cases (count and coverage)
   - Automation Framework
   - Automated Tests (API, DB, CLI, GUI)
   - Documentation
4. Quality Metrics
5. Challenges and Solutions
6. Recommendations for Future Improvements
7. Conclusion

Format as a detailed markdown report.
"""
        
        context_str = str(all_results)
        response = self.generate_response(prompt, context=context_str)
        
        report = {
            'final_report': response,
            'generated_at': self.get_timestamp(),
            'project_status': 'completed',
            'generated_by': self.name
        }
        
        self.log_activity("Final project report generated")
        return report
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
