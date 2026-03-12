"""Gemini API client for Jarvis assistant."""
import os
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

    def ask(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
                "max_output_tokens": 150  # Keeps responses short + saves tokens
            }
        )
        return response.text.strip()