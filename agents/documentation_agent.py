"""
Documentation Agent - Creates comprehensive documentation for the automation framework.
"""

from typing import Dict, Optional
from .base_agent import BaseAgent
from .agent_prompts import get_agent_prompt
from loguru import logger


class DocumentationAgent(BaseAgent):
    """Documentation Agent that creates all necessary documentation."""
    
    def __init__(self):
        super().__init__(
            name="Documentation Agent",
            role="Create comprehensive documentation for automation framework",
            temperature=0.7
        )
    
    def get_system_prompt(self) -> str:
        """Get system prompt for documentation agent."""
        return get_agent_prompt('documentation')
    
    def execute_task(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Execute documentation task.
        
        Args:
            task: Task dictionary
            context: Optional context
            
        Returns:
            Task result
        """
        doc_type = task.get('type', 'all')
        
        if doc_type == 'all':
            return self.generate_all_documentation(context)
        elif doc_type == 'readme':
            return {'readme': self.generate_readme(context)}
        elif doc_type == 'installation':
            return {'installation': self.generate_installation_guide(context)}
        elif doc_type == 'architecture':
            return {'architecture': self.generate_architecture_doc(context)}
        else:
            return self.generate_all_documentation(context)
    
    def generate_all_documentation(self, context: Optional[str] = None) -> Dict:
        """
        Generate all documentation.
        
        Args:
            context: All project information
            
        Returns:
            All documentation
        """
        logger.info("Generating all documentation...")
        
        documentation = {
            'README.md': self.generate_readme(context),
            'INSTALLATION.md': self.generate_installation_guide(context),
            'ARCHITECTURE.md': self.generate_architecture_doc(context),
            'USAGE.md': self.generate_usage_guide(context),
            'DEBUGGING.md': self.generate_debugging_guide(context),
            'CONTRIBUTING.md': self.generate_contributing_guide(context),
            'API_REFERENCE.md': self.generate_api_reference(context),
            'CHANGELOG.md': self.generate_changelog(context)
        }
        
        self.log_activity("All documentation generated", {
            'documents': len(documentation)
        })
        
        return documentation
    
    def generate_readme(self, context: Optional[str] = None) -> str:
        """Generate README.md."""
        logger.info("Generating README.md...")
        
        prompt = f"""
Generate a comprehensive README.md for the test automation framework.

CONTEXT:
{context}

The README should include:

# Test Automation Framework

## Overview
Brief description of the framework and its purpose

## Features
- Backend testing (API, Database, CLI)
- Frontend testing (GUI with Selenium)
- Integration and E2E testing
- Comprehensive reporting
- CI/CD ready
- List all key features

## Project Structure
```
automation_framework/
├── config/
├── backend/
│   ├── api/
│   ├── database/
│   └── cli/
├── frontend/
│   ├── pages/
│   ├── tests/
│   └── utilities/
├── integration/
├── e2e/
├── utilities/
└── reports/
```

## Technology Stack
- Python 3.11+
- TypeScript
- Selenium WebDriver
- pytest
- Jest
- And other technologies used

## Quick Start
```bash
# Clone repository
git clone [repository-url]

# Setup
./setup.sh

# Run tests
pytest backend/
npm test
```

## Prerequisites
List all prerequisites

## Installation
See INSTALLATION.md for detailed instructions

## Usage
See USAGE.md for detailed usage guide

## Running Tests

### Backend Tests
```bash
# API tests
pytest backend/api/tests/

# Database tests
pytest backend/database/tests/

# CLI tests
pytest backend/cli/tests/
```

### Frontend Tests
```bash
# GUI tests
npm test
```

### Integration Tests
```bash
pytest integration/
```

### E2E Tests
```bash
pytest e2e/
```

## Configuration
How to configure the framework

## Reporting
Where to find test reports and how to generate them

## CI/CD Integration
Brief on CI/CD setup

## Documentation
Links to other documentation files

## Contributing
See CONTRIBUTING.md

## License
License information

## Support
How to get help

## Authors
Project team information

Format as a professional, well-structured markdown document.
"""
        
        return self.generate_response(prompt, context=context)
    
    def generate_installation_guide(self, context: Optional[str] = None) -> str:
        """Generate installation guide."""
        logger.info("Generating INSTALLATION.md...")
        
        prompt = f"""
Generate a comprehensive installation guide (INSTALLATION.md).

CONTEXT:
{context}

Include:

# Installation Guide

## Table of Contents

## System Requirements
- Operating System requirements
- Python version
- Node.js version
- Other dependencies

## Prerequisites Installation

### macOS
```bash
# Install Homebrew
# Install Python
# Install Node.js
```

### Linux
```bash
# Commands for Linux
```

### Windows
```powershell
# Commands for Windows
```

## Framework Installation

### Step 1: Clone Repository
```bash
git clone [url]
cd automation_framework
```

### Step 2: Python Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### Step 3: Node.js Dependencies
```bash
cd frontend
npm install
cd ..
```

### Step 4: Configuration
```bash
cp .env.example .env
# Edit .env with your settings
```

### Step 5: Database Setup (if applicable)
Steps to setup test database

### Step 6: Verification
```bash
# Run a simple test to verify installation
pytest --version
npm test -- --version
```

## Browser Driver Installation

### ChromeDriver
Instructions for installing ChromeDriver

### GeckoDriver (Firefox)
Instructions for GeckoDriver

### Other Drivers
As needed

## IDE Setup (Optional)

### VS Code
Recommended extensions and settings

### PyCharm
Setup instructions

## Troubleshooting

### Common Issues
List common installation issues and solutions

### Platform-Specific Issues
macOS specific issues
Linux specific issues
Windows specific issues

## Next Steps
After installation is complete, refer to USAGE.md

Format as clear, step-by-step markdown documentation.
"""
        
        return self.generate_response(prompt, context=context)
    
    def generate_architecture_doc(self, context: Optional[str] = None) -> str:
        """Generate architecture documentation."""
        logger.info("Generating ARCHITECTURE.md...")
        
        prompt = f"""
Generate comprehensive architecture documentation (ARCHITECTURE.md).

CONTEXT:
{context}

Include:

# Framework Architecture

## Overview
High-level architecture description

## Design Principles
- Modularity
- Reusability
- Maintainability
- Scalability
- Other principles followed

## Architecture Diagram
```
[Include ASCII diagram or description for creating diagram]
```

## Component Architecture

### Backend Testing Components

#### API Testing
- BaseAPIClient design
- Endpoint implementations
- Request/Response handling
- Authentication layer

#### Database Testing
- Database connection management
- Model layer
- Query execution
- Transaction handling

#### CLI Testing
- CLI wrapper design
- Command execution
- Output parsing

### Frontend Testing Components

#### Page Object Model
- Base Page design
- Page-specific implementations
- Component reusability

#### Utilities
- Wait helpers
- Screenshot utilities
- Test data management

## Framework Layers

### 1. Configuration Layer
Purpose and implementation

### 2. Core Layer
Base classes and utilities

### 3. Test Layer
Test implementation

### 4. Reporting Layer
Report generation

## Design Patterns Used
- Page Object Model
- Factory Pattern
- Singleton Pattern (for connections)
- Builder Pattern (for test data)
- Others used

## Data Flow
How data flows through the framework

## Error Handling Strategy
How errors are handled at each layer

## Logging Strategy
Logging approach and levels

## Extension Points
How to extend the framework

## Technology Decisions
Why specific technologies were chosen

## Performance Considerations
Performance optimization techniques used

## Security Considerations
Security best practices implemented

Format as detailed technical documentation.
"""
        
        return self.generate_response(prompt, context=context)
    
    def generate_usage_guide(self, context: Optional[str] = None) -> str:
        """Generate usage guide."""
        logger.info("Generating USAGE.md...")
        
        prompt = f"""
Generate a comprehensive usage guide (USAGE.md).

Include:
- How to write new tests
- How to run specific tests
- How to use test data
- How to configure tests
- How to generate reports
- Best practices
- Examples

Format as user-friendly markdown documentation.
"""
        
        return self.generate_response(prompt, context=context)
    
    def generate_debugging_guide(self, context: Optional[str] = None) -> str:
        """Generate debugging guide."""
        logger.info("Generating DEBUGGING.md...")
        
        prompt = f"""
Generate a comprehensive debugging guide (DEBUGGING.md).

Include:
- How to enable debug mode
- How to read logs
- Common errors and solutions
- How to debug failing tests
- How to capture screenshots/videos
- How to use browser DevTools
- Debugging in IDE
- Tips and tricks

Format as practical troubleshooting documentation.
"""
        
        return self.generate_response(prompt, context=context)
    
    def generate_contributing_guide(self, context: Optional[str] = None) -> str:
        """Generate contributing guide."""
        logger.info("Generating CONTRIBUTING.md...")
        
        prompt = f"""
Generate CONTRIBUTING.md covering:
- How to contribute
- Code style guidelines
- PR process
- Testing requirements
- Documentation requirements

Format as contributor-friendly documentation.
"""
        
        return self.generate_response(prompt, context=context)
    
    def generate_api_reference(self, context: Optional[str] = None) -> str:
        """Generate API reference documentation."""
        logger.info("Generating API_REFERENCE.md...")
        
        prompt = f"""
Generate API reference documentation (API_REFERENCE.md).

CONTEXT:
{context}

Document all major classes and methods:
- BaseAPIClient
- BaseDBHandler
- CLIWrapper
- BasePage
- Utilities

Include:
- Class descriptions
- Method signatures
- Parameters
- Return values
- Examples

Format as reference documentation.
"""
        
        return self.generate_response(prompt, context=context)
    
    def generate_changelog(self, context: Optional[str] = None) -> str:
        """Generate changelog."""
        return """# Changelog

## [1.0.0] - Initial Release

### Added
- Complete test automation framework
- Backend testing (API, Database, CLI)
- Frontend testing (Selenium + TypeScript)
- Integration and E2E testing
- Comprehensive reporting
- CI/CD integration
- Complete documentation
"""
