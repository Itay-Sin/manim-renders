"""Scene 6: the turn. ~5.4 s of motion plus a 0.6 s hold (6.0 s).

One word changes and the whole thing breaks: SMB lands in the question in
red, and the frame dims around it. Ends dimmed, which scene 7 opens on.

Narration (srt + 0.5 s):
  0.55   "Now change one word."
  1.78   "Show me my open SMB opportunities."
"""

from manim import *
from common import (
    make_ai_client, make_mcp_server, make_api_box, make_background,
    make_tool_card, make_caption, make_dot_grid, make_bubble,
    ctx_fill_target, make_shadow,
    BG, INK, MUTED, PURPLE, TEAL, GREY, SLATE, ALERT_RED,
    CODE_FONT, UI_FONT,
)

TOOL_SPECS = [
    ("fetch_opportunities", "Returns opportunities, filtered by status",
     "status: open | closed"),
    ("fetch_accounts", "Returns accounts and their fields",
     "account_id: text"),
    ("update_deal", "Updates fields on one deal",
     "deal_id, fields"),
]


class Scene06TheTurn(Scene):
    def construct(self):
        # --------------------- base layout, as scene 5 left it ------------
        bg = make_background()
        grid = make_dot_grid()
        client = make_ai_client().move_to(UP * 1.78)
        server = make_mcp_server().move_to(DOWN * 0.92)
        apis = make_api_box().move_to(DOWN * 2.52)

        cards = VGroup(*[make_tool_card(*s) for s in TOOL_SPECS])
        cards.arrange(RIGHT, buff=0.18)
        cards.scale_to_fit_width(5.1)
        for card, dx in zip(cards, (-1.0, 0.0, 1.0)):
            card.scale(0.56).move_to(
                client.llm.get_center() + DOWN * 0.1 + RIGHT * dx)
        apis.endpoints.set_opacity(0.55)
        client.ctx_fill.become(ctx_fill_target(client, 0.92))

        # Matches scene 5's end state: one meter row — number, unit, tag —
        # centred in the gap between the LLM box and the context bar, so
        # nothing jumps at the cut (operator note 2026-11-07).
        meter_num = Text("55,000", font=UI_FONT, font_size=18, color=INK)
        meter_unit = Text("tokens", font=UI_FONT, font_size=12, color=MUTED)
        before_tag = Text("before any work", font=UI_FONT, font_size=11,
                          color=MUTED)
        meter = VGroup(meter_num, meter_unit, before_tag)
        meter.arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
        gap_y = (client.llm.get_bottom()[1]
                 + client.ctx_outline.get_top()[1]) / 2
        meter.move_to([client.shell.get_center()[0], gap_y, 0])

        wire_top = Line(client.shell.get_bottom(), server.shell.get_top())
        wire_bot = Line(server.shell.get_bottom(), apis.shell.get_top())
        for w in (wire_top, wire_bot):
            w.set_stroke(GREY, 2.2, opacity=0.75)

        self.add(bg, grid, wire_top, wire_bot, client, server, apis,
                 cards, meter)
        self.wait(0.3)

        # ------------- beat 1: the question returns (0.5-1.7 s) -----------
        bubble = make_bubble("show me my open opportunities", width=4.6)
        bubble.scale(0.9).move_to(UP * 3.38)
        cap = make_caption("Now change one word.")
        # Voice sync: "Now change one word" is heard 0.59-1.21 (word table
        # + 0.5 s mux delay). The 0.6 s fade starts half its run ahead at
        # 0.3, so the bubble PEAKS at 0.9, on "change one".
        self.play(FadeIn(bubble, shift=DOWN * 0.2), FadeIn(cap), run_time=0.6)
        self.wait(0.4)

        # ------------- beat 2: SMB lands, in red (1.8-3.7 s) --------------
        # The new text colours only the new word. Text drops spaces from its
        # submobjects: "showmemyopen" is 12 chars, so SMB sits at [12:15].
        bubble2 = make_bubble("show me my open SMB opportunities", width=4.9)
        bubble2.text[12:15].set_color(ALERT_RED)
        bubble2.scale(0.9).move_to(UP * 3.38)
        cap2 = make_caption("Show me my open SMB opportunities.")
        self.play(FadeOut(cap), run_time=0.2)
        # A sequential swap, not FadeTransform: transforming one bubble into
        # the other left the new text's word spacing mangled.
        # Voice sync: "Show me my open SMB opportunities" starts at 1.88
        # heard. The new bubble's 0.4 s fade runs 1.7-2.1, so it PEAKS at
        # 2.1, on "my open", with the red SMB fully legible before the word
        # "SMB" itself lands at 2.65.
        self.play(FadeOut(bubble), run_time=0.2)
        self.play(FadeIn(bubble2), FadeIn(cap2), run_time=0.4)
        cap = cap2

        # The frame dims around the question; only SMB stays loud.
        shade = Rectangle(width=8, height=10)
        shade.set_stroke(width=0).set_fill(BG, opacity=0.0)
        self.add(shade)
        self.add(bubble2, cap)  # keep the question and caption above the dim
        # Voice sync: the dim runs 2.1-2.6 and COMPLETES right as "SMB" is
        # heard at 2.65 - the word lands on an already-dimmed frame.
        self.play(shade.animate.set_fill(BG, opacity=0.65), run_time=0.5)

        # The hinge of the whole video is one word, so the word becomes an
        # event: a big copy jumps out of the bubble into the dimmed centre,
        # holds, and folds back in.
        big_smb = bubble2.text[12:15].copy()
        big_smb.set_z_index(3)
        self.add(big_smb)
        # Voice sync: the jump-out is the scene's dramatic beat and
        # deliberately runs PAST the voice (ends 4.17): it launches at 3.1,
        # right on "opportunities" (3.09 heard), and the box closes around
        # it at 4.0, so the boxed hold spans the voice ending.
        self.wait(0.5)
        self.play(big_smb.animate.scale(4.5).move_to(DOWN * 0.3),
                  run_time=0.6)
        box = SurroundingRectangle(big_smb, buff=0.22, corner_radius=0.12)
        box.set_stroke(ALERT_RED, 3).set_z_index(3)
        self.play(Create(box), run_time=0.3)
        self.wait(0.9)
        self.play(FadeOut(box),
                  big_smb.animate.scale(1 / 4.5)
                  .move_to(bubble2.text[12:15].get_center()),
                  run_time=0.5)
        self.remove(big_smb)

        # ------------------------------------------------- final hold ----
        self.wait(0.6)
