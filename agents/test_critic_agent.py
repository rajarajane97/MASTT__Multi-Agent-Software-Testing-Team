"""
Test Critic Agent - Reviews test cases and provides feedback.
"""

from typing import Dict, List, Optional
from .base_agent import BaseAgent
from .agent_prompts import get_agent_prompt
from loguru import logger
import json


class TestCriticAgent(BaseAgent):
    """Test Critic Agent that reviews and critiques test cases."""
    
    def __init__(self):
        super().__init__(
            name="Test Critic",
            role="Review test cases and provide constructive feedback",
            temperature=0.6
        )
    
    def get_system_prompt(self) -> str:
        """Get system prompt for test critic."""
        return get_agent_prompt('test_critic')
    
    def execute_task(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Execute test case review task.
        
        Args:
            task: Task dictionary
            context: Optional context
            
        Returns:
            Task result
        """
        test_cases = task.get('test_cases', [])
        return self.review_test_cases(test_cases, context)
    
    def review_test_cases(self, test_cases: List[Dict], context: Optional[str] = None) -> Dict:
        """
        Review test cases and provide detailed feedback.
        
        Args:
            test_cases: Test cases to review
            context: Additional context
            
        Returns:
            Review feedback
        """
        logger.info(f"Reviewing {len(test_cases)} test cases...")
        
        # Convert test cases to string for prompt
        test_cases_str = json.dumps(test_cases, indent=2) if isinstance(test_cases, list) else str(test_cases)
        
        prompt = f"""
Review the following test cases and provide comprehensive feedback:

TEST CASES TO REVIEW:
{test_cases_str}

CONTEXT:
{context}

Provide a detailed review covering:

1. COMPLETENESS
   - Are all scenarios covered (happy path, edge cases, error cases)?
   - Missing test scenarios
   - Coverage gaps
   - Boundary conditions coverage

2. CLARITY & EXECUTABILITY
   - Are test steps clear and unambiguous?
   - Can someone execute these without confusion?
   - Are preconditions clearly stated?
   - Are expected results verifiable?

3. TEST DATA QUALITY
   - Is test data specific and realistic?
   - Are edge cases covered in test data?
   - Is invalid data included for negative testing?

4. EXPECTED RESULTS
   - Are expected results specific and measurable?
   - Can results be verified automatically?
   - Are error messages and codes specified?

5. STRUCTURE & ORGANIZATION
   - Logical grouping and categorization
   - Consistent formatting
   - Appropriate priority assignments
   - Clear test case IDs

6. AUTOMATION READINESS
   - Can these test cases be automated easily?
   - Are steps atomic and clear?
   - Dependencies clearly stated?

7. CATEGORY-SPECIFIC REVIEW
   For API tests:
   - HTTP methods correct?
   - Status codes specified?
   - Request/Response formats clear?
   
   For Database tests:
   - SQL operations clear?
   - Data integrity checks included?
   
   For GUI tests:
   - Element locators mentioned?
   - User actions clear?
   
   For Integration/E2E tests:
   - Cross-component flows clear?
   - Data flow validated?

8. ISSUES FOUND
   CRITICAL:
   - List critical issues (missing scenarios, unclear steps, wrong expected results)
   
   IMPORTANT:
   - List important improvements needed
   
   MINOR:
   - List minor enhancements

9. MISSING SCENARIOS
   - List specific test scenarios that should be added

10. RECOMMENDATIONS
    - Specific, actionable recommendations for improvement
    - Examples of improved test cases

11. STRENGTHS
    - What is done well in these test cases?

12. OVERALL ASSESSMENT
    - Quality score (1-10)
    - Approval status (Approved/Needs Revision/Rejected)
    - Summary and key action items

Provide specific feedback with examples where helpful.
"""
        
        response = self.generate_response(prompt, context=context)
        
        review = {
            'review_feedback': response,
            'reviewer': self.name,
            'test_cases_reviewed': len(test_cases) if isinstance(test_cases, list) else 1,
            'review_status': self.determine_approval_status(response),
            'quality_score': self.extract_quality_score(response)
        }
        
        self.log_activity("Test cases review completed", {
            'count': review['test_cases_reviewed'],
            'status': review['review_status']
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
        
        if 'rejected' in review_lower:
            return 'rejected'
        elif 'needs revision' in review_lower or 'critical' in review_lower:
            return 'needs_revision'
        elif 'approved' in review_lower:
            return 'approved'
        else:
            return 'needs_revision'
    
    def extract_quality_score(self, review_text: str) -> Optional[int]:
        """
        Extract quality score from review text.
        
        Args:
            review_text: Review text
            
        Returns:
            Quality score or None
        """
        import re
        
        # Look for quality score pattern
        score_patterns = [
            r'quality score[:\s]+(\d+)',
            r'score[:\s]+(\d+)/10',
            r'rating[:\s]+(\d+)'
        ]
        
        for pattern in score_patterns:
            match = re.search(pattern, review_text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def quick_validation(self, test_case: Dict) -> Dict:
        """
        Quick validation of test case structure.
        
        Args:
            test_case: Test case dictionary
            
        Returns:
            Validation results
        """
        required_fields = [
            'test_case_id',
            'title',
            'category',
            'priority',
            'test_steps',
            'expected_results'
        ]
        
        missing_fields = []
        present_fields = []
        
        for field in required_fields:
            if field in test_case and test_case[field]:
                present_fields.append(field)
            else:
                missing_fields.append(field)
        
        # Check if test steps are detailed enough
        steps_quality = 'good'
        if 'test_steps' in test_case:
            steps = test_case['test_steps']
            if isinstance(steps, str):
                step_count = len(steps.split('\n'))
            elif isinstance(steps, list):
                step_count = len(steps)
            else:
                step_count = 0
            
            if step_count < 3:
                steps_quality = 'too_brief'
        
        validation = {
            'is_valid': len(missing_fields) == 0,
            'present_fields': present_fields,
            'missing_fields': missing_fields,
            'completeness_score': len(present_fields) / len(required_fields) * 100,
            'steps_quality': steps_quality
        }
        
        return validation
    
    def compare_test_cases(self, original: List[Dict], revised: List[Dict]) -> Dict:
        """
        Compare original and revised test cases.
        
        Args:
            original: Original test cases
            revised: Revised test cases
            
        Returns:
            Comparison report
        """
        logger.info("Comparing original and revised test cases...")
        
        comparison = {
            'original_count': len(original),
            'revised_count': len(revised),
            'added_count': max(0, len(revised) - len(original)),
            'improvements': []
        }
        
        # Simple comparison - in real scenario, would do more detailed analysis
        if len(revised) > len(original):
            comparison['improvements'].append('Added more test cases')
        
        return comparison
