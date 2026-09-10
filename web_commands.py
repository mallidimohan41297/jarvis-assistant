import re
import subprocess
import webbrowser

from logger import logger


class WebCommands:
    def __init__(self):
        self.shortcuts = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "youtube music": "https://music.youtube.com",
            "chatgpt": "https://chatgpt.com",
            "github": "https://www.github.com",
            "linkedin": "https://www.linkedin.com",
            "instagram": "https://www.instagram.com",
            "coursera": "https://www.coursera.org",
            "udemy": "https://www.udemy.com",
            "gmail": "https://mail.google.com",
            "google classroom": "https://classroom.google.com",
        }

        self.apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "calc": "calc.exe",
            "paint": "mspaint.exe",
            "cmd": "cmd.exe",
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "brave": "brave.exe",
            "vscode": "code",
            "vs code": "code",
            "pycharm": "pycharm",
            "codeblocks": "codeblocks.exe",
            "devcpp": "devcpp.exe",
            "gitbash": "git-bash.exe",
            "telegram": "telegram.exe",
            "bluestacks": "HD-Player.exe",
            "virtualbox": "VirtualBox.exe",
        }

    @staticmethod
    def _normalize(text):
        text = text.lower().strip()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return re.sub(r"\s+", " ", text)

    @staticmethod
    def _remove_action_words(text):
        return re.sub(
            r"\b(please|open|launch|start|run|go to|show me|visit)\b",
            " ",
            text,
        )

    def _find_target(self, text):
        normalized = self._normalize(text)
        cleaned = self._remove_action_words(normalized)
        candidates = sorted(
            list(self.shortcuts) + list(self.apps),
            key=len,
            reverse=True,
        )

        for name in candidates:
            if re.search(rf"\b{re.escape(name)}\b", cleaned):
                return name
        return None

    def handle_command(self, command):
        """Return a result only when the command maps to a local action."""
        target = self._find_target(command)
        if not target:
            return None
        return self.open_website(target)

    def open_website(self, site_name):
        clean_name = self._normalize(site_name)

        if clean_name in self.shortcuts:
            url = self.shortcuts[clean_name]
            try:
                webbrowser.open(url)
                return f"Opening {clean_name}."
            except Exception as exc:
                logger.error(f"Browser action failed: {exc}")
                return "Could not open the browser."

        if clean_name in self.apps:
            try:
                subprocess.Popen(self.apps[clean_name], shell=True)
                return f"Launching {clean_name}."
            except Exception as exc:
                logger.error(f"App launch failed: {exc}")
                return f"Could not launch {clean_name}."

        return None
