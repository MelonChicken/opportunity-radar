"""
LLM Client for OpenAI API interactions.
Implements singleton pattern and provides common LLM operations.
"""
import logging
from typing import Optional, Dict, Any
from openai import OpenAI
from openai.types.chat import ChatCompletion

from ..config import get_settings

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Singleton LLM client for OpenAI API.
    Provides centralized access to LLM operations with error handling.
    """
    
    _instance: Optional['LLMClient'] = None
    _client: Optional[OpenAI] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the LLM client if not already initialized."""
        if self._client is None:
            settings = get_settings()
            api_key = settings.openai_api_key
            
            if api_key:
                self._client = OpenAI(api_key=api_key)
                logger.info("LLM client initialized successfully")
            else:
                logger.warning("No OpenAI API key found. LLM client not initialized.")
    
    @classmethod
    def get_instance(cls) -> 'LLMClient':
        """
        Get the singleton instance of LLMClient.
        
        Returns:
            LLMClient: The singleton instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @property
    def is_available(self) -> bool:
        """Check if the LLM client is available (API key configured)."""
        return self._client is not None
    
    def chat_completion(
        self,
        messages: list[Dict[str, str]],
        model: Optional[str] = None,
        response_format: Optional[Dict[str, str]] = None,
        temperature: float = 1.0,
        max_tokens: Optional[int] = None
    ) -> Optional[ChatCompletion]:
        """
        Create a chat completion.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (defaults to config setting)
            response_format: Response format specification (e.g., {"type": "json_object"})
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            ChatCompletion object or None if client not available
        """
        if not self.is_available:
            logger.warning("LLM client not available. Skipping API call.")
            return None
        
        settings = get_settings()
        model = model or settings.openai_model
        
        try:
            kwargs: Dict[str, Any] = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
            }
            
            if response_format:
                kwargs["response_format"] = response_format
            
            if max_tokens:
                kwargs["max_tokens"] = max_tokens
            
            response = self._client.chat.completions.create(**kwargs)
            
            logger.debug(f"LLM API call successful. Model: {model}, Tokens: "
                        f"{response.usage.total_tokens if response.usage else 'N/A'}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error calling LLM API: {e}", exc_info=True)
            return None
    
    def simple_completion(
        self,
        prompt: str,
        system_message: str = "You are a helpful assistant.",
        **kwargs
    ) -> Optional[str]:
        """
        Simple completion with a single user prompt.
        
        Args:
            prompt: User prompt
            system_message: System message
            **kwargs: Additional arguments for chat_completion
            
        Returns:
            Response content as string or None
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        response = self.chat_completion(messages, **kwargs)
        
        if response and response.choices:
            return response.choices[0].message.content
        
        return None
