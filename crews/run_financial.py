##crews/run_financial.py
### Only runs the FinancialCrew in isolation
## Simple script for testing just the financial analysis

from financial_crew import FinancialCrew
import logging
from crewai import Process

def run_financial_analysis(company: str = "AMZN"):
    """Execute the financial analysis workflow"""
    try:
        logging.info(f"Initializing financial analysis for {company}")
        
        # Initialize crew
        crew = FinancialCrew(company=company).create()
        
        # Execute tasks
        logging.info("Starting crew execution...")
        results = crew.kickoff()
        
        logging.info(f"Analysis completed for {company}")
        print(f"\nFinal Output:\n{results}")
        
        return results
        
    except Exception as e:
        logging.error(f"Error in financial analysis: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Example usage (can modify to accept command line args)
    run_financial_analysis(company="AMZN")