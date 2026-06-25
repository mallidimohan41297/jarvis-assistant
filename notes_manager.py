import os
import json
from datetime import datetime
from config import Config
from logger import logger

class NotesManager:
    def __init__(self):
        self.filename = Config.STORAGE_FILE
        self._initialize_storage()

    def _initialize_storage(self):
        if not os.path.exists(self.filename):
            try:
                with open(self.filename, "w", encoding="utf-8") as file:
                    json.dump({}, file)
            except IOError as e:
                logger.error(f"Failed to build file storage ecosystem: {e}")

    def _load_all_notes(self) -> dict:
        try:
            if not os.path.exists(self.filename):
                return {}
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            logger.error("Storage document corrupted. Resetting memory allocations.")
            return {}

    def _save_all_notes(self, notes: dict) -> bool:
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(notes, file, indent=4, ensure_ascii=False)
                return True
        except IOError as e:
            logger.error(f"Failed to execute local storage save: {e}")
            return False

    def save_note(self, title: str, content: str) -> str:
        if not title.strip():
            return "Error: Note title cannot be empty."
        notes = self._load_all_notes()
        notes[title] = {
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if self._save_all_notes(notes):
            return f"Successfully saved note: '{title}'"
        return "Error: Failed to write note data to local disk storage."

    def read_note(self, title: str) -> str:
        notes = self._load_all_notes()
        if title in notes:
            return f"\n--- {title} ({notes[title]['created_at']}) ---\n{notes[title]['content']}\n"
        return f"Error: Note titled '{title}' not found."

    def list_notes(self) -> str:
        notes = self._load_all_notes()
        if not notes:
            return "No notes stored inside the local storage file."
        output = "\n--- Contained Storage Sub-files ---\n"
        for index, title in enumerate(notes.keys(), 1):
            output += f"{index}. {title} (Saved on: {notes[title]['created_at']})\n"
        return output

    def delete_note(self, title: str) -> str:
        notes = self._load_all_notes()
        if title in notes:
            del notes[title]
            if self._save_all_notes(notes):
                return f"Successfully deleted note: '{title}'"
        return f"Error: Note titled '{title}' could not be located."