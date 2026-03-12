import threading
import time
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))

from src.stt_vosk import transcribe_wav
from src.tts_espeak import speak
from src.gemini import GeminiClient
from src.audio_io import cleanup

_lock = threading.Lock()
_gemini = GeminiClient()


def run_pipeline(wav_path: str):
    """Transcribe → Gemini → Speak. Thread-safe."""
    if not _lock.acquire(blocking=False):
        print("⏳ Still processing previous request...")
        return
    try:
        # Transcribe
        print("📝 Transcribing...")
        text = transcribe_wav(wav_path)
        if not text:
            print("❌ No speech detected")
            speak("Sorry, I didn't catch that")
            return

        print(f"   You said: {text}")

        # Gemini
        print("🤔 Thinking...")
        answer = _ask_gemini(text)
        if not answer:
            speak("Sorry, I couldn't get a response")
            return

        print(f"   Jarvis: {answer}")

        # Speak
        print("🔊 Speaking...")
        speak(answer)
        print("✅ Done")
    finally:
        cleanup(wav_path)
        _lock.release()


def _ask_gemini(prompt: str, max_retries: int = 3) -> str:
    """Call Gemini with retry + exponential backoff for 429s."""
    for attempt in range(max_retries):
        try:
            return _gemini.ask(prompt)
        except Exception as e:
            err = str(e)
            if "429" in err and attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"   Rate limited, retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"   Gemini error: {e}")
                return ""
    return ""
