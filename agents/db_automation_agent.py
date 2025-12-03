"""
Database Automation Agent - Generates Python-based database test automation code.
"""

from typing import Dict, List, Optional
from .base_agent import BaseAgent
from .agent_prompts import get_agent_prompt
from loguru import logger


class DBAutomationAgent(BaseAgent):
    """Database Automation Agent that generates database test automation code."""
    
    def __init__(self):
        super().__init__(
            name="DB Automation Agent",
            role="Generate Python-based database test automation",
            temperature=0.7
        )
    
    def get_system_prompt(self) -> str:
        """Get system prompt for DB automation."""
        return get_agent_prompt('db_automation')
    
    def execute_task(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Execute DB automation task.
        
        Args:
            task: Task dictionary
            context: Optional context
            
        Returns:
            Task result
        """
        test_cases = task.get('test_cases', [])
        framework = task.get('framework', {})
        
        return self.generate_db_automation(test_cases, framework, context)
    
    def generate_db_automation(self,
                               test_cases: List[Dict],
                               framework: Dict,
                               context: Optional[str] = None) -> Dict:
        """
        Generate database automation code.
        
        Args:
            test_cases: Database test cases
            framework: Framework design
            context: Additional context
            
        Returns:
            Generated automation code
        """
        logger.info("Generating database automation code...")
        
        prompt = f"""
Generate complete Python-based database test automation code based on:

TEST CASES:
{test_cases}

FRAMEWORK DESIGN:
{framework}

CONTEXT:
{context}

Generate the following files with complete, executable code:

1. backend/database/db_connection.py
```python
# Complete database connection handler
# Support multiple database types (PostgreSQL, MySQL, MongoDB, Redis)
# Include:
# - Connection pooling
# - Transaction management
# - Query execution
# - Error handling
# - Connection retry logic
# - Context managers

import psycopg2
from psycopg2 import pool
from typing import List, Dict, Optional, Any
import logging

class DatabaseConnection:
    def __init__(self, db_config: Dict):
        # Implementation
        pass
    
    def execute_query(self, query: str, params: Optional[tuple] = None):
        # Implementation
        pass
    
    def execute_many(self, query: str, data: List[tuple]):
        # Implementation
        pass
    
    def fetch_one(self, query: str, params: Optional[tuple] = None):
        # Implementation
        pass
    
    def fetch_all(self, query: str, params: Optional[tuple] = None):
        # Implementation
        pass
    
    # ... more methods
```

2. backend/database/models/base_model.py
```python
# Base model class for database operations
# ORM-like interface
# CRUD operations

from backend.database.db_connection import DatabaseConnection

class BaseModel:
    table_name = None
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    def create(self, data: Dict):
        # Implementation
        pass
    
    def read(self, id: Any):
        # Implementation
        pass
    
    def update(self, id: Any, data: Dict):
        # Implementation
        pass
    
    def delete(self, id: Any):
        # Implementation
        pass
    
    def find_all(self, filters: Optional[Dict] = None):
        # Implementation
        pass
```

3. backend/database/models/user_model.py
```python
# Example model implementation
# Create similar models for each table

from backend.database.models.base_model import BaseModel

class UserModel(BaseModel):
    table_name = "users"
    
    def find_by_email(self, email: str):
        # Implementation
        pass
    
    def find_by_username(self, username: str):
        # Implementation
        pass
```

4. backend/database/tests/test_database.py
```python
# Complete test file implementing ALL database test cases
# Use pytest framework
# Include:
# - Fixtures for DB setup/teardown
# - Transaction rollback for test isolation
# - CRUD operation tests
# - Data integrity tests
# - Constraint validation tests

import pytest
from backend.database.db_connection import DatabaseConnection
from backend.database.models.user_model import UserModel

@pytest.fixture(scope="function")
def db_connection():
    # Setup with transaction
    yield
    # Rollback transaction

@pytest.fixture
def user_model(db_connection):
    return UserModel(db_connection)

class TestUserModel:
    def test_create_user(self, user_model):
        # Test implementation from test cases
        pass
    
    def test_read_user(self, user_model):
        # Test implementation
        pass
    
    def test_update_user(self, user_model):
        # Test implementation
        pass
    
    def test_delete_user(self, user_model):
        # Test implementation
        pass
    
    def test_unique_constraint_email(self, user_model):
        # Test implementation
        pass
    
    # ... implement ALL test cases
```

5. backend/database/fixtures.py
```python
# Database fixtures for testing
# Include:
# - Database connection fixture
# - Test data setup/teardown
# - Transaction management
# - Schema setup fixtures

import pytest
from backend.database.db_connection import DatabaseConnection
from config.config import Config

@pytest.fixture(scope="session")
def db_connection():
    # Create connection
    conn = DatabaseConnection(Config.DB_CONFIG)
    yield conn
    # Close connection
    conn.close()

@pytest.fixture(scope="function")
def db_transaction(db_connection):
    # Start transaction
    db_connection.begin_transaction()
    yield db_connection
    # Rollback transaction
    db_connection.rollback()

@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password_hash": "hashed_password"
    }
```

6. backend/database/test_data/db_test_data.json
```json
{
  "users": [
    {
      "username": "user1",
      "email": "user1@example.com",
      "role": "admin"
    },
    {
      "username": "user2",
      "email": "user2@example.com",
      "role": "user"
    }
  ],
  "invalid_data": {
    "duplicate_email": "user1@example.com",
    "invalid_email": "not-an-email",
    "empty_username": ""
  }
}
```

7. backend/database/utilities/data_validators.py
```python
# Data validation utilities
# Schema validators
# Constraint checkers

def validate_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_foreign_key(db_connection, table: str, column: str, value: Any) -> bool:
    # Implementation
    pass
```

8. backend/database/utilities/db_helpers.py
```python
# Database helper utilities
# Query builders
# Data generators
# Migration helpers

def generate_test_data(model_name: str, count: int) -> List[Dict]:
    # Generate random test data
    pass

def truncate_table(db_connection, table_name: str):
    # Safely truncate table
    pass
```

Generate COMPLETE, PRODUCTION-READY code for all files. Each file should:
- Be fully implemented (no TODOs or placeholders)
- Include proper error handling
- Have logging
- Include docstrings
- Be executable immediately
- Follow Python best practices
- Include type hints
- Handle database-specific edge cases

Make the code robust enough to handle:
- Connection failures
- Transaction rollbacks
- Constraint violations
- Deadlocks
- Concurrent access
"""
        
        response = self.generate_response(prompt, context=context)
        
        automation_code = {
            'db_automation_code': response,
            'language': 'Python',
            'framework': 'pytest + SQLAlchemy/psycopg2',
            'test_cases_automated': len(test_cases) if isinstance(test_cases, list) else 'all',
            'created_by': self.name,
            'files_generated': [
                'backend/database/db_connection.py',
                'backend/database/models/*.py',
                'backend/database/tests/test_database.py',
                'backend/database/fixtures.py',
                'backend/database/test_data/db_test_data.json',
                'backend/database/utilities/data_validators.py',
                'backend/database/utilities/db_helpers.py'
            ]
        }
        
        self.log_activity("Database automation code generated", {
            'test_cases': automation_code['test_cases_automated']
        })
        
        return automation_code
