"""
Configuration loading utilities.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import langwatch
from ..core.exceptions import ConfigurationError

class ConfigLoader:
    """
    Centralized configuration loading and validation.
    """
    
    def __init__(self):
        self._config = {}
        self._loaded = False
    
    def load(self, env_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from environment variables.
        
        Args:
            env_file: Optional path to .env file
            
        Returns:
            Dictionary with configuration
        """
        if self._loaded:
            return self._config
        
        # Load environment variables
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv(os.path.join(os.getcwd(), ".env"))
            load_dotenv()
        
        # Load API keys
        self._config = {
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "langwatch_api_key": os.getenv("LANGWATCH_API_KEY"),
            "firecrawl_api_key": os.getenv("FIRECRAWL_API_KEY"),
            "github_access_token": os.getenv("GITHUB_ACCESS_TOKEN"),
            "morph_api_key": os.getenv("MORPH_API_KEY"),
            "cerebras_api_key": os.getenv("CEREBRAS_API_KEY"),
            "mistral_api_key": os.getenv("MISTRAL_API_KEY"),
            "openrouter_api_key": os.getenv("OPENROUTER_API_KEY"),
        }
        
        # Initialize LangWatch if key is available
        if self._config["langwatch_api_key"]:
            try:
                langwatch.setup(api_key=self._config["langwatch_api_key"])
            except Exception as e:
                print(f"Warning: Failed to initialize LangWatch: {e}")
        
        self._loaded = True
        return self._config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        if not self._loaded:
            self.load()
        return self._config.get(key, default)
    
    def validate_required_keys(self, required_keys: list) -> None:
        """
        Validate that required API keys are present.
        
        Args:
            required_keys: List of required configuration keys
            
        Raises:
            ConfigurationError: If required keys are missing
        """
        if not self._loaded:
            self.load()
        
        missing_keys = []
        for key in required_keys:
            if not self._config.get(key):
                missing_keys.append(key)
        
        if missing_keys:
            raise ConfigurationError(
                f"Missing required configuration keys: {', '.join(missing_keys)}"
            )
    
    def has_key(self, key: str) -> bool:
        """Check if a configuration key exists and has a value."""
        if not self._loaded:
            self.load()
        return bool(self._config.get(key))
    
    def get_available_tools(self) -> Dict[str, bool]:
        """Get a dictionary of available tools based on API keys."""
        if not self._loaded:
            self.load()
        
        return {
            "firecrawl": self.has_key("firecrawl_api_key"),
            "github": self.has_key("github_access_token"),
            "morph": self.has_key("morph_api_key"),
            "cerebras": self.has_key("cerebras_api_key"),
            "mistral": self.has_key("mistral_api_key"),
            "openrouter": self.has_key("openrouter_api_key"),
        }

# Global instance
_config_loader = ConfigLoader()

def get_config() -> ConfigLoader:
    """Get the global configuration loader instance."""
    return _config_loader