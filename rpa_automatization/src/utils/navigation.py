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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NavigationManager:
    """Manages authentication and login for the ERP system."""
    
    async def navigation_turnos(self, page: Page) -> bool:
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
            
            # Click TurnsConf. button
            logger.info("Clicking 'Turnos Conf.'...")
            await page.get_by_role("option", name="Turnos Conf.").click()
            #await page.wait_for_load_state("networkidle")
            #await asyncio.sleep(2)
            await page.wait_for_timeout(200)
            # Click Configuración Turnos
            logger.info("Clicking 'Configuración Turnos'...")
            await page.get_by_role("button", name="Configuración Turnos").click()
            #await asyncio.sleep(2)
            await page.wait_for_timeout(200)
            # Click Turnos menu
            logger.info("Clicking 'Turnos' menu...")
            await page.get_by_role("menuitem", name="Turnos").click()
            #await asyncio.sleep(2)
            await page.wait_for_timeout(200)
            # Abrir/cerrar panel de búsqueda
            logger.info("Toggling search panel...")
            await page.get_by_title("Mostrar u ocultar panel de búsqueda").click()
            #await asyncio.sleep(2)
            await page.wait_for_timeout(200)
            # Seleccionar item
            logger.info("Selecting 'TurnosDiariosPorÁrea'...")
            await page.locator("[title='TurnosDiariosPorÁrea']").first.click()
            #await asyncio.sleep(2)
            await page.wait_for_timeout(300)

            await page.get_by_title("Mostrar u ocultar panel de búsqueda").click()
            #await asyncio.sleep(2)
            #await page.pause()
            # Marcar checkbox - MÚLTIPLES MÉTODOS
            logger.info("Selecting checkbox...")
            await page.locator(".o-checkbox").click()
            #await asyncio.sleep(2)
            await page.wait_for_timeout(200)
            #await self._click_checkbox_safe(page)
            
            # Acciones -> Exportar
            logger.info("Opening export dialog...")
            await page.get_by_role("button", name="Acciones").click()
            #await asyncio.sleep(2)
            await page.wait_for_timeout(200)
            await page.get_by_role("menuitem", name="Exportar").click()
            #await asyncio.sleep(2)
            await page.wait_for_timeout(200)

            # Configurar exportación
            logger.info("Configuring export options...")
            await page.get_by_role("checkbox", name="Deseo actualizar datos (").check()
            #await asyncio.sleep(2)
            await page.wait_for_timeout(200)
            await page.get_by_role("radio", name="CSV").check()
            #await asyncio.sleep(2)
            await page.wait_for_timeout(200)
            await page.get_by_role("combobox").select_option("90")
            #await asyncio.sleep(2)
            await page.wait_for_timeout(200)
            # Iniciar exportación
            logger.info("Starting export...")
            await page.get_by_role("button", name="Exportar").click()
            
            # Esperar completación
            #await page.wait_for_load_state("networkidle")
            #await asyncio.sleep(4)

            logger.info("✅ Export successful")
            
            
            # 2. Preparar carpeta downloads
            downloads_path = Path("./downloads")
            downloads_path.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = downloads_path / f"turnos_{timestamp}.csv"

            # 3. Capturar descarga
            async with page.expect_download() as download_info:
                await page.get_by_role("button", name="Exportar").click()
                #await page.click("text=Exportar CSV")  # o selector real

            download = await download_info.value

            # 4. Guardar archivo físicamente
            await download.save_as(file_path)

            print(f"📥 CSV guardado en: {file_path}")

            logger.info("✅ Save csv successful")
            return True
        
        except Exception as e:
            logger.error(f"❌ Export error: {e}")
            return False
    
    async def _click_checkbox_safe(self, page: Page):
        """Safe checkbox clicking with multiple fallbacks"""
        methods = [
            # Método 0: Label específico
            #lambda: page.locator('label[for="checkbox-comp-142"]').click(),
            #funciona
            #lambda: page.get_by_role("row", name="Display Name Area  Usuario").get_by_label("", exact=True).check(),
            # Método 1: Input checkbox
            lambda:  page.locator(".o-checkbox").click(),
            # Método 2: Input checkbox
            lambda: page.locator(".o_group_caret").first.click(),
            # Método 3: Input checkbox
            lambda: page.locator(".o-checkbox").first.uncheck(),
            # Método 4: Input checkbox
            lambda: page.get_by_label("", exact=True).check(),
            # Método 5: Input checkbox-Funciona
            lambda: page.locator('input[type="checkbox"]').first.click(),
            # Método 6: Set checked
            lambda: page.locator('input[type="checkbox"]').first.set_checked(True),
            # Método 7: Force click
            lambda: page.locator('input[type="checkbox"]').first.click(force=True),
        ]
        
        for i, method in enumerate(methods, 1):
            try:
                await method()
                await asyncio.sleep(0.5)
                # Verificar
                is_checked = await page.locator('input[type="checkbox"]').first.is_checked()
                if is_checked:
                    logger.info(f"Checkbox selected with method {i}")
                    return
            except Exception as e:
                logger.debug(f"Method {i} failed: {e}")
        
        logger.error("All checkbox methods failed")
    
    

