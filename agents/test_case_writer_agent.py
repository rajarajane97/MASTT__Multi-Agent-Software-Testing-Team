"""
Test Case Writer Agent - Creates detailed test cases.
"""

from typing import Dict, List, Optional
from .base_agent import BaseAgent
from .agent_prompts import get_agent_prompt
from loguru import logger
import json


class TestCaseWriterAgent(BaseAgent):
    """Test Case Writer Agent that creates comprehensive test cases."""
    
    def __init__(self):
        super().__init__(
            name="Test Case Writer",
            role="Write detailed and comprehensive test cases",
            temperature=0.7
        )
    
    def get_system_prompt(self) -> str:
        """Get system prompt for test case writer."""
        return get_agent_prompt('test_case_writer')
    
    def execute_task(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Execute test case writing task.
        
        Args:
            task: Task dictionary
            context: Optional context
            
        Returns:
            Task result
        """
        task_type = task.get('type', 'write_all_test_cases')
        category = task.get('category', 'all')
        
        if task_type == 'write_all_test_cases':
            return self.write_all_test_cases(context)
        elif task_type == 'write_category_test_cases':
            return self.write_category_test_cases(category, context)
        else:
            return self.write_all_test_cases(context)
    
    def write_all_test_cases(self, context: Optional[str] = None) -> Dict:
        """
        Write all test cases for the project.
        
        Args:
            context: Test plan and code analysis context
            
        Returns:
            All test cases
        """
        logger.info("Writing all test cases...")
        
        # Write test cases for each category
        categories = ['api', 'database', 'cli', 'gui', 'integration', 'e2e']
        
        all_test_cases = {
            'api_test_cases': [],
            'database_test_cases': [],
            'cli_test_cases': [],
            'gui_test_cases': [],
            'integration_test_cases': [],
            'e2e_test_cases': []
        }
        
        for category in categories:
            logger.info(f"Writing {category} test cases...")
            result = self.write_category_test_cases(category, context)
            all_test_cases[f'{category}_test_cases'] = result.get('test_cases', [])
        
        # Generate summary
        total_count = sum(len(tc) for tc in all_test_cases.values())
        
        summary = {
            'total_test_cases': total_count,
            'breakdown': {k: len(v) for k, v in all_test_cases.items()},
            'created_by': self.name
        }
        
        all_test_cases['summary'] = summary
        
        self.log_activity("All test cases written", {'total': total_count})
        return all_test_cases
    
    def write_category_test_cases(self, category: str, context: Optional[str] = None) -> Dict:
        """
        Write test cases for a specific category.
        
        Args:
            category: Test category (api, database, cli, gui, integration, e2e)
            context: Context
            
        Returns:
            Test cases for category
        """
        logger.info(f"Writing {category} test cases...")
        
        category_prompts = {
            'api': self._get_api_test_case_prompt(),
            'database': self._get_database_test_case_prompt(),
            'cli': self._get_cli_test_case_prompt(),
            'gui': self._get_gui_test_case_prompt(),
            'integration': self._get_integration_test_case_prompt(),
            'e2e': self._get_e2e_test_case_prompt()
        }
        
        specific_prompt = category_prompts.get(category, '')
        
        prompt = f"""
Based on the test plan and code analysis, write comprehensive test cases for {category.upper()} testing.

Context:
{context}

{specific_prompt}

For each test case, provide:
- Test Case ID (format: TC_{category.upper()}_001, TC_{category.upper()}_002, etc.)
- Title (clear, descriptive)
- Category: {category}
- Priority: Critical/High/Medium/Low
- Preconditions (what must be true before test)
- Test Steps (numbered, clear, executable)
- Test Data (specific data to use)
- Expected Results (clear, verifiable)
- Postconditions (cleanup, state after test)
- Tags (for organization)

Generate at least 15-20 test cases covering:
- Happy path scenarios
- Edge cases
- Error scenarios
- Boundary conditions
- Security scenarios (if applicable)

Format as JSON array of test case objects for easy parsing and automation.
"""
        
        response = self.generate_response(prompt, context=context)
        
        # Try to parse JSON from response
        test_cases = self._extract_test_cases_from_response(response, category)
        
        result = {
            'category': category,
            'test_cases': test_cases,
            'count': len(test_cases),
            'created_by': self.name
        }
        
        self.log_activity(f"{category} test cases written", {'count': len(test_cases)})
        return result
    
    def _extract_test_cases_from_response(self, response: str, category: str) -> List[Dict]:
        """Extract test cases from response text."""
        try:
            # Try to parse as JSON
            import re
            
            # Find JSON array in response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                test_cases = json.loads(json_match.group(0))
                return test_cases
        except:
            pass
        
        # If JSON parsing fails, return response as single item
        return [{
            'test_case_id': f'TC_{category.upper()}_001',
            'raw_content': response,
            'note': 'Test cases need to be parsed manually'
        }]
    
    def _get_api_test_case_prompt(self) -> str:
        """Get API test case specific prompt."""
        return """
Write API test cases covering:
- GET requests (valid IDs, invalid IDs, filtering, pagination)
- POST requests (valid data, invalid data, missing fields)
- PUT/PATCH requests (full updates, partial updates, invalid updates)
- DELETE requests (valid deletes, cascade deletes, invalid deletes)
- Authentication scenarios (valid token, invalid token, expired token)
- Authorization scenarios (access control, permissions)
- Error responses (400, 401, 403, 404, 500)
- Header validation
- Request/Response schema validation
"""
    
    def _get_database_test_case_prompt(self) -> str:
        """Get database test case specific prompt."""
        return """
Write database test cases covering:
- CRUD operations on each table
- Data integrity constraints (foreign keys, unique constraints)
- Transaction handling
- Concurrent access scenarios
- Data validation rules
- Cascade operations
- Index performance
- Stored procedures (if any)
- Triggers (if any)
- Data migration scenarios
"""
    
    def _get_cli_test_case_prompt(self) -> str:
        """Get CLI test case specific prompt."""
        return """
Write CLI test cases covering:
- Valid command execution
- Invalid command handling
- Argument validation
- Flag combinations
- Help text display
- Error messages
- Exit codes
- Input/Output redirection
- Environment variable handling
- Configuration file handling
"""
    
    def _get_gui_test_case_prompt(self) -> str:
        """Get GUI test case specific prompt."""
        return """
Write GUI test cases covering:
- Page navigation
- Form submissions (valid and invalid)
- Button clicks and interactions
- Input field validations
- Dropdown and select interactions
- Checkbox and radio button handling
- Error message display
- Success message display
- Modal dialogs
- Responsive behavior
- Cross-browser scenarios
- Accessibility features
"""
    
    def _get_integration_test_case_prompt(self) -> str:
        """Get integration test case specific prompt."""
        return """
Write integration test cases covering:
- Frontend-Backend integration
- API-Database integration
- Third-party service integration
- Authentication flow integration
- Data flow across components
- Event handling across system
- Error propagation
- Transaction handling across services
"""
    
    def _get_e2e_test_case_prompt(self) -> str:
        """Get E2E test case specific prompt."""
        return """
Write end-to-end test cases covering:
- Complete user journeys (from login to task completion)
- Critical business workflows
- Multi-step processes
- Cross-component interactions
- User scenarios from start to finish
- Happy path end-to-end flows
- Error recovery scenarios
- Real-world usage patterns
"""
    
    def revise_test_cases(self, original_cases: List[Dict], feedback: str, context: Optional[str] = None) -> Dict:
        """
        Revise test cases based on feedback.
        
        Args:
            original_cases: Original test cases
            feedback: Feedback from critic
            context: Additional context
            
        Returns:
            Revised test cases
        """
        logger.info("Revising test cases based on feedback...")
        
        prompt = f"""
Original Test Cases:
{json.dumps(original_cases, indent=2)}

Feedback from Test Critic:
{feedback}

Revise the test cases by:
1. Addressing all feedback points
2. Adding missing scenarios
3. Improving clarity
4. Fixing ambiguities
5. Enhancing test data
6. Improving expected results

Provide the complete revised test cases in the same JSON format.
"""
        
        response = self.generate_response(prompt, context=context)
        
        revised_cases = self._extract_test_cases_from_response(response, 'revised')
        
        result = {
            'revised_test_cases': revised_cases,
            'count': len(revised_cases),
            'changes': 'Incorporated feedback from test critic',
            'created_by': self.name
        }
        
        self.log_activity("Test cases revised")
        return result
