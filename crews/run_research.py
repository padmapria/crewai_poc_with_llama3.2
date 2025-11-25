##crews/run_research.py
### Only runs the ResearchCrew in isolation
## Simple script for testing just the research analysis
from research_crew import ResearchCrew
import logging
from crewai import Process

def run_research_analysis(company: str = "AMZN"):
    """Execute the market research workflow"""
    try:
        logging.info(f"Initializing market research for {company}")
        
        # Initialize crew
        crew = ResearchCrew(company=company).create()
        
        # Execute tasks
        logging.info("Starting crew execution...")
        results = crew.kickoff()
        
        logging.info(f"Research completed for {company}")
        print(f"\nFinal Research Report:\n{results}")
        
        return results
        
    except Exception as e:
        logging.error(f"Error in research analysis: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Example usage - can be modified to accept command line arguments
    run_research_analysis(company="AMZN")