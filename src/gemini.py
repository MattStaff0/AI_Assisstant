"""Gemini API client for Jarvis assistant with conversation memory."""
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load .env from repo root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

SYSTEM_INSTRUCTION = """You are Jarvis, a personal AI assistant.

Style:
- Keep responses to 1-3 sentences since you're speaking out loud
- Be helpful, friendly, and direct
- No markdown, bullet points, or special formatting - just natural speech
- Sound conversational, not robotic

You can help with anything: questions, outfit advice, planning, reminders, brainstorming, or just chatting."""


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")
        self.client = genai.Client(api_key=api_key)
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
        
        # Conversation memory
        self.history = []
        self.max_history = 10  # Keep last 10 exchanges (20 messages)
        self.last_interaction = time.time()
        self.timeout_minutes = 10  # Clear history after 10 min of inactivity

    def ask(self, prompt: str) -> str:
        # Auto-clear history if inactive for too long
        if time.time() - self.last_interaction > (self.timeout_minutes * 60):
            if self.history:
                print("🧹 Conversation cleared (timeout)")
            self.history = []
        
        self.last_interaction = time.time()
        
        # Add user message to history
        self.history.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })
        
        # Trim history if too long (keep last N exchanges)
        max_messages = self.max_history * 2  # Each exchange = 2 messages
        if len(self.history) > max_messages:
            self.history = self.history[-max_messages:]
        
        # Make API call with full history
        response = self.client.models.generate_content(
            model=self.model,
            contents=self.history,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
                "max_output_tokens": 150
            }
        )
        
        assistant_reply = response.text
        
        # Add assistant response to history
        self.history.append({
            "role": "model",
            "parts": [{"text": assistant_reply}]
        })
        
        return assistant_reply

    def clear_history(self):
        """Manually clear conversation history."""
        self.history = []
        print("🧹 Conversation cleared")