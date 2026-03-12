import sys
from pathlib import Path

# Ensure project root is on sys.path so all imports resolve
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gpiozero import Button
from signal import pause

from src.audio_io import start_recording, stop_recording
from src.assistant import run_pipeline


btn = Button(21, pull_up=True, bounce_time=0.1)


def on_press():
    print("🎤 Recording...")
    start_recording()


def on_release():
    print("⏹️ Stopped recording")
    wav_path = stop_recording()
    run_pipeline(wav_path)


btn.when_pressed = on_press
btn.when_released = on_release

print("🤖 Jarvis ready. Press button to talk (Ctrl+C to quit).")
pause()
