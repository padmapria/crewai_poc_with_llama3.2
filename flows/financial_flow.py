from typing import Dict, Any, Optional
from crews.financial_crew import FinancialCrew
from crews.research_crew import ResearchCrew
from config.settings import settings
import logging
from datetime import datetime
from pathlib import Path

class FinancialFlow:
    def __init__(self, company: str):
        self.company = company
        self.logger = logging.getLogger(__name__)
        self._initialize_crews()
        self._setup_directories()

    def _setup_directories(self):
        """Ensure required directories exist"""
        Path("reports").mkdir(exist_ok=True)

    def _initialize_crews(self):
        """Lazy initialization"""
        self._financial_crew = None
        self._research_crew = None

    @property
    def financial_crew(self) -> FinancialCrew:
        if not self._financial_crew:
            self._financial_crew = FinancialCrew(self.company)
            self.logger.info(f"Initialized FinancialCrew for {self.company}")
        return self._financial_crew

    @property
    def research_crew(self) -> ResearchCrew:
        if not self._research_crew:
            self._research_crew = ResearchCrew(self.company)
            self.logger.info(f"Initialized ResearchCrew for {self.company}")
        return self._research_crew

    def execute(self) -> Dict[str, Any]:
        """Orchestrate financial analysis pipeline"""
        results = {
            "company": self.company,
            "timestamp": datetime.now().isoformat(),
            "financial": None,
            "research": None,
            "status": "success"
        }
        
        try:
            # Phase 1: Core Financial Analysis
            financial_data = self._execute_financial_analysis()
            results["financial"] = str(financial_data)
            
            # Phase 2: Conditional Research
            try:
                if self._requires_research(financial_data):
                    research_data = self._execute_market_research()
                    results["research"] = str(research_data)
                else:
                    results["research"] = {"status": "skipped"}
            except Exception as research_error:
                results["research"] = {"status": "failed", "error": str(research_error)}
                results["status"] = "partial_success"
                
            return results
            
        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {str(e)}")
            results["status"] = "failed"
            results["error"] = str(e)
            return results

    def _execute_financial_analysis(self) -> Any:
        """Execute financial crew with enhanced logging"""
        self.logger.info("Starting financial analysis...")
        return self.financial_crew.create().kickoff()

    def _execute_market_research(self) -> Any:
        """Execute research crew with enhanced logging"""
        self.logger.info("Starting market research...")
        return self.research_crew.create().kickoff()

    def _requires_research(self, financial_data: Any) -> bool:
        """Determine if research phase should execute"""
        # Convert CrewOutput to dict if possible
        data = getattr(financial_data, "dict", lambda: {})()
        return data.get("needs_research", True)  # Default to True if unsure