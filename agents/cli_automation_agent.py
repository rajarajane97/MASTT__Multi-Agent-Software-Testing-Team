"""
CLI Automation Agent - Generates Python-based CLI test automation code.
"""

from typing import Dict, List, Optional
from .base_agent import BaseAgent
from .agent_prompts import get_agent_prompt
from loguru import logger


class CLIAutomationAgent(BaseAgent):
    """CLI Automation Agent that generates CLI test automation code."""
    
    def __init__(self):
        super().__init__(
            name="CLI Automation Agent",
            role="Generate Python-based CLI test automation",
            temperature=0.7
        )
    
    def get_system_prompt(self) -> str:
        """Get system prompt for CLI automation."""
        return get_agent_prompt('cli_automation')
    
    def execute_task(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Execute CLI automation task.
        
        Args:
            task: Task dictionary
            context: Optional context
            
        Returns:
            Task result
        """
        test_cases = task.get('test_cases', [])
        framework = task.get('framework', {})
        
        return self.generate_cli_automation(test_cases, framework, context)
    
    def generate_cli_automation(self,
                                test_cases: List[Dict],
                                framework: Dict,
                                context: Optional[str] = None) -> Dict:
        """
        Generate CLI automation code.
        
        Args:
            test_cases: CLI test cases
            framework: Framework design
            context: Additional context
            
        Returns:
            Generated automation code
        """
        logger.info("Generating CLI automation code...")
        
        prompt = f"""
Generate complete Python-based CLI test automation code based on:

TEST CASES:
{test_cases}

FRAMEWORK DESIGN:
{framework}

CONTEXT:
{context}

Generate the following files with complete, executable code:

1. backend/cli/cli_wrapper.py
```python
# Complete CLI wrapper implementation
# Include:
# - Command execution via subprocess
# - Output capture (stdout, stderr)
# - Exit code validation
# - Timeout handling
# - Environment variable management
# - Working directory management
# - Shell command support

import subprocess
from typing import Optional, Dict, List, Tuple
import logging
import shlex

class CLIWrapper:
    def __init__(self, cli_path: str, default_timeout: int = 30):
        self.cli_path = cli_path
        self.default_timeout = default_timeout
        self.logger = logging.getLogger(__name__)
    
    def execute_command(self, 
                       args: List[str],
                       input_data: Optional[str] = None,
                       env: Optional[Dict] = None,
                       timeout: Optional[int] = None,
                       cwd: Optional[str] = None) -> Tuple[int, str, str]:
        \"\"\"
        Execute CLI command.
        
        Returns:
            Tuple of (exit_code, stdout, stderr)
        \"\"\"
        # Implementation
        pass
    
    def execute_with_input(self, args: List[str], input_data: str):
        # Implementation
        pass
    
    def parse_output(self, output: str, format: str = 'text'):
        # Parse output (text, JSON, XML)
        pass
```

2. backend/cli/parsers/output_parser.py
```python
# Output parsing utilities
# Support different output formats

import json
import xml.etree.ElementTree as ET
from typing import Any, Dict

class OutputParser:
    @staticmethod
    def parse_json(output: str) -> Dict:
        # Implementation
        pass
    
    @staticmethod
    def parse_table(output: str) -> List[List[str]]:
        # Parse tabular output
        pass
    
    @staticmethod
    def parse_key_value(output: str) -> Dict:
        # Parse key: value format
        pass
```

3. backend/cli/tests/test_cli.py
```python
# Complete test file implementing ALL CLI test cases
# Use pytest framework

import pytest
from backend.cli.cli_wrapper import CLIWrapper
from config.config import Config

@pytest.fixture
def cli_wrapper():
    return CLIWrapper(Config.CLI_PATH)

class TestCLICommands:
    def test_help_command(self, cli_wrapper):
        # Test implementation
        exit_code, stdout, stderr = cli_wrapper.execute_command(['--help'])
        assert exit_code == 0
        assert 'usage' in stdout.lower()
    
    def test_version_command(self, cli_wrapper):
        # Test implementation
        pass
    
    def test_command_with_args(self, cli_wrapper):
        # Test implementation
        pass
    
    def test_invalid_command(self, cli_wrapper):
        # Test implementation
        exit_code, stdout, stderr = cli_wrapper.execute_command(['invalid'])
        assert exit_code != 0
        assert stderr != ''
    
    def test_command_with_input(self, cli_wrapper):
        # Test with stdin input
        pass
    
    def test_command_timeout(self, cli_wrapper):
        # Test timeout handling
        pass
    
    # ... implement ALL test cases
```

4. backend/cli/fixtures.py
```python
# CLI testing fixtures

import pytest
import tempfile
import os
from backend.cli.cli_wrapper import CLIWrapper

@pytest.fixture
def cli_wrapper():
    wrapper = CLIWrapper('/path/to/cli')
    yield wrapper

@pytest.fixture
def temp_workspace():
    # Create temporary directory for CLI operations
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def sample_input_file():
    # Create sample input file
    pass
```

5. backend/cli/test_data/cli_test_data.json
```json
{{
  "valid_commands": [
    {{
      "command": ["list", "--all"],
      "expected_exit_code": 0,
      "expected_output_contains": ["total", "items"]
    }},
    {{
      "command": ["create", "--name", "test"],
      "expected_exit_code": 0
    }}
  ],
  "invalid_commands": [
    {{
      "command": ["invalid"],
      "expected_exit_code": 1,
      "expected_error_contains": ["unknown command"]
    }}
  ],
  "test_inputs": {{
    "config_file": "config.yaml",
    "data_file": "data.json"
  }}
}}
```

6. backend/cli/utilities/command_builder.py
```python
# CLI command builder utility
# Build complex commands programmatically

class CommandBuilder:
    def __init__(self, base_command: str):
        self.base_command = base_command
        self.args = []
        self.flags = {{}}
    
    def add_arg(self, arg: str):
        self.args.append(arg)
        return self
    
    def add_flag(self, flag: str, value: Optional[str] = None):
        self.flags[flag] = value
        return self
    
    def build(self) -> List[str]:
        # Build complete command
        pass
```

7. backend/cli/utilities/validators.py
```python
# CLI output validators

import re

def validate_exit_code(actual: int, expected: int) -> bool:
    return actual == expected

def validate_output_contains(output: str, expected_text: str) -> bool:
    return expected_text in output

def validate_output_matches(output: str, pattern: str) -> bool:
    return bool(re.search(pattern, output))

def validate_json_output(output: str) -> bool:
    import json
    try:
        json.loads(output)
        return True
    except:
        return False
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
- Process timeouts
- Command failures
- Invalid output formats
- Permission issues
- Missing dependencies
- Different shell environments
"""
        
        response = self.generate_response(prompt, context=context)
        
        automation_code = {
            'cli_automation_code': response,
            'language': 'Python',
            'framework': 'pytest + subprocess',
            'test_cases_automated': len(test_cases) if isinstance(test_cases, list) else 'all',
            'created_by': self.name,
            'files_generated': [
                'backend/cli/cli_wrapper.py',
                'backend/cli/parsers/output_parser.py',
                'backend/cli/tests/test_cli.py',
                'backend/cli/fixtures.py',
                'backend/cli/test_data/cli_test_data.json',
                'backend/cli/utilities/command_builder.py',
                'backend/cli/utilities/validators.py'
            ]
        }
        
        self.log_activity("CLI automation code generated", {
            'test_cases': automation_code['test_cases_automated']
        })
        
        return automation_code
