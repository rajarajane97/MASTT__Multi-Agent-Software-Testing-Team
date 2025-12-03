"""
Code Analyzer for parsing and analyzing source code repositories.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import git
from radon.complexity import cc_visit
from radon.metrics import mi_visit, h_visit
import lizard
from loguru import logger


class CodeAnalyzer:
    """Analyzes code repositories to extract structure and metrics."""
    
    def __init__(self, repo_path: str):
        """
        Initialize code analyzer.
        
        Args:
            repo_path: Path to local repository or GitHub URL
        """
        self.repo_path = repo_path
        self.is_remote = repo_path.startswith('http')
        self.local_path = None
        self.analysis_results = {}
        
    def prepare_repository(self) -> str:
        """
        Prepare repository for analysis (clone if remote).
        
        Returns:
            Local path to repository
        """
        if self.is_remote:
            # Clone repository
            clone_dir = Path('./temp_repos')
            clone_dir.mkdir(exist_ok=True)
            
            repo_name = self.repo_path.split('/')[-1].replace('.git', '')
            self.local_path = clone_dir / repo_name
            
            if self.local_path.exists():
                logger.info(f"Repository already cloned at {self.local_path}")
            else:
                logger.info(f"Cloning repository from {self.repo_path}")
                git.Repo.clone_from(self.repo_path, self.local_path, depth=1)
                logger.info("Clone complete")
        else:
            self.local_path = Path(self.repo_path)
            
        return str(self.local_path)
    
    def analyze_structure(self) -> Dict:
        """
        Analyze repository structure.
        
        Returns:
            Dictionary containing structure analysis
        """
        structure = {
            'directories': [],
            'files_by_type': {},
            'total_files': 0,
            'languages': set()
        }
        
        for root, dirs, files in os.walk(self.local_path):
            # Skip hidden and common build directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', 'build', 'dist', '__pycache__']]
            
            rel_root = os.path.relpath(root, self.local_path)
            if rel_root != '.':
                structure['directories'].append(rel_root)
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                structure['total_files'] += 1
                ext = Path(file).suffix
                
                if ext not in structure['files_by_type']:
                    structure['files_by_type'][ext] = []
                    
                file_path = os.path.join(rel_root, file)
                structure['files_by_type'][ext].append(file_path)
                
                # Detect language
                if ext in ['.py']:
                    structure['languages'].add('Python')
                elif ext in ['.js', '.jsx', '.ts', '.tsx']:
                    structure['languages'].add('JavaScript/TypeScript')
                elif ext in ['.java']:
                    structure['languages'].add('Java')
                elif ext in ['.go']:
                    structure['languages'].add('Go')
                elif ext in ['.rb']:
                    structure['languages'].add('Ruby')
                elif ext in ['.cs']:
                    structure['languages'].add('C#')
        
        structure['languages'] = list(structure['languages'])
        return structure
    
    def analyze_python_files(self) -> List[Dict]:
        """
        Analyze Python files for complexity and maintainability.
        
        Returns:
            List of analysis results for Python files
        """
        python_analysis = []
        
        for root, dirs, files in os.walk(self.local_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', 'build', 'dist', '__pycache__']]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.local_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code = f.read()
                        
                        # Cyclomatic complexity
                        complexity = cc_visit(code)
                        
                        # Maintainability index
                        mi = mi_visit(code, multi=True)
                        
                        # Halstead metrics
                        halstead = h_visit(code)
                        
                        analysis = {
                            'file': rel_path,
                            'lines_of_code': len(code.splitlines()),
                            'complexity': [
                                {
                                    'name': item.name,
                                    'complexity': item.complexity,
                                    'lineno': item.lineno
                                }
                                for item in complexity
                            ],
                            'maintainability_index': mi,
                            'halstead_metrics': {
                                'volume': halstead.total.volume if halstead.total else 0,
                                'difficulty': halstead.total.difficulty if halstead.total else 0,
                                'effort': halstead.total.effort if halstead.total else 0
                            }
                        }
                        
                        python_analysis.append(analysis)
                        
                    except Exception as e:
                        logger.warning(f"Could not analyze {rel_path}: {str(e)}")
        
        return python_analysis
    
    def analyze_with_lizard(self) -> Dict:
        """
        Use Lizard to analyze multiple languages.
        
        Returns:
            Lizard analysis results
        """
        try:
            analysis = lizard.analyze(
                paths=[str(self.local_path)],
                exclude_pattern='node_modules/*,venv/*,build/*,dist/*,__pycache__/*'
            )
            
            results = {
                'average_cyclomatic_complexity': 0,
                'average_nloc': 0,
                'files': [],
                'total_functions': 0
            }
            
            total_cc = 0
            total_nloc = 0
            function_count = 0
            
            for file_info in analysis:
                file_data = {
                    'filename': file_info.filename,
                    'nloc': file_info.nloc,
                    'token_count': file_info.token_count,
                    'functions': []
                }
                
                for func in file_info.function_list:
                    file_data['functions'].append({
                        'name': func.name,
                        'start_line': func.start_line,
                        'cyclomatic_complexity': func.cyclomatic_complexity,
                        'nloc': func.nloc,
                        'token_count': func.token_count
                    })
                    
                    total_cc += func.cyclomatic_complexity
                    total_nloc += func.nloc
                    function_count += 1
                
                results['files'].append(file_data)
            
            if function_count > 0:
                results['average_cyclomatic_complexity'] = total_cc / function_count
                results['average_nloc'] = total_nloc / function_count
            
            results['total_functions'] = function_count
            
            return results
            
        except Exception as e:
            logger.error(f"Lizard analysis failed: {str(e)}")
            return {}
    
    def identify_test_types(self) -> Dict:
        """
        Identify what types of tests are needed.
        
        Returns:
            Dictionary of test types required
        """
        structure = self.analysis_results.get('structure', {})
        test_types = {
            'backend': {
                'api': False,
                'database': False,
                'cli': False
            },
            'frontend': {
                'gui': False,
                'components': False
            },
            'integration': False,
            'e2e': False
        }
        
        # Check for API frameworks
        for ext, files in structure.get('files_by_type', {}).items():
            for file in files:
                file_lower = file.lower()
                
                # Backend API detection
                if any(keyword in file_lower for keyword in ['api', 'route', 'endpoint', 'controller', 'handler']):
                    test_types['backend']['api'] = True
                
                # Database detection
                if any(keyword in file_lower for keyword in ['model', 'schema', 'migration', 'database', 'db']):
                    test_types['backend']['database'] = True
                
                # CLI detection
                if any(keyword in file_lower for keyword in ['cli', 'command', 'cmd']):
                    test_types['backend']['cli'] = True
                
                # Frontend detection
                if ext in ['.jsx', '.tsx', '.vue'] or 'component' in file_lower:
                    test_types['frontend']['gui'] = True
                    test_types['frontend']['components'] = True
        
        # If both backend and frontend exist, enable integration and E2E
        has_backend = any(test_types['backend'].values())
        has_frontend = any(test_types['frontend'].values())
        
        if has_backend and has_frontend:
            test_types['integration'] = True
            test_types['e2e'] = True
        
        return test_types
    
    def full_analysis(self) -> Dict:
        """
        Perform complete code analysis.
        
        Returns:
            Complete analysis results
        """
        logger.info("Starting code analysis...")
        
        # Prepare repository
        self.prepare_repository()
        
        # Analyze structure
        logger.info("Analyzing repository structure...")
        structure = self.analyze_structure()
        
        # Analyze Python files
        logger.info("Analyzing Python files...")
        python_analysis = self.analyze_python_files()
        
        # Lizard analysis
        logger.info("Running Lizard analysis...")
        lizard_analysis = self.analyze_with_lizard()
        
        # Identify test types
        logger.info("Identifying test types...")
        test_types = self.identify_test_types()
        
        self.analysis_results = {
            'repository_path': str(self.local_path),
            'structure': structure,
            'python_analysis': python_analysis,
            'lizard_analysis': lizard_analysis,
            'test_types': test_types,
            'summary': {
                'total_files': structure['total_files'],
                'languages': structure['languages'],
                'requires_backend_testing': any(test_types['backend'].values()),
                'requires_frontend_testing': any(test_types['frontend'].values()),
                'requires_integration_testing': test_types['integration'],
                'requires_e2e_testing': test_types['e2e']
            }
        }
        
        logger.info("Code analysis complete")
        return self.analysis_results
    
    def save_analysis(self, output_path: str):
        """Save analysis results to JSON file."""
        output_file = Path(output_path) / 'code_analysis.json'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
        
        logger.info(f"Analysis saved to {output_file}")
