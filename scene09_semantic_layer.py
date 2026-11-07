"""Scene 9: the semantic layer. ~12 s of motion plus a 1 s hold.

The red fades, the actors make room, and an amber zone slides in between the
MCP server and your APIs: the semantic model, pure knowledge. Ends on the
reflowed layout scene 10 opens on.

Narration (srt + 0.5 s):
  0.55   "That gap is what a semantic layer fills."
  3.02   "At its heart is a semantic model: files that describe your data
          in business terms."
  7.83   "The objects, how they relate, and what your words mean."
  11.15  "Pure knowledge."
"""

from manim import *
from common import (
    make_ai_client, make_mcp_server, make_api_box, make_background,
    make_tool_card, make_caption, make_dot_grid, make_bubble,
    make_sem_zone, make_sem_stack, make_object_card, ctx_fill_target,
    make_shadow,
    BG, INK, MUTED, PURPLE, TEAL, GREY, SLATE, ALERT_RED, AMBER,
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


class Scene09SemanticLayer(Scene):
    def construct(self):
        # ------------- base layout, dimmed, as scene 8 left it ------------
        bg = make_background()
        grid = make_dot_grid()
        client = make_ai_client().move_to(UP * 1.78)
        server = make_mcp_server().move_to(DOWN * 0.75)
        apis = make_api_box().move_to(DOWN * 2.4)
        cards = VGroup(*[make_tool_card(*s) for s in TOOL_SPECS])
        cards.arrange(RIGHT, buff=0.18)
        cards.scale_to_fit_width(5.1)
        for card, dx in zip(cards, (-1.08, 0.0, 1.08)):
            card.scale(0.6).move_to(
                client.llm.get_center() + DOWN * 0.1 + RIGHT * dx)
        apis.endpoints.set_opacity(0.55)
        client.ctx_fill.become(ctx_fill_target(client, 0.92))
        wire_top = Line(client.shell.get_bottom(), server.shell.get_top())
        wire_bot = Line(server.shell.get_bottom(), apis.shell.get_top())
        for w in (wire_top, wire_bot):
            w.set_stroke(GREY, 2.2, opacity=0.75)
        shade = Rectangle(width=8, height=10)
        shade.set_stroke(width=0).set_fill(BG, opacity=0.65)
        bubble = make_bubble("show me my open SMB opportunities", width=4.9)
        bubble.text[12:15].set_color(ALERT_RED)
        bubble.scale(0.9).move_to(UP * 3.38)
        self.add(bg, grid, wire_top, wire_bot, client, server, apis,
                 cards, shade, bubble)
        self.wait(0.3)

        # ------ beat 1: the gap gets filled (0.5-3 s) ---------------------
        cap = make_caption("That gap is what a semantic layer fills.")
        self.play(FadeOut(shade), FadeOut(bubble), FadeIn(cap), run_time=0.6)

        # The actors make room: everything compacts, and the context window
        # resets for the fresh approach.
        cg = VGroup(client, cards)
        self.play(
            cg.animate.scale(0.62).move_to(UP * 2.25),
            server.animate.scale(0.65).move_to(UP * 0.6),
            apis.animate.scale(0.7).move_to(DOWN * 2.82),
            FadeOut(wire_top), FadeOut(wire_bot),
            run_time=0.9,
        )
        self.play(Transform(client.ctx_fill, ctx_fill_target(client, 0.08)),
                  run_time=0.3)

        zone = make_sem_zone().move_to(DOWN * 1.2)
        w1 = Line(client.shell.get_bottom(), server.shell.get_top())
        w2 = Line(server.shell.get_bottom(), zone.shell.get_top())
        w3 = Line(zone.shell.get_bottom(), apis.shell.get_top())
        for w in (w1, w2, w3):
            w.set_stroke(GREY, 2.2, opacity=0.75)
        self.play(FadeIn(zone, shift=LEFT * 0.6),
                  FadeIn(w1), FadeIn(w2), FadeIn(w3), run_time=0.8)

        # ------ beat 2: the semantic model builds up (3-7.8 s) ------------
        cap2 = make_caption("At its heart: a semantic model, in business terms.")
        self.play(FadeOut(cap), run_time=0.2)
        self.play(FadeIn(cap2), run_time=0.3)
        cap = cap2

        stack = make_sem_stack(4)
        stack.move_to(zone.shell.get_center() + LEFT * 1.7 + DOWN * 0.08)
        # Word-level sync: hold until "a semantic model" (heard 3.9 s) before
        # the stack builds.
        self.wait(0.4)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.12, scale=0.8)
                          for c in stack.cards], lag_ratio=0.25),
            run_time=1.4,
        )
        self.play(FadeIn(stack.label), run_time=0.3)
        self.wait(2.2)

        # ------ beat 3: objects, relations, words (7.8-11.1 s) ------------
        cap2 = make_caption("The objects, how they relate, your words.")
        self.play(FadeOut(cap), run_time=0.2)
        cap = cap2

        opp = make_object_card("Opportunity", ["status"], width=1.6).scale(0.8)
        acc = make_object_card("Account", ["segment"], width=1.6).scale(0.8)
        opp.move_to(zone.shell.get_center() + RIGHT * 0.55 + UP * 0.08)
        acc.move_to(zone.shell.get_center() + RIGHT * 2.05 + UP * 0.08)
        rel = Line(opp.card.get_right(), acc.card.get_left())
        rel.set_stroke(AMBER, 2.5)
        self.play(FadeIn(opp), FadeIn(acc), FadeIn(cap2), run_time=0.6)
        # Word-level sync: the relation line draws on "how they relate"
        # (heard 9.0 s), not right after the cards.
        self.wait(0.5)
        self.play(Create(rel), run_time=0.4)

        tag_open = Text("“open”", font=UI_FONT, font_size=12,
                        color=AMBER)
        tag_smb = Text("“SMB”", font=UI_FONT, font_size=12,
                       color=AMBER)
        tag_open.next_to(opp, DOWN, buff=0.1)
        tag_smb.next_to(acc, DOWN, buff=0.1)
        # Word-level sync: the word tags land on "and what your words mean"
        # (heard 10.0 s).
        self.wait(0.6)
        self.play(FadeIn(tag_open, shift=UP * 0.08),
                  FadeIn(tag_smb, shift=UP * 0.08), run_time=0.5)
        self.wait(0.6)

        # ------ beat 4: pure knowledge (11.2 s) ---------------------------
        cap2 = make_caption("Pure knowledge.")
        self.play(FadeOut(cap), run_time=0.2)
        self.play(FadeIn(cap2),
                  zone.shell.animate.set_stroke(AMBER, 4),
                  run_time=0.5)
        self.play(zone.shell.animate.set_stroke(AMBER, 2.5), run_time=0.4)

        # ------------------------------------------------- final hold ----
        self.wait(1.5)
