import json
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("GEMINI_API_KEY", "test-key")

from notes_manager import NotesManager
from config import Config


class TestNotesManager(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.original = Config.STORAGE_FILE
        Config.STORAGE_FILE = str(Path(self.tmp.name) / "notes.json")
        self.notes = NotesManager()

    def tearDown(self):
        Config.STORAGE_FILE = self.original
        self.tmp.cleanup()

    def test_save_read_list_delete(self):
        self.assertIn("Successfully saved", self.notes.save_note("Test", "Hello"))
        self.assertIn("Hello", self.notes.read_note("Test"))
        self.assertIn("Test", self.notes.list_notes())
        self.assertIn("Successfully deleted", self.notes.delete_note("Test"))
        self.assertIn("not found", self.notes.read_note("Test"))

    def test_empty_title(self):
        self.assertIn("cannot be empty", self.notes.save_note("   ", "x"))

    def test_overwrite(self):
        self.notes.save_note("Test", "one")
        self.notes.save_note("Test", "two")
        self.assertIn("two", self.notes.read_note("Test"))
        with open(Config.STORAGE_FILE, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["Test"]["content"], "two")


if __name__ == "__main__":
    unittest.main()
