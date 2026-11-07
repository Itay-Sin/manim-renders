"""Scene 11: why it scales. ~10 s of motion plus a 1 s hold.

The semantic model grows into a tall stack outside the AI client, while the
context window stays nearly empty: 55,000 tokens crossed out, a few hundred
in their place.

Narration (srt + 0.5 s):
  0.55   "And because the semantic model sits outside the LLM, it can be
          huge."
  4.67   "You only spend tokens on that short exchange, not on tens of
          thousands of tokens of definitions."
"""

from manim import *
from common import (
    make_ai_client, make_background, make_caption, make_dot_grid,
    make_sem_card, ctx_fill_target,
    BG, INK, MUTED, PURPLE, TEAL, GREY, SLATE, AMBER, ALERT_RED,
    CODE_FONT, UI_FONT,
)


class Scene11WhyItScales(Scene):
    def construct(self):
        bg = make_background()
        grid = make_dot_grid()

        # The client moves to the upper left, still carrying its dimmed LLM
        # and nearly empty context window from scene 10.
        client = make_ai_client()
        client.llm.set_stroke(PURPLE, 3, opacity=0.35)
        client.llm.set_fill(PURPLE, opacity=0.02)
        client.llm_label.set_opacity(0.4)
        client.scale(0.62).move_to(LEFT * 1.35 + UP * 1.7)
        client.ctx_fill.become(ctx_fill_target(client, 0.18))

        self.add(bg, grid, client)
        self.wait(0.3)

        # ------ beat 1: the model can be huge (0.5-4.6 s) -----------------
        cap = make_caption("The semantic model sits outside the LLM.")
        seed = VGroup(*[
            make_sem_card().shift(UP * 0.13 * i + RIGHT * 0.07 * i)
            for i in range(4)
        ])
        seed.move_to(RIGHT * 1.95 + DOWN * 2.6)
        self.play(FadeIn(cap), FadeIn(seed, shift=LEFT * 0.4), run_time=0.7)

        # The stack grows and grows: thousands of definitions, none of them
        # anywhere near the context window.
        tall = VGroup()
        for i in range(12):
            c = make_sem_card()
            c.move_to(RIGHT * (1.95 + 0.05 * (i % 3))
                      + DOWN * 2.0 + UP * i * 0.48)
            tall.add(c)
        # Word-level sync: the growth finishes as "it can be huge" lands
        # (heard 3.6-3.9 s) instead of a second before it.
        self.wait(0.5)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in tall],
                        lag_ratio=0.12),
            run_time=1.8,
        )
        big_tag = Text("thousands of definitions", font=UI_FONT, font_size=15,
                       color=AMBER)
        big_tag.rotate(PI / 2)
        big_tag.next_to(tall, RIGHT, buff=0.14)
        self.play(FadeIn(big_tag), run_time=0.4)
        self.wait(1.0)

        # ------ beat 2: you only pay for the exchange (4.7-9.7 s) ---------
        cap2 = make_caption("You only pay for the short exchange.")
        self.play(FadeOut(cap), run_time=0.2)
        self.play(FadeIn(cap2),
                  Indicate(client.ctx_outline, color=PURPLE,
                           scale_factor=1.08),
                  run_time=0.7)
        cap = cap2

        # Two tiny packets trade places between client and stack: that is
        # the whole token bill.
        out_pkt = RoundedRectangle(corner_radius=0.08, width=0.3, height=0.16)
        out_pkt.set_stroke(width=0).set_fill(PURPLE, 1.0)
        out_pkt.move_to(client.shell.get_right() + RIGHT * 0.1)
        in_pkt = RoundedRectangle(corner_radius=0.08, width=0.3, height=0.16)
        in_pkt.set_stroke(width=0).set_fill(AMBER, 1.0)
        in_pkt.move_to(tall[2].get_left() + LEFT * 0.1 + DOWN * 0.25)
        out_home = out_pkt.get_center()
        in_home = in_pkt.get_center()
        # The exchange runs twice: the scene's whole claim is this loop, and
        # one 0.8 s pass was gone before it registered. Each pass fades in,
        # travels, fades out, so nothing teleports between passes.
        for _ in range(2):
            out_pkt.move_to(out_home)
            in_pkt.move_to(in_home)
            self.play(FadeIn(out_pkt), FadeIn(in_pkt), run_time=0.15)
            self.play(
                out_pkt.animate.move_to(tall[2].get_left() + LEFT * 0.1),
                in_pkt.animate.move_to(client.shell.get_right()
                                       + RIGHT * 0.1 + DOWN * 0.25),
                run_time=0.7,
            )
            self.play(FadeOut(out_pkt, scale=0.4), FadeOut(in_pkt, scale=0.4),
                      run_time=0.15)

        # The old bill, crossed out; the new one, barely a number.
        old_num = Text("55,000 tokens", font=UI_FONT, font_size=22,
                       color=MUTED)
        old_num.move_to(LEFT * 1.35 + DOWN * 0.75)
        strike = Line(old_num.get_left() + LEFT * 0.08,
                      old_num.get_right() + RIGHT * 0.08)
        strike.set_stroke(ALERT_RED, 3)
        # Text, not Integer: DecimalNumber renders through LaTeX, which this
        # machine does not have.
        new_val = ValueTracker(0)
        new_unit = Text("tokens", font=UI_FONT, font_size=16, color=MUTED)
        new_unit.next_to(old_num, DOWN, buff=0.3)
        new_unit.shift(RIGHT * 0.55)
        new_num = always_redraw(
            lambda: Text(f"{int(new_val.get_value()):,}", font=UI_FONT,
                         font_size=30, color=INK)
            .next_to(new_unit, LEFT, buff=0.12, aligned_edge=DOWN))
        # INK, not teal: teal is reserved for executing code, and this is a
        # number.
        few_tag = Text("a few hundred", font=UI_FONT, font_size=14,
                       color=INK)
        few_tag.next_to(new_unit, DOWN, buff=0.14)

        self.play(FadeIn(old_num), run_time=0.4)
        # The unit fades in with the strike, so it doesn't pop in one frame.
        self.play(Create(strike), FadeIn(new_unit), run_time=0.4)
        self.add(new_num)
        self.play(new_val.animate.set_value(340), run_time=1.1)
        self.play(FadeIn(few_tag), run_time=0.3)

        # ------------------------------------------------- final hold ----
        self.wait(1.7)
