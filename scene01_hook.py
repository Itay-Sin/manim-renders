"""Scene 1: hook. ~9 s of motion plus a 1 s hold.

Two concept chips get mixed up, snap apart, and the example question appears
and parks top-right as the thread for the whole video.

Narration:
  0-5   "MCP and the semantic layer are two different ideas that often get
         mixed up."
  5-9   "Let's walk through both, with one example question."
"""

from manim import *
from common import (
    make_background, make_dot_grid, make_caption, make_chip, make_bubble,
    BG, INK, MUTED, PURPLE, TEAL, AMBER, GREY, UI_FONT,
)


class Scene01Hook(Scene):
    def construct(self):
        bg = make_background()
        grid = make_dot_grid()
        self.add(bg, grid)
        self.wait(0.3)  # house style: breath before the first play

        # Two concept chips, clearly apart (diagonal: the sem chip is wide,
        # so sharing a row would make them touch from frame one).
        mcp = make_chip("MCP", TEAL, "#EFF9F7")
        sem = make_chip("semantic layer", AMBER, "#FBF3E8")
        mcp.move_to(UP * 1.75 + LEFT * 1.4)
        sem.move_to(UP * 0.35 + RIGHT * 0.6)

        cap = make_caption("MCP and the semantic layer often get mixed up.")
        self.play(FadeIn(mcp, scale=0.9), FadeIn(sem, scale=0.9), FadeIn(cap),
                  run_time=0.9)
        # Voice sync: "mixed up" is heard at ~4.4 s (word table + 0.5 s mux
        # delay), so the tangle waits for it instead of leading it by 3 s.
        self.wait(2.9)

        # They drift into each other: the "mixed up" tangle. Corners overlap,
        # both labels stay readable. No set_opacity here: on the whole chip
        # group it would also crank the soft shadow copies to 0.85 and the
        # chips would drag a harsh dark shadow for the rest of the scene.
        self.play(
            mcp.animate.move_to(UP * 1.25 + LEFT * 1.0).rotate(0.06),
            sem.animate.move_to(UP * 0.62 + RIGHT * 0.5).rotate(-0.06),
            run_time=1.3,
        )
        # No wait: the snap apart rides straight out of the tangle, landing
        # on "Let's walk through both" (~5.3 s heard).

        # Snap apart to clean positions, stacked for the vertical frame.
        self.play(
            mcp.animate.rotate(-0.06).move_to(UP * 2.15),
            sem.animate.rotate(0.06).move_to(UP * 0.75),
            run_time=0.8,
        )

        # The one example question lands late, once both ideas are parted,
        # and stays where it appears (no park: it would crowd the top edge).
        bubble = make_bubble("show me my open SMB opportunities", width=4.9)
        bubble.move_to(DOWN * 1.3)
        cap2 = make_caption("Let's walk through both, with one example question.")
        # Voice sync: the bubble must not lead "one example question" (heard
        # ~6.6-7.2 s), so the swap follows the snap with no wait.
        self.play(FadeOut(cap), run_time=0.2)
        self.play(FadeIn(bubble, shift=UP * 0.2), FadeIn(cap2), run_time=0.7)
        cap = cap2
        self.play(Indicate(bubble.text, color=PURPLE, scale_factor=1.04),
                  run_time=0.8)

        # ------------------------------------------------- final hold ----
        # Audio (7.44 s mp3 + 0.5 s mux delay) ends ~7.94 s; this leaves a
        # ~1.2 s tail, above the 0.9 s minimum.
        self.wait(1.2)
