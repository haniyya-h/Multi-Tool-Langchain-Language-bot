import groq
import os

class ConversationTool:
    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = "llama-3.1-8b-instant"
    
    def generate_conversation(self, prompt: str, language: str) -> str:
        """Generate a conversation dialogue."""
        try:
            conversation_prompt = f"""You are a {language} tutor. Roleplay a short conversation.
Keep sentences simple and encourage the learner to respond.
The conversation should be educational and engaging.

User prompt: {prompt}

Start the conversation:"""
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": conversation_prompt}],
                model=self.model_name,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Conversation generation error: {str(e)}"
