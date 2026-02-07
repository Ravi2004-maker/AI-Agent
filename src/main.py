import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.core import Agent
from src.utils.logger import setup_logger

logger = setup_logger("main")

def main():
    logger.info("Agent starting...")
    # Default to example.com if no URL provided
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"

    agent = Agent(headless=True)
    try:
        title = agent.run(url)
        logger.info(f"Successfully visited {url}. Title: {title}")
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
