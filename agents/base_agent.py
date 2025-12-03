"""
Base Agent class for all AI agents in the system.
"""

import os
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import google.generativeai as genai
from loguru import logger


class BaseAgent(ABC):
    """Base class for all AI agents."""
    
    def __init__(self, 
                 name: str,
                 role: str,
                 model_name: str = None,
                 temperature: float = 0.7,
                 max_tokens: int = 8192):
        """
        Initialize base agent.
        
        Args:
            name: Agent name
            role: Agent role/responsibility
            model_name: Gemini model name
            temperature: Temperature for generation
            max_tokens: Maximum tokens for generation
        """
        self.name = name
        self.role = role
        self.model_name = model_name or os.getenv('GEMINI_MODEL', 'gemini-1.5-pro')
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Configure Gemini
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                'temperature': self.temperature,
                'max_output_tokens': self.max_tokens
            }
        )
        
        # System prompt
        self.system_prompt = self.get_system_prompt()
        
        # Conversation history
        self.conversation_history = []
        
        logger.info(f"Agent initialized: {self.name} ({self.role})")
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for this agent.
        Must be implemented by subclasses.
        
        Returns:
            System prompt string
        """
        pass
    
    def generate_response(self, 
                         prompt: str, 
                         context: Optional[str] = None,
                         additional_instructions: Optional[str] = None) -> str:
        """
        Generate a response using Gemini.
        
        Args:
            prompt: User prompt
            context: Additional context
            additional_instructions: Additional instructions
            
        Returns:
            Generated response
        """
        try:
            # Build full prompt
            full_prompt = f"{self.system_prompt}\n\n"
            
            if context:
                full_prompt += f"=== CONTEXT ===\n{context}\n\n"
            
            if additional_instructions:
                full_prompt += f"=== ADDITIONAL INSTRUCTIONS ===\n{additional_instructions}\n\n"
            
            full_prompt += f"=== TASK ===\n{prompt}"
            
            # Generate response
            logger.info(f"{self.name} generating response...")
            response = self.model.generate_content(full_prompt)
            
            result = response.text
            
            # Store in conversation history
            self.conversation_history.append({
                'role': 'user',
                'content': prompt
            })
            self.conversation_history.append({
                'role': 'assistant',
                'content': result
            })
            
            logger.info(f"{self.name} response generated ({len(result)} chars)")
            return result
            
        except Exception as e:
            logger.error(f"Error generating response for {self.name}: {str(e)}")
            raise
    
    def chat(self, message: str, context: Optional[str] = None) -> str:
        """
        Have a conversation with the agent.
        
        Args:
            message: User message
            context: Optional context
            
        Returns:
            Agent response
        """
        # Build conversation context
        conversation_context = ""
        if self.conversation_history:
            conversation_context = "\n=== CONVERSATION HISTORY ===\n"
            for entry in self.conversation_history[-5:]:  # Last 5 exchanges
                role = entry['role'].upper()
                content = entry['content'][:200]  # Truncate for context
                conversation_context += f"{role}: {content}\n"
        
        full_context = conversation_context
        if context:
            full_context += f"\n{context}"
        
        return self.generate_response(message, context=full_context)
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []
        logger.info(f"{self.name} conversation history reset")
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of conversation."""
        return {
            'agent_name': self.name,
            'total_exchanges': len(self.conversation_history) // 2,
            'history': self.conversation_history
        }
    
    @abstractmethod
    def execute_task(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Execute a specific task.
        Must be implemented by subclasses.
        
        Args:
            task: Task dictionary with parameters
            context: Optional context
            
        Returns:
            Task result dictionary
        """
        pass
    
    def format_output(self, content: Any, output_type: str = "json") -> str:
        """
        Format agent output.
        
        Args:
            content: Content to format
            output_type: Output format type
            
        Returns:
            Formatted output
        """
        if output_type == "json":
            import json
            return json.dumps(content, indent=2)
        elif output_type == "markdown":
            if isinstance(content, dict):
                output = f"# {self.name} Output\n\n"
                for key, value in content.items():
                    output += f"## {key}\n{value}\n\n"
                return output
            return str(content)
        else:
            return str(content)
    
    def validate_output(self, output: Any, expected_keys: List[str] = None) -> bool:
        """
        Validate agent output.
        
        Args:
            output: Output to validate
            expected_keys: Expected keys in output
            
        Returns:
            True if valid, False otherwise
        """
        if expected_keys and isinstance(output, dict):
            return all(key in output for key in expected_keys)
        return output is not None
    
    def log_activity(self, activity: str, details: Optional[Dict] = None):
        """
        Log agent activity.
        
        Args:
            activity: Activity description
            details: Optional activity details
        """
        log_entry = f"[{self.name}] {activity}"
        if details:
            log_entry += f" - {details}"
        logger.info(log_entry)
