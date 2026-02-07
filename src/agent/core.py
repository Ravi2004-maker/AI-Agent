from src.agent.browser import BrowserManager
from src.utils.logger import setup_logger

logger = setup_logger("agent_core")

class Agent:
    def __init__(self, headless: bool = True):
        self.browser_manager = BrowserManager(headless=headless)

    def run(self, url: str):
        """Executes the agent's main loop (demonstration)."""
        try:
            self.browser_manager.start()
            self.browser_manager.goto(url)
            page_title = self.browser_manager.page.title()
            logger.info(f"Page title: {page_title}")
            return page_title
        except Exception as e:
            logger.error(f"Error running agent: {e}")
            raise
        finally:
            self.browser_manager.close()
