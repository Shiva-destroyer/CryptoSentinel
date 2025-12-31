"""
Interactive Console UI for CryptoSentinel using Rich library.

Provides a stunning terminal interface with colors, tables, panels,
and progress bars for all cryptographic operations.

Developer: saisrujanmurthy@gmail.com
"""

import time
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.text import Text
from rich.rule import Rule
from rich import box

# Import all modules
from crypto_sentinel.ciphers import (
    CaesarCipher,
    VigenereCipher,
    XORCipher,
    SubstitutionCipher,
    MorseHandler,
)
from crypto_sentinel.hashing import MD5Hasher, SHA256Hasher, ChecksumValidator
from crypto_sentinel.security import PasswordAnalyzer, Base64Encoder
from crypto_sentinel.core.exceptions import CryptoSentinelError


class CryptoConsole:
    """
    Interactive console interface for CryptoSentinel framework.
    
    Features:
        - Colored ASCII art banner
        - Rich tables for menu navigation
        - Progress bars and spinners for operations
        - Comparison tables for input/output
        - Error panels with graceful handling
    
    Color Palette:
        - Cyan: Headers and titles
        - Green: Success messages
        - Red: Errors and warnings
        - Yellow: Prompts and highlights
        - Magenta: Special features
    """
    
    def __init__(self) -> None:
        """Initialize console with rich styling."""
        self.console = Console()
        
        # Initialize cipher instances
        self.ciphers = {
            'caesar': CaesarCipher(),
            'vigenere': VigenereCipher(),
            'xor': XORCipher(),
            'substitution': SubstitutionCipher(),
            'morse': MorseHandler(),
        }
        
        # Initialize hashing instances
        self.hashers = {
            'md5': MD5Hasher(),
            'sha256': SHA256Hasher(),
        }
        self.checksum_validator = ChecksumValidator()
        
        # Initialize security tools
        self.password_analyzer = PasswordAnalyzer()
        self.base64_encoder = Base64Encoder()
    
    def display_banner(self) -> None:
        """Display stunning ASCII art banner in a panel."""
        banner_text = """
 ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ 
██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗
██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║
██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║
╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝
 ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ 
                                                     
███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗     
██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     
███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     
╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     
███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
        """
        
        subtitle = Text(
            "Advanced Cryptographic Framework & Security Tools",
            style="italic cyan"
        )
        
        banner_panel = Panel(
            Text(banner_text, style="bold cyan") + "\n" + subtitle,
            border_style="cyan",
            box=box.DOUBLE,
            padding=(1, 2)
        )
        
        self.console.print(banner_panel)
        self.console.print(
            "[dim]Version 1.0.0 | Developer: saisrujanmurthy@gmail.com[/dim]\n",
            justify="center"
        )
    
    def display_compact_header(self, title: str) -> None:
        """Display a clean, compact header instead of the full banner.
        
        Args:
            title: The title/section name to display
        """
        self.console.print()
        self.console.print(
            Rule(
                f"[bold cyan]CryptoSentinel[/bold cyan] [dim]│[/dim] [yellow]{title}[/yellow]",
                style="cyan"
            )
        )
        self.console.print()
    
    def main_menu(self) -> str:
        """Display main menu and return user choice."""
        self.display_compact_header("Main Menu")
        
        table = Table(
            box=box.ROUNDED,
            border_style="cyan",
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Option", style="yellow", justify="center", width=8)
        table.add_column("Category", style="cyan", width=25)
        table.add_column("Description", style="white", width=50)
        
        table.add_row(
            "1",
            "🔐 Classical Ciphers",
            "Caesar, Vigenère, XOR, Substitution, Morse"
        )
        table.add_row(
            "2",
            "🔑 Hashing Tools",
            "MD5, SHA-256, Checksum Validation"
        )
        table.add_row(
            "3",
            "🛡️  Security Tools",
            "Password Analysis, Base64 Encoding"
        )
        table.add_row(
            "4",
            "❌ Exit",
            "Close CryptoSentinel"
        )
        
        self.console.print(table)
        
        choice = Prompt.ask(
            "\n[bold yellow]Select an option[/bold yellow]",
            choices=["1", "2", "3", "4"],
            default="1"
        )
        
        return choice
    
    def cipher_menu(self) -> str:
        """Display cipher selection menu."""
        self.display_compact_header("Classical Ciphers")
        
        table = Table(
            box=box.ROUNDED,
            border_style="cyan",
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Option", style="yellow", justify="center", width=8)
        table.add_column("Cipher", style="cyan", width=20)
        table.add_column("Type", style="white", width=20)
        table.add_column("Cracking Method", style="green", width=30)
        
        table.add_row("1", "Caesar Cipher", "Shift", "Chi-squared frequency analysis")
        table.add_row("2", "Vigenère Cipher", "Polyalphabetic", "IoC-based key detection")
        table.add_row("3", "XOR Cipher", "Binary", "Single-byte brute force")
        table.add_row("4", "Substitution", "Monoalphabetic", "Hill climbing algorithm")
        table.add_row("5", "Morse Code", "Encoding", "Dictionary lookup")
        table.add_row("6", "← Back", "Return to Main", "")
        
        self.console.print(table)
        
        choice = Prompt.ask(
            "\n[bold yellow]Select a cipher[/bold yellow]",
            choices=["1", "2", "3", "4", "5", "6"],
            default="1"
        )
        
        return choice
    
    def hashing_menu(self) -> str:
        """Display hashing tools menu."""
        self.display_compact_header("Hashing Tools")
        
        table = Table(
            box=box.ROUNDED,
            border_style="cyan",
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Option", style="yellow", justify="center", width=8)
        table.add_column("Tool", style="cyan", width=25)
        table.add_column("Description", style="white", width=50)
        
        table.add_row("1", "MD5 Hash", "Fast checksum (not secure)")
        table.add_row("2", "SHA-256 Hash", "Secure cryptographic hash")
        table.add_row("3", "File Checksum", "Validate file integrity")
        table.add_row("4", "← Back", "Return to Main Menu")
        
        self.console.print(table)
        
        choice = Prompt.ask(
            "\n[bold yellow]Select a tool[/bold yellow]",
            choices=["1", "2", "3", "4"],
            default="1"
        )
        
        return choice
    
    def security_menu(self) -> str:
        """Display security tools menu."""
        self.display_compact_header("Security Tools")
        
        table = Table(
            box=box.ROUNDED,
            border_style="cyan",
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Option", style="yellow", justify="center", width=8)
        table.add_column("Tool", style="cyan", width=25)
        table.add_column("Description", style="white", width=50)
        
        table.add_row("1", "Password Analyzer", "Entropy & strength analysis")
        table.add_row("2", "Base64 Encoder", "Encode/decode Base64")
        table.add_row("3", "← Back", "Return to Main Menu")
        
        self.console.print(table)
        
        choice = Prompt.ask(
            "\n[bold yellow]Select a tool[/bold yellow]",
            choices=["1", "2", "3"],
            default="1"
        )
        
        return choice
    
    def process_cipher_interaction(self, cipher_name: str) -> None:
        """Process cipher encrypt/decrypt/crack operations with rich UI."""
        cipher_map = {
            '1': ('caesar', 'Caesar Cipher'),
            '2': ('vigenere', 'Vigenère Cipher'),
            '3': ('xor', 'XOR Cipher'),
            '4': ('substitution', 'Substitution Cipher'),
            '5': ('morse', 'Morse Code'),
        }
        
        cipher_key, cipher_display = cipher_map[cipher_name]
        cipher = self.ciphers[cipher_key]
        
        self.console.print(f"\n[bold cyan]═══ {cipher_display} ═══[/bold cyan]\n")
        
        # Ask operation
        operation = Prompt.ask(
            "[bold yellow]Operation[/bold yellow]",
            choices=["encrypt", "decrypt", "crack"],
            default="encrypt"
        )
        
        # Ask input type
        input_type = Prompt.ask(
            "[bold yellow]Input type[/bold yellow]",
            choices=["text", "file"],
            default="text"
        )
        
        try:
            # Get input
            if input_type == "text":
                data = Prompt.ask("[bold yellow]Enter text[/bold yellow]")
            else:
                filepath = Prompt.ask("[bold yellow]Enter file path[/bold yellow]")
                with open(filepath, 'r') as f:
                    data = f.read()
            
            # Get key if needed
            key = None
            if operation in ["encrypt", "decrypt"]:
                if cipher_key == "caesar":
                    key = int(Prompt.ask("[bold yellow]Enter shift (0-25)[/bold yellow]", default="3"))
                elif cipher_key == "vigenere":
                    key = Prompt.ask("[bold yellow]Enter keyword[/bold yellow]")
                elif cipher_key == "xor":
                    key_input = Prompt.ask("[bold yellow]Enter key (integer or string)[/bold yellow]")
                    try:
                        key = int(key_input)
                    except ValueError:
                        key = key_input
                elif cipher_key == "substitution":
                    key = Prompt.ask(
                        "[bold yellow]Enter 26-letter key[/bold yellow]",
                        default="QWERTYUIOPASDFGHJKLZXCVBNM"
                    )
            
            # Process with animation
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                transient=True
            ) as progress:
                task = progress.add_task(
                    f"[cyan]Processing {operation}...",
                    total=100
                )
                
                # Simulate processing for UX
                for i in range(100):
                    time.sleep(0.01)
                    progress.update(task, advance=1)
                
                # Perform operation
                if operation == "encrypt":
                    result = cipher.encrypt(data, key=key)
                elif operation == "decrypt":
                    result = cipher.decrypt(data, key=key)
                else:  # crack
                    crack_result = cipher.crack(data)
                    result = crack_result.get('plaintext', 'Failed to crack')
                    if cipher_key != 'morse':
                        key = crack_result.get('key', 'N/A')
            
            # Display results in comparison table
            result_table = Table(
                title=f"[bold green]✓ {operation.upper()} Complete[/bold green]",
                box=box.DOUBLE,
                border_style="green",
                show_header=True,
                header_style="bold cyan"
            )
            
            result_table.add_column("Input", style="yellow", width=40)
            result_table.add_column("Output", style="green", width=40)
            
            # Truncate long outputs
            input_display = data[:100] + "..." if len(data) > 100 else data
            result_display = str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
            
            result_table.add_row(input_display, result_display)
            
            self.console.print("\n")
            self.console.print(result_table)
            
            if operation == "crack" and cipher_key != 'morse':
                info_panel = Panel(
                    f"[bold cyan]Detected Key:[/bold cyan] {key}\n"
                    f"[bold cyan]Confidence:[/bold cyan] {crack_result.get('confidence', 'N/A')}",
                    title="[bold magenta]Crack Details[/bold magenta]",
                    border_style="magenta"
                )
                self.console.print(info_panel)
        
        except FileNotFoundError:
            self.console.print(
                Panel(
                    "[bold red]Error: File not found![/bold red]\n"
                    "Please check the file path and try again.",
                    title="❌ File Error",
                    border_style="red"
                )
            )
        except CryptoSentinelError as e:
            self.console.print(
                Panel(
                    f"[bold red]Error: {str(e)}[/bold red]",
                    title="❌ Cipher Error",
                    border_style="red"
                )
            )
        except Exception as e:
            self.console.print(
                Panel(
                    f"[bold red]Unexpected Error: {str(e)}[/bold red]",
                    title="❌ Error",
                    border_style="red"
                )
            )
        
        # Pause before returning
        self.console.print("\n")
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def process_hashing_operation(self, tool_choice: str) -> None:
        """Process hashing operations with rich UI."""
        try:
            if tool_choice == "1":  # MD5
                hasher = self.hashers['md5']
                algo_name = "MD5"
            elif tool_choice == "2":  # SHA-256
                hasher = self.hashers['sha256']
                algo_name = "SHA-256"
            elif tool_choice == "3":  # Checksum validation
                self.process_checksum_validation()
                return
            
            self.console.print(f"\n[bold cyan]═══ {algo_name} Hashing ═══[/bold cyan]\n")
            
            # Ask input type
            input_type = Prompt.ask(
                "[bold yellow]Input type[/bold yellow]",
                choices=["text", "file"],
                default="text"
            )
            
            # Process with animation
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True
            ) as progress:
                task = progress.add_task(
                    f"[cyan]Computing {algo_name} hash...",
                    total=100
                )
                
                if input_type == "text":
                    data = Prompt.ask("[bold yellow]Enter text[/bold yellow]")
                    
                    for i in range(100):
                        time.sleep(0.005)
                        progress.update(task, advance=1)
                    
                    hash_result = hasher.hash_string(data)
                else:
                    filepath = Prompt.ask("[bold yellow]Enter file path[/bold yellow]")
                    
                    for i in range(100):
                        time.sleep(0.01)
                        progress.update(task, advance=1)
                    
                    hash_result = hasher.hash_file(filepath)
            
            # Display result
            result_panel = Panel(
                f"[bold yellow]Input:[/bold yellow] {data[:50] + '...' if input_type == 'text' and len(data) > 50 else data if input_type == 'text' else filepath}\n\n"
                f"[bold green]{algo_name} Hash:[/bold green]\n"
                f"[cyan]{hash_result}[/cyan]\n\n"
                f"[dim]Algorithm: {hasher.algorithm_name} | Digest Size: {hasher.digest_size} bytes[/dim]",
                title=f"[bold green]✓ {algo_name} Hash Complete[/bold green]",
                border_style="green",
                box=box.DOUBLE
            )
            
            self.console.print("\n")
            self.console.print(result_panel)
        
        except FileNotFoundError:
            self.console.print(
                Panel(
                    "[bold red]Error: File not found![/bold red]\n"
                    "Please check the file path and try again.",
                    title="❌ File Error",
                    border_style="red"
                )
            )
        except Exception as e:
            self.console.print(
                Panel(
                    f"[bold red]Error: {str(e)}[/bold red]",
                    title="❌ Hashing Error",
                    border_style="red"
                )
            )
        
        self.console.print("\n")
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def process_checksum_validation(self) -> None:
        """Process file checksum validation."""
        self.console.print("\n[bold cyan]═══ File Checksum Validation ═══[/bold cyan]\n")
        
        try:
            mode = Prompt.ask(
                "[bold yellow]Validation mode[/bold yellow]",
                choices=["compare", "verify"],
                default="verify"
            )
            
            if mode == "compare":
                file1 = Prompt.ask("[bold yellow]First file path[/bold yellow]")
                file2 = Prompt.ask("[bold yellow]Second file path[/bold yellow]")
                algorithm = Prompt.ask(
                    "[bold yellow]Algorithm[/bold yellow]",
                    choices=["md5", "sha256"],
                    default="sha256"
                )
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True
                ) as progress:
                    task = progress.add_task("[cyan]Comparing files...", total=100)
                    
                    for i in range(100):
                        time.sleep(0.01)
                        progress.update(task, advance=1)
                    
                    result = self.checksum_validator.compare_files(file1, file2, algorithm)
                
                # Display result
                status = "✓ MATCH" if result['match'] else "✗ MISMATCH"
                color = "green" if result['match'] else "red"
                
                comparison_table = Table(
                    title=f"[bold {color}]{status}[/bold {color}]",
                    box=box.DOUBLE,
                    border_style=color
                )
                
                comparison_table.add_column("File", style="cyan", width=30)
                comparison_table.add_column("Hash", style="yellow", width=64)
                
                comparison_table.add_row(Path(file1).name, result['hash1'])
                comparison_table.add_row(Path(file2).name, result['hash2'])
                
                self.console.print("\n")
                self.console.print(comparison_table)
            
            else:  # verify mode
                filepath = Prompt.ask("[bold yellow]File path[/bold yellow]")
                expected_hash = Prompt.ask("[bold yellow]Expected hash[/bold yellow]")
                algorithm = Prompt.ask(
                    "[bold yellow]Algorithm[/bold yellow]",
                    choices=["md5", "sha256"],
                    default="sha256"
                )
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True
                ) as progress:
                    task = progress.add_task("[cyan]Verifying file...", total=100)
                    
                    for i in range(100):
                        time.sleep(0.01)
                        progress.update(task, advance=1)
                    
                    result = self.checksum_validator.validate_file(
                        filepath, expected_hash, algorithm
                    )
                
                status = "✓ VERIFIED" if result['match'] else "✗ FAILED"
                color = "green" if result['match'] else "red"
                
                result_panel = Panel(
                    f"[bold cyan]File:[/bold cyan] {Path(filepath).name}\n\n"
                    f"[bold yellow]Computed Hash:[/bold yellow]\n{result['computed_hash']}\n\n"
                    f"[bold yellow]Expected Hash:[/bold yellow]\n{result['expected_hash']}\n\n"
                    f"[bold {color}]Status: {status}[/bold {color}]",
                    title=f"[bold {color}]Checksum Verification[/bold {color}]",
                    border_style=color,
                    box=box.DOUBLE
                )
                
                self.console.print("\n")
                self.console.print(result_panel)
        
        except Exception as e:
            self.console.print(
                Panel(
                    f"[bold red]Error: {str(e)}[/bold red]",
                    title="❌ Validation Error",
                    border_style="red"
                )
            )
        
        self.console.print("\n")
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def process_password_analysis(self) -> None:
        """Process password analysis with colored progress bar."""
        self.console.print("\n[bold cyan]═══ Password Strength Analyzer ═══[/bold cyan]\n")
        
        password = Prompt.ask(
            "[bold yellow]Enter password to analyze[/bold yellow]",
            password=True
        )
        
        # Analyze with animation
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Analyzing password...", total=100)
            
            for i in range(100):
                time.sleep(0.01)
                progress.update(task, advance=1)
            
            result = self.password_analyzer.analyze(password)
        
        # Determine color based on score
        score = result['score']
        if score < 40:
            bar_color = "red"
            strength_emoji = "🔴"
        elif score < 70:
            bar_color = "yellow"
            strength_emoji = "🟡"
        else:
            bar_color = "green"
            strength_emoji = "🟢"
        
        # Display strength bar
        self.console.print("\n[bold cyan]Password Strength:[/bold cyan]")
        
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40, style=bar_color),
            TextColumn(f"[bold {bar_color}]{{task.percentage:>3.0f}}%[/bold {bar_color}]"),
        ) as progress:
            task = progress.add_task(f"{strength_emoji} Strength", total=100)
            
            # Animate bar filling up
            for i in range(score + 1):
                progress.update(task, completed=i)
                time.sleep(0.01)
        
        # Display detailed metrics
        metrics_panel = Panel(
            f"[bold cyan]Score:[/bold cyan] {score}/100\n"
            f"[bold cyan]Strength Level:[/bold cyan] {result['strength_level'].upper().replace('_', ' ')}\n\n"
            f"[bold yellow]Technical Metrics:[/bold yellow]\n"
            f"  • Length: {result['length']} characters\n"
            f"  • Character Pool: {result['pool_size']}\n"
            f"  • Entropy: {result['entropy_bits']} bits\n"
            f"  • Crack Time: {result['crack_time_display']}\n\n"
            f"[bold magenta]Recommendations:[/bold magenta]\n" +
            "\n".join(f"  • {rec}" for rec in result['recommendations'][:5]),
            title=f"[bold cyan]📊 Analysis Results[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
        
        self.console.print("\n")
        self.console.print(metrics_panel)
        
        # Show entropy formula
        formula_text = Text()
        formula_text.append("Formula: ", style="dim")
        formula_text.append("E = L × log₂(R)", style="bold cyan")
        formula_text.append(f"  →  {result['entropy_bits']} = {result['length']} × log₂({result['pool_size']})", style="dim")
        
        self.console.print(formula_text, justify="center")
        
        self.console.print("\n")
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def process_base64_operation(self) -> None:
        """Process Base64 encoding/decoding."""
        self.console.print("\n[bold cyan]═══ Base64 Encoder ═══[/bold cyan]\n")
        
        try:
            operation = Prompt.ask(
                "[bold yellow]Operation[/bold yellow]",
                choices=["encode", "decode"],
                default="encode"
            )
            
            data = Prompt.ask(f"[bold yellow]Enter data to {operation}[/bold yellow]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True
            ) as progress:
                task = progress.add_task(f"[cyan]{operation.capitalize()}ing...", total=100)
                
                for i in range(100):
                    time.sleep(0.005)
                    progress.update(task, advance=1)
                
                if operation == "encode":
                    result = self.base64_encoder.encrypt(data)
                else:
                    result = self.base64_encoder.decrypt(data)
            
            # Display result
            result_table = Table(
                title=f"[bold green]✓ {operation.upper()} Complete[/bold green]",
                box=box.DOUBLE,
                border_style="green"
            )
            
            result_table.add_column("Input", style="yellow", width=40)
            result_table.add_column("Output", style="green", width=40)
            
            input_display = data[:100] + "..." if len(data) > 100 else data
            result_display = str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
            
            result_table.add_row(input_display, result_display)
            
            self.console.print("\n")
            self.console.print(result_table)
            
            if operation == "decode":
                self.console.print(
                    Panel(
                        "[bold yellow]Note:[/bold yellow] Base64 is encoding, NOT encryption!\n"
                        "Anyone can decode Base64 - it provides no security.",
                        title="⚠️  Security Warning",
                        border_style="yellow"
                    )
                )
        
        except Exception as e:
            self.console.print(
                Panel(
                    f"[bold red]Error: {str(e)}[/bold red]",
                    title="❌ Base64 Error",
                    border_style="red"
                )
            )
        
        self.console.print("\n")
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def clear_screen(self) -> None:
        """Clear the console screen."""
        self.console.clear()
