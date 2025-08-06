# main.py
from flows.financial_flow import FinancialFlow
import logging
from typing import Dict, Any

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('financial_flow.log'),
            logging.StreamHandler()
        ]
    )

def main(company: str = "AMZN") -> Dict[str, Any]:
    try:
        configure_logging()
        logging.info(f"Initializing financial flow for {company}")
        
        flow = FinancialFlow(company=company)
        results = flow.execute()
        
        logging.info(f"Flow completed successfully for {company}")
        print(f"\nFinal Results:\n{results}")
        return results
        
    except Exception as e:
        logging.error(f"Flow execution failed: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    import sys
    company = sys.argv[1] if len(sys.argv) > 1 else "AMZN"
    main(company)