#!/bin/bash
# One-time setup in a fresh container. Run from the videogen folder.
set -e
cd "$(dirname "$0")"
mkdir -p series episodes
pip install --break-system-packages -q piper-tts numpy scipy pillow playwright >/dev/null
which ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg >/dev/null)
mkdir -p ~/voices
# Download female voice (amy-medium) for young adult female narrator
[ -f ~/voices/en_US-amy-medium.onnx ] || python3 -m piper.download_voices en_US-amy-medium --data-dir ~/voices
cd render
[ -f bundle.js ] || { npm init -y >/dev/null; npm i -s @excalidraw/utils@0.1.5 esbuild >/dev/null; npx esbuild entry.js --bundle --format=iife --outfile=bundle.js --log-level=error; }
python3 sprites_render.py
chmod +x run_video.sh shrink2p.sh
echo "videogen ready"
