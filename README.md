# JARVIS – AI Desktop Assistant

A modern AI-powered desktop assistant built with **Python**, **Google Gemini API**, and **CustomTkinter**, featuring an intuitive graphical interface for AI conversations, voice interaction, notes management, and browser automation.

---

## Overview

JARVIS is a modular desktop AI assistant inspired by intelligent virtual assistants. It combines Google's Gemini AI with speech recognition and desktop automation to provide a seamless user experience.

The project follows a modular architecture, making it easy to extend with new AI capabilities, voice features, productivity tools, and desktop integrations.

---

## Features

### AI Chat

* Real-time conversation with Google Gemini
* Context-aware chat sessions
* Automatic error handling
* Modern chat interface

### Voice Assistant

* Speech-to-text using SpeechRecognition
* Text-to-speech responses using pyttsx3
* Voice command support
* Hands-free interaction

### Notes Manager

* Create notes
* View saved notes
* Delete notes
* Local JSON-based storage

### Web & Applications

* Open websites
* Launch desktop applications
* Browser automation
* Quick productivity shortcuts

### Modern GUI

* Built with CustomTkinter
* Dark theme interface
* Responsive layout
* Multiple functional tabs
* Professional desktop design

### Error Handling

* API failure recovery
* Network exception handling
* Invalid API key detection
* Request retry mechanism
* Logging support

---

## Screenshots

### Main Interface

<img src="screenshots/home.png" width="900">

### AI Chat

<img src="screenshots/chat.png" width="900">

### Voice Assistant

<img src="screenshots/voice.png" width="900">

### Notes Manager

<img src="screenshots/notes.png" width="900">

---

## Tech Stack

### Programming Language

* Python 3.12+

### AI

* Google Gemini API
* google-genai SDK

### GUI

* CustomTkinter

### Voice

* SpeechRecognition
* PyAudio
* pyttsx3

### Utilities

* python-dotenv
* logging
* JSON
* threading
* webbrowser

---

## Project Structure

```
jarvis_assistant/

│
├── ui_app.py
├── main.py
├── config.py
├── gemini.py
├── listener.py
├── speaker.py
├── notes_manager.py
├── web_commands.py
├── logger.py
├── ui_renderer.py
├── exceptions.py
├── requirements.txt
├── .env.example
├── README.md
└── screenshots/
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/jarvis-assistant.git
```

Move into the project

```bash
cd jarvis-assistant
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
MODEL_NAME=gemini-2.5-flash
```

---

## Usage

Run the application

```bash
python ui_app.py
```

You can:

* Chat with Gemini AI
* Use voice commands
* Save and manage notes
* Open websites and applications
* Experience a modern desktop assistant

---

## Future Improvements

* Conversation history database
* Multiple AI providers (Gemini, OpenAI, Groq, OpenRouter)
* Weather integration
* Calendar integration
* Email assistant
* File management
* System monitoring
* Plugin architecture
* Authentication
* Cross-platform installer

---

## License

This project is licensed under the MIT License.

---

## Author

**Mallidi Mohan**

B.Tech Mathematics & Computing
Indian Institute of Technology Goa

GitHub:
https://github.com/mallidimohan41297

LinkedIn:
https://www.linkedin.com/in/mallidimohan

---

## Acknowledgements

* Google Gemini API
* CustomTkinter
* SpeechRecognition
* Python Community

---

## Star the Repository

If you found this project useful, consider giving it a ⭐ on GitHub.
