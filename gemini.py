import time
from google import genai
from google.genai.errors import APIError
from config import Config
from logger import logger
from exceptions import ExternalAPIError
from ui_renderer import TerminalUI

class GeminiEngine:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            logger.critical("Initialization crash: API key missing from environment.")
            raise ExternalAPIError("Key configuration exception.")
        try:
            self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
            self.chat = self.client.chats.create(model=Config.MODEL_NAME)
        except Exception as e:
            logger.exception("Failed to connect initialization pipeline to Google Services.")
            raise ExternalAPIError(f"Handshake error: {e}")

    def ask_jarvis(self, user_message: str) -> str:
        """Sends user prompts to the Gemini API, utilizing exponential backoff for reliability."""
        TerminalUI.show_spinner("Inference engine executing")
        retries = 3
        delay = 1.0
        
        for attempt in range(retries):
            try:
                response = self.chat.send_message(user_message)
                return response.text
            except APIError as e:
                logger.warning(f"API Error on attempt {attempt + 1}: {e.message}")
                if attempt < retries - 1:
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    return "System Error: Network connection dropped. Please check your link connection."
            except Exception as e:
                logger.error(f"Unexpected runtime failure: {str(e)}")
                return "System Error: Internal calculation error encountered."