import sys
import time
from concurrent.futures import ThreadPoolExecutor
from config import Config
from gemini import GeminiEngine
from notes_manager import NotesManager
from web_commands import WebCommands
from listener import VoiceListener
from speaker import VoiceSpeaker
from ui_renderer import TerminalUI
from logger import logger

class JarvisOrchestrator:
    def __init__(self):
        TerminalUI.clear_screen()
        TerminalUI.render_header("JARVIS ENGINE INITIALIZATION")
        TerminalUI.show_spinner("Mapping asynchronous subsystem cores")
        
        try:
            self.ai = GeminiEngine()
            self.notes = NotesManager()
            self.web = WebCommands()
            self.listener = VoiceListener()
            self.speaker = VoiceSpeaker()
            # Thread pool to prevent audio tasks from freezing the main loop
            self.executor = ThreadPoolExecutor(max_workers=2)
            logger.info("Asynchronous infrastructure completely operational.")
        except Exception as e:
            print(f"{TerminalUI.RED}CRITICAL BOOT ERROR: {e}{TerminalUI.RESET}")
            logger.critical(f"System boot failed: {str(e)}")
            sys.exit(1)

    def main_loop(self):
        while True:
            TerminalUI.clear_screen()
            TerminalUI.render_header("JARVIS CORE ENVIRONMENT")
            TerminalUI.render_menu([
                "AI Conversational Console",
                "Local Storage Ledger",
                "Browser Interface Automation",
                "Hands-Free Voice Mode",
                "Terminate Core Systems"
            ])
            
            choice = input(f"\n{TerminalUI.BOLD}Select runtime directory (1-5): {TerminalUI.RESET}").strip()
            
            if choice == "1":
                self.run_chat()
            elif choice == "2":
                self.run_notes()
            elif choice == "3":
                self.run_web()
            elif choice == "4":
                self.run_voice()
            elif choice == "5":
                print(f"\n{TerminalUI.YELLOW}Shutting down runtime systems securely...{TerminalUI.RESET}")
                self.executor.shutdown(wait=False)
                break
            else:
                print(f"{TerminalUI.RED}Unknown command parameter option selection.{TerminalUI.RESET}")
                time.sleep(1)

    def run_chat(self):
        TerminalUI.clear_screen()
        TerminalUI.render_header("CORE 1: CONVERSATIONAL SYSTEM")
        print(f"{TerminalUI.YELLOW}Type 'back' to escape back to mainframe lines.{TerminalUI.RESET}\n")
        
        while True:
            user_input = input(f"{TerminalUI.BOLD}You:{TerminalUI.RESET} ").strip()
            if user_input.lower() == 'back':
                break
            if not user_input:
                continue
            reply = self.ai.ask_jarvis(user_input)
            print(f"\n{TerminalUI.CYAN}{TerminalUI.BOLD}Jarvis:{TerminalUI.RESET} {reply}\n")

    def run_notes(self):
        while True:
            TerminalUI.clear_screen()
            TerminalUI.render_header("CORE 2: LOCAL STORAGE LEDGER")
            TerminalUI.render_menu([
                "Commit New Entry",
                "Read Existing Entry",
                "Index Contained Documents",
                "Erase Entry Metadata File",
                "Return to Mainframe Menu"
            ])
            choice = input(f"\n{TerminalUI.BOLD}Selection (1-5): {TerminalUI.RESET}").strip()
            
            if choice == "1":
                title = input("Input new document reference key: ").strip()
                content = input("Input payload data details: ").strip()
                print(f"\n{TerminalUI.GREEN}{self.notes.save_note(title, content)}{TerminalUI.RESET}")
                time.sleep(1.5)
            elif choice == "2":
                title = input("Input target document lookup reference: ").strip()
                print(self.notes.read_note(title))
                input("\nPress enter to continue...")
            elif choice == "3":
                print(self.notes.list_notes())
                input("\nPress enter to continue...")
            elif choice == "4":
                title = input("Input target erasure specification tag: ").strip()
                print(f"\n{TerminalUI.RED}{self.notes.delete_note(title)}{TerminalUI.RESET}")
                time.sleep(1.5)
            elif choice == "5":
                break

    def run_web(self):
        TerminalUI.clear_screen()
        TerminalUI.render_header("CORE 3: INTERFACE AUTOMATION")
        print("Available shortcuts: google, youtube, chatgpt, github, linkedin")
        site = input(f"\n{TerminalUI.BOLD}Input shortcut keyword string: {TerminalUI.RESET}").strip()
        result = self.web.open_website(site)
        print(f"\n{TerminalUI.GREEN}{result}{TerminalUI.RESET}")
        time.sleep(1.5)

    def run_voice(self):
        TerminalUI.clear_screen()
        TerminalUI.render_header("CORE 4: HANDS-FREE VOICE PIPELINE")
        print(f"{TerminalUI.YELLOW}Say 'back' out loud to exit to mainframe panel.{TerminalUI.RESET}\n")
        self.speaker.speak("Hands-free system tracking cores operational.")
        
        while True:
            # Execute audio capture on worker threads to keep UI fluid
            future_text = self.executor.submit(self.listener.listen)
            TerminalUI.show_spinner("System listening", duration=0.5)
            voice_text = future_text.result()
            
            if not voice_text:
                continue
                
            print(f"{TerminalUI.GREEN}Recognized Token:{TerminalUI.RESET} {voice_text}")
            
            if voice_text.lower() == "back":
                self.speaker.speak("Deactivating voice automated pipelines.")
                break
                
            is_shortcut = False
            for shortcut in self.web.shortcuts.keys():
                if shortcut in voice_text.lower():
                    response = self.web.open_website(shortcut)
                    self.speaker.speak(response)
                    is_shortcut = True
                    break
                    
            if is_shortcut:
                continue
                
            reply = self.ai.ask_jarvis(voice_text)
            # Run speaking asynchronously
            self.executor.submit(self.speaker.speak, reply)
            print(f"\n{TerminalUI.CYAN}{TerminalUI.BOLD}Jarvis:{TerminalUI.RESET} {reply}\n")

if __name__ == "__main__":
    jarvis = JarvisOrchestrator()
    jarvis.main_loop()