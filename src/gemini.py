import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # reads .env from repo root if you run from root; see note below

class GeminiClient:
    def __init__(self, model: str = "gemini-2.0-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("Missing GEMINI_API_KEY. Put it in .env or export it.")
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def ask(self, text: str) -> str:
        resp = self.client.models.generate_content(
            model=self.model,
            contents=text
        )
        return (resp.text or "").strip()