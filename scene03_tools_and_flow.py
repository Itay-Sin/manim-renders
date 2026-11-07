"""Scene 3: tools and the flow. ~14.6 s of motion plus a 0.9 s hold.

Vertical 4:5 master (1080x1350) for the LinkedIn/Facebook feed: the flow runs
top to bottom — AI client, MCP server, your APIs — and back up. Frame coords:
x in [-3.2, 3.2], y in [-4, 4]. A title strip and dot grid fill the frame.

Narration beats:
  0-3    "The server exposes your APIs as tools."
  3-8    "Each tool has a name, a description, and a schema for its inputs."
  8-11   "The client hands those to the LLM,"
  11-14  "which picks the tool that fits and fills in the inputs,"
  14-17  "and then the server runs it."
"""

from manim import *
from common import (
    make_ai_client, make_mcp_server, make_api_box, make_background,
    make_tool_card, make_big_tool_card, make_packet, make_data_rows,
    make_caption, make_title_strip, make_dot_grid, ctx_fill_target,
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
        bg = make_background()
        grid = make_dot_grid()
        strip = make_title_strip("MCP", "Tools and the flow")
        client = make_ai_client().move_to(UP * 1.78)
        server = make_mcp_server().move_to(DOWN * 0.92)
        apis = make_api_box().move_to(DOWN * 2.52)

        wire_top = Line(client.shell.get_bottom(), server.shell.get_top())
        wire_bot = Line(server.shell.get_bottom(), apis.shell.get_top())
        for w in (wire_top, wire_bot):
            w.set_stroke(GREY, 2.2, opacity=0.75)

        cap = make_caption("The server exposes your APIs as tools.")
        self.add(bg, grid)
        self.wait(0.3)  # house style: breath before the first play
        self.play(FadeIn(strip), FadeIn(client), FadeIn(server), FadeIn(apis),
                  FadeIn(wire_top), FadeIn(wire_bot), FadeIn(cap),
                  run_time=0.6)

        # ----------------------- beat 1: APIs become tools (0-3 s) --------
        # Endpoints lift UP from the API card into the server as a card row.
        cards = VGroup(*[make_tool_card(*s) for s in TOOL_SPECS])
        cards.arrange(RIGHT, buff=0.18)
        cards.scale_to_fit_width(5.1)
        cards.move_to(server.shell.get_center() + DOWN * 0.18)

        lift_anims = []
        ghosts = VGroup()
        for ep, card in zip(apis.endpoints, cards):
            ghost = ep.copy().set_opacity(0.55)
            ghosts.add(ghost)
            self.add(ghost)
            # FadeTransform, not ReplacementTransform: a point-morph between
            # text and a card reads as scribble for over a second.
            lift_anims.append(FadeTransform(ep, card))
        self.play(LaggedStart(*lift_anims, lag_ratio=0.3), run_time=2.0)

        # -------------- beat 2: anatomy of one tool card (3-8 s) ----------
        dim = Rectangle(width=8, height=10)
        dim.set_stroke(width=0).set_fill(BG, opacity=0.65)
        big = make_big_tool_card(*TOOL_SPECS[0]).move_to(UP * 0.35)

        cap2 = make_caption("Each tool has a name, a description, and an input schema.")
        # Captions swap sequentially: cross-fading in place leaves two texts
        # stacked and unreadable for the whole play.
        # Voice sync: "Each tool has..." is heard at ~3.4 s (word table +
        # 0.5 s mux delay). The beat PEAKS on the phrase rather than starting
        # on it: the 0.6 s zoom starts at ~3.1 (half its run_time early) so
        # the big card is fully on by ~3.7, during "has a name" — no wait
        # after the lift.
        self.play(FadeOut(cap), run_time=0.2)
        self.play(FadeIn(dim), FadeTransform(cards[0].copy(), big),
                  FadeIn(cap2), run_time=0.6)
        cap = cap2

        # Voice sync: name / description / schema are heard at ~4.1 / 4.9 /
        # 5.9 s. Each highlight finishes DRAWING on its word (Create ends at
        # the word time); the per-row pre-waits space the three 0.8 s cycles
        # to the narration's uneven gaps.
        for pre, row in zip((0.23, 0.0, 0.14), big.rows):
            if pre:
                self.wait(pre)
            hl = SurroundingRectangle(row, buff=0.1, corner_radius=0.08)
            hl.set_stroke(TEAL, 2)
            self.play(Create(hl), run_time=0.2)
            self.wait(0.4)
            self.play(FadeOut(hl), run_time=0.2)

        self.play(
            big.animate.scale_to_fit_width(cards[0].width)
               .move_to(cards[0]).set_opacity(0),
            FadeOut(dim),
            # 0.5, not 0.6: buys the hand-to-LLM move an earlier start so it
            # peaks on "hands those to the LLM" (heard ~7.9-8.7).
            run_time=0.5,
        )
        self.remove(big)

        # ----------- beat 3: cards go UP to the LLM (8-11 s) --------------
        minis = cards  # same objects, shrunk into a row inside the LLM box
        anchor = client.llm.get_center() + DOWN * 0.1
        targets = [anchor + RIGHT * dx for dx in (-1.0, 0.0, 1.0)]
        cap2 = make_caption("The client hands those to the LLM...")
        self.play(FadeOut(cap), run_time=0.2)
        self.play(
            LaggedStart(*[
                card.animate.scale(0.56).move_to(pos)
                for card, pos in zip(minis, targets)
            ], lag_ratio=0.2),
            FadeIn(cap2),
            run_time=1.0,
        )
        cap = cap2

        chunk = Square(0.26).set_stroke(width=0).set_fill(PURPLE_FILL, 0.9)
        chunk.move_to(client.llm.get_bottom())
        new_fill = ctx_fill_target(client, 0.33)
        self.add(chunk)
        self.play(chunk.animate.scale(0.6).move_to(new_fill.get_center()),
                  run_time=0.4)
        self.play(Transform(client.ctx_fill, new_fill), FadeOut(chunk),
                  run_time=0.4)

        # ------- beat 4: pick the tool, fill the input (11-14 s) ----------
        cap2 = make_caption("...which picks the tool that fits and fills in the inputs,")
        # Voice sync: the Indicate's visible peak (its midpoint) lands on
        # "picks" (heard ~9.85); the 0.3 wait places the play at 9.5-10.1.
        self.wait(0.3)
        self.play(FadeOut(cap), run_time=0.2)
        self.play(Indicate(client.llm, color=PURPLE, scale_factor=1.05),
                  FadeIn(cap2),
                  run_time=0.6)
        cap = cap2

        # The highlight sweeps ACROSS the row of minis.
        sweep = Rectangle(width=minis[0].width + 0.2,
                          height=minis[0].height + 0.25)
        sweep.set_stroke(width=0).set_fill(PURPLE, 0.25)
        sweep.move_to(minis[0])
        # Tightened sweep (0.15/0.4/0.25) so it lands back on the chosen card
        # right at "fits" (heard ~10.7) and the typing can start on "fills".
        self.play(FadeIn(sweep, run_time=0.15))
        self.play(sweep.animate.move_to(minis[2]), run_time=0.4)
        self.play(sweep.animate.move_to(minis[0]), run_time=0.25)

        # A scale pop, not a shift: shifting would ram neighbours or labels.
        self.play(FadeOut(sweep, run_time=0.15),
                  minis[0].animate.scale(1.08),
                  run_time=0.15)
        ring = SurroundingRectangle(minis[0], buff=0.05, corner_radius=0.06)
        ring.set_stroke(PURPLE_FILL, 2.5)
        self.play(Create(ring), run_time=0.15)

        # The filled input types below the LLM box, inside the client shell,
        # in the gap above the context-window bar.
        # Voice sync: the letter-by-letter fill runs ~11.2-12.0, starting ON
        # "fills" (heard ~11.2) and completing on "the inputs" (~11.7).
        filled = Text("status = open", font=CODE_FONT, font_size=15,
                      color=INK)
        filled.next_to(client.llm, DOWN, buff=0.1)
        self.play(AddTextLetterByLetter(filled), run_time=0.8)

        # ------------- beat 5: the server runs it (14-17 s) ---------------
        # The call leaves the chosen card as a packet; the card stays put.
        pkt = make_packet().move_to(minis[0].get_bottom() + DOWN * 0.12)
        cap2 = make_caption("and then the server runs it.")
        self.play(FadeOut(cap), run_time=0.2)
        self.play(FadeIn(pkt, scale=0.3), FadeOut(ring), FadeOut(filled),
                  minis[0].animate.scale(1 / 1.08),
                  FadeIn(cap2), run_time=0.2)
        cap = cap2

        # One continuous journey DOWN to the server, dropping onto the wire.
        # Voice sync: 0.6 s ride starting ~12.4 so the packet ARRIVES at the
        # server at ~13.0, on "the server runs it" (heard ~12.9-13.4).
        p1 = VMobject().set_points_smoothly([
            pkt.get_center(),
            [wire_top.get_x(), client.shell.get_bottom()[1] - 0.08, 0],
            server.shell.get_center() + UP * 0.1,
        ])
        self.play(MoveAlongPath(pkt, p1), run_time=0.6)

        # The server visibly runs it: flash, spark, a small label.
        # The Flash peaks at ~13.3, on "runs it".
        run_tag = Text("runs the call", font=UI_FONT, font_size=18, color=TEAL)
        run_tag.next_to(server.title, RIGHT, buff=0.3)
        self.play(server.shell.animate.set_stroke(TEAL, 6),
                  FadeIn(run_tag, shift=DOWN * 0.1), run_time=0.15)
        self.play(server.shell.animate.set_stroke(TEAL, 2.5),
                  Flash(pkt, color=TEAL, line_length=0.18, num_lines=10),
                  run_time=0.3)

        # Onward DOWN to the exact endpoint it maps to, which lights up.
        # Compressed (0.6 -> 0.4) and OVERLAPPED into the last phrase: the
        # endpoint lights up at ~13.9, right as the voice ends.
        p2 = VMobject().set_points_smoothly([
            pkt.get_center(),
            [wire_bot.get_x(), apis.shell.get_top()[1] + 0.08, 0],
            ghosts[0].get_center(),
        ])
        self.play(MoveAlongPath(pkt, p2), run_time=0.4)
        self.play(FadeOut(pkt, scale=0.4),
                  ghosts[0].animate.set_opacity(1.0).set_color(TEAL),
                  run_time=0.1)

        # Data rows travel back UP from that endpoint and are absorbed by the
        # context window: tool results consume context (sets up scene 5).
        # Rule-2 tail: the voice ends ~13.9, so the endpoint revert, the data
        # rows' return and their absorption are ONE ~0.5 s settle (0.33 +
        # 0.13, frame-exact at 15 fps), not the former 2.2 s silent journey.
        moving = make_data_rows(3)
        for bar in moving:
            bar.move_to(ghosts[0].get_center()).scale(0.5)
        fill2 = ctx_fill_target(client, 0.45)
        # Two plain plays, not a Succession: a FadeOut nested inside a
        # Succession never got cleaned up and left a stray data row in the
        # end state scene 4 opens on (frame-checked 2026-11-07).
        self.play(
            ghosts[0].animate.set_opacity(0.55).set_color(SLATE),
            FadeOut(run_tag),
            LaggedStart(*[
                m.animate.move_to(client.ctx_outline.get_center())
                for m in moving
            ], lag_ratio=0.18),
            run_time=0.33,
        )
        self.play(FadeOut(moving), Transform(client.ctx_fill, fill2),
                  run_time=0.13)

        # ------------------------------------------------- final hold ----
        # Audio (13.44 s mp3 + 0.5 s mux delay) ends ~13.9 s; the packet
        # reaches the endpoint inside the last phrase, the 0.6 s settle ends
        # ~14.6, and the scene holds static for 0.9 s.
        self.wait(0.9)
