from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Core LLM Configuration
    LLM_PROVIDER: str = "ollama"
    DEFAULT_LLM: str = "ollama/llama3.2:1b"  
    FALLBACK_LLM: str = "gemma3:1b"
    VERBOSE: bool = True

    # Ollama Configuration
    OLLAMA_MODEL: str = "ollama/llama3.2:1b"  
    OLLAMA_FALLBACK_MODEL: str = "gemma3:1b"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_NUM_CTX: int = 1024

    # Performance Settings
    MAX_TOKENS: int = 1024
    GENERIC_MAX_TOKENS: int = 2048
    TEMPERATURE: float = 0.5

    # Other Providers
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-1106-preview"
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_MODEL: str = "deepseek-chat"

    # Tool Configurations
    SEC_API_KEY: Optional[str] = None
    ALPHAVANTAGE_API_KEY: Optional[str] = None

    # Agent-Specific Overrides
    WRITING_LLM_MODEL: str = "llama3.2:1b"
    WRITING_LLM_TEMPERATURE: float = 0.3
    WRITING_LLM_MAX_TOKENS: int = 512

    FINANCIAL_LLM_MODEL: str = "ollama/llama3.2:1b"  
    FINANCIAL_LLM_TEMPERATURE: float = 0.4
    FINANCIAL_LLM_MAX_TOKENS: int = 512

    RESEARCH_LLM_MODEL: str = "llama3.2:1b"
    RESEARCH_LLM_TEMPERATURE: float = 0.4
    RESEARCH_LLM_MAX_TOKENS: int = 512

    class Config:
        env_file = ".env"
        extra = "ignore"  # This will ignore extra env vars without raising errors

settings = Settings()