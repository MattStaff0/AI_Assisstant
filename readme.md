This is the readme for the ai "jarvis"
All we have installed is ffmpeg, alsa-utils


The flow: 
sudo apt update
sudo apt install -y ffmpeg alsa-utils

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 main.py

Jan 20
    want to build the foundation with the button tap, pi listens for a couple seconds and then will send something to the gemini api, later will be able to route this to a local model on my pc
