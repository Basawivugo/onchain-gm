#!/usr/bin/env python3
"""Main entry point for GM Sender with interactive menu."""
import os
import sys
import asyncio
from utils.menu import main_menu
from utils.wallet_manager import ensure_data_dir
from utils.version_checker import VERSION_CHECKER, check_app_integrity

async def main():
    """Main entry point."""
    # Ensure data directory exists
    ensure_data_dir()
    
    # Check app integrity (non-blocking)
    try:
        check_app_integrity()
    except Exception as e:
        print(f"Warning: Could not check app integrity: {e}")
    
    # Check for updates on startup
    try:
        update_info = VERSION_CHECKER.check_for_updates(silent=False)
        if update_info.get('update_available'):
            VERSION_CHECKER.print_update_banner(update_info)
            
            # Ask user if they want to continue with outdated version
            response = input("Do you want to continue with the current version? (y/n): ").lower()
            if response not in ['y', 'yes']:
                print("Please update to the latest version and try again.")
                print(f"Download: {update_info.get('release_url', '')}")
                return
    except Exception as e:
        print(f"Warning: Could not check for updates: {e}")
        print("Continuing with current version...\n")
    
    # Run the main menu
    await main_menu()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 