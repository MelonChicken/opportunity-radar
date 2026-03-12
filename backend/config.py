"""
Centralized configuration management for Research Radar.
Uses Pydantic Settings for type-safe environment variable loading.
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo-1106"
    
    # Data Directories
    data_dir: Path = Path(__file__).parent.parent / "data"
    
    # RSS Feed Configuration
    rss_feed_url: str = "https://feeds.feedburner.com/GlobalPressRoom"
    
    # Pipeline Configuration
    max_signals_per_report: int = 20
    min_sentence_length: int = 20
    max_sentence_length: int = 500
    
    # LLM Parameters
    llm_timeout: int = 30
    llm_max_retries: int = 3
    
    # Logging
    log_level: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def reports_file(self) -> Path:
        """Path to reports.json file."""
        return self.data_dir / "reports.json"
    
    @property
    def cards_file(self) -> Path:
        """Path to cards.json file."""
        return self.data_dir / "cards.json"
    
    @property
    def discarded_file(self) -> Path:
        """Path to discarded_signals.json file."""
        return self.data_dir / "discarded_signals.json"


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance (singleton pattern).
    
    Returns:
        Settings: The application settings
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# Export commonly used paths
def get_data_dir() -> Path:
    """Get the data directory path."""
    return get_settings().data_dir


def get_openai_api_key() -> Optional[str]:
    """Get the OpenAI API key."""
    return get_settings().openai_api_key
