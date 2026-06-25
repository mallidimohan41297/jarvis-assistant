import pyttsx3
from logger import logger

class VoiceSpeaker:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self._configure_voice()
        except Exception as e:
            logger.critical(f"Failed to instantiate native audio speech drivers: {e}")
            self.engine = None

    def _configure_voice(self):
        if not self.engine:
            return
        try:
            self.engine.setProperty("rate", 175)
            self.engine.setProperty("volume", 1.0)
            voices = self.engine.getProperty("voices")
            
            # Safe index boundary fallback implementation
            if len(voices) > 1:
                self.engine.setProperty("voice", voices[1].id)
            elif len(voices) > 0:
                self.engine.setProperty("voice", voices[0].id)
        except Exception as e:
            logger.error(f"Voice driver calibration adjustment failure: {e}")

    def speak(self, text: str):
        if not text.strip() or not self.engine:
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Vocal synthesis engine failed to write wave stream: {e}")