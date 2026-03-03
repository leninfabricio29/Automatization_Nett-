"""
Authentication module for Playwright browser automation.
Handles login functionality and session management.
"""

from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import json
from pathlib import Path
from config.settings import get_settings

import asyncio
import logging
from datetime import datetime
import pandas as pd
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VisitsNavigationManager:
    """Manages authentication and login for the ERP system."""
    
    async def navigation_visits(self, page: Page) -> bool:
        """
        Perform navigation and export in Odoo.
        
        Args:
            page: Playwright page object
            
        Returns:
            bool: True if export was successful
        """
        try:
            # Configurar timeout
            #page.set_default_timeout(30000)

            # Click Helpdesk button
            logger.info("Clicking 'Helpdesk'...")
            await page.get_by_role("option", name="Helpdesk").click()
            #await page.wait_for_load_state("networkidle")
            #await asyncio.sleep(2)
            # Navegar a Tickets -> All Tickets
            logger.info("Navigating to 'Tickets' -> 'All Tickets'...")
            await page.get_by_role("button", name="Tickets", exact=True).click()
            
            await page.get_by_role("menuitem", name="All Tickets").click()
            await page.wait_for_timeout(200)
            # Abrir/cerrar panel de búsqueda
            
            logger.info("Toggling search panel...")
            await page.get_by_title("Mostrar u ocultar panel de búsqueda").click()
            
            
            # Seleccionar item
            logger.info("Selecting 'Filtros compartidos'")
            await page.get_by_role("button", name="Filtros compartidos").click()
            
            
            # Seleccionar filtro creado
            logger.info("Selecting filter")
            await page.get_by_text("TicketsHoy", exact=True).click()
            

            # Ocultar panel de búsqueda
            logger.info("Toggling search panel...")
            await page.get_by_title("Mostrar u ocultar panel de búsqueda").click()
            await page.wait_for_timeout(300)
            #await page.pause()
            # Marcar checkbox - MÚLTIPLES MÉTODOS
            logger.info("Selecting checkbox...")
            await page.locator(".o-checkbox").click()
            
            #await self._click_checkbox_safe(page)
            
            # Acciones -> Exportar
            logger.info("Opening export dialog...")
            await page.get_by_role("button", name="Acciones").click()
           
            await page.get_by_role("menuitem", name="Exportar").click()
            
            
            # Configurar exportación
            logger.info("Configuring export options...")
            await page.get_by_role("checkbox", name="Deseo actualizar datos (").check()
            
            await page.get_by_role("radio", name="CSV").check()
            
            
            await page.get_by_role("combobox").select_option("431")
            await page.wait_for_timeout(300)
            
            # Iniciar exportación
            logger.info("Starting export...")
             # 1. Preparar carpeta downloads
            downloads_path = Path("./downloads/visits")
            downloads_path.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = downloads_path / f"visits_{timestamp}.csv"
            # 2. Capturar descarga
            async with page.expect_download() as download_info:
                await page.get_by_role("button", name="Exportar").click()
                #await page.click("text=Exportar CSV")  # o selector real

            download = await download_info.value

            # 3. Guardar archivo físicamente
            await download.save_as(str(file_path))

            print(f"📥 CSV guardado en: {file_path}")

            logger.info("✅ Export and Save csv successful")
            return True
        
        except Exception as e:
            logger.error(f"❌ Export error: {e}")
            return False
    
    
    
    

