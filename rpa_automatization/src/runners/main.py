"""
Test flow for RPA automation.
Tests the complete login and session management flow.
"""

import asyncio
import sys
from pathlib import Path
from turtle import update

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils import AuthManager, BrowserManager, NavigationManager, ContractsNavigationManager, VisitsNavigationManager
from config import DatabaseConfig, get_settings

#
from datetime import datetime, UTC
from etl.reader import read_turnos_csv, get_latest_turnos_csv
from etl.reader_contracts import read_contracts_csv, get_latest_contracts_csv
from etl.reader_visits import read_visits_csv, get_latest_visits_csv
from etl.transformer import transform_turnos, transform_contracts, transform_visits
from etl.repository import save_turnos, save_contracts, save_visits
from etl.metrics.turns_metrics import calcular_metricas_turnos
from etl.metrics.turns_metrics import agrupar_turnos_por_area
from etl.repository_metrics import save_metricas_mensuales

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
        #await asyncio.sleep(1)
        await page.wait_for_timeout(200)
        # Initialize navigation manager
        navigation_manager = NavigationManager()
        await navigation_manager.navigation_turnos(page)

        # Take screenshot for verification
        print(f"\n📸 Taking screenshot...")
        await browser_manager.take_screenshot("./outputs/export_flow_screenshot.png")

        print(f"\n✅ Test flow completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test flow error: {e}")
        raise
    
    finally:
        print(f"\n🔌 Closing browser...")
        await browser_manager.close()

    # ===========================
    # POST-RPA: CSV → MongoDB
    # ===========================
    #print("\n📄 Procesando CSV y guardando en MongoDB...")
    #procesar_csv_turnos("./outputs/turnos.csv")

    #print(f"\n✅ Test flow completed successfully!")
    
    #
    #csv_path = Path("./downloads/turnos_20260120_081032.csv")
    csv_path = get_latest_turnos_csv()
    print(f"📄 Archivo detectado: {csv_path.name}")

    df = read_turnos_csv(csv_path)
    documents = transform_turnos(df, csv_path.name)
    inserted, update = save_turnos(documents)
    
    print(f"✔ {update} turnos existentes y actualizados en MongoDB")
    print(f"✔ {inserted} turnos nuevos agregados en MongoDB")

    #agrupar turnos por area
    turnos_por_area = agrupar_turnos_por_area(documents)

    hoy = datetime.now(UTC)

    for area_destino, turnos_area in turnos_por_area.items():
        metricas = calcular_metricas_turnos(turnos_area)

        save_metricas_mensuales(
            anio=hoy.year,
            mes=hoy.month,
            area=area_destino,
            dia=hoy.day,
            metricas=metricas
        )

    print("📊 Métricas mensuales actualizadas para todas las áreas")

async def contracts_flow():
    #return None
    """Login flow and sales management"""
    
    print("=" * 60)
    print("🚀 RPA Automation - Contracts Module")
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
        await browser_manager.take_screenshot("./outputs/contracts_module_flow_screenshot.png")
        #await asyncio.sleep(1)
        await page.wait_for_timeout(200)
        # Initialize navigation manager
        contracts_navigation_manager = ContractsNavigationManager()
        await contracts_navigation_manager.navigation_contracts(page)

        # Take screenshot for verification
        print(f"\n📸 Taking screenshot...")
        await browser_manager.take_screenshot("./outputs/export_contracts_module_flow_screenshot.png")

        print(f"\n✅ The contracts module flow was completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test flow error: {e}")
        raise
    
    finally:
        print(f"\n🔌 Closing browser...")
        await browser_manager.close()

    # ===========================
    # POST-RPA: CSV → MongoDB
    # ===========================
    #print("\n📄 Procesando CSV y guardando en MongoDB...")
    #procesar_csv_turnos("./outputs/turnos.csv")

    #print(f"\n✅ Test flow completed successfully!")
    
    #
    #csv_path = Path("./downloads/turnos_20260120_081032.csv")
    csv_path = get_latest_contracts_csv()
    print(f"📄 Archivo detectado: {csv_path.name}")

    df = read_contracts_csv(csv_path)
    documents = transform_contracts(df, csv_path.name)
    inserted, update = save_contracts(documents)

    print(f"✔ {update} contratos existentes y actualizados en MongoDB")
    print(f"✔ {inserted} contratos nuevos agregados en MongoDB")
    

    #agrupar turnos por area
    #turnos_por_area = agrupar_turnos_por_area(documents)

    #hoy = datetime.now(UTC)

    #for area_destino, turnos_area in turnos_por_area.items():
        #metricas = calcular_metricas_turnos(turnos_area)

        #save_metricas_mensuales(
            #anio=hoy.year,
            #mes=hoy.month,
            #area=area_destino,
            #dia=hoy.day,
            #metricas=metricas
        #)

    #print("📊 Métricas mensuales actualizadas para todas las áreas")

async def visits_flow():
    """Login flow and visits management"""
    
    print("=" * 60)
    print("🚀 RPA Automation - Visits Module")
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
        await browser_manager.take_screenshot("./outputs/visits_module_flow_screenshot.png")
        #await asyncio.sleep(1)
        await page.wait_for_timeout(200)
        # Initialize navigation manager
        visits_navigation_manager = VisitsNavigationManager()
        await visits_navigation_manager.navigation_visits(page)

        # Take screenshot for verification
        print(f"\n📸 Taking screenshot...")
        await browser_manager.take_screenshot("./outputs/export_visits_module_flow_screenshot.png")
        print(f"\n✅ The visits module flow was completed successfully!")

    except Exception as e:
        print(f"\n❌ Test flow error: {e}")
        raise
    
    finally:
        print(f"\n🔌 Closing browser...")
        await browser_manager.close()

    # ===========================
    # POST-RPA: CSV → MongoDB
    # ===========================
    #print("\n📄 Procesando CSV y guardando en MongoDB...")
    #procesar_csv_turnos("./outputs/turnos.csv")

    #print(f"\n✅ Test flow completed successfully!")
    
    #
    #csv_path = Path("./downloads/turnos_20260120_081032.csv")
    csv_path = get_latest_visits_csv()
    print(f"📄 Archivo detectado: {csv_path.name}")

    df = read_visits_csv(csv_path)
    documents = transform_visits(df, csv_path.name)
    inserted, update = save_visits(documents)

    print(f"✔ {update} tickets existentes y actualizadas en MongoDB")
    print(f"✔ {inserted} tickets nuevos agregados en MongoDB")

    #agrupar turnos por area
    #turnos_por_area = agrupar_turnos_por_area(documents)

    #hoy = datetime.now(UTC)

    #for area_destino, turnos_area in turnos_por_area.items():
        #metricas = calcular_metricas_turnos(turnos_area)

        #save_metricas_mensuales(
            #anio=hoy.year,
            #mes=hoy.month,
            #area=area_destino,
            #dia=hoy.day,
            #metricas=metricas
        #)

    #print("📊 Métricas mensuales actualizadas para todas las áreas")


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
        
        #await test_login_flow()
        await contracts_flow()
        #await visits_flow()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())