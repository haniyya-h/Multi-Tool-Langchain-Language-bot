import groq
import os

class GrammarTool:
    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = "llama-3.1-8b-instant"
    
    def correct_grammar(self, text: str, language: str) -> str:
        """Correct grammar and provide explanation."""
        try:
            prompt = f"Correct this sentence in {language}. Also explain the correction briefly in English.\n\nOriginal: {text}\n\nCorrected:"
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.1
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Grammar correction error: {str(e)}"
