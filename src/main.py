from gpiozero import Button
from signal import pause
import time

# BCM numbering (GPIO21). Physical pin 40.
btn = Button(21, pull_up=True, bounce_time=0.05)

def on_press():
    print(f"PRESSED  @ {time.strftime('%H:%M:%S')}")

def on_release():
    print(f"RELEASED @ {time.strftime('%H:%M:%S')}")

btn.when_pressed = on_press
btn.when_released = on_release

print("Ready. Press the button (Ctrl+C to quit).")
pause()