import json
import wave
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))

from vosk import Model, KaldiRecognizer
from config.settings import VOSK_MODEL_PATH, SAMPLE_RATE

print("Loading Vosk model...")
_model = Model(str(VOSK_MODEL_PATH))
print("Vosk model loaded.")


def transcribe_wav(wav_path: str) -> str:
    """Transcribe a wav file using Vosk. Returns transcript or empty string."""
    try:
        wf = wave.open(wav_path, "rb")
    except Exception as e:
        print(f"Cannot open wav: {e}")
        return ""

    rec = KaldiRecognizer(_model, SAMPLE_RATE)
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)
    wf.close()

    result = json.loads(rec.FinalResult())
    return result.get("text", "").strip()
