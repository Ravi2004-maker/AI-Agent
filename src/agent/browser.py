from typing import Optional

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from src.agent.config import AgentConfig
from src.utils.logger import setup_logger

logger = setup_logger("browser_manager")

class BrowserManager:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None

    def start(self):
        """Starts the Playwright browser session."""
        if self.playwright:
            raise RuntimeError("Browser session already started.")
        logger.info("Starting browser session...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.config.headless)
        context_options = {}
        if self.config.user_agent:
            context_options["user_agent"] = self.config.user_agent
        if self.config.viewport:
            width, height = self.config.viewport
            context_options["viewport"] = {"width": width, "height": height}
        self.context = self.browser.new_context(**context_options)
        self.page = self.context.new_page()
        self.context.set_default_timeout(self.config.default_timeout_ms)
        logger.info("Browser session started.")

    def close(self):
        """Closes the browser session."""
        logger.info("Closing browser session...")
        errors = []
        if self.context:
            try:
                self.context.close()
            except Exception as exc:
                errors.append(exc)
        if self.browser:
            try:
                self.browser.close()
            except Exception as exc:
                errors.append(exc)
        if self.playwright:
            try:
                self.playwright.stop()
            except Exception as exc:
                errors.append(exc)
        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None
        if errors:
            for exc in errors:
                logger.warning("Error while closing browser session: %s", exc)
        logger.info("Browser session closed.")

    def goto(self, url: str, timeout_ms: Optional[int] = None):
        """Navigates to a URL."""
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        logger.info(f"Navigating to {url}")
        self.page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
