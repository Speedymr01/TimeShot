"""
TimeShot Launcher
=================

Launch the TimeShot parkour shooter game.
"""

import sys
import os

def show_menu():
    """Display the launcher menu."""
    print("=" * 50)
    print("TIMESHOT LAUNCHER")
    print("=" * 50)
    print()
    print("Choose an option:")
    print("  1. Play Game")
    print("  2. Exit")
    print()

def main():
    """Main launcher function."""
    while True:
        show_menu()
        choice = input("Enter your choice (1-2): ").strip()
        
        if choice == '1':
            print("Starting TimeShot game...")
            os.system("python main.py")
            break
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
            print()

if __name__ == "__main__":
    main()