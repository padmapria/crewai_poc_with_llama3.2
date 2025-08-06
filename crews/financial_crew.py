from crewai import Agent, Crew, Task, Process
from config.settings import settings
from config.llm_loader import create_agent  # Use centralized agent creation
from config.llm_loader import load_yaml_config 

class FinancialCrew:
    def __init__(self, company: str = "Unspecified"):
        self.company = company
        
        # Initialize agents with proper LLM configs
        self.writer = create_agent('config/agents/content_writer.yaml')
        self.analyst = create_agent('config/agents/financial_analyst.yaml')
        
        if settings.VERBOSE:
            print(f"\nFinancial Crew LLM Configurations:")
            print(f"Writer: {self.writer.llm.model} (temp: {self.writer.llm.temperature})")
            print(f"Analyst: {self.analyst.llm.model} (temp: {self.analyst.llm.temperature})")

    def create(self) -> Crew:
        # Load task configs properly
        analysis_config = load_yaml_config('config/tasks/analysis.yaml')
        report_config = load_yaml_config('config/tasks/report_writing.yaml')

        analysis_task = Task(
            description=analysis_config['description'].format(company=self.company),
            agent=self.analyst,
            expected_output=analysis_config['expected_output'],
            config={
                'allow_delegation': analysis_config.get('allow_delegation', False),
                'tools': analysis_config.get('tools', [])
            }
        )
        
        report_task = Task(
            description=report_config['description'].format(company=self.company),
            agent=self.writer,
            context=[analysis_task],
            expected_output=report_config['expected_output'],
            config={
                'allow_delegation': report_config.get('allow_delegation', False),
                'tools': report_config.get('tools', [])
            },
            output_file=f"reports/{self.company}_financial.md"
        )
        
        return Crew(
            agents=[self.analyst, self.writer],
            tasks=[analysis_task, report_task],
            process=Process.sequential,
            verbose=settings.VERBOSE,
            memory=False
        )