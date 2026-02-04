import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Always load .env from the project root (one level above src/)
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class GeminiClient:
    def __init__(self, model: str = "gemini-2.5-flash-lite"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(f"Missing GEMINI_API_KEY. Expected it in {ENV_PATH}")
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def ask(self, text: str) -> str:
        resp = self.client.models.generate_content(
            model=self.model,
            contents=text
        )
        return (resp.text or "").strip()
