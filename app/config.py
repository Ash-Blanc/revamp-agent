from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """Application settings using Pydantic Settings."""
    
    # API Keys
    openai_api_key: Optional[str] = Field(None, validation_alias='OPENAI_API_KEY')
    langwatch_api_key: Optional[str] = Field(None, validation_alias='LANGWATCH_API_KEY')
    firecrawl_api_key: Optional[str] = Field(None, validation_alias='FIRECRAWL_API_KEY')
    github_access_token: Optional[str] = Field(None, validation_alias='GITHUB_ACCESS_TOKEN')
    morph_api_key: Optional[str] = Field(None, validation_alias='MORPH_API_KEY')
    cerebras_api_key: Optional[str] = Field(None, validation_alias='CEREBRAS_API_KEY')
    mistral_api_key: Optional[str] = Field(None, validation_alias='MISTRAL_API_KEY')
    openrouter_api_key: Optional[str] = Field(None, validation_alias='OPENROUTER_API_KEY')

    # Model IDs
    primary_model_id: str = "gpt-4o"
    cerebras_model_id: str = "llama-4-scout-17b-16e-instruct"
    mistral_model_id: str = "mistral-large-latest"
    openrouter_model_id: str = "anthropic/claude-3.5-sonnet"

    # Application Defaults
    default_branch_name: str = "hackathon-revamp"
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

settings = Settings()
