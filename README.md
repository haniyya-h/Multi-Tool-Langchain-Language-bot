# Language Learning Buddy 🌍

A complete AI-powered language learning application built with FastAPI, Groq LLM, and HTMX. Features interactive conversations with context memory and support for 13 languages including Urdu.

## Features

- **Translation Tool**: Translate text between 13 languages including Urdu
- **Grammar Correction**: Get grammar corrections with explanations in any supported language
- **Pronunciation Tool**: Generate audio pronunciation using gTTS
- **Interactive Conversation Practice**: Back-and-forth conversations with AI tutor that remembers context
- **AI Language Tutor**: Intelligent chat assistant with conversation memory
- **Real-time Audio**: Play pronunciation audio directly in the browser

## Prerequisites

- Python 3.8+
- Groq API key (get one at [console.groq.com](https://console.groq.com))

## Installation

1. **Clone or download this project**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Groq API key:**
   
   **Option A: Create a .env file (recommended)**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your actual API key
   # Get your API key from: https://console.groq.com
   ```
   
   **Option B: Environment variable**
   ```bash
   # Windows
   set GROQ_API_KEY=your_groq_api_key_here
   
   # Linux/Mac
   export GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application:**
   ```bash
   python run.py
   # OR
   uvicorn main:app --reload
   ```

5. **Open your browser and go to:**
   ```
   http://127.0.0.1:8000/
   ```

## Quick Start

1. **Translation**: Select languages and translate text instantly
2. **Grammar Check**: Get corrections with explanations
3. **Pronunciation**: Generate and play audio for any text
4. **Conversation Practice**: Start interactive roleplay scenarios
5. **AI Tutor**: Chat with an AI that remembers your conversation

## Usage

### Translation Tool
- Enter text you want to translate
- Select source and target languages (13 languages including Urdu)
- Get instant translation with formatted results

### Grammar Check
- Enter text to check
- Select the language
- Get corrections with detailed explanations

### Pronunciation Tool
- Enter text to pronounce
- Select the language
- Get an embedded audio player that works directly in the browser

### Interactive Conversation Practice
- Describe what you want to practice (e.g., "Ordering food at a restaurant")
- Select the target language
- Have back-and-forth conversations with the AI tutor
- AI remembers context and builds on previous responses
- Continue the conversation with new input fields

### AI Language Tutor
- Start a conversation about language learning
- AI remembers the entire conversation context
- Get personalized help based on conversation history
- Continue chatting with seamless input fields

### Supported Languages
English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, Arabic, Hindi, **Urdu**

## Key Features

### 🧠 **Context Memory**
- AI remembers entire conversation history
- Builds on previous responses for better learning
- Maintains context across multiple interactions

### 💬 **Interactive Conversations**
- Back-and-forth dialogue with AI tutor
- Real-time conversation practice
- Seamless input fields for continuing chats

### 🔊 **Audio Integration**
- Direct audio playback in browser
- No external audio players needed
- Works with all 13 supported languages

### 🌍 **Multi-Language Support**
- 13 languages including Urdu
- Bidirectional translation
- Language-specific grammar checking
- Native pronunciation for each language

## Project Structure

```
language_learning_buddy/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── tools/                 # Individual tool implementations
│   ├── translation_tool.py
│   ├── grammar_tool.py
│   ├── tts_tool.py
│   └── conversation_tool.py
├── templates/             # HTML templates
│   └── index.html
└── static/               # Static files
    ├── css/
    │   └── style.css
    └── audio/            # Generated audio files
```

## API Endpoints

- `GET /` - Main application interface
- `POST /translate` - Translation endpoint
- `POST /grammar` - Grammar correction endpoint
- `POST /pronounce` - Audio generation endpoint
- `POST /conversation` - Conversation practice endpoint
- `POST /chat` - AI agent chat endpoint

## Technologies Used

- **FastAPI**: Modern Python web framework
- **Groq**: High-performance LLM inference (llama-3.1-8b-instant model)
- **HTMX**: Dynamic HTML without JavaScript frameworks
- **Jinja2**: Template engine
- **gTTS**: Google Text-to-Speech for 13 languages including Urdu
- **Uvicorn**: ASGI server
- **python-dotenv**: Environment variable management

## Troubleshooting

### Common Issues

1. **"GROQ_API_KEY not found" error**
   - Make sure you've set the environment variable correctly
   - Restart your terminal/command prompt after setting the variable

2. **Audio files not playing**
   - Check that the `static/audio/` directory exists
   - Make sure your browser supports the audio format

3. **Translation not working**
   - Verify your Groq API key is valid
   - Check your internet connection

4. **Port already in use**
   - Change the port: `uvicorn main:app --reload --port 8001`

## Development

To run in development mode with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues, please check the troubleshooting section above or create an issue in the project repository.
