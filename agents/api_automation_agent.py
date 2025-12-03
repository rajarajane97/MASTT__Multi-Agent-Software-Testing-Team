"""
API Automation Agent - Generates Python-based API test automation code.
"""

from typing import Dict, List, Optional
from .base_agent import BaseAgent
from .agent_prompts import get_agent_prompt
from loguru import logger


class APIAutomationAgent(BaseAgent):
    """API Automation Agent that generates API test automation code."""
    
    def __init__(self):
        super().__init__(
            name="API Automation Agent",
            role="Generate Python-based API test automation",
            temperature=0.7
        )
    
    def get_system_prompt(self) -> str:
        """Get system prompt for API automation."""
        return get_agent_prompt('api_automation')
    
    def execute_task(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Execute API automation task.
        
        Args:
            task: Task dictionary
            context: Optional context
            
        Returns:
            Task result
        """
        test_cases = task.get('test_cases', [])
        framework = task.get('framework', {})
        
        return self.generate_api_automation(test_cases, framework, context)
    
    def generate_api_automation(self, 
                                test_cases: List[Dict], 
                                framework: Dict,
                                context: Optional[str] = None) -> Dict:
        """
        Generate API automation code.
        
        Args:
            test_cases: API test cases
            framework: Framework design
            context: Additional context
            
        Returns:
            Generated automation code
        """
        logger.info("Generating API automation code...")
        
        prompt = f"""
Generate complete Python-based API test automation code based on:

TEST CASES:
{test_cases}

FRAMEWORK DESIGN:
{framework}

CONTEXT:
{context}

Generate the following files with complete, executable code:

1. backend/api/base_api.py
```python
# Complete implementation of BaseAPIClient class
# Include:
# - HTTP methods (GET, POST, PUT, PATCH, DELETE)
# - Authentication handling (Bearer token, Basic auth, API key)
# - Request/Response logging
# - Retry logic with exponential backoff
# - Error handling
# - Request/Response validation
# - Session management

import requests
from typing import Dict, Optional, Any
import logging
from config.config import Config

class BaseAPIClient:
    def __init__(self, base_url: str, auth_token: Optional[str] = None):
        # Implementation here
        pass
    
    def get(self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None):
        # Implementation
        pass
    
    # ... more methods
```

2. backend/api/endpoints/user_api.py
```python
# Example API endpoint implementation
# Create similar files for each endpoint category

from backend.api.base_api import BaseAPIClient

class UserAPI(BaseAPIClient):
    def create_user(self, user_data: Dict):
        # Implementation
        pass
    
    def get_user(self, user_id: str):
        # Implementation
        pass
    
    # ... more methods
```

3. backend/api/tests/test_api.py
```python
# Complete test file implementing ALL test cases
# Use pytest framework
# Include:
# - Fixtures for setup/teardown
# - Parameterized tests
# - Assertions
# - Test data
# - Error handling
# - Logging

import pytest
from backend.api.endpoints.user_api import UserAPI

@pytest.fixture
def api_client():
    # Setup
    yield
    # Teardown

class TestUserAPI:
    def test_create_user_success(self, api_client):
        # Test implementation from test cases
        pass
    
    def test_create_user_invalid_data(self, api_client):
        # Test implementation
        pass
    
    # ... implement ALL test cases
```

4. backend/api/fixtures.py
```python
# Pytest fixtures for API tests
# Include:
# - API client fixture
# - Test data fixtures
# - Setup/Teardown fixtures
# - Authentication fixtures

import pytest

@pytest.fixture(scope="session")
def api_client():
    # Implementation
    pass
```

5. backend/api/test_data/api_test_data.json
```json
{
  "valid_user": {
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!"
  },
  "invalid_user": {
    "username": "",
    "email": "invalid-email"
  }
}
```

6. backend/api/utilities/validators.py
```python
# API response validators
# JSON schema validation
# Status code validators
# Header validators

from jsonschema import validate

def validate_user_response(response_data: Dict):
    schema = {{
        "type": "object",
        "properties": {{
            "id": {{"type": "string"}},
            "username": {{"type": "string"}},
            "email": {{"type": "string", "format": "email"}}
        }},
        "required": ["id", "username", "email"]
    }}
    validate(instance=response_data, schema=schema)
```

Generate COMPLETE, PRODUCTION-READY code for all files. Each file should:
- Be fully implemented (no TODOs or placeholders)
- Include proper error handling
- Have logging
- Include docstrings
- Be executable immediately
- Follow Python best practices
- Include type hints

Make the code robust enough to handle:
- Network errors
- Timeout scenarios
- Authentication failures
- Invalid responses
- Rate limiting
"""
        
        response = self.generate_response(prompt, context=context)
        
        automation_code = {
            'api_automation_code': response,
            'language': 'Python',
            'framework': 'pytest + requests',
            'test_cases_automated': len(test_cases) if isinstance(test_cases, list) else 'all',
            'created_by': self.name,
            'files_generated': [
                'backend/api/base_api.py',
                'backend/api/endpoints/*.py',
                'backend/api/tests/test_api.py',
                'backend/api/fixtures.py',
                'backend/api/test_data/api_test_data.json',
                'backend/api/utilities/validators.py'
            ]
        }
        
        self.log_activity("API automation code generated", {
            'test_cases': automation_code['test_cases_automated']
        })
        
        return automation_code
    
    def generate_api_client_library(self, endpoints: List[str], context: Optional[str] = None) -> str:
        """Generate API client library for specific endpoints."""
        logger.info("Generating API client library...")
        
        prompt = f"""
Generate a complete Python API client library for these endpoints:

{endpoints}

The library should:
- Be reusable and well-structured
- Handle all HTTP methods
- Include authentication
- Have proper error handling
- Be well-documented
- Include usage examples

Generate complete, production-ready code.
"""
        
        return self.generate_response(prompt, context=context)
