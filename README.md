# AI Chatbot

This project is a program that can record a short 5 second audio clip from the user and transcribe it as an input using the OpenAI Whisper API as an input for OpenAI chatGPT input.
It will return it and using the google cloud tts API it will play an audio clip of the bots message.
I have set up a basic kind of darth vader voice using google cloud's tts, however there is not voice cloning on google cloud so it doesn't really sound like it. I tried google's free tts and it didn't have any customization options.
This google cloud one had some customization, but no cloning although it did have a free trial option.
The personality settings and voice modifications can be altered as needed.

---

## Features

- **Audio Recording**: Records user audio using the `sounddevice` library.
- **Speech Transcription**: Converts recorded speech to text using OpenAI's Whisper model.
- **AI Chat Response**: Generates conversational responses using OpenAI's GPT-3.5 Turbo API.
- **Text-to-Speech (TTS)**: Synthesizes responses into audio with Google Cloud Text-to-Speech.
- **Darth Vader Voice Effects**: Enhances the TTS output with pitch lowering, distortion, and metallic resonance.

---

## Setup and Installation

### Prerequisites
1. **Python 3.8 or newer**: Ensure Python is installed on your system. [Download Python](https://www.python.org/downloads/).
2. **Google Cloud API Key**: Obtain a JSON file for Google Cloud Text-to-Speech from [Google Cloud Console](https://console.cloud.google.com/).
3. **OpenAI API Key**: Obtain an API key from [OpenAI](https://platform.openai.com/).

### Dependencies
Install the required Python libraries with `pip`:

```bash
pip install openai-whisper pyttsx3 gtts pydub playsound google-cloud-texttospeech sounddevice soundfile keyboard
