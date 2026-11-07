"""Caption track: subtitles burned at mux time, off the animation timeline.

The scenes render their captions fully transparent (see make_caption in
common.py); the visible captions come from here, driven by the narration's
own word timings, so they can never drift against the voice and never move
a visual.

Two jobs in one file:

1. As a script, it segments each scene's narration (vo_sNN.srt for the
   sentence text, words_sNN.txt for per-word onsets) into caption chunks
   and writes captions_sNN.tsv: display_start, display_end, text. Display
   times are in muxed-scene time: word onset + 0.5 s audio delay − 0.3 s
   caption lead. Chunks within a sentence run back to back.

2. As a Manim scene (CaptionPlate), it renders one caption plate — the
   exact make_caption geometry, visible — to a transparent full-frame PNG,
   for ffmpeg to overlay. Text comes from the CAPTION_TEXT env var:

   manim -s -t -r 1080,1350 caption_track.py CaptionPlate

Usage for the TSVs:

   python caption_track.py <scratchpad_dir> <scene_video_seconds...>

where the 12 durations cap each scene's last caption end.
"""
import os
import re
import sys

from manim import *
from common import INK, UI_FONT

MAX_CHARS = 44          # one plate line before scaling kicks in
LEAD = 0.30             # caption cuts in this long before its first word
MUX_DELAY = 0.50        # audio is muxed with this delay
SENT_TAIL = 0.70        # last chunk of a sentence lingers this long


def norm(w):
    return re.sub(r"[^\w'-]", "", w).lower()


def read_words(path):
    out = []
    for line in open(path):
        t, w = line.split(None, 1)
        out.append((float(t), w.strip()))
    return out


def read_srt_lines(path):
    lines = []
    for block in open(path).read().strip().split("\n\n"):
        rows = block.split("\n")
        lines.append(" ".join(" ".join(rows[2:]).split()))
    return lines


def chunk_sentence(words):
    """Split a sentence's (token, onset) list into caption-sized chunks,
    preferring to break just after punctuation."""
    chunks, cur, cur_len = [], [], 0
    for tok, t in words:
        add = len(tok) + (1 if cur else 0)
        if cur and cur_len + add > MAX_CHARS:
            chunks.append(cur)
            cur, cur_len = [], 0
            add = len(tok)
        cur.append((tok, t))
        cur_len += add
        if tok[-1] in ",;:" and cur_len >= 24:
            chunks.append(cur)
            cur, cur_len = [], 0
    if cur:
        chunks.append(cur)
    # A tiny trailing chunk ("out.") reads as a stutter: fold it back into
    # the previous chunk and let the plate scale the text instead.
    if len(chunks) > 1 and sum(len(t) + 1 for t, _ in chunks[-1]) <= 12:
        chunks[-2].extend(chunks.pop())
    return chunks


def build_tsv(base, idx, scene_len):
    words = read_words(f"{base}/words_s{idx}.txt")
    sentences = read_srt_lines(f"{base}/vo_s{idx}.srt")
    ptr = 0
    rows = []
    for sent in sentences:
        toks = sent.split()
        timed = []
        for tok in toks:
            if ptr < len(words) and norm(words[ptr][1]) == norm(tok):
                timed.append((tok, words[ptr][0]))
                ptr += 1
            elif timed:
                # Token the TTS merged or split; inherit the last onset.
                timed.append((tok, timed[-1][1]))
            else:
                timed.append((tok, words[ptr][0] if ptr < len(words) else 0))
        chunks = chunk_sentence(timed)
        for i, ch in enumerate(chunks):
            start = ch[0][1] + MUX_DELAY - LEAD
            if i + 1 < len(chunks):
                end = chunks[i + 1][0][1] + MUX_DELAY - LEAD
            else:
                nxt = words[ptr][0] + MUX_DELAY - LEAD if ptr < len(words) \
                    else scene_len
                end = min(ch[-1][1] + MUX_DELAY + SENT_TAIL + 0.6, nxt,
                          scene_len - 0.05)
            text = " ".join(t for t, _ in ch)
            rows.append((max(start, 0.05), end, text))
    with open(f"{base}/captions_s{idx}.tsv", "w") as f:
        for s, e, t in rows:
            f.write(f"{s:.2f}\t{e:.2f}\t{t}\n")
    return rows


class CaptionPlate(Scene):
    """One visible caption plate on a transparent frame, for overlaying."""

    def construct(self):
        text = os.environ["CAPTION_TEXT"]
        t = Text(text, font=UI_FONT, font_size=25, color=INK)
        if t.width > 5.5:
            t.scale_to_fit_width(5.5)
        plate = RoundedRectangle(corner_radius=0.19,
                                 width=t.width + 0.5, height=0.6)
        plate.set_stroke(width=0).set_fill("#FFFFFF", opacity=0.9)
        t.move_to(plate.get_center())
        g = VGroup(plate, t)
        g.to_edge(DOWN, buff=0.18)
        self.add(g)


if __name__ == "__main__":
    base = sys.argv[1]
    lens = [float(x) for x in sys.argv[2:]]
    for n, scene_len in enumerate(lens, start=1):
        idx = f"{n:02d}"
        rows = build_tsv(base, idx, scene_len)
        print(f"s{idx}: {len(rows)} captions, "
              f"last ends {rows[-1][1]:.2f} (video {scene_len})")
