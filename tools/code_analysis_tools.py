"""
Code analysis tools for extracting information from source code.
"""

import ast
import re
from typing import Dict, List, Optional
from pathlib import Path
from loguru import logger


class CodeAnalysisTools:
    """Tools for analyzing source code."""
    
    @staticmethod
    def extract_python_functions(file_path: str) -> List[Dict]:
        """
        Extract function definitions from Python file.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            List of function information
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Get docstring
                    docstring = ast.get_docstring(node) or ""
                    
                    # Get parameters
                    params = [arg.arg for arg in node.args.args]
                    
                    # Get decorators
                    decorators = [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list]
                    
                    functions.append({
                        'name': node.name,
                        'line_number': node.lineno,
                        'parameters': params,
                        'docstring': docstring,
                        'decorators': decorators,
                        'is_async': isinstance(node, ast.AsyncFunctionDef)
                    })
            
            return functions
            
        except Exception as e:
            logger.error(f"Error extracting Python functions from {file_path}: {str(e)}")
            return []
    
    @staticmethod
    def extract_python_classes(file_path: str) -> List[Dict]:
        """
        Extract class definitions from Python file.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            List of class information
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Get docstring
                    docstring = ast.get_docstring(node) or ""
                    
                    # Get base classes
                    bases = []
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            bases.append(base.id)
                        elif isinstance(base, ast.Attribute):
                            bases.append(f"{base.value.id}.{base.attr}")
                    
                    # Get methods
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            methods.append({
                                'name': item.name,
                                'line_number': item.lineno,
                                'is_async': isinstance(item, ast.AsyncFunctionDef)
                            })
                    
                    classes.append({
                        'name': node.name,
                        'line_number': node.lineno,
                        'docstring': docstring,
                        'base_classes': bases,
                        'methods': methods
                    })
            
            return classes
            
        except Exception as e:
            logger.error(f"Error extracting Python classes from {file_path}: {str(e)}")
            return []
    
    @staticmethod
    def extract_imports(file_path: str, language: str = 'python') -> List[str]:
        """
        Extract import statements from file.
        
        Args:
            file_path: Path to file
            language: Programming language
            
        Returns:
            List of imports
        """
        imports = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if language == 'python':
                # Parse Python imports
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module or ''
                        for alias in node.names:
                            imports.append(f"{module}.{alias.name}" if module else alias.name)
            
            elif language in ['javascript', 'typescript']:
                # Parse JS/TS imports using regex
                import_patterns = [
                    r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]',
                    r'require\([\'"](.+?)[\'"]\)'
                ]
                
                for pattern in import_patterns:
                    matches = re.findall(pattern, content)
                    imports.extend(matches)
            
            elif language == 'java':
                # Parse Java imports
                import_pattern = r'import\s+([\w.]+);'
                matches = re.findall(import_pattern, content)
                imports.extend(matches)
            
            return list(set(imports))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error extracting imports from {file_path}: {str(e)}")
            return []
    
    @staticmethod
    def detect_test_framework(file_path: str, language: str = 'python') -> Optional[str]:
        """
        Detect testing framework used in file.
        
        Args:
            file_path: Path to file
            language: Programming language
            
        Returns:
            Detected framework name or None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            if language == 'python':
                if 'import pytest' in content or 'from pytest' in content:
                    return 'pytest'
                elif 'import unittest' in content or 'from unittest' in content:
                    return 'unittest'
                elif 'import nose' in content:
                    return 'nose'
            
            elif language in ['javascript', 'typescript']:
                if 'jest' in content:
                    return 'jest'
                elif 'mocha' in content:
                    return 'mocha'
                elif 'jasmine' in content:
                    return 'jasmine'
                elif 'cypress' in content:
                    return 'cypress'
            
            elif language == 'java':
                if 'junit' in content:
                    return 'junit'
                elif 'testng' in content:
                    return 'testng'
            
            return None
            
        except Exception as e:
            logger.error(f"Error detecting test framework in {file_path}: {str(e)}")
            return None
    
    @staticmethod
    def extract_api_endpoints(file_path: str, language: str = 'python') -> List[Dict]:
        """
        Extract API endpoints from file.
        
        Args:
            file_path: Path to file
            language: Programming language
            
        Returns:
            List of API endpoint information
        """
        endpoints = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if language == 'python':
                # FastAPI / Flask patterns
                patterns = [
                    (r'@app\.(get|post|put|delete|patch)\([\'"](.+?)[\'"]\)', 'fastapi/flask'),
                    (r'@router\.(get|post|put|delete|patch)\([\'"](.+?)[\'"]\)', 'fastapi'),
                    (r'@route\([\'"](.+?)[\'"].*?methods=\[([^\]]+)\]', 'flask')
                ]
                
                for pattern, framework in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        if len(match.groups()) == 2:
                            endpoints.append({
                                'method': match.group(1).upper(),
                                'path': match.group(2),
                                'framework': framework
                            })
            
            elif language in ['javascript', 'typescript']:
                # Express patterns
                patterns = [
                    r'app\.(get|post|put|delete|patch)\([\'"](.+?)[\'"]\)',
                    r'router\.(get|post|put|delete|patch)\([\'"](.+?)[\'"]\)'
                ]
                
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        endpoints.append({
                            'method': match.group(1).upper(),
                            'path': match.group(2),
                            'framework': 'express'
                        })
            
            return endpoints
            
        except Exception as e:
            logger.error(f"Error extracting API endpoints from {file_path}: {str(e)}")
            return []
    
    @staticmethod
    def extract_database_models(file_path: str, language: str = 'python') -> List[Dict]:
        """
        Extract database model definitions.
        
        Args:
            file_path: Path to file
            language: Programming language
            
        Returns:
            List of model information
        """
        models = []
        
        try:
            if language == 'python':
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # Look for SQLAlchemy models
                if 'Base' in code or 'declarative_base' in code:
                    tree = ast.parse(code)
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            # Check if it's a model class
                            for base in node.bases:
                                if isinstance(base, ast.Name) and base.id in ['Base', 'Model']:
                                    models.append({
                                        'name': node.name,
                                        'line_number': node.lineno,
                                        'orm': 'sqlalchemy'
                                    })
                                    break
            
            return models
            
        except Exception as e:
            logger.error(f"Error extracting database models from {file_path}: {str(e)}")
            return []
    
    @staticmethod
    def analyze_file_complexity(file_path: str) -> Dict:
        """
        Analyze file complexity metrics.
        
        Args:
            file_path: Path to file
            
        Returns:
            Complexity metrics
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.splitlines()
            
            return {
                'total_lines': len(lines),
                'code_lines': len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
                'comment_lines': len([line for line in lines if line.strip().startswith('#')]),
                'blank_lines': len([line for line in lines if not line.strip()]),
                'file_size_bytes': len(content.encode('utf-8'))
            }
            
        except Exception as e:
            logger.error(f"Error analyzing file complexity: {str(e)}")
            return {}
