# JARVIS – AI Desktop Assistant

JARVIS is a desktop AI assistant built with **Python**, **Google Gemini API**, and **CustomTkinter**. The project combines conversational AI, voice interaction, note management, and simple desktop automation into a clean and easy-to-use application.

The main goal of this project was to explore how different Python libraries can work together to create a practical AI assistant with a modern desktop interface. The codebase is organized into separate modules so that new features can be added without affecting the existing functionality.

---

## Features

### AI Chat

* Chat with Google's Gemini model in real time
* Maintains conversation context during a session
* Gracefully handles API and network errors
* Simple and responsive chat interface

### Voice Assistant

* Convert speech to text using SpeechRecognition
* Hear AI responses through text-to-speech
* Hands-free interaction with voice commands

### Notes Manager

* Create personal notes
* View saved notes
* Delete notes when no longer needed
* Store notes locally using JSON

### Desktop Utilities

* Open frequently used websites
* Launch desktop applications
* Quick shortcuts for common tasks

### Modern User Interface

* Built entirely with CustomTkinter
* Clean dark theme
* Tab-based navigation
* Responsive desktop layout

### Reliability

* Handles invalid API keys
* Detects network failures
* Includes structured logging
* Prevents application crashes with exception handling

---

## Screenshots

### Home

<img src="screenshots/home.png" width="900">

### AI Chat

<img src="screenshots/chat.png" width="900">

### Voice Assistant

<img src="screenshots/voice.png" width="900">

### Notes

<img src="screenshots/notes.png" width="900">

---

## Tech Stack

**Language**

* Python 3.12+

**AI**

* Google Gemini API
* google-genai SDK

**GUI**

* CustomTkinter

**Voice**

* SpeechRecognition
* PyAudio
* pyttsx3

**Utilities**

* python-dotenv
* threading
* logging
* JSON
* webbrowser

---

## Project Structure

```text
jarvis_assistant/

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

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/jarvis-assistant.git
```

### 2. Move into the project directory

```bash
cd jarvis-assistant
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 5. Install the required packages

```bash
pip install -r requirements.txt
```

### 6. Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
MODEL_NAME=gemini-2.5-flash
```

---

## Running the Project

Start the application with:

```bash
python ui_app.py
```

Once the application starts, you can:

* Chat with Gemini AI
* Use voice commands
* Create and manage notes
* Open websites and desktop applications

---

## Future Improvements

Some features planned for future versions include:

* Persistent conversation history
* Support for multiple AI providers
* Weather information
* Calendar integration
* Email assistant
* File management tools
* System monitoring
* Plugin support
* User authentication
* Cross-platform installer

---

## License

This project is licensed under the **MIT License**.

---

## Author

**Mallidi Mohan**

B.Tech, Mathematics & Computing
Indian Institute of Technology Goa

**GitHub**

https://github.com/mallidimohan41297

**LinkedIn**

https://www.linkedin.com/in/mallidimohan

---

## Acknowledgements

Special thanks to the open-source community and the tools that made this project possible:

* Google Gemini API
* CustomTkinter
* SpeechRecognition
* Python Community

---

## Support

If you found this project helpful or interesting, consider giving the repository a ⭐. It helps others discover the project and motivates future improvements.
