#!/bin/bash
# usage: render/run_video.sh N   -> builds episodes of group N, combines, renders, shrinks to <30 MB
set -e
cd "$(dirname "$0")/.."
N=$1
OUT=$(python3 -c "import json;print(json.load(open('series.json'))['out'])")
PREFIX=$(python3 -c "import json;print(json.load(open('series.json')).get('file_prefix','Video'))")
for e in $(python3 -c "from combine import GROUPS;print(' '.join(str(x) for x in GROUPS[$N-1][1]))"); do python3 episodes/ep$(printf %02d $e).py; done
python3 combine.py $N
(cd render && python3 sprites_render.py > /dev/null)        # picks up any new speech bubbles
cd render
SLUG=$(python3 -c "import sys;sys.path.insert(0,'..');from combine import GROUPS;import re;print(re.sub(r'[^A-Za-z0-9]+','_',GROUPS[$N-1][0]).strip('_'))")
export PLAN=../$OUT/v$N/plan.json WORK=work_${OUT}_v$N OUTFILE="../$OUT/final/${PREFIX}${N}_${SLUG}.mp4" CRF=21
mkdir -p ../$OUT/final
echo "== v$N start $(date +%T)"
python3 engine.py tts
python3 engine.py steps > /dev/null
python3 engine.py all
cp $WORK/subtitles.srt "../$OUT/final/${PREFIX}${N}_${SLUG}.srt"
echo "== v$N done $(date +%T) $(du -m "$OUTFILE" | cut -f1) MB"
