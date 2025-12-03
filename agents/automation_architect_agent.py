"""
Automation Architect Agent - Designs the complete test automation framework.
"""

from typing import Dict, Optional
from .base_agent import BaseAgent
from .agent_prompts import get_agent_prompt
from loguru import logger


class AutomationArchitectAgent(BaseAgent):
    """Automation Architect Agent that designs the test automation framework."""
    
    def __init__(self):
        super().__init__(
            name="Automation Architect",
            role="Design comprehensive test automation framework",
            temperature=0.7
        )
    
    def get_system_prompt(self) -> str:
        """Get system prompt for automation architect."""
        return get_agent_prompt('automation_architect')
    
    def execute_task(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Execute automation framework design task.
        
        Args:
            task: Task dictionary
            context: Optional context
            
        Returns:
            Task result
        """
        return self.design_framework(task, context)
    
    def design_framework(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Design complete automation framework.
        
        Args:
            task: Task parameters
            context: Test plan and code analysis context
            
        Returns:
            Framework design and code
        """
        logger.info("Designing automation framework...")
        
        prompt = f"""
Design a comprehensive test automation framework based on the following requirements:

CONTEXT:
{context}

Create a complete automation framework with the following:

1. FRAMEWORK STRUCTURE
Design the directory structure for:
```
automation_framework/
├── config/                  # Configuration files
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   └── environments.yaml   # Environment configs
├── backend/                # Backend testing
│   ├── __init__.py
│   ├── api/               # API tests
│   │   ├── __init__.py
│   │   ├── base_api.py    # Base API client
│   │   ├── endpoints/     # Endpoint-specific tests
│   │   └── fixtures.py
│   ├── database/          # Database tests
│   │   ├── __init__.py
│   │   ├── db_connection.py
│   │   ├── models/
│   │   └── fixtures.py
│   └── cli/               # CLI tests
│       ├── __init__.py
│       ├── cli_wrapper.py
│       └── fixtures.py
├── frontend/              # Frontend testing (Selenium + TypeScript)
│   ├── pages/            # Page Objects
│   │   ├── base_page.ts
│   │   └── [page_name]_page.ts
│   ├── components/       # Reusable components
│   ├── tests/           # GUI tests
│   └── fixtures/
├── integration/          # Integration tests
│   └── tests/
├── e2e/                 # End-to-end tests
│   └── scenarios/
├── utilities/           # Shared utilities
│   ├── __init__.py
│   ├── logger.py
│   ├── data_generator.py
│   ├── assertions.py
│   └── helpers.py
├── reports/            # Test reports output
├── test_data/          # Test data files
│   ├── api_test_data.json
│   ├── db_test_data.json
│   └── gui_test_data.json
├── requirements.txt    # Python dependencies
├── package.json       # Node.js dependencies
├── pytest.ini         # Pytest configuration
├── jest.config.js     # Jest configuration
└── README.md
```

2. CONFIGURATION MANAGEMENT (Python)
Create config.py that handles:
- Environment-specific configurations
- API base URLs
- Database connections
- Timeouts and retry logic
- Logging configuration
- Report paths

3. BASE CLASSES

a) Base API Client (Python):
```python
class BaseAPIClient:
    # HTTP client with common methods
    # Authentication handling
    # Request/Response logging
    # Retry logic
    # Error handling
```

b) Base Database Handler (Python):
```python
class BaseDBHandler:
    # Connection management
    # Query execution
    # Transaction handling
    # Data validation utilities
```

c) Base CLI Wrapper (Python):
```python
class CLIWrapper:
    # Command execution
    # Output parsing
    # Exit code validation
```

d) Base Page Object (TypeScript):
```typescript
class BasePage {{
    # WebDriver instance
    # Common page methods
    # Wait utilities
    # Screenshot capture
}}
```

4. UTILITIES

Create utilities for:
- Custom logger with different log levels
- Test data generator
- Custom assertions
- Report generation
- Screenshot capture
- Video recording
- File operations
- Date/Time utilities

5. FIXTURES AND SETUP

Pytest fixtures for:
- API client initialization
- Database connection setup/teardown
- Test data setup/cleanup
- Browser setup (for integration)

Jest/TypeScript setup:
- WebDriver initialization
- Browser configuration
- Test environment setup

6. REPORTING

Integration with:
- pytest-html for Python tests
- Allure for detailed reporting
- Custom JSON reports
- JUnit XML for CI/CD

7. CI/CD INTEGRATION

Configuration files for:
- GitHub Actions
- Jenkins
- GitLab CI

8. ERROR HANDLING & LOGGING

- Centralized error handling
- Structured logging
- Debug mode support
- Log rotation

Provide the complete framework code with:
- All configuration files
- Base classes with full implementation
- Utilities with complete code
- Requirements files
- README with setup instructions

Generate actual, executable Python and TypeScript code that can be copy-pasted and used.
"""
        
        response = self.generate_response(prompt, context=context)
        
        framework = {
            'framework_design': response,
            'version': '1.0',
            'languages': ['Python', 'TypeScript'],
            'created_by': self.name,
            'components': [
                'configuration',
                'backend_framework',
                'frontend_framework',
                'utilities',
                'reporting',
                'ci_cd'
            ]
        }
        
        self.log_activity("Automation framework designed")
        return framework
    
    def generate_config_files(self, context: Optional[str] = None) -> Dict:
        """Generate configuration files."""
        logger.info("Generating configuration files...")
        
        prompt = f"""
Generate the following configuration files:

1. config/config.py - Python configuration management
2. config/environments.yaml - Environment configurations
3. pytest.ini - Pytest configuration
4. requirements.txt - Python dependencies
5. package.json - Node.js/TypeScript dependencies
6. jest.config.js - Jest configuration for TypeScript tests
7. .env.example - Environment variables template

Include all necessary configurations for:
- Multiple environments (dev, staging, prod)
- API endpoints
- Database connections
- Browser configurations
- Timeout settings
- Retry logic
- Logging levels
- Report paths

Provide complete, working configuration files.
"""
        
        response = self.generate_response(prompt, context=context)
        
        return {
            'config_files': response,
            'created_by': self.name
        }
    
    def generate_base_classes(self, context: Optional[str] = None) -> Dict:
        """Generate base classes for framework."""
        logger.info("Generating base classes...")
        
        prompt = f"""
Generate complete implementations for these base classes:

1. backend/api/base_api.py - Base API client
2. backend/database/db_connection.py - Base database handler
3. backend/cli/cli_wrapper.py - Base CLI wrapper
4. frontend/pages/base_page.ts - Base page object (TypeScript)
5. utilities/logger.py - Custom logger
6. utilities/assertions.py - Custom assertions

Each class should be production-ready with:
- Complete implementation
- Error handling
- Logging
- Documentation
- Type hints
- Examples

Generate actual, executable code.
"""
        
        response = self.generate_response(prompt, context=context)
        
        return {
            'base_classes': response,
            'created_by': self.name
        }
