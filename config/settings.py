from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TMP_DIR = PROJECT_ROOT / "tmp"
VOSK_MODEL_PATH = PROJECT_ROOT / "models" / "vosk-model-small-en-us-0.15"

# Audio devices (named devices from ~/.asoundrc)
MIC_DEVICE = "mic"
SPEAKER_DEVICE = "speaker"

# Audio format (Vosk requires 16kHz mono)
SAMPLE_RATE = 16000
CHANNELS = 1
FORMAT = "S16_LE"

# Ensure tmp dir exists
TMP_DIR.mkdir(exist_ok=True)
