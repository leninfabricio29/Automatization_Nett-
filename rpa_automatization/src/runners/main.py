"""
Test flow for RPA automation.
Tests the complete login and session management flow.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils import AuthManager, BrowserManager
from config import DatabaseConfig, get_settings


async def test_login_flow():
    """Test the complete login and session management flow."""
    
    print("=" * 60)
    print("🚀 RPA Automation - Test Flow")
    print("=" * 60)
    
    # Initialize settings and database
    settings = get_settings()
    print(f"\n📋 Settings loaded:")
    print(f"  - ERP URL: {settings.login_url}")
    print(f"  - Environment: {settings.app_env}")
    print(f"  - Headless: {settings.playwright_headless}")
    
    # Test database connection
    print(f"\n🗄️  Testing database connection...")
    db_health = DatabaseConfig.health_check()
    if db_health:
        print("  ✅ Database connection OK")
    else:
        print("  ⚠️  Database connection failed (check your .env)")
    
    # Initialize browser
    print(f"\n🌐 Initializing browser...")
    browser_manager = BrowserManager()
    
    try:
        page = await browser_manager.initialize()
        
        # Initialize auth manager
        auth_manager = AuthManager()
        
        # Check if session already exists
        if auth_manager.session_exists():
            print(f"\n💾 Session found! Loading existing session...")
            success = await auth_manager.load_session(browser_manager.get_context())
            
            if success:
                # Try to navigate to ERP with existing session
                print(f"\n🔄 Navigating to ERP with existing session...")
                await page.goto(settings.login_url)
                await page.wait_for_load_state("networkidle")
                
                # Check if still logged in
                if settings.login_url not in page.url:
                    print(f"  ✅ Session is still valid!")
                    print(f"  📍 Current URL: {page.url}")
                else:
                    print(f"  ⚠️  Session expired, performing new login...")
                    await perform_login(auth_manager, page, browser_manager)
            else:
                await perform_login(auth_manager, page, browser_manager)
        else:
            print(f"\n🔐 No session found. Performing initial login...")
            await perform_login(auth_manager, page, browser_manager)
        
        # Take screenshot for verification
        print(f"\n📸 Taking screenshot...")
        await browser_manager.take_screenshot("./outputs/test_flow_screenshot.png")
        
        print(f"\n✅ Test flow completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test flow error: {e}")
        raise
    
    finally:
        print(f"\n🔌 Closing browser...")
        await browser_manager.close()


async def perform_login(auth_manager: AuthManager, page, browser_manager: BrowserManager):
    """
    Perform login and save session.
    
    Args:
        auth_manager: Authentication manager instance
        page: Playwright page object
        browser_manager: Browser manager instance
    """
    success = await auth_manager.login(page)
    
    if success:
        print(f"\n💾 Saving session...")
        await auth_manager.save_session(browser_manager.get_context())
        print(f"  ✅ Session saved!")
    else:
        print(f"  ⚠️  Login failed - check credentials in .env")


async def main():
    """Run the test flow."""
    try:
        await test_login_flow()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
