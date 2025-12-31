#!/usr/bin/env python3
"""
Demo script to showcase CryptoSentinel CLI features.

This script demonstrates the UI capabilities without requiring user interaction.

Developer: saisrujanmurthy@gmail.com
"""

import time
from crypto_sentinel.ui import CryptoConsole
from rich.console import Console
from rich.panel import Panel


def demo_ui_features():
    """Demonstrate UI features."""
    console = Console()
    crypto_console = CryptoConsole()
    
    # Display banner
    crypto_console.display_banner()
    time.sleep(2)
    
    # Show main menu
    console.print("\n[bold yellow]═══ Main Menu Demo ═══[/bold yellow]\n")
    # We can't actually run main_menu() without user input, so show the table structure
    
    from rich.table import Table
    from rich import box
    
    table = Table(
        title="[bold cyan]Main Menu[/bold cyan]",
        box=box.ROUNDED,
        border_style="cyan",
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Option", style="yellow", justify="center", width=8)
    table.add_column("Category", style="cyan", width=25)
    table.add_column("Description", style="white", width=50)
    
    table.add_row("1", "🔐 Classical Ciphers", "Caesar, Vigenère, XOR, Substitution, Morse")
    table.add_row("2", "🔑 Hashing Tools", "MD5, SHA-256, Checksum Validation")
    table.add_row("3", "🛡️  Security Tools", "Password Analysis, Base64 Encoding")
    table.add_row("4", "❌ Exit", "Close CryptoSentinel")
    
    console.print(table)
    time.sleep(2)
    
    # Demo Caesar cipher encryption
    console.print("\n\n[bold yellow]═══ Caesar Cipher Demo ═══[/bold yellow]\n")
    
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=False
    ) as progress:
        task = progress.add_task("[cyan]Processing encryption...", total=100)
        
        for i in range(100):
            time.sleep(0.01)
            progress.update(task, advance=1)
    
    # Show result
    result_table = Table(
        title="[bold green]✓ ENCRYPT Complete[/bold green]",
        box=box.DOUBLE,
        border_style="green",
        show_header=True,
        header_style="bold cyan"
    )
    
    result_table.add_column("Input", style="yellow", width=40)
    result_table.add_column("Output", style="green", width=40)
    result_table.add_row("HELLO WORLD", "KHOOR ZRUOG")
    
    console.print(result_table)
    
    info_panel = Panel(
        "[bold cyan]Cipher:[/bold cyan] Caesar\n"
        "[bold cyan]Key:[/bold cyan] 3\n"
        "[bold cyan]Operation:[/bold cyan] Encrypt",
        title="[bold magenta]Details[/bold magenta]",
        border_style="magenta"
    )
    console.print(info_panel)
    
    time.sleep(2)
    
    # Demo password analysis
    console.print("\n\n[bold yellow]═══ Password Analyzer Demo ═══[/bold yellow]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False
    ) as progress:
        task = progress.add_task("[cyan]Analyzing password...", total=100)
        
        for i in range(100):
            time.sleep(0.01)
            progress.update(task, advance=1)
    
    # Strength bar
    console.print("\n[bold cyan]Password Strength:[/bold cyan]")
    
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40, style="green"),
        TextColumn("[bold green]{task.percentage:>3.0f}%[/bold green]"),
    ) as progress:
        task = progress.add_task("🟢 Strength", total=100)
        
        for i in range(74):
            progress.update(task, completed=i)
            time.sleep(0.01)
    
    # Analysis results
    metrics_panel = Panel(
        "[bold cyan]Score:[/bold cyan] 73/100\n"
        "[bold cyan]Strength Level:[/bold cyan] STRONG\n\n"
        "[bold yellow]Technical Metrics:[/bold yellow]\n"
        "  • Length: 11 characters\n"
        "  • Character Pool: 94\n"
        "  • Entropy: 72.1 bits\n"
        "  • Crack Time: millions of years\n\n"
        "[bold magenta]Recommendations:[/bold magenta]\n"
        "  • Consider increasing length to 12+ characters for better security",
        title="[bold cyan]📊 Analysis Results[/bold cyan]",
        border_style="cyan",
        box=box.DOUBLE
    )
    
    console.print("\n")
    console.print(metrics_panel)
    
    time.sleep(2)
    
    # Demo hashing
    console.print("\n\n[bold yellow]═══ SHA-256 Hashing Demo ═══[/bold yellow]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False
    ) as progress:
        task = progress.add_task("[cyan]Computing SHA-256 hash...", total=100)
        
        for i in range(100):
            time.sleep(0.005)
            progress.update(task, advance=1)
    
    result_panel = Panel(
        "[bold yellow]Input:[/bold yellow] Hello World\n\n"
        "[bold green]SHA-256 Hash:[/bold green]\n"
        "[cyan]a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e[/cyan]\n\n"
        "[dim]Algorithm: SHA-256 | Digest Size: 32 bytes[/dim]",
        title="[bold green]✓ SHA-256 Hash Complete[/bold green]",
        border_style="green",
        box=box.DOUBLE
    )
    
    console.print("\n")
    console.print(result_panel)
    
    time.sleep(2)
    
    # Final message
    console.print("\n\n")
    goodbye_panel = Panel(
        "[bold cyan]UI Demo Complete![/bold cyan]\n\n"
        "[green]All features demonstrated:[/green]\n"
        "  ✓ ASCII art banner with colors\n"
        "  ✓ Rich tables for menus\n"
        "  ✓ Progress bars and spinners\n"
        "  ✓ Comparison tables\n"
        "  ✓ Colored panels\n"
        "  ✓ Error handling (graceful)\n\n"
        "[yellow]To use interactively:[/yellow]\n"
        "  python cli.py\n\n"
        "[dim]Built with Rich library 🎨[/dim]",
        title="[bold magenta]🎉 Demo Complete[/bold magenta]",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(goodbye_panel, justify="center")
    console.print("")


if __name__ == "__main__":
    demo_ui_features()
