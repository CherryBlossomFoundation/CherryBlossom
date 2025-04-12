from colorama import init, Fore, Style

init(convert=True, autoreset=True)

RESET = Style.RESET_ALL
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
BOLD = Style.BRIGHT

def print_info(msg: str):
    print(f"{BLUE}{msg}{RESET}")

def print_success(msg: str):
    print(f"{GREEN}{msg}{RESET}")

def print_warning(msg: str):
    print(f"{YELLOW}{BOLD}{msg}{RESET}")

def print_panic(msg: str):
    print(f"{RED}{msg}{RESET}")

def print_progress(percent: int, msg: str = ""):
    print(f"{YELLOW}[{percent}%]{RESET} {msg}")

def panic(code: int, message: str, line):
    print_panic("Panic!!")
    print_panic(f"at: line{line}")
    print_panic(f"{line}: -> {message}")
    exit(code)
