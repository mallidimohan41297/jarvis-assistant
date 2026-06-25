import webbrowser
import os
import subprocess
from logger import logger

class WebCommands:
    def __init__(self):
        # 🌐 1. Website Shortcuts
        self.shortcuts = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "chatgpt": "https://chatgpt.com",
            "github": "https://www.github.com",
            "linkedin": "https://www.linkedin.com",
            "instagram": "https://www.instagram.com",
            "coursera": "https://www.coursera.org",
            "udemy": "https://www.udemy.com",
            "gmail": "https://mail.google.com",
            "google classroom": "https://classroom.google.com"
        }
        
        # 💻 2. Windows System & Desktop App Shortcuts
        # Using exact Windows executable system hooks or default launcher paths
        self.apps = {
            # Standard System Tools
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "cmd": "cmd.exe",
            
            # Browsers
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "brave": "brave.exe",
            
            # Developer Code Editors
            "vscode": "code",
            "pycharm": "pycharm",
            "codeblocks": "codeblocks.exe",
            "devcpp": "devcpp.exe",
            "gitbash": "git-bash.exe",
            
            # Communication & Socials
            "telegram": "telegram.exe",
            
            # Gaming & Virtualization Engines
            "bluestacks": "HD-Player.exe",
            "virtualbox": "VirtualBox.exe"
        }

    def open_website(self, site_name: str) -> str:
        clean_name = site_name.strip().lower()
        
        # Action Step A: Handle Web Link Mapping
        if clean_name in self.shortcuts:
            url = self.shortcuts[clean_name]
            try:
                webbrowser.open(url)
                return f"Opening {site_name.capitalize()} in your browser, sir."
            except Exception as e:
                logger.error(f"Browser automation failed to open link path: {e}")
                return "System Error: Failed to open web browser."
                
        # Action Step B: Handle Local Application Launching
        elif clean_name in self.apps:
            app_cmd = self.apps[clean_name]
            try:
                # subprocess.Popen spawns the app process cleanly without halting Jarvis
                subprocess.Popen(app_cmd, shell=True)
                return f"Launching {site_name.capitalize()} right away, sir."
            except Exception as e:
                logger.error(f"Failed to launch desktop app: {e}")
                return f"System Error: Could not launch {site_name}."
                
        return f"Error: Command token '{site_name}' is not mapped inside my configurations."