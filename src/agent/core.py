from urllib.parse import urlparse

from src.agent.browser import BrowserManager
from src.agent.config import AgentConfig
from src.utils.logger import setup_logger

logger = setup_logger("agent_core")

class Agent:
    def __init__(self, config: AgentConfig | None = None):
        self.config = config or AgentConfig.from_env()
        self.browser_manager = BrowserManager(config=self.config)

    def run(self, url: str, timeout_ms: int | None = None):
        """Executes the agent's main loop (demonstration)."""
        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string.")
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL provided: {url}")
        navigation_timeout = timeout_ms or self.config.navigation_timeout_ms
        try:
            self.browser_manager.start()
            self.browser_manager.goto(url, timeout_ms=navigation_timeout)
            page_title = self.browser_manager.page.title()
            logger.info(f"Page title: {page_title}")
            return page_title
        except Exception as e:
            logger.error(f"Error running agent: {e}")
            raise
        finally:
            self.browser_manager.close()
