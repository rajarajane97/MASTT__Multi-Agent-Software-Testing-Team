"""
Document processing and analysis tools.
"""

import re
from typing import Dict, List, Optional
from loguru import logger


class DocumentTools:
    """Tools for analyzing and processing documents."""
    
    @staticmethod
    def extract_requirements(text: str) -> List[str]:
        """
        Extract requirement statements from text.
        
        Args:
            text: Document text
            
        Returns:
            List of requirements
        """
        requirements = []
        
        # Common requirement patterns
        patterns = [
            r'(?:shall|must|should|will)\s+(.+?)(?:\.|$)',
            r'(?:requirement|req|REQ)[\s#:-]*(\d+)[:\s]*(.+?)(?:\.|$)',
            r'(?:the system|application|user)\s+(?:shall|must|should|will)\s+(.+?)(?:\.|$)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                req = match.group(0).strip()
                if len(req) > 10 and req not in requirements:
                    requirements.append(req)
        
        return requirements
    
    @staticmethod
    def extract_test_scenarios(text: str) -> List[Dict]:
        """
        Extract test scenario descriptions from text.
        
        Args:
            text: Document text
            
        Returns:
            List of test scenarios
        """
        scenarios = []
        
        # Look for test case patterns
        patterns = [
            r'(?:test case|tc|scenario)[\s#:-]*(\d+)[:\s]*(.+?)(?:\n|$)',
            r'(?:given|when|then)\s+(.+?)(?:\n|$)',
            r'(?:verify|validate|ensure|check)\s+(?:that\s+)?(.+?)(?:\.|$)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                scenario = {
                    'text': match.group(0).strip(),
                    'extracted_from': 'pattern_match'
                }
                scenarios.append(scenario)
        
        return scenarios
    
    @staticmethod
    def extract_api_specs(text: str) -> List[Dict]:
        """
        Extract API specifications from text.
        
        Args:
            text: Document text
            
        Returns:
            List of API specifications
        """
        api_specs = []
        
        # Look for API endpoint patterns
        endpoint_pattern = r'(?:GET|POST|PUT|DELETE|PATCH)\s+([/\w\-{}]+)'
        matches = re.finditer(endpoint_pattern, text, re.IGNORECASE)
        
        for match in matches:
            method_path = match.group(0).split()
            if len(method_path) == 2:
                api_specs.append({
                    'method': method_path[0].upper(),
                    'path': method_path[1],
                    'source': 'document'
                })
        
        return api_specs
    
    @staticmethod
    def extract_database_schema(text: str) -> List[Dict]:
        """
        Extract database schema information from text.
        
        Args:
            text: Document text
            
        Returns:
            List of table/schema information
        """
        schemas = []
        
        # Look for table definitions
        table_patterns = [
            r'(?:table|entity)[\s:]+(\w+)',
            r'CREATE TABLE\s+(\w+)',
            r'(?:columns?|fields?)[\s:]+(.+?)(?:\n|$)'
        ]
        
        for pattern in table_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                schemas.append({
                    'definition': match.group(0).strip(),
                    'extracted_from': 'document'
                })
        
        return schemas
    
    @staticmethod
    def extract_business_rules(text: str) -> List[str]:
        """
        Extract business rules from text.
        
        Args:
            text: Document text
            
        Returns:
            List of business rules
        """
        rules = []
        
        # Common business rule patterns
        patterns = [
            r'(?:business rule|rule|br)[\s#:-]*(\d+)[:\s]*(.+?)(?:\.|$)',
            r'(?:if|when)\s+(.+?)\s+(?:then|,)',
            r'(?:must not|cannot|should not)\s+(.+?)(?:\.|$)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                rule = match.group(0).strip()
                if len(rule) > 15 and rule not in rules:
                    rules.append(rule)
        
        return rules
    
    @staticmethod
    def categorize_document(text: str, filename: str = "") -> str:
        """
        Categorize document type based on content.
        
        Args:
            text: Document text
            filename: Document filename
            
        Returns:
            Document category
        """
        text_lower = text.lower()
        filename_lower = filename.lower()
        
        # Check for various document types
        if any(keyword in text_lower for keyword in ['requirement', 'functional spec', 'specification']):
            return 'requirements'
        elif any(keyword in text_lower for keyword in ['test plan', 'testing strategy']):
            return 'test_plan'
        elif any(keyword in text_lower for keyword in ['test case', 'test scenario']):
            return 'test_cases'
        elif any(keyword in text_lower for keyword in ['api', 'endpoint', 'swagger', 'openapi']):
            return 'api_documentation'
        elif any(keyword in text_lower for keyword in ['database', 'schema', 'erd', 'entity']):
            return 'database_documentation'
        elif any(keyword in text_lower for keyword in ['user guide', 'manual', 'how to']):
            return 'user_documentation'
        elif any(keyword in filename_lower for keyword in ['readme', 'contributing', 'changelog']):
            return 'project_documentation'
        else:
            return 'general'
    
    @staticmethod
    def extract_user_stories(text: str) -> List[Dict]:
        """
        Extract user stories from text.
        
        Args:
            text: Document text
            
        Returns:
            List of user stories
        """
        stories = []
        
        # User story pattern: "As a <role>, I want <goal> so that <benefit>"
        pattern = r'(?:as a|as an)\s+(.+?),?\s+i\s+(?:want|need|would like)\s+(?:to\s+)?(.+?)(?:\s+so that\s+(.+?))?(?:\.|$)'
        
        matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
        
        for match in matches:
            story = {
                'role': match.group(1).strip(),
                'goal': match.group(2).strip(),
                'benefit': match.group(3).strip() if match.group(3) else '',
                'full_text': match.group(0).strip()
            }
            stories.append(story)
        
        return stories
    
    @staticmethod
    def extract_acceptance_criteria(text: str) -> List[str]:
        """
        Extract acceptance criteria from text.
        
        Args:
            text: Document text
            
        Returns:
            List of acceptance criteria
        """
        criteria = []
        
        # Look for Given-When-Then patterns
        gwt_pattern = r'(?:given|when|then)\s+(.+?)(?:\n|$)'
        matches = re.finditer(gwt_pattern, text, re.IGNORECASE)
        
        for match in matches:
            criterion = match.group(0).strip()
            if criterion not in criteria:
                criteria.append(criterion)
        
        # Look for acceptance criteria sections
        ac_pattern = r'(?:acceptance criteria|ac)[:\s]+(.+?)(?:\n\n|$)'
        matches = re.finditer(ac_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            ac_text = match.group(1).strip()
            # Split by bullet points or numbers
            items = re.split(r'[\n•\-\*\d+\.]', ac_text)
            for item in items:
                item = item.strip()
                if item and len(item) > 10:
                    criteria.append(item)
        
        return criteria
    
    @staticmethod
    def summarize_document(text: str, max_length: int = 500) -> str:
        """
        Create a summary of document text.
        
        Args:
            text: Document text
            max_length: Maximum summary length
            
        Returns:
            Document summary
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # If text is short enough, return as is
        if len(text) <= max_length:
            return text
        
        # Extract first few sentences
        sentences = re.split(r'[.!?]+', text)
        summary = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if len(summary) + len(sentence) + 2 <= max_length:
                summary += sentence + ". "
            else:
                break
        
        return summary.strip()
