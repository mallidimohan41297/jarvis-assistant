# 🤖 JARVIS - My AI Desktop Assistant

Welcome to **Jarvis**! I am 17 years old, and I built this production-grade, modular AI desktop assistant using Python and the Google Gemini API. It can talk, listen, manage notes, and control apps on my Windows computer.

---

## 🚀 Cool Features I Built

* **🧠 AI Brain Mode:** Powered by the brand-new Google Gemini 2.5 Flash model to answer any question instantly.
* **🎙️ Hands-Free Voice Mode:** Speaks out loud to me and listens to my voice using my microphone.
* **💻 Windows App Control:** Opens apps right off my desktop screen (like VS Code, Chrome, PyCharm, and BlueStacks).
* **📓 Local Notebook Ledger:** Saves private notes directly onto my hard drive inside a `notes.json` file.
* **🎨 Professional UI:** Features a cool, custom-colored terminal menu layout with loading animations.

---

## 📂 Project Structure

This project follows clean code principles by splitting tasks into different files:

* `main.py` - The central nervous system that runs the main menu loops.
* `gemini.py` - Manages connection streams to the Google Gemini AI core.
* `web_commands.py` - Handles browser links and opens Windows applications.
* `listener.py` & `speaker.py` - Controls the microphone ears and vocal speech engines.
* `notes_manager.py` - Handles local database writing and file management.
* `ui_renderer.py` - Renders the clean terminal interface boxes and animations.

---

## 🛠️ Installation & Setup

If you want to run my project on your computer, follow these simple steps:

1. **Install the required packages:**
   ```bash
   pip install google-genai python-dotenv SpeechRecognition pyttsx3 pyaudio
