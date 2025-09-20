import groq
import os

class TranslationTool:
    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = "llama-3.1-8b-instant"
    
    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Translate text from source language to target language."""
        try:
            prompt = f"Translate this text from {src_lang} to {tgt_lang}:\n\n{text}\n\nTranslation:"
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.1
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Translation error: {str(e)}"
