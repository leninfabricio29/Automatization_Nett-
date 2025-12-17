"""
Browser manager for Playwright automation.
Handles browser initialization and context creation.
"""

from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from config.settings import get_settings


class BrowserManager:
    """Manages Playwright browser instance and contexts."""
    
    def __init__(self):
        """Initialize browser manager with settings."""
        self.settings = get_settings()
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
    
    async def initialize(self) -> Page:
        """
        Initialize browser and create a new context.
        
        Returns:
            Page: Playwright page object ready to use
        """
        try:
            playwright = await async_playwright().start()
            
            # Launch browser
            self.browser = await playwright.chromium.launch(
                headless=self.settings.playwright_headless,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )
            
            # Create context with custom settings
            self.context = await self.browser.new_context()
            
            # Create page
            self.page = await self.context.new_page()
            
            # Set timeout for all operations
            self.page.set_default_timeout(self.settings.playwright_timeout)
            
            print("✅ Browser initialized successfully")
            return self.page
            
        except Exception as e:
            print(f"❌ Browser initialization error: {e}")
            raise
    
    async def close(self) -> None:
        """Close browser and clean up resources."""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            print("✅ Browser closed successfully")
        except Exception as e:
            print(f"❌ Error closing browser: {e}")
    
    async def take_screenshot(self, filename: str = "screenshot.png") -> None:
        """
        Take a screenshot of the current page.
        
        Args:
            filename: Name of the screenshot file
        """
        try:
            await self.page.screenshot(path=filename)
            print(f"✅ Screenshot saved: {filename}")
        except Exception as e:
            print(f"❌ Error taking screenshot: {e}")
    
    def get_page(self) -> Page:
        """Get current page object."""
        return self.page
    
    def get_context(self) -> BrowserContext:
        """Get current browser context."""
        return self.context
