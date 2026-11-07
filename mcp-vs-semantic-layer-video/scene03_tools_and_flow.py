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
    BG, INK, MUTED, LIGHT_GREY, PURPLE, PURPLE_FILL, TEAL, GREY, SLATE,
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
        ghosts = VGroup()
        for ep, card in zip(apis.endpoints, cards):
            ghost = ep.copy().set_opacity(0.55)
            ghosts.add(ghost)
            self.add(ghost)
            # FadeTransform, not ReplacementTransform: a point-morph between
            # text and a card reads as scribble for over a second.
            lift_anims.append(FadeTransform(ep, card))
        self.play(LaggedStart(*lift_anims, lag_ratio=0.3), run_time=2.4)

        # -------------- beat 2: anatomy of one tool card (3-8 s) ----------
        dim = Rectangle(width=16, height=9)
        dim.set_stroke(width=0).set_fill(BG, opacity=0.65)
        big = make_big_tool_card(*TOOL_SPECS[0]).move_to(UP * 0.15)

        cap2 = make_caption("Each tool has a name, a description, and an input schema.")
        # Captions swap sequentially: cross-fading in place leaves two texts
        # stacked and unreadable for the whole play.
        self.play(FadeOut(cap), run_time=0.2)
        self.play(FadeIn(dim), FadeTransform(cards[0].copy(), big),
                  FadeIn(cap2), run_time=0.7)
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
        self.play(FadeOut(cap), run_time=0.25)
        self.play(
            LaggedStart(*[
                card.animate.scale(0.42).move_to(pos)
                for card, pos in zip(minis, targets)
            ], lag_ratio=0.2),
            FadeIn(cap2),
            run_time=1.35,
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
        self.play(FadeOut(cap), run_time=0.2)
        self.play(Indicate(client.llm, color=PURPLE, scale_factor=1.05),
                  FadeIn(cap2),
                  run_time=0.6)
        cap = cap2

        sweep = Rectangle(width=minis[0].width + 0.25, height=0.55)
        sweep.set_stroke(width=0).set_fill(PURPLE, 0.25)
        sweep.move_to(minis[0])
        self.play(FadeIn(sweep, run_time=0.15))
        self.play(sweep.animate.move_to(minis[2]), run_time=0.6)
        self.play(sweep.animate.move_to(minis[0]), run_time=0.4)

        # A scale pop, not an upward shift: shifting the top card up rams it
        # into the "LLM" label.
        self.play(FadeOut(sweep, run_time=0.2),
                  minis[0].animate.scale(1.08),
                  run_time=0.3)
        ring = SurroundingRectangle(minis[0], buff=0.05, corner_radius=0.06)
        ring.set_stroke(PURPLE_FILL, 2.5)
        self.play(Create(ring), run_time=0.3)

        # The filled input types below the LLM box, inside the client shell;
        # next to the card it would spill out over the wire.
        filled = Text("status = open", font=CODE_FONT, font_size=15,
                      color=INK)
        filled.next_to(client.llm, DOWN, buff=0.18)
        self.play(AddTextLetterByLetter(filled), run_time=1.0)

        # ------------- beat 5: the server runs it (14-17 s) ---------------
        # The call leaves the chosen card as a packet; the card stays put.
        pkt = make_packet().move_to(minis[0].get_right() + RIGHT * 0.18)
        cap2 = make_caption("and then the server runs it.")
        self.play(FadeOut(cap), run_time=0.15)
        self.play(FadeIn(pkt, scale=0.3), FadeOut(ring), FadeOut(filled),
                  minis[0].animate.scale(1 / 1.08),
                  FadeIn(cap2), run_time=0.3)
        cap = cap2

        # One continuous journey to the server, dropping onto the wire.
        p1 = VMobject().set_points_smoothly([
            pkt.get_center(),
            [client.shell.get_right()[0] + 0.15, wire_left.get_y(), 0],
            server.shell.get_center(),
        ])
        self.play(MoveAlongPath(pkt, p1), run_time=0.9)

        # The server visibly runs it: flash, spark, a small label.
        run_tag = Text("runs the call", font=UI_FONT, font_size=18, color=TEAL)
        run_tag.next_to(server.title, DOWN, buff=0.18)
        self.play(server.shell.animate.set_stroke(TEAL, 6),
                  FadeIn(run_tag, shift=DOWN * 0.1), run_time=0.25)
        self.play(server.shell.animate.set_stroke(TEAL, 2.5),
                  Flash(pkt, color=TEAL, line_length=0.18, num_lines=10),
                  run_time=0.35)

        # Onward to the exact endpoint it maps to, which lights up.
        p2 = VMobject().set_points_smoothly([
            pkt.get_center(),
            [apis.shell.get_left()[0] - 0.15, wire_right.get_y(), 0],
            ghosts[0].get_center(),
        ])
        self.play(MoveAlongPath(pkt, p2), run_time=0.7)
        self.play(FadeOut(pkt, scale=0.4),
                  ghosts[0].animate.set_opacity(1.0).set_color(TEAL),
                  run_time=0.3)
        self.play(ghosts[0].animate.set_opacity(0.55).set_color(SLATE),
                  FadeOut(run_tag), run_time=0.3)

        # Data rows travel back from that endpoint into the client.
        # DOWN * 2.1 keeps a clear gap under the "context window" label;
        # at 1.9 the top bar reads as an underline on it.
        rows = make_data_rows(3)
        rows.move_to(client.shell.get_center() + DOWN * 2.1)
        moving = rows.copy()
        for bar in moving:
            bar.move_to(ghosts[0].get_center()).scale(0.5)
        self.play(
            LaggedStart(*[
                m.animate.scale(2.0).move_to(b.get_center())
                for m, b in zip(moving, rows)
            ], lag_ratio=0.15),
            run_time=1.1,
        )

        # ------------------------------------------------- final hold ----
        self.wait(1.0)
