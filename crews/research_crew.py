##crews/research_crew.py
from crewai import Agent, Crew, Task, Process
from config.settings import settings
from config.llm_loader import create_agent, load_yaml_config
from pathlib import Path
import logging
from datetime import datetime

class ResearchCrew:
    def __init__(self, company: str):
        self.company = company
        self.logger = logging.getLogger(__name__)
        
        # Initialize agents with proper LLM configs
        self.writer = create_agent('config/agents/content_writer.yaml')
        self.researcher = create_agent('config/agents/research_analyst.yaml')
        
        if settings.VERBOSE:
            print(f"\nResearch Crew LLM Configurations:")
            print(f"Writer: {self.writer.llm.model} (temp: {self.writer.llm.temperature})")
            print(f"Researcher: {self.researcher.llm.model} (temp: {self.researcher.llm.temperature})")

    def create(self) -> Crew:
        """Create and configure the research crew with enhanced output handling"""
        # Load task configs
        research_config = load_yaml_config('config/tasks/research.yaml')
        report_config = load_yaml_config('config/tasks/report_writing.yaml')

        # Prepare output directory
        self._prepare_output_directory()

        research_task = Task(
        description=f"Create ethical analysis framework for {self.company}",
        agent=self.researcher,
        expected_output="Methodology guide with placeholder examples",
        config={
            'allow_delegation': False,
            'tools': [],
            'constraints': [
                "Only demonstrate analysis techniques",
                "Use placeholder values for all calculations"
            ]
            }
        )
        
        report_task = Task(
            description=report_config['description'].format(company=self.company),
            agent=self.writer,
            context=[research_task],
            expected_output=report_config['expected_output'],
            config={
                'allow_delegation': report_config.get('allow_delegation', False),
                'tools': report_config.get('tools', [])
            },
            output_file=self._generate_output_filename('md')  # Updated file handling
        )
        
        return Crew(
            agents=[self.researcher, self.writer],
            tasks=[research_task, report_task],
            process=Process.sequential,
            verbose=settings.VERBOSE,
            memory=False
        )

    def _prepare_output_directory(self):
        """Ensure reports directory exists"""
        Path("reports").mkdir(exist_ok=True)
        self.logger.info(f"Output directory prepared at {Path('reports').absolute()}")

    def _generate_output_filename(self, extension: str) -> str:
        """Generate timestamped filename with company name"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/{self.company}_research_{timestamp}.{extension}"
        self.logger.info(f"Output will be saved to {filename}")
        return filename

    def run(self) -> dict:
        """Execute the research crew and return results"""
        try:
            crew = self.create()
            results = crew.kickoff()
            
            # Save additional formatted versions
            self._save_additional_formats(results)
            
            return {
                "status": "success",
                "company": self.company,
                "output_file": self._generate_output_filename('md'),
                "timestamp": datetime.now().isoformat(),
                "results": results
            }
            
        except Exception as e:
            self.logger.error(f"Research failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "company": self.company,
                "timestamp": datetime.now().isoformat()
            }

    def _save_additional_formats(self, content: str):
        """Save report in multiple formats"""
        try:
            # Save as text file
            txt_file = self._generate_output_filename('txt')
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Optionally save as PDF (requires fpdf)
            if settings.SAVE_PDF:
                try:
                    from fpdf import FPDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, txt=content)
                    pdf.output(self._generate_output_filename('pdf'))
                except ImportError:
                    self.logger.warning("PDF generation skipped - fpdf not installed")
                    
        except Exception as e:
            self.logger.error(f"Failed to save additional formats: {str(e)}")