"""
Authentication module for Playwright browser automation.
Handles login functionality and session management.
"""

from playwright.async_api import Browser, BrowserContext, Page
import json
from pathlib import Path
from config.settings import get_settings


class AuthManager:
    """Manages authentication and login for the ERP system."""
    
    def __init__(self):
        """Initialize authentication manager with settings."""
        self.settings = get_settings()
        self.login_url = self.settings.login_url
        self.username = self.settings.login_username
        self.password = self.settings.login_password
        self.session_storage_path = Path(self.settings.session_storage_path)
    
    def get_session_file(self) -> Path:
        """
        Get path to session storage file.
        
        Returns:
            Path: Path to the session JSON file
        """
        self.session_storage_path.mkdir(parents=True, exist_ok=True)
        return self.session_storage_path / "auth_state.json"
    
    async def login(self, page: Page) -> bool:
        """
        Perform login on the ERP system.
        
        Args:
            page: Playwright page object
            
        Returns:
            bool: True if login was successful
        """
        try:
            # Navigate to login page
            await page.goto(self.login_url)
            await page.wait_for_load_state("networkidle")
            
            # Find and fill username field
            username_field = page.get_by_role("textbox", name="Correo electrónico")
            await username_field.click()
            await username_field.fill(self.username)
            
            # Find and fill password field
            password_field = page.get_by_role("textbox", name="Contraseña Restablecer")
            await password_field.click()
            await password_field.fill(self.password)
            
            # Click login button
            login_button = page.get_by_role("button", name="Iniciar sesión")
            await login_button.click()
            
            # Wait for navigation after login
            await page.wait_for_load_state("networkidle")
            
            # Check if login was successful (URL changed or success element present)
            if page.url == self.login_url:
                print("❌ Login failed - URL did not change")
                return False
            
            print("✅ Login successful")
            return True
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    async def save_session(self, context: BrowserContext) -> None:
        """
        Save authentication cookies and storage to file.
        
        Args:
            context: Playwright browser context
        """
        try:
            state = await context.storage_state(path=str(self.get_session_file()))
            print(f"✅ Session saved to {self.get_session_file()}")
        except Exception as e:
            print(f"❌ Error saving session: {e}")
    
    async def load_session(self, context: BrowserContext) -> bool:
        """
        Load authentication cookies and storage from file.
        
        Args:
            context: Playwright browser context
            
        Returns:
            bool: True if session was loaded successfully
        """
        session_file = self.get_session_file()
        
        if not session_file.exists():
            print(f"⚠️  Session file not found: {session_file}")
            return False
        
        try:
            await context.add_init_script(
                f"window.localStorage.setItem('sessionData', {json.dumps(json.load(open(session_file)))})"
            )
            
            # Load cookies
            with open(session_file, 'r') as f:
                state = json.load(f)
                if "cookies" in state:
                    await context.add_cookies(state["cookies"])
            
            print("✅ Session loaded from file")
            return True
            
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return False
    
    def session_exists(self) -> bool:
        """
        Check if a valid session file exists.
        
        Returns:
            bool: True if session file exists
        """
        return self.get_session_file().exists()
    
    def clear_session(self) -> None:
        """Delete the saved session file."""
        session_file = self.get_session_file()
        if session_file.exists():
            session_file.unlink()
            print(f"✅ Session cleared: {session_file}")
