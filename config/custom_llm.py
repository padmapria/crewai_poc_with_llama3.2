from langchain_community.llms import Ollama
from crewai.agents import Agent

class OllamaAgent(Agent):
    def __init__(self, model: str, **kwargs):
        llm = Ollama(
            model=model,
            base_url="http://localhost:11434",
            temperature=kwargs.pop('temperature', 0.7)
        )
        super().__init__(llm=llm, **kwargs)