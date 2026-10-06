#!/bin/bash
# usage: shrink2p.sh in.mp4 out.mp4
f=$1; o=$2; cd /tmp/$(basename $o .mp4)_2p 2>/dev/null || { mkdir -p /tmp/$(basename $o .mp4)_2p; cd /tmp/$(basename $o .mp4)_2p; }
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
vb=$(python3 -c "print(int(27.8*8*1024*1024/$d/1000 - 48))")
ffmpeg -y -loglevel error -i "$f" -vf "scale=1280:720,fps=24" -c:v libx264 -preset medium -tune animation -b:v ${vb}k -pass 1 -an -f mp4 /dev/null && \
ffmpeg -y -loglevel error -i "$f" -vf "scale=1280:720,fps=24" -c:v libx264 -preset medium -tune animation -b:v ${vb}k -pass 2 -c:a aac -b:a 48k -ac 1 "$o" && echo "ok $o $(du -m "$o"|cut -f1)MB"
