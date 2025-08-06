# config/llm_loader.py
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from config.settings import settings
from crewai import Agent, Crew, Task, Process
import yaml
from pathlib import Path


def load_yaml(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)

def get_llm(model_name: str, temperature: float, max_tokens: int):
    """Initialize LLM based on provider"""
    if settings.LLM_PROVIDER == "ollama":
        return Ollama(
            model=model_name,
            temperature=temperature,
            num_ctx=max_tokens,
            base_url=settings.OLLAMA_BASE_URL
        )
    elif settings.LLM_PROVIDER == "openai":
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=settings.OPENAI_API_KEY
        )
    else:
        raise ValueError(f"Unsupported provider: {settings.LLM_PROVIDER}")

def load_yaml_config(file_path: str) -> dict:
    """Load YAML configuration from file"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")
    
    with open(path, 'r') as file:
        return yaml.safe_load(file)

        
def create_agent(config_path: str) -> Agent:
    """Create agent with Ollama LLM"""
    config = load_yaml_config(config_path)
    
    llm_config = config.get("llm", {})
    llm = Ollama(
        model=llm_config["model"], 
        base_url=llm_config.get("base_url", "http://localhost:11434"),
        temperature=llm_config.get("temperature", 0.7)
    )
    
    return Agent(
        role=config["role"],
        goal=config["goal"],
        backstory=config["backstory"],
        llm=llm,
        tools=config.get("tools", []),
        verbose=config.get("verbose", True)
    )