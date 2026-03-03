"""
Navigation module for RPA automation.
Handles navigation to specific modules in the ERP system.
"""

from playwright.async_api import Page, Locator
from typing import Optional
import logging
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


class NavigationManager:
    """Manages navigation between modules in the ERP system."""
    
    def __init__(self, page: Page):
        """
        Initialize navigation manager.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.output_dir = Path("./outputs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    async def wait_for_element(self, selector: str, timeout: int = 3000) -> Optional[Locator]:
        """
        Wait for an element to be visible.
        
        Args:
            selector: CSS selector
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            Optional[Locator]: Element if found, None otherwise
        """
        try:
            element = self.page.locator(selector).first
            await element.wait_for(state="visible", timeout=timeout)
            return element
        except Exception:
            return None
    
    async def click_by_text(self, text: str, exact: bool = True) -> bool:
        """
        Click on an element by its text content.
        
        Args:
            text: Text to search for
            exact: Whether to match exact text
            
        Returns:
            bool: True if clicked successfully
        """
        try:
            element = self.page.get_by_text(text, exact=exact)
            await element.wait_for(state="visible", timeout=3000)
            await element.click()
            await self.page.wait_for_load_state("networkidle")
            logger.info(f"Clicked: '{text}'")
            return True
        except Exception as e:
            logger.warning(f"Could not click '{text}': {e}")
            return False    
    
    async def navigate_to_turnos_conf(self) -> bool:
        """
        Navigate to the 'Turnos Conf.' module.
        
        Returns:
            bool: True if navigation successful
        """
        
        #logger.info("Navigating to 'Turnos Conf.' module...")
        
        # Try to find and click the module
        if await self.click_by_text("Turnos Conf."):
            return True
        

       
        # Click login button
        #configuration_turnos_button = page.get_by_role("button", name="Configuración Turnos")
        #await configuration_turnos_button.click()
        if await self.click_by_text("Configuración Turnos"):
            return True
        if await self.click_by_text("Turnos"):
            return True
        if await self.click_by_text("Buscar..."):
            return True
        
        if await self.click_by_text("TurnosDiariosPorÁrea"):
            return True
        # If not found, try with Apps menu
        logger.info("Trying via Apps menu...")
        
        # Open Apps menu
        apps_button = await self.wait_for_element('button[title="Configuración Turnos"]')
        if apps_button:
            await apps_button.click()
            
            # Search for module
            search_input = await self.wait_for_element('input[placeholder="Configuración Turnos"]')
            if search_input:
                await search_input.fill("Turnos Conf.")
                
                # Click the module
                module_element = await self.wait_for_element('.o_app:has-text("Configuración Turnos")')
                if module_element:
                    await module_element.click()
                    await self.page.wait_for_load_state("networkidle")
                    logger.info("Successfully navigated to 'Turnos Conf.' via Apps menu")
                    return True
        
        logger.error("Could not find 'Turnos Conf.' module")
        return False
    
    async def navigate_to_configuracion_turnos(self) -> bool:
        """
        Navigate to 'Configuración Turnos' from within Turnos Conf. module.
        
        Returns:
            bool: True if navigation successful
        """
        logger.info("Navigating to 'Configuración Turnos'...")
        
        login_button = page.get_by_role("button", name="Configuración Turnos")
        await login_button.click()
        
        # Look in dropdown menus
        dropdowns = self.page.locator('.dropdown-toggle, .oe_secondary_menu_section')
        for i in range(await dropdowns.count()):
            dropdown = dropdowns.nth(i)
            if await dropdown.is_visible():
                text = await dropdown.text_content()
                if "Configuración" in text or "Turnos" in text:
                    await dropdown.click()
                    
                    # Look for the item in dropdown
                    menu_item = self.page.locator('.dropdown-menu a:has-text("Configuración Turnos")').first
                    if await menu_item.is_visible():
                        await menu_item.click()
                        await self.page.wait_for_load_state("networkidle")
                        logger.info("Found in dropdown menu")
                        return True
        
        logger.error("Could not find 'Configuración Turnos'")
        return False
    
    async def navigate_to_turnos(self) -> bool:
        """
        Navigate to 'Turnos' from within Configuración Turnos.
        
        Returns:
            bool: True if navigation successful
        """
        logger.info("Navigating to 'Turnos'...")
        
        # Try exact text first
        if await self.click_by_text("Turnos", exact=True):
            return True
        
        # Try partial match
        if await self.click_by_text("Turnos", exact=False):
            return True
        
        # Look in the secondary menu
        menu_items = self.page.locator('.oe_secondary_submenu a')
        for i in range(await menu_items.count()):
            item = menu_items.nth(i)
            text = await item.text_content()
            if "Turnos" in text.strip():
                await item.click()
                await self.page.wait_for_load_state("networkidle")
                logger.info("Found in secondary menu")
                return True
        
        logger.error("Could not find 'Turnos'")
        return False
    
    async def take_screenshot(self, step_name: str) -> bool:
        """
        Take a screenshot of the current page.
        
        Args:
            step_name: Name for the screenshot file
            
        Returns:
            bool: True if screenshot taken successfully
        """
        try:
            filepath = self.output_dir / f"{step_name}.png"
            await self.page.screenshot(path=str(filepath))
            logger.info(f"Screenshot saved: {filepath}")
            return True
        except Exception as e:
            logger.warning(f"Could not take screenshot: {e}")
            return False
    
    async def complete_turnos_navigation(self) -> bool:
        """
        Complete navigation flow: Turnos Conf. > Configuración Turnos > Turnos.
        
        Returns:
            bool: True if all steps successful
        """
        logger.info("Starting Turnos navigation flow...")
        
        # Step 1: Navigate to Turnos Conf.
        if not await self.navigate_to_turnos_conf():
            return False
        
        await self.take_screenshot("01_turnos_conf")
        
        # Step 2: Navigate to Configuración Turnos
        if not await self.navigate_to_configuracion_turnos():
            return False
        
        await self.take_screenshot("02_configuracion_turnos")
        
        # Step 3: Navigate to Turnos
        if not await self.navigate_to_turnos():
            return False
        
        await self.take_screenshot("03_turnos_final")
        
        logger.info("Turnos navigation completed successfully!")
        return True