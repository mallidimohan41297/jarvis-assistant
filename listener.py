import speech_recognition as sr
from logger import logger

class VoiceListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 2500  # Adjusted sensitivity baseline
        self.recognizer.dynamic_energy_threshold = True

    def listen(self) -> str:
        """Captures audio waves safely, filtering out silence and environmental noise."""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
                audio_data = self.recognizer.listen(source, timeout=4, phrase_time_limit=8)
                return self.recognizer.recognize_google(audio_data)
        except sr.WaitTimeoutError:
            return ""  # Continuous cycling safety fallback
        except sr.UnknownValueError:
            return ""  # Unrecognized noise input parameters
        except sr.RequestError as e:
            logger.error(f"Voice transmission client handshake exception: {e}")
            return "System Error: Connection error with translation server."
        except Exception as e:
            logger.error(f"Critical audio parsing exception: {e}")
            return ""