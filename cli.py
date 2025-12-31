#!/usr/bin/env python3
"""
CryptoSentinel - Interactive Command Line Interface

Main entry point for the CryptoSentinel framework. Provides an interactive
terminal interface for all cryptographic operations.

Usage:
    python cli.py

Developer: saisrujanmurthy@gmail.com
"""

import sys
from crypto_sentinel.ui.console_ui import CryptoConsole
from rich.console import Console
from rich.panel import Panel


def main() -> None:
    """Main CLI loop with graceful error handling."""
    console = Console()
    crypto_console = CryptoConsole()
    
    try:
        # Display banner ONCE at startup
        crypto_console.clear_screen()
        crypto_console.display_banner()
        
        # Main loop
        while True:
            try:
                # Main menu (compact header)
                choice = crypto_console.main_menu()
                
                if choice == "1":  # Classical Ciphers
                    while True:
                        crypto_console.clear_screen()
                        
                        cipher_choice = crypto_console.cipher_menu()
                        
                        if cipher_choice == "6":  # Back
                            break
                        
                        crypto_console.process_cipher_interaction(cipher_choice)
                
                elif choice == "2":  # Hashing Tools
                    while True:
                        crypto_console.clear_screen()
                        
                        hash_choice = crypto_console.hashing_menu()
                        
                        if hash_choice == "4":  # Back
                            break
                        
                        crypto_console.process_hashing_operation(hash_choice)
                
                elif choice == "3":  # Security Tools
                    while True:
                        crypto_console.clear_screen()
                        
                        security_choice = crypto_console.security_menu()
                        
                        if security_choice == "3":  # Back
                            break
                        
                        if security_choice == "1":
                            crypto_console.process_password_analysis()
                        elif security_choice == "2":
                            crypto_console.process_base64_operation()
                
                elif choice == "4":  # Exit
                    crypto_console.clear_screen()
                    goodbye_panel = Panel(
                        "[bold cyan]Thank you for using CryptoSentinel![/bold cyan]\n\n"
                        "[green]Stay secure! 🔐[/green]\n\n"
                        "[dim]Built with ❤️ by saisrujanmurthy@gmail.com[/dim]",
                        title="[bold magenta]👋 Goodbye[/bold magenta]",
                        border_style="cyan",
                        padding=(1, 2)
                    )
                    console.print(goodbye_panel, justify="center")
                    sys.exit(0)
                
                # Clear screen after operation for clean return to main menu
                crypto_console.clear_screen()
            
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully within menu
                console.print("\n[yellow]⚠️  Operation cancelled[/yellow]")
                continue
    
    except KeyboardInterrupt:
        # Handle Ctrl+C at top level
        crypto_console.clear_screen()
        
        interrupt_panel = Panel(
            "[bold yellow]⚠️  Interrupted by user[/bold yellow]\n\n"
            "[cyan]CryptoSentinel closed safely.[/cyan]\n\n"
            "[dim]No operations were harmed in the making of this exit 😊[/dim]",
            title="[bold red]🛑 Keyboard Interrupt[/bold red]",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print("\n")
        console.print(interrupt_panel, justify="center")
        console.print("")
        sys.exit(0)
    
    except Exception as e:
        # Handle unexpected errors
        crypto_console.clear_screen()
        
        error_panel = Panel(
            f"[bold red]Unexpected Error:[/bold red]\n\n"
            f"[yellow]{type(e).__name__}:[/yellow] {str(e)}\n\n"
            f"[dim]Please report this issue to: saisrujanmurthy@gmail.com[/dim]",
            title="[bold red]❌ Fatal Error[/bold red]",
            border_style="red",
            padding=(1, 2)
        )
        console.print("\n")
        console.print(error_panel, justify="center")
        console.print("")
        sys.exit(1)


if __name__ == "__main__":
    main()
