"""
GitHub integration tools for agents.
"""

import os
from typing import Dict, List, Optional
import git
from pathlib import Path
import requests
from loguru import logger


class GitHubTools:
    """Tools for interacting with GitHub repositories."""
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize GitHub tools.
        
        Args:
            github_token: GitHub personal access token
        """
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.headers = {}
        
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
    
    def clone_repository(self, repo_url: str, target_dir: str) -> str:
        """
        Clone a GitHub repository.
        
        Args:
            repo_url: GitHub repository URL
            target_dir: Target directory for cloning
            
        Returns:
            Path to cloned repository
        """
        try:
            target_path = Path(target_dir)
            target_path.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Cloning repository: {repo_url}")
            git.Repo.clone_from(repo_url, target_path, depth=1)
            
            logger.info(f"Repository cloned to: {target_path}")
            return str(target_path)
            
        except Exception as e:
            logger.error(f"Failed to clone repository: {str(e)}")
            raise
    
    def get_repository_info(self, owner: str, repo: str) -> Dict:
        """
        Get repository information from GitHub API.
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Repository information
        """
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'name': data['name'],
                'description': data.get('description', ''),
                'language': data.get('language', ''),
                'languages_url': data.get('languages_url', ''),
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
                'open_issues': data.get('open_issues_count', 0),
                'created_at': data.get('created_at', ''),
                'updated_at': data.get('updated_at', ''),
                'default_branch': data.get('default_branch', 'main')
            }
            
        except Exception as e:
            logger.error(f"Failed to get repository info: {str(e)}")
            return {}
    
    def get_repository_languages(self, owner: str, repo: str) -> Dict:
        """
        Get programming languages used in repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Dictionary of languages and their byte counts
        """
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/languages"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Failed to get repository languages: {str(e)}")
            return {}
    
    def get_file_content(self, owner: str, repo: str, file_path: str, branch: str = 'main') -> str:
        """
        Get content of a specific file from repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            file_path: Path to file in repository
            branch: Branch name
            
        Returns:
            File content
        """
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
            params = {'ref': branch}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            import base64
            content = base64.b64decode(response.json()['content']).decode('utf-8')
            
            return content
            
        except Exception as e:
            logger.error(f"Failed to get file content: {str(e)}")
            return ""
    
    def list_repository_files(self, owner: str, repo: str, path: str = "", branch: str = 'main') -> List[Dict]:
        """
        List files in a repository path.
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: Path in repository
            branch: Branch name
            
        Returns:
            List of files
        """
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            params = {'ref': branch}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            files = []
            for item in response.json():
                files.append({
                    'name': item['name'],
                    'path': item['path'],
                    'type': item['type'],
                    'size': item.get('size', 0),
                    'url': item.get('html_url', '')
                })
            
            return files
            
        except Exception as e:
            logger.error(f"Failed to list repository files: {str(e)}")
            return []
    
    def parse_github_url(self, url: str) -> Dict:
        """
        Parse GitHub URL to extract owner and repo.
        
        Args:
            url: GitHub repository URL
            
        Returns:
            Dictionary with owner and repo
        """
        # Remove .git suffix if present
        url = url.rstrip('.git')
        
        # Handle different URL formats
        if 'github.com/' in url:
            parts = url.split('github.com/')[-1].split('/')
            if len(parts) >= 2:
                return {
                    'owner': parts[0],
                    'repo': parts[1]
                }
        
        return {}
