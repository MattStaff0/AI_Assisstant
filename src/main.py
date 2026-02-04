from gpiozero import Button
from signal import pause
import time

from gemini import GeminiClient

# BCM numbering (GPIO21). Physical pin 40.
btn = Button(21, pull_up=True, bounce_time=0.05)

gemini = GeminiClient(model="gemini-2.5-flash-lite")

def on_press():
    print(f"PRESSED  @ {time.strftime('%H:%M:%S')}")
    # This is where the logic should be placed in order to record a voice, this is SPEECH -> TEXT
    # After this we can either send the api response here or maybe in the on realease since this could just be updating a global variable and use it in on release!

def on_release():
    # This is where logic for turning the text to speech and then being able to output to speakers to hear
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