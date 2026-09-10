import os
import sys
import time


class TerminalUI:
    """Minimal white/orange terminal UI."""

    ORANGE = "\033[38;5;208m"
    WHITE = "\033[97m"
    DIM = "\033[90m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    @classmethod
    def render_header(cls, title="JARVIS"):
        print(f"{cls.ORANGE}{cls.BOLD}{'─' * 52}{cls.RESET}")
        print(f"{cls.WHITE}{cls.BOLD}{title.center(52)}{cls.RESET}")
        print(f"{cls.ORANGE}{'─' * 52}{cls.RESET}\n")

    @classmethod
    def render_menu(cls, options):
        for idx, option in enumerate(options, 1):
            print(f" {cls.ORANGE}{idx}{cls.RESET}  {cls.WHITE}{option}{cls.RESET}")
        print()

    @classmethod
    def show_spinner(cls, message, duration=1.0):
        frames = ["·", "•", "●", "•"]
        end_time = time.time() + duration
        while time.time() < end_time:
            for frame in frames:
                sys.stdout.write(f"\r {cls.ORANGE}{frame}{cls.RESET} {message}...")
                sys.stdout.flush()
                time.sleep(0.08)
        sys.stdout.write("\r" + " " * (len(message) + 8) + "\r")
        sys.stdout.flush()

    @classmethod
    def prompt(cls, text):
        return input(f"{cls.ORANGE}>{cls.RESET} {text}").strip()

    @classmethod
    def success(cls, text):
        print(f"{cls.ORANGE}{text}{cls.RESET}")

    @classmethod
    def error(cls, text):
        print(f"{cls.RED}{text}{cls.RESET}")
