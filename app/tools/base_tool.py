"""
Base tool class with common functionality.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from agno.tools import Toolkit

class BaseTool(Toolkit, ABC):
    """
    Base class for custom tools with common functionality.
    """
    
    def __init__(self, name: str):
        super().__init__(name=name)
        self._cache = {}
        self._cache_enabled = True
    
    def enable_cache(self):
        """Enable result caching."""
        self._cache_enabled = True
    
    def disable_cache(self):
        """Disable result caching."""
        self._cache_enabled = False
        self._cache.clear()
    
    def clear_cache(self):
        """Clear the cache."""
        self._cache.clear()
    
    def _get_cache_key(self, *args, **kwargs) -> str:
        """Generate a cache key from arguments."""
        import hashlib
        import json
        
        # Create a deterministic string from args and kwargs
        cache_data = {
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        cache_string = json.dumps(cache_data, sort_keys=True, default=str)
        
        # Generate hash
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _cached_call(self, func_name: str, func, *args, **kwargs):
        """
        Execute a function with caching support.
        
        Args:
            func_name: Name of the function for cache key
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result (cached or fresh)
        """
        if not self._cache_enabled:
            return func(*args, **kwargs)
        
        cache_key = f"{func_name}_{self._get_cache_key(*args, **kwargs)}"
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        result = func(*args, **kwargs)
        self._cache[cache_key] = result
        
        return result
    
    def _safe_execute(self, func, *args, **kwargs):
        """
        Execute a function with error handling.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result or empty list on error
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Warning: Tool execution failed: {e}")
            return []
    
    @abstractmethod
    def get_tool_info(self) -> Dict[str, Any]:
        """
        Get information about this tool.
        
        Returns:
            Dictionary with tool information
        """
        pass