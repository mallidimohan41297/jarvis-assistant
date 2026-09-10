# JARVIS — AI Desktop Assistant

A lightweight Python desktop assistant using Google's Gemini API, voice input/output, local notes, and desktop/web shortcuts.

## Features

- Gemini conversational AI
- Voice input with SpeechRecognition
- Text-to-speech with pyttsx3
- Local JSON notes
- Website and Windows app shortcuts
- Natural commands such as `open YouTube music` or `launch Brave`
- Automated tests
- Minimal white/orange terminal UI

## Setup

### 1. Python

Use Python 3.13 on Windows for the smoothest dependency installation.

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env` and add your own API key:

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Never commit `.env` or place an API key directly in source code.

### 4. Run

```bash
python main.py
```

### 5. Test

```bash
python -m pytest -q
```

## Voice examples

- `open YouTube music`
- `open GitHub`
- `launch Brave`
- `open VS Code`
- `open Gmail`
- `open Calculator`
- Normal questions are sent to Gemini when they are not local commands.

## Project structure

```text
.
├── main.py
├── gemini.py
├── config.py
├── web_commands.py
├── notes_manager.py
├── listener.py
├── speaker.py
├── ui_renderer.py
├── logger.py
├── exceptions.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Security

API keys are loaded from `.env` and `.env` is excluded by `.gitignore`. Use a fresh key for your local setup and never publish it to GitHub.
