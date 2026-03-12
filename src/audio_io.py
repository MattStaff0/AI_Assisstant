import subprocess
import time
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))

from config.settings import MIC_DEVICE, SAMPLE_RATE, CHANNELS, FORMAT, TMP_DIR

_process = None
_wav_path = None


def start_recording():
    """Start recording audio via arecord. Returns the wav path."""
    global _process, _wav_path
    _wav_path = str(TMP_DIR / f"recording_{int(time.time())}.wav")
    try:
        _process = subprocess.Popen(
            ["arecord", "-D", MIC_DEVICE, "-f", FORMAT,
             "-r", str(SAMPLE_RATE), "-c", str(CHANNELS), _wav_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        print(f"Recording error: {e}")
        _process = None
    return _wav_path


def stop_recording():
    """Stop the arecord subprocess. Returns the wav path."""
    global _process
    if _process:
        _process.terminate()
        _process.wait()
        _process = None
    return _wav_path


def cleanup(wav_path):
    """Delete a wav file."""
    try:
        __import__("os").remove(wav_path)
    except OSError:
        pass
