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


class ContractsNavigationManager:
    """Manages authentication and login for the ERP system."""
    
    async def navigation_contracts(self, page: Page) -> bool:
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
            
            # Click Contratos button
            logger.info("Clicking 'Contratos'...")
            await page.get_by_role("option", name="Contratos").click()
            #await page.wait_for_load_state("networkidle")
            #await asyncio.sleep(2)
        
            # Abrir/cerrar panel de búsqueda
            logger.info("Toggling search panel...")
            await page.get_by_title("Mostrar u ocultar panel de búsqueda").click()
            #await asyncio.sleep(2)
            
            # Seleccionar item
            logger.info("Selecting 'Filtros compartidos'")
            await page.get_by_role("button", name="Filtros compartidos").click()
            #await asyncio.sleep(2)
            
            # Seleccionar filtro creado
            logger.info("Selecting filter")
            await page.get_by_text("ContratosHoy").click()
            #await asyncio.sleep(2)
            await page.wait_for_timeout(300)
            # Ocultar panel de búsqueda
            await page.get_by_title("Mostrar u ocultar panel de búsqueda").click()
            #await asyncio.sleep(2)
            #await page.pause()
            await page.wait_for_timeout(300)
            # Marcar checkbox - MÚLTIPLES MÉTODOS
            logger.info("Selecting checkbox...")
            await page.locator(".o-checkbox").click()
            #await asyncio.sleep(2)
            #await self._click_checkbox_safe(page)
            
            # Acciones -> Exportar
            logger.info("Opening export dialog...")
            await page.get_by_role("button", name="Acciones").click()
            #await asyncio.sleep(2)
            await page.get_by_role("menuitem", name="Exportar").click()
            #await asyncio.sleep(2)
            
            # Configurar exportación
            logger.info("Configuring export options...")
            await page.get_by_role("checkbox", name="Deseo actualizar datos (").check()
            #await asyncio.sleep(2)
            await page.get_by_role("radio", name="CSV").check()
            #await asyncio.sleep(2)
            
            await page.get_by_role("combobox").select_option("446")
            #await asyncio.sleep(2)
            await page.wait_for_timeout(300)
            # Iniciar exportación
            logger.info("Starting export...")
            await page.get_by_role("button", name="Exportar").click()
            
            # Esperar completación
            #await page.wait_for_load_state("networkidle")
            #await asyncio.sleep(4)

            logger.info("✅ Export successful")
            
            
            # 2. Preparar carpeta downloads
            downloads_path = Path("./downloads/contracts")
            downloads_path.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = downloads_path / f"contratos_{timestamp}.csv"

            # 3. Capturar descarga
            async with page.expect_download() as download_info:
                await page.get_by_role("button", name="Exportar").click()
                #await page.click("text=Exportar CSV")  # o selector real

            download = await download_info.value

            # 4. Guardar archivo físicamente
            await download.save_as(str(file_path))

            print(f"📥 CSV guardado en: {file_path}")

            logger.info("✅ Save csv successful")
            return True
        
        except Exception as e:
            logger.error(f"❌ Export error: {e}")
            return False
    
    
    
    

