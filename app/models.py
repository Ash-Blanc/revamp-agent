from typing import Any, Optional
from agno.models.openai import OpenAIChat
from app.config import settings
from app.utils.logger import logger

# Try imports
try:
    from agno.models.cerebras import Cerebras
    CEREBRAS_AVAILABLE = True
except ImportError:
    CEREBRAS_AVAILABLE = False

try:
    from agno.models.mistral import MistralChat
    MISTRAL_AVAILABLE = True
except ImportError:
    MISTRAL_AVAILABLE = False

try:
    from agno.models.openrouter import OpenRouter
    OPENROUTER_AVAILABLE = True
except ImportError:
    OPENROUTER_AVAILABLE = False

class ModelFactory:
    """Factory for creating LLM instances with fallback logic."""
    
    @staticmethod
    def get_coding_model() -> Any:
        """
        Get the coding model with fallback logic:
        1. Cerebras (Primary)
        2. Mistral (Fallback 1)
        3. OpenRouter (Fallback 2)
        4. OpenAI (Final Fallback)
        """
        # Try Cerebras
        if CEREBRAS_AVAILABLE and settings.cerebras_api_key:
            try:
                logger.info("Initializing Cerebras model for coding.")
                return Cerebras(id=settings.cerebras_model_id, api_key=settings.cerebras_api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize Cerebras: {e}")
        
        # Try Mistral
        if MISTRAL_AVAILABLE and settings.mistral_api_key:
            try:
                logger.info("Initializing Mistral model for coding.")
                return MistralChat(id=settings.mistral_model_id, api_key=settings.mistral_api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize Mistral: {e}")
        
        # Try OpenRouter
        if OPENROUTER_AVAILABLE and settings.openrouter_api_key:
            try:
                logger.info("Initializing OpenRouter model for coding.")
                return OpenRouter(id=settings.openrouter_model_id, api_key=settings.openrouter_api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenRouter: {e}")
                
        # Fallback to OpenAI
        logger.warning("No specialized coding models available, falling back to OpenAI.")
        return OpenAIChat(id=settings.primary_model_id, api_key=settings.openai_api_key)

    @staticmethod
    def get_strategy_model() -> Any:
        """Get the primary strategy model (default: OpenAI)."""
        return OpenAIChat(id=settings.primary_model_id, api_key=settings.openai_api_key)
