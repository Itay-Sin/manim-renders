"""Scene 3: tools and the flow. ~17 s of motion plus a 1 s hold.

Narration beats:
  0-3    "The server exposes your APIs as tools."
  3-8    "Each tool has a name, a description, and a schema for its inputs."
  8-11   "The client hands those to the LLM,"
  11-14  "which picks the tool that fits and fills in the inputs,"
  14-17  "and then the server runs it."
"""

from manim import *
from common import (
    make_ai_client, make_mcp_server, make_api_box,
    make_tool_card, make_big_tool_card, make_packet, make_data_rows,
    make_caption, ctx_fill_target,
    BG, INK, MUTED, LIGHT_GREY, PURPLE, PURPLE_FILL, TEAL, GREY, CODE_FONT,
)

TOOL_SPECS = [
    ("fetch_opportunities", "Returns opportunities, filtered by status",
     "status: open | closed"),
    ("fetch_accounts", "Returns accounts and their fields",
     "account_id: text"),
    ("update_deal", "Updates fields on one deal",
     "deal_id, fields"),
]


class Scene03ToolsAndFlow(Scene):
    def construct(self):
        # ------------------------------------------------- base layout ----
        client = make_ai_client().move_to(LEFT * 4.35)
        server = make_mcp_server().move_to(RIGHT * 0.55)
        apis = make_api_box().move_to(RIGHT * 5.0)

        wire_left = Line(client.shell.get_right(), server.shell.get_left())
        wire_right = Line(server.shell.get_right(), apis.shell.get_left())
        for w in (wire_left, wire_right):
            w.set_stroke(GREY, 2.2, opacity=0.75)

        cap = make_caption("The server exposes your APIs as tools.")
        self.play(FadeIn(client), FadeIn(server), FadeIn(apis),
                  FadeIn(wire_left), FadeIn(wire_right), FadeIn(cap),
                  run_time=0.6)

        # ----------------------- beat 1: APIs become tools (0-3 s) --------
        cards = VGroup(*[make_tool_card(*s) for s in TOOL_SPECS])
        cards.arrange(DOWN, buff=0.2)
        cards.move_to(server.shell.get_center() + DOWN * 0.3)

        lift_anims = []
        for ep, card in zip(apis.endpoints, cards):
            ghost = ep.copy().set_opacity(0.55)
            self.add(ghost)
            lift_anims.append(ReplacementTransform(ep, card, path_arc=0.5))
        self.play(LaggedStart(*lift_anims, lag_ratio=0.3), run_time=2.4)

        # -------------- beat 2: anatomy of one tool card (3-8 s) ----------
        dim = Rectangle(width=16, height=9)
        dim.set_stroke(width=0).set_fill(BG, opacity=0.65)
        big = make_big_tool_card(*TOOL_SPECS[0]).move_to(UP * 0.15)

        cap2 = make_caption("Each tool has a name, a description, and an input schema.")
        self.play(FadeIn(dim), TransformFromCopy(cards[0], big),
                  FadeOut(cap), FadeIn(cap2), run_time=0.9)
        cap = cap2

        for row in big.rows:
            hl = SurroundingRectangle(row, buff=0.1, corner_radius=0.08)
            hl.set_stroke(TEAL, 2)
            self.play(Create(hl), run_time=0.3)
            self.wait(0.55)
            self.play(FadeOut(hl), run_time=0.25)

        self.play(
            big.animate.scale_to_fit_width(cards[0].width)
               .move_to(cards[0]).set_opacity(0),
            FadeOut(dim),
            run_time=0.6,
        )
        self.remove(big)

        # ----------- beat 3: cards go to the LLM (8-11 s) -----------------
        minis = cards  # same objects, scaled down into the LLM box
        targets = []
        anchor = client.llm.get_center() + DOWN * 0.25
        for i in range(3):
            targets.append(anchor + UP * (0.55 - 0.55 * i))
        cap2 = make_caption("The client hands those to the LLM...")
        self.play(
            LaggedStart(*[
                card.animate.scale(0.42).move_to(pos)
                for card, pos in zip(minis, targets)
            ], lag_ratio=0.2),
            FadeOut(cap), FadeIn(cap2),
            run_time=1.6,
        )
        cap = cap2

        chunk = Square(0.26).set_stroke(width=0).set_fill(PURPLE_FILL, 0.9)
        chunk.move_to(client.llm.get_bottom())
        new_fill = ctx_fill_target(client, 0.33)
        self.add(chunk)
        self.play(chunk.animate.scale(0.6).move_to(new_fill.get_center()),
                  run_time=0.6)
        self.play(Transform(client.ctx_fill, new_fill), FadeOut(chunk),
                  run_time=0.35)

        # ------- beat 4: pick the tool, fill the input (11-14 s) ----------
        cap2 = make_caption("...which picks the tool that fits and fills in the inputs,")
        self.play(Indicate(client.llm, color=PURPLE, scale_factor=1.05),
                  FadeOut(cap), FadeIn(cap2),
                  run_time=0.8)
        cap = cap2

        sweep = Rectangle(width=minis[0].width + 0.25, height=0.55)
        sweep.set_stroke(width=0).set_fill(PURPLE, 0.25)
        sweep.move_to(minis[0])
        self.play(FadeIn(sweep, run_time=0.15))
        self.play(sweep.animate.move_to(minis[2]), run_time=0.6)
        self.play(sweep.animate.move_to(minis[0]), run_time=0.4)

        ring = SurroundingRectangle(minis[0], buff=0.05, corner_radius=0.06)
        ring.set_stroke(PURPLE_FILL, 2.5)
        self.play(FadeOut(sweep, run_time=0.2),
                  minis[0].animate.shift(UP * 0.1),
                  run_time=0.3)
        ring.move_to(minis[0].get_center() + UP * 0.1)
        self.play(Create(ring), run_time=0.3)

        filled = Text("status = open", font=CODE_FONT, font_size=15,
                      color=INK)
        filled.next_to(minis[0], RIGHT, buff=0.18)
        self.play(AddTextLetterByLetter(filled), run_time=1.0)

        # ------------- beat 5: the server runs it (14-17 s) ---------------
        pkt = make_packet().move_to(minis[0].get_center())
        cap2 = make_caption("and then the server runs it.")
        self.play(ReplacementTransform(VGroup(minis[0], filled), pkt),
                  FadeOut(ring), FadeOut(cap), FadeIn(cap2),
                  run_time=0.5)
        cap = cap2

        self.play(pkt.animate.move_to(
            [pkt.get_x(), wire_left.get_y(), 0]), run_time=0.25)
        self.play(pkt.animate.move_to(server.shell.get_center()),
                  run_time=0.6)
        self.play(server.shell.animate.set_stroke(TEAL, 5), run_time=0.15)
        self.play(server.shell.animate.set_stroke(TEAL, 2.5), run_time=0.2)
        self.play(pkt.animate.move_to(apis.shell.get_center()), run_time=0.5)
        self.play(FadeOut(pkt), run_time=0.2)

        rows = make_data_rows(3)
        rows.move_to(client.shell.get_center() + DOWN * 2.0)
        self.play(
            LaggedStart(*[
                bar.animate.move_to(pos)
                for bar, pos in zip(
                    rows.copy().move_to(apis.shell.get_center()),
                    [b.get_center() for b in rows],
                )
            ], lag_ratio=0.2),
            run_time=1.0,
        )

        # ------------------------------------------------- final hold ----
        self.wait(1.0)
