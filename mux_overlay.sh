#!/bin/zsh
# Mux each scene's render with its delayed voiceover and burn the caption
# plates from captions_sNN.tsv as timed overlays. Usage: mux_overlay.sh
set -e
SP="/private/tmp/claude-504/-Users-itaysinvani-Itay-Second-Brain/c8c8dd9a-b39e-49e1-a5e7-c867b7fc366e/scratchpad"
FF=~/miniforge3/envs/manim/bin/ffmpeg
cd "$SP"

typeset -A VIDS
VIDS=(
  1 media-final2/videos/scene01_hook/1350p30/Scene01Hook.mp4
  2 media-final2/videos/scene02_what_is_mcp/1350p30/Scene02WhatIsMCP.mp4
  3 media-final2/videos/scene03_tools_and_flow/1350p30/Scene03ToolsAndFlow.mp4
  4 media-final2/videos/scene04_easy_question/1350p30/Scene04EasyQuestion.mp4
  5 media-final2/videos/scene05_knowledge/1350p30/Scene05Knowledge.mp4
  6 media-final2/videos/scene06_the_turn/1350p30/Scene06TheTurn.mp4
  7 media-final2/videos/scene07_smb_invisible/1350p30/Scene07SmbInvisible.mp4
  8 media-final2/videos/scene08_two_bad_options/1350p30/Scene08TwoBadOptions.mp4
  9 media-final2/videos/scene09_semantic_layer/1350p30/Scene09SemanticLayer.mp4
  10 media-final2/videos/scene10_resolved/1350p30/Scene10Resolved.mp4
  11 media-final2/videos/scene11_why_it_scales/1350p30/Scene11WhyItScales.mp4
  12 media-final2/videos/scene12_close/1350p30/Scene12Close.mp4
)

# Scenes whose top-right corner is busy carry no watermark: the question
# bubble reaches it in 4/6/7/8/9, the title strip in 2/5, and scene 12's
# closing elements cross it. Verified per-frame by scan_corner.py
# (operator note 2026-11-07).
NO_WM=(2 4 5 6 7 8 9 12)

for n in 1 2 3 4 5 6 7 8 9 10 11 12; do
  nn=$(printf "%02d" $n)
  tsv="captions_s${nn}.tsv"
  inputs=(-i "${VIDS[$n]}")
  filter=""
  prev="[0:v]"
  k=0
  while IFS=$'\t' read -r s e txt; do
    k=$((k+1))
    inputs+=(-i "plates/s${nn}_${k}.png")
    out="[v$k]"
    filter+="${prev}[${k}:v]overlay=0:0:enable='between(t,${s},${e})'${out};"
    prev="$out"
  done < "$tsv"
  if [[ ! " ${NO_WM[@]} " =~ " ${n} " ]]; then
    k=$((k+1))
    inputs+=(-i "plates/watermark.png")
    filter+="${prev}[${k}:v]overlay=0:0[v$k];"
    prev="[v$k]"
  fi
  inputs+=(-i "vo_s${nn}.mp3")
  aidx=$((k+1))
  # apad + -shortest: the audio is padded with REAL silence to exactly the
  # video's length. Without it each segment's audio ended at the voice, and
  # the concat stage filled the gap with smeared speech fragments (ghost
  # audio near every scene boundary). The talk track must live strictly
  # inside its own scene.
  filter+="[${aidx}:a]adelay=500|500,apad[aout]"
  $FF -y "${inputs[@]}" -filter_complex "$filter" \
    -map "$prev" -map "[aout]" -shortest \
    -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
    -c:a aac -b:a 160k "seg_s${n}.mp4" -loglevel error
  echo "seg_s${n}.mp4 done ($k captions)"
done
echo MUX_OVERLAY_ALL_DONE
