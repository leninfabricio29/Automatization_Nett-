"""
Utilities module for RPA automation.
Exports authentication and browser management classes.
"""

from src.utils.auth import AuthManager
from src.utils.browser import BrowserManager
from src.utils.navigation import NavigationManager

from src.utils.navigation_contracts import ContractsNavigationManager
from src.utils.navigation_visits import VisitsNavigationManager

__all__ = [
    "AuthManager",
    "BrowserManager",
    "NavigationManager",
    "ContractsNavigationManager",
    "VisitsNavigationManager",
]
