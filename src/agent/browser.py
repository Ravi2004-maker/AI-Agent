from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from src.utils.logger import setup_logger

logger = setup_logger("browser_manager")

class BrowserManager:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None

    def start(self):
        """Starts the Playwright browser session."""
        logger.info("Starting browser session...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        logger.info("Browser session started.")

    def close(self):
        """Closes the browser session."""
        logger.info("Closing browser session...")
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        logger.info("Browser session closed.")

    def goto(self, url: str):
        """Navigates to a URL."""
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        logger.info(f"Navigating to {url}")
        self.page.goto(url)
