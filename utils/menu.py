"""Menu utilities for the GM sender."""
import os
import sys
import asyncio
from .wallet_manager import load_private_keys, get_wallet_info, shuffle_wallets
from .config import Config
from chains import AVAILABLE_CHAINS, get_chain

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    clear_screen()
    print("=" * 60)
    print("                 ONCHAIN GM SENDER                 ")
    print("=" * 60)
    print()

def print_config_info():
    """Print current configuration information."""
    print("Current Configuration:")
    print("-" * 60)
    print(f"Selected Chain: {Config.get_chain()}")
    print(f"Delay between wallets: {Config.get_delay_range_display()}")
    print(f"Shuffle wallets: {'Yes' if Config.should_shuffle_wallets() else 'No'}")
    print("-" * 60)
    print()

def print_main_menu():
    """Print the main menu options."""
    print("Main Menu:")
    print("1. Send GM (using .env configuration)")
    print("2. Exit")
    print()

async def handle_send_gm_configured():
    """Handle sending GM using the configuration from .env file."""
    print_header()
    print_config_info()
    
    chain_name = Config.get_chain()
    
    if chain_name == "all":
        await handle_send_gm_all()
    else:
        await handle_send_gm_specific(chain_name)

async def handle_send_gm_specific(chain_name):
    """Handle sending GM on a specific chain."""
    print_header()
    
    # Get chain
    chain_class = get_chain(chain_name)
    if not chain_class:
        print(f"Chain {chain_name} not found.")
        input("Press Enter to return to main menu...")
        return
    
    # Initialize the chain
    chain = chain_class()
    
    # Get wallets
    private_keys = load_private_keys()
    if not private_keys:
        print(f"No private keys found in data/private_keys.txt")
        print("Please add your private keys and try again.")
        input("Press Enter to return to main menu...")
        return
    
    shuffle_enabled = Config.should_shuffle_wallets()
    delay_range = Config.get_delay_range_display()
    
    print(f"Sending GM on {chain.NAME} from {len(private_keys)} wallet(s)")
    print(f"Delay between wallets: {delay_range}")
    print(f"Wallets shuffled: {'Yes' if shuffle_enabled else 'No'}")
    print("-" * 60)
    
    results = []
    for i, private_key in enumerate(private_keys, 1):
        print(f"\nProcessing wallet {i}/{len(private_keys)}")
        result = await chain.send_gm(private_key)
        results.append(result)
        
        # Add random delay between wallets (except for the last one)
        if i < len(private_keys):
            delay = Config.get_random_delay_between_wallets()
            if delay > 0:
                print(f"⏳ Waiting {delay:.1f}s before next wallet...")
                await asyncio.sleep(delay)
    
    # Print summary
    success_count = sum(1 for r in results if r.get("success", False))
    print(f"\n===== Summary =====")
    print(f"Total wallets: {len(results)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(results) - success_count}")
    
    input("\nPress Enter to return to main menu...")

async def handle_send_gm_all():
    """Handle sending GM on all available chains."""
    print_header()
    
    # Get wallets
    private_keys = load_private_keys()
    if not private_keys:
        print(f"No private keys found in data/private_keys.txt")
        print("Please add your private keys and try again.")
        input("Press Enter to return to main menu...")
        return
    
    shuffle_enabled = Config.should_shuffle_wallets()
    delay_range = Config.get_delay_range_display()
    
    print(f"Sending GM on all chains from {len(private_keys)} wallet(s)")
    print(f"Delay between wallets: {delay_range}")
    print(f"Wallets shuffled: {'Yes' if shuffle_enabled else 'No'}")
    print("-" * 60)
    
    all_results = []
    
    # Process each chain
    for chain_id, chain_class in AVAILABLE_CHAINS.items():
        # Initialize the chain
        chain = chain_class()
        print(f"\n=== Processing chain: {chain.NAME} ===")
        
        chain_results = []
        for i, private_key in enumerate(private_keys, 1):
            print(f"\nProcessing wallet {i}/{len(private_keys)}")
            result = await chain.send_gm(private_key)
            chain_results.append(result)
            all_results.append(result)
            
            # Add random delay between wallets (except for the last one)
            if i < len(private_keys):
                delay = Config.get_random_delay_between_wallets()
                if delay > 0:
                    print(f"⏳ Waiting {delay:.1f}s before next wallet...")
                    await asyncio.sleep(delay)
        
        # Print chain summary
        success_count = sum(1 for r in chain_results if r.get("success", False))
        print(f"\n{chain.NAME} Summary: {success_count} successful, {len(chain_results) - success_count} failed")
    
    # Print overall summary
    success_count = sum(1 for r in all_results if r.get("success", False))
    print(f"\n===== Overall Summary =====")
    print(f"Total transactions: {len(all_results)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(all_results) - success_count}")
    
    input("\nPress Enter to return to main menu...")

async def main_menu():
    """Display and handle the main menu."""
    while True:
        print_header()
        print_config_info()
        print_main_menu()
        
        try:
            choice = input("Enter your choice (1-2): ")
            
            if choice == "1":
                await handle_send_gm_configured()
            elif choice == "2":
                print("Exiting GM Sender. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(1) 