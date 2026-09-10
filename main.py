import sys
import time
from concurrent.futures import ThreadPoolExecutor

from gemini import GeminiEngine
from listener import VoiceListener
from logger import logger
from notes_manager import NotesManager
from speaker import VoiceSpeaker
from ui_renderer import TerminalUI
from web_commands import WebCommands


class JarvisOrchestrator:
    def __init__(self):
        TerminalUI.clear_screen()
        TerminalUI.render_header("JARVIS")
        TerminalUI.show_spinner("Starting", 0.7)

        try:
            self.ai = GeminiEngine()
            self.notes = NotesManager()
            self.web = WebCommands()
            self.listener = VoiceListener()
            self.speaker = VoiceSpeaker()
            self.executor = ThreadPoolExecutor(max_workers=2)
            logger.info("JARVIS started successfully.")
        except Exception as exc:
            TerminalUI.error(f"Startup failed: {exc}")
            logger.critical(f"Startup failed: {exc}")
            sys.exit(1)

    def main_loop(self):
        while True:
            TerminalUI.clear_screen()
            TerminalUI.render_header()
            TerminalUI.render_menu([
                "Chat",
                "Notes",
                "Open",
                "Voice",
                "Exit",
            ])
            choice = TerminalUI.prompt("Choose")

            if choice == "1":
                self.run_chat()
            elif choice == "2":
                self.run_notes()
            elif choice == "3":
                self.run_web()
            elif choice == "4":
                self.run_voice()
            elif choice == "5":
                self.executor.shutdown(wait=False)
                TerminalUI.success("Goodbye.")
                break
            else:
                TerminalUI.error("Invalid choice.")
                time.sleep(0.8)

    def run_chat(self):
        TerminalUI.clear_screen()
        TerminalUI.render_header("CHAT")
        print("Type 'back' to return.\n")

        while True:
            user_input = TerminalUI.prompt("You")
            if user_input.lower() == "back":
                return
            if not user_input:
                continue

            reply = self.ai.ask_jarvis(user_input)
            print(f"\n{TerminalUI.ORANGE}JARVIS{TerminalUI.RESET}  {reply}\n")

    def run_notes(self):
        while True:
            TerminalUI.clear_screen()
            TerminalUI.render_header("NOTES")
            TerminalUI.render_menu([
                "Add",
                "Read",
                "List",
                "Delete",
                "Back",
            ])
            choice = TerminalUI.prompt("Choose")

            if choice == "1":
                title = TerminalUI.prompt("Title")
                content = TerminalUI.prompt("Note")
                TerminalUI.success(self.notes.save_note(title, content))
                time.sleep(1)
            elif choice == "2":
                title = TerminalUI.prompt("Title")
                print(self.notes.read_note(title))
                input("\nPress Enter...")
            elif choice == "3":
                print(self.notes.list_notes())
                input("\nPress Enter...")
            elif choice == "4":
                title = TerminalUI.prompt("Title")
                TerminalUI.success(self.notes.delete_note(title))
                time.sleep(1)
            elif choice == "5":
                return
            else:
                TerminalUI.error("Invalid choice.")

    def run_web(self):
        TerminalUI.clear_screen()
        TerminalUI.render_header("OPEN")
        print("Websites: Google, YouTube, ChatGPT, GitHub, LinkedIn, Instagram, Gmail")
        print("Apps: Chrome, Edge, Brave, VS Code, Notepad, Calculator, Paint\n")
        target = TerminalUI.prompt("Open")
        result = self.web.handle_command(target)
        TerminalUI.success(result)
        time.sleep(1.2)

    def run_voice(self):
        TerminalUI.clear_screen()
        TerminalUI.render_header("VOICE")
        print("Say 'back' to return.\n")
        self.speaker.speak("Voice mode is ready.")

        while True:
            future_text = self.executor.submit(self.listener.listen)
            TerminalUI.show_spinner("Listening", 0.5)
            voice_text = future_text.result()

            if not voice_text:
                continue

            print(f"{TerminalUI.ORANGE}You{TerminalUI.RESET}  {voice_text}")

            if voice_text.strip().lower() == "back":
                self.speaker.speak("Voice mode closed.")
                return

            command_result = self.web.handle_command(voice_text)
            if command_result:
                self.speaker.speak(command_result)
                continue

            reply = self.ai.ask_jarvis(voice_text)
            self.executor.submit(self.speaker.speak, reply)
            print(f"\n{TerminalUI.ORANGE}JARVIS{TerminalUI.RESET}  {reply}\n")


if __name__ == "__main__":
    JarvisOrchestrator().main_loop()
