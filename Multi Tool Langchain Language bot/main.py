from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import groq
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import tools
from tools.translation_tool import TranslationTool
from tools.grammar_tool import GrammarTool
from tools.tts_tool import TTSTool
from tools.conversation_tool import ConversationTool

app = FastAPI(title="Language Learning Buddy")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Initialize tools (will be created when needed)
translation_tool = None
grammar_tool = None
tts_tool = None
conversation_tool = None

def get_tools():
    """Initialize tools when needed to ensure API key is available."""
    global translation_tool, grammar_tool, tts_tool, conversation_tool
    
    # Check if API key is set
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise Exception("GROQ_API_KEY environment variable is not set. Please set your Groq API key.")
    
    if translation_tool is None:
        try:
            translation_tool = TranslationTool()
            grammar_tool = GrammarTool()
            tts_tool = TTSTool()
            conversation_tool = ConversationTool()
        except Exception as e:
            raise Exception(f"Failed to initialize tools. Please check your GROQ_API_KEY: {str(e)}")
    
    return translation_tool, grammar_tool, tts_tool, conversation_tool

# Simple Groq wrapper class for AI chat
class GroqLLM:
    def __init__(self, api_key: str, model_name: str = "llama-3.1-8b-instant"):
        self.client = groq.Groq(api_key=api_key)
        self.model_name = model_name
    
    def chat(self, message: str, conversation_history: list = None) -> str:
        try:
            # Create a system prompt that explains the available tools
            system_prompt = """You are a helpful language learning assistant. You have access to these tools:
1. Translation: Translate text between languages
2. Grammar Correction: Correct grammar and explain errors
3. Pronunciation: Generate audio pronunciation
4. Conversation Practice: Create roleplay conversations

When users ask for specific tasks, guide them to use the appropriate tool. For general language learning questions, provide helpful advice."""
            
            # Build messages with conversation history
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

# Initialize Groq LLM for chat (will be created when needed)
llm = None

# Conversation state management
conversations = {}  # Store conversation history by session ID

def get_llm():
    """Initialize LLM when needed to ensure API key is available."""
    global llm
    if llm is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise Exception("GROQ_API_KEY environment variable is not set. Please set your Groq API key.")
        llm = GroqLLM(api_key=api_key, model_name="llama-3.1-8b-instant")
    return llm

def get_conversation(session_id: str):
    """Get or create conversation history for a session."""
    if session_id not in conversations:
        conversations[session_id] = []
    return conversations[session_id]

def add_to_conversation(session_id: str, role: str, content: str):
    """Add a message to conversation history."""
    conversation = get_conversation(session_id)
    conversation.append({"role": role, "content": content})
    # Keep only last 20 messages to avoid context overflow
    if len(conversation) > 20:
        conversation.pop(0)

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/translate")
async def translate(
    text: str = Form(...),
    src_lang: str = Form(...),
    tgt_lang: str = Form(...)
):
    """Translate text from source to target language."""
    try:
        translation_tool, _, _, _ = get_tools()
        result = translation_tool.translate(text, src_lang, tgt_lang)
        
        # Return HTML instead of JSON
        translation_html = f"""
        <div class="success">
            <h3>Translation Result</h3>
            <p><strong>Original ({src_lang}):</strong> {text}</p>
            <p><strong>Translation ({tgt_lang}):</strong> {result}</p>
        </div>
        """
        return HTMLResponse(content=translation_html)
    except Exception as e:
        error_html = f"""
        <div class="error">
            <h3>Translation Error</h3>
            <p>{str(e)}</p>
        </div>
        """
        return HTMLResponse(content=error_html, status_code=500)

@app.post("/grammar")
async def grammar_check(
    text: str = Form(...),
    language: str = Form(...)
):
    """Correct grammar and provide explanation."""
    try:
        _, grammar_tool, _, _ = get_tools()
        result = grammar_tool.correct_grammar(text, language)
        
        # Return HTML instead of JSON
        grammar_html = f"""
        <div class="success">
            <h3>Grammar Correction</h3>
            <p><strong>Original:</strong> {text}</p>
            <p><strong>Corrected:</strong></p>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 10px;">
                {result}
            </div>
        </div>
        """
        return HTMLResponse(content=grammar_html)
    except Exception as e:
        error_html = f"""
        <div class="error">
            <h3>Grammar Check Error</h3>
            <p>{str(e)}</p>
        </div>
        """
        return HTMLResponse(content=error_html, status_code=500)

@app.post("/pronounce")
async def pronounce(
    text: str = Form(...),
    language: str = Form(...)
):
    """Generate audio pronunciation."""
    try:
        _, _, tts_tool, _ = get_tools()
        audio_path = tts_tool.generate_audio(text, language)
        
        # Return HTML with audio element instead of JSON
        audio_html = f"""
        <div class="success">
            <h3>Audio Generated Successfully!</h3>
            <p><strong>Text:</strong> {text}</p>
            <p><strong>Language:</strong> {language}</p>
            <audio controls style="width: 100%; margin-top: 10px;">
                <source src="{audio_path}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        </div>
        """
        return HTMLResponse(content=audio_html)
    except Exception as e:
        error_html = f"""
        <div class="error">
            <h3>Error Generating Audio</h3>
            <p>{str(e)}</p>
        </div>
        """
        return HTMLResponse(content=error_html, status_code=500)

@app.post("/conversation")
async def conversation(
    prompt: str = Form(...),
    language: str = Form(...),
    session_id: str = Form("default"),
    user_response: str = Form("")
):
    """Generate interactive conversation practice."""
    try:
        llm = get_llm()
        conversation_history = get_conversation(session_id)
        
        if not user_response:
            # Start new conversation
            system_prompt = f"""You are a {language} language tutor. Start a conversation about: {prompt}
            
Keep the conversation simple and educational. Ask questions to encourage the learner to respond.
Start with a greeting and the first question or statement about the topic.
Keep responses short and encourage participation."""
            
            # Clear previous conversation for new topic
            conversations[session_id] = []
            add_to_conversation(session_id, "system", system_prompt)
            
            # Get initial AI response
            result = llm.chat("", conversation_history)
            add_to_conversation(session_id, "assistant", result)
        else:
            # Continue existing conversation
            add_to_conversation(session_id, "user", user_response)
            
            # Get AI response
            result = llm.chat(user_response, conversation_history)
            add_to_conversation(session_id, "assistant", result)
        
        # Return HTML with conversation history
        conversation_html = f"""
        <div class="success">
            <h3>Conversation Practice - {language.title()}</h3>
            <p><strong>Topic:</strong> {prompt}</p>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 10px;">
                {result}
            </div>
            <div style="margin-top: 15px;">
                <form hx-post="/conversation" hx-target="#conversation-result" hx-indicator="#conversation-loading" style="display: flex; gap: 10px;">
                    <input type="hidden" name="prompt" value="{prompt}">
                    <input type="hidden" name="language" value="{language}">
                    <input type="hidden" name="session_id" value="{session_id}">
                    <input type="text" name="user_response" placeholder="Your response in {language}..." style="flex: 1; padding: 10px; border: 2px solid #e2e8f0; border-radius: 5px;" required>
                    <button type="submit" style="padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                </form>
                <div id="conversation-loading" class="loading" hx-indicator>Thinking...</div>
                <div style="margin-top: 10px;">
                    <button onclick="location.reload()" style="padding: 8px 16px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">Start New Conversation</button>
                </div>
            </div>
        </div>
        """
        return HTMLResponse(content=conversation_html)
    except Exception as e:
        error_html = f"""
        <div class="error">
            <h3>Conversation Error</h3>
            <p>{str(e)}</p>
        </div>
        """
        return HTMLResponse(content=error_html, status_code=500)

@app.post("/chat")
async def chat(message: str = Form(...), session_id: str = Form("default")):
    """AI chat endpoint with conversation history."""
    try:
        llm = get_llm()
        
        # Get conversation history
        conversation_history = get_conversation(session_id)
        
        # Add user message to conversation
        add_to_conversation(session_id, "user", message)
        
        # Get AI response with conversation history
        result = llm.chat(message, conversation_history)
        
        # Add AI response to conversation
        add_to_conversation(session_id, "assistant", result)
        
        # Return HTML with conversation history
        chat_html = f"""
        <div class="success">
            <h3>AI Response</h3>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 10px;">
                {result}
            </div>
            <div style="margin-top: 15px;">
                <form hx-post="/chat" hx-target="#chat-result" hx-indicator="#chat-loading" style="display: flex; gap: 10px;">
                    <input type="hidden" name="session_id" value="{session_id}">
                    <input type="text" name="message" placeholder="Continue the conversation..." style="flex: 1; padding: 10px; border: 2px solid #e2e8f0; border-radius: 5px;" required>
                    <button type="submit" style="padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                </form>
                <div id="chat-loading" class="loading" hx-indicator>Thinking...</div>
            </div>
        </div>
        """
        return HTMLResponse(content=chat_html)
    except Exception as e:
        error_html = f"""
        <div class="error">
            <h3>Chat Error</h3>
            <p>{str(e)}</p>
        </div>
        """
        return HTMLResponse(content=error_html, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
