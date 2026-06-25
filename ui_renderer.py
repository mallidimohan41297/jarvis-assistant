import sys
import time
import os

class TerminalUI:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def render_header(cls, title: str):
        print(f"{cls.CYAN}{cls.BOLD}{'=' * 50}")
        print(f" {title.center(48)}")
        print(f"{'=' * 50}{cls.RESET}\n")

    @classmethod
    def render_menu(cls, options: list):
        for idx, option in enumerate(options, 1):
            print(f" {cls.CYAN}{idx}.{cls.RESET} {option}")
        print(f"\n{cls.CYAN}{'=' * 50}{cls.RESET}")

    @classmethod
    def show_spinner(cls, message: str, duration: float = 1.0):
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        end_time = time.time() + duration
        while time.time() < end_time:
            for frame in frames:
                sys.stdout.write(f"\r {cls.YELLOW}{frame}{cls.RESET} {message}...")
                sys.stdout.flush()
                time.sleep(0.06)
        sys.stdout.write("\r" + " " * (len(message) + 15) + "\r")
        sys.stdout.flush()