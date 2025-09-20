from gtts import gTTS
import os
import uuid
from pathlib import Path

class TTSTool:
    def __init__(self):
        self.audio_dir = Path("static/audio")
        self.audio_dir.mkdir(exist_ok=True)
    
    def generate_audio(self, text: str, language: str) -> str:
        """Generate audio file from text and return the file path."""
        try:
            # Create unique filename
            filename = f"audio_{uuid.uuid4().hex[:8]}.mp3"
            filepath = self.audio_dir / filename
            
            # Generate TTS
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(str(filepath))
            
            # Return relative path for web access
            return f"/static/audio/{filename}"
        except Exception as e:
            return f"TTS error: {str(e)}"
    
    def get_supported_languages(self) -> dict:
        """Return supported languages for gTTS."""
        return {
            "en": "English",
            "es": "Spanish", 
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh": "Chinese",
            "ar": "Arabic",
            "hi": "Hindi",
            "ur": "Urdu"
        }
