from gpiozero import Button
from signal import pause
import time

from gemini import GeminiClient

# BCM numbering (GPIO21). Physical pin 40.
btn = Button(21, pull_up=True, bounce_time=0.05)

gemini = GeminiClient(model="gemini-2.0-flash")

def on_press():
    print(f"PRESSED  @ {time.strftime('%H:%M:%S')}")

def on_release():
    print(f"RELEASED @ {time.strftime('%H:%M:%S')}")
    prompt = "Give me a one-sentence helpful tip for staying productive tonight."
    try:
        answer = gemini.ask(prompt)
        print(f"Gemini: {answer}\n")
    except Exception as e:
        print(f"Gemini error: {e}\n")

btn.when_pressed = on_press
btn.when_released = on_release

print("Ready. Press the button (Ctrl+C to quit).")
pause()