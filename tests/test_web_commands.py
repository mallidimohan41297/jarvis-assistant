import unittest
from unittest.mock import patch

from web_commands import WebCommands


class TestWebCommands(unittest.TestCase):
    def setUp(self):
        self.web = WebCommands()

    @patch("web_commands.webbrowser.open")
    def test_open_website(self, mock_open):
        result = self.web.open_website("youtube")
        mock_open.assert_called_once_with("https://www.youtube.com")
        self.assertEqual(result, "Opening youtube.")

    @patch("web_commands.subprocess.Popen")
    def test_open_app(self, mock_popen):
        result = self.web.open_website("notepad")
        mock_popen.assert_called_once_with("notepad.exe", shell=True)
        self.assertEqual(result, "Launching notepad.")

    @patch("web_commands.webbrowser.open")
    def test_voice_command_routes_to_website(self, mock_open):
        result = self.web.handle_command("please open YouTube music")
        mock_open.assert_called_once_with("https://music.youtube.com")
        self.assertEqual(result, "Opening youtube music.")

    @patch("web_commands.subprocess.Popen")
    def test_voice_command_routes_to_app(self, mock_popen):
        result = self.web.handle_command("launch brave browser")
        mock_popen.assert_called_once_with("brave.exe", shell=True)
        self.assertEqual(result, "Launching brave.")

    def test_unknown_command_is_not_local_action(self):
        self.assertIsNone(self.web.handle_command("tell me about recursion"))


if __name__ == "__main__":
    unittest.main()
