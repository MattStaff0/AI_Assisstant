import os
import subprocess
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))

from config.settings import SPEAKER_DEVICE


def speak(text: str):
    """Speak text using espeak-ng routed to the ALSA speaker device."""
    if not text or not text.strip():
        return
    env = os.environ.copy()
    env["ALSA_DEFAULT"] = SPEAKER_DEVICE
    try:
        subprocess.run(
            ["espeak-ng", text.strip()],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        print(f"TTS error: {e}")
