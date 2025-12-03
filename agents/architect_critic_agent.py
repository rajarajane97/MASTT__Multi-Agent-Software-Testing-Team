"""
Architect Critic Agent - Reviews test plans and provides feedback.
"""

from typing import Dict, Optional
from .base_agent import BaseAgent
from .agent_prompts import get_agent_prompt
from loguru import logger


class ArchitectCriticAgent(BaseAgent):
    """Architect Critic Agent that reviews and critiques test plans."""
    
    def __init__(self):
        super().__init__(
            name="Test Architect Critic",
            role="Review test plans and provide constructive feedback",
            temperature=0.6
        )
    
    def get_system_prompt(self) -> str:
        """Get system prompt for architect critic."""
        return get_agent_prompt('architect_critic')
    
    def execute_task(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Execute test plan review task.
        
        Args:
            task: Task dictionary
            context: Optional context
            
        Returns:
            Task result
        """
        test_plan = task.get('test_plan', '')
        return self.review_test_plan(test_plan, context)
    
    def review_test_plan(self, test_plan: str, context: Optional[str] = None) -> Dict:
        """
        Review test plan and provide detailed feedback.
        
        Args:
            test_plan: Test plan to review
            context: Additional context
            
        Returns:
            Review feedback
        """
        logger.info("Reviewing test plan...")
        
        prompt = f"""
Review the following test plan critically and provide comprehensive feedback:

TEST PLAN TO REVIEW:
{test_plan}

ADDITIONAL CONTEXT:
{context}

Provide a detailed review covering:

1. COMPLETENESS ASSESSMENT
   - Are all sections present and adequately detailed?
   - Missing components or areas
   - Gaps in coverage

2. TECHNICAL ACCURACY
   - Are technical approaches sound?
   - Are best practices followed?
   - Are tools and frameworks appropriate?
   - Technology-specific concerns

3. BACKEND TESTING REVIEW
   - API testing strategy evaluation
   - Database testing approach
   - CLI testing coverage
   - Missing backend scenarios

4. FRONTEND TESTING REVIEW
   - GUI testing strategy evaluation
   - Component testing approach
   - Cross-browser considerations
   - Accessibility considerations

5. INTEGRATION & E2E TESTING
   - Integration points coverage
   - End-to-end scenario adequacy
   - Critical user journey coverage

6. NON-FUNCTIONAL TESTING
   - Performance testing adequacy
   - Security testing coverage
   - Scalability considerations

7. RISK ANALYSIS
   - Are high-risk areas identified?
   - Mitigation strategies adequate?
   - Missing risks

8. TIMELINE & RESOURCES
   - Realistic estimates?
   - Resource allocation appropriate?
   - Dependencies clearly defined?

9. CLARITY & ORGANIZATION
   - Document structure and flow
   - Clarity of instructions
   - Readability and usability

10. PRIORITIZED RECOMMENDATIONS
    CRITICAL (Must Fix):
    - List critical issues that must be addressed
    
    IMPORTANT (Should Fix):
    - List important improvements
    
    NICE TO HAVE (Could Improve):
    - List enhancement suggestions

11. STRENGTHS
    - What is done well in this plan?

12. OVERALL ASSESSMENT
    - Summary of review
    - Approval status (Approved/Needs Revision/Rejected)
    - Key action items

Format the feedback clearly with specific examples and actionable recommendations.
"""
        
        response = self.generate_response(prompt, context=context)
        
        review = {
            'review_feedback': response,
            'reviewer': self.name,
            'review_status': self.determine_approval_status(response),
            'critical_issues_count': self.count_critical_issues(response),
            'recommendation': 'See detailed feedback for improvements'
        }
        
        self.log_activity("Test plan review completed", {
            'status': review['review_status'],
            'critical_issues': review['critical_issues_count']
        })
        
        return review
    
    def determine_approval_status(self, review_text: str) -> str:
        """
        Determine approval status from review text.
        
        Args:
            review_text: Review feedback text
            
        Returns:
            Status: approved, needs_revision, or rejected
        """
        review_lower = review_text.lower()
        
        if 'rejected' in review_lower or 'major issues' in review_lower:
            return 'rejected'
        elif 'needs revision' in review_lower or 'critical' in review_lower:
            return 'needs_revision'
        elif 'approved' in review_lower:
            return 'approved'
        else:
            return 'needs_revision'
    
    def count_critical_issues(self, review_text: str) -> int:
        """
        Count critical issues in review.
        
        Args:
            review_text: Review text
            
        Returns:
            Count of critical issues
        """
        import re
        
        # Try to find CRITICAL section and count items
        critical_section = re.search(
            r'CRITICAL.*?(?=IMPORTANT|NICE TO HAVE|STRENGTHS|$)',
            review_text,
            re.DOTALL | re.IGNORECASE
        )
        
        if critical_section:
            # Count bullet points or numbered items
            items = re.findall(r'[-*•\d+\.]', critical_section.group(0))
            return max(len(items) - 1, 0)  # Subtract 1 for the header
        
        return 0
    
    def quick_validation(self, test_plan: str) -> Dict:
        """
        Quick validation of test plan structure.
        
        Args:
            test_plan: Test plan text
            
        Returns:
            Validation results
        """
        logger.info("Performing quick validation...")
        
        required_sections = [
            'overview',
            'scope',
            'approach',
            'strategy',
            'backend',
            'frontend',
            'integration',
            'test environment',
            'timeline',
            'deliverables'
        ]
        
        test_plan_lower = test_plan.lower()
        
        missing_sections = []
        present_sections = []
        
        for section in required_sections:
            if section in test_plan_lower:
                present_sections.append(section)
            else:
                missing_sections.append(section)
        
        validation = {
            'is_valid': len(missing_sections) == 0,
            'present_sections': present_sections,
            'missing_sections': missing_sections,
            'completeness_score': len(present_sections) / len(required_sections) * 100
        }
        
        return validation
