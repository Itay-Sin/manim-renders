"""Scene 5: where the knowledge comes from. ~15 s of motion plus a 1 s hold.

The server never reasons; the LLM only knows what the descriptions say, and
those sit in the context window. Five servers cost ~55,000 tokens before any
work. Ends with the token meter parked inside the client.

Narration (srt + 0.5 s):
  0.55   "The server never reasons."
  2.11   "Everything the LLM knows comes from those descriptions, and they
          all sit in its context window."
  7.72   "That costs tokens."
  9.08   "In one Anthropic example, five servers used about fifty five
          thousand tokens on definitions alone."
"""

from manim import *
from common import (
    make_ai_client, make_mcp_server, make_api_box, make_background,
    make_tool_card, make_caption, make_title_strip, make_dot_grid,
    ctx_fill_target,
    BG, INK, MUTED, PURPLE, PURPLE_FILL, TEAL, GREY, SLATE,
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


class Scene05Knowledge(Scene):
    def construct(self):
        # --------------------- base layout, as scene 4 left it ------------
        bg = make_background()
        grid = make_dot_grid()
        strip = make_title_strip("MCP", "Where the knowledge comes from")
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
        client.ctx_fill.become(ctx_fill_target(client, 0.55))

        wire_top = Line(client.shell.get_bottom(), server.shell.get_top())
        wire_bot = Line(server.shell.get_bottom(), apis.shell.get_top())
        for w in (wire_top, wire_bot):
            w.set_stroke(GREY, 2.2, opacity=0.75)

        # The extra-server ghosts use negative z_index; push the page layers
        # further back so the ghosts still render above them.
        bg.set_z_index(-20)
        grid.set_z_index(-19)
        # The definition shower crosses the client card's lower edge; keep the
        # "context window" label above the travelling squares.
        client.ctx_label.set_z_index(2)
        self.add(bg, grid, wire_top, wire_bot, client, server, apis, cards)
        self.wait(0.3)

        # ------------- beat 1: the server never reasons (0.5-2 s) ---------
        cap = make_caption("The server never reasons.")
        self.play(FadeIn(strip), FadeIn(cap), run_time=0.6)

        run_tag = Text("just runs the call", font=UI_FONT, font_size=16,
                       color=TEAL)
        # Under the title, centred: at the title's right the tag ran past
        # the server card's edge (operator note 2026-11-07).
        run_tag.next_to(server.title, DOWN, buff=0.18)
        self.play(FadeIn(run_tag, shift=LEFT * 0.1),
                  Indicate(client.llm, color=PURPLE, scale_factor=1.05),
                  run_time=0.8)
        self.wait(0.1)

        # ----- beat 2: the descriptions live in the context (2.1-7.7) -----
        cap2 = make_caption("Everything the LLM knows sits in its context window.")
        self.play(FadeOut(cap), run_time=0.2)
        self.play(FadeIn(cap2), run_time=0.3)
        cap = cap2

        # Each tool card pulses, then sends a small chunk into the bar.
        chunks = VGroup(*[
            Square(0.2).set_stroke(width=0).set_fill(PURPLE_FILL, 0.9)
            .move_to(c.get_center()) for c in cards
        ])
        fill_a = ctx_fill_target(client, 0.62)
        # Word-level sync: the fly belongs to "comes from those descriptions"
        # ("comes" heard at 3.78). Peak-on-phrase: the 1.15 s fly starts at
        # ~3.47 (about half early) so it COMPLETES at ~4.7, on
        # "descriptions" (heard 4.45), not a second after it.
        self.wait(0.8)
        # Fade the chunks in before they fly, so they don't pop in one frame.
        self.play(FadeIn(chunks, lag_ratio=0.15, scale=0.6), run_time=0.25)
        self.play(
            LaggedStart(*[
                chunk.animate.scale(0.5).move_to(fill_a.get_right())
                for chunk in chunks
            ], lag_ratio=0.25),
            run_time=1.15,
        )
        # The merge into the bar is "sit in its context window" ("sit" heard
        # at 5.85); the 0.4 s merge runs ~5.67-6.07, peaking right on it.
        self.wait(1.0)
        self.play(FadeOut(chunks), Transform(client.ctx_fill, fill_a),
                  run_time=0.4)
        self.wait(1.33)

        # --------------------- beat 3: that costs tokens (7.7-9) ----------
        cap2 = make_caption("That costs tokens.")
        self.play(FadeOut(cap), run_time=0.2)
        # The meter lives INSIDE the client card: the client pays the bill.
        # Text, not Integer: DecimalNumber renders through LaTeX, which this
        # machine does not have.
        meter_val = ValueTracker(0)
        meter_unit = Text("tokens", font=UI_FONT, font_size=12, color=MUTED)
        meter_unit.next_to(client.title, RIGHT, buff=1.35,
                           aligned_edge=DOWN)
        # Pin the unit's right edge inside the shell: positioned off the
        # title alone, "tokens" (and the tag below it) ran past the card's
        # right edge (operator note 2026-11-07).
        meter_unit.shift(LEFT * (meter_unit.get_right()[0]
                                 - client.shell.get_right()[0] + 0.3))
        meter_num = always_redraw(
            lambda: Text(f"{int(meter_val.get_value()):,}", font=UI_FONT,
                         font_size=18, color=INK)
            .next_to(meter_unit, LEFT, buff=0.1, aligned_edge=DOWN))
        self.play(FadeIn(cap2), FadeIn(meter_unit, shift=DOWN * 0.1),
                  run_time=0.5)
        self.add(meter_num)
        cap = cap2
        # The meter play above runs ~7.6-8.13, peaking on "costs tokens"
        # (heard 7.95-8.8). Beat 4's ghost servers belong to "five servers"
        # (heard 10.72), not to the preamble "In one Anthropic example":
        # the 1.0 s stack starts ~10.2 (half early) and completes at ~11.2,
        # on "servers".
        self.wait(1.87)

        # ------ beat 4: five servers, 55k tokens (9.1-14.5) ---------------
        cap2 = make_caption("Five servers: ~55,000 tokens before any work.")
        self.play(FadeOut(cap), run_time=0.2)

        # Four more servers stack up behind the first, slightly offset.
        extras = VGroup()
        for i in range(1, 5):
            ghost = server.shell.copy()
            ghost.set_fill("#FFFFFF", opacity=1.0).set_stroke(TEAL, 1.6,
                                                              opacity=0.7)
            ghost.shift(UP * 0.1 * i + LEFT * 0.1 * i)
            ghost.set_z_index(-i)
            extras.add(ghost)
        # A x5 chip on the title row says "five servers" even with the sound
        # off; the ghost shells alone are too subtle.
        x5_text = Text("×5", font=UI_FONT, font_size=16, color="#FFFFFF",
                       weight=BOLD)
        x5_pill = RoundedRectangle(corner_radius=0.12,
                                   width=x5_text.width + 0.26, height=0.34)
        x5_pill.set_stroke(width=0).set_fill(TEAL, 1.0)
        x5_text.move_to(x5_pill.get_center())
        x5 = VGroup(x5_pill, x5_text)
        x5.next_to(server.title, LEFT, buff=0.25)
        self.play(
            LaggedStart(*[FadeIn(g, shift=LEFT * 0.2) for g in extras],
                        lag_ratio=0.2),
            FadeIn(x5, scale=0.6),
            FadeIn(cap2),
            run_time=1.0,
        )
        cap = cap2

        # A shower of definition chunks pours into the bar while the meter
        # counts up to ~55,000.
        fill_b = ctx_fill_target(client, 0.92)
        shower = VGroup()
        for i in range(10):
            sq = Square(0.14).set_stroke(width=0).set_fill(PURPLE_FILL, 0.9)
            sq.move_to(server.shell.get_top()
                       + LEFT * (1.6 - 0.35 * (i % 5)) + UP * 0.05)
            shower.add(sq)
        # Fade the shower in before it flies, so it doesn't pop in one frame.
        self.play(FadeIn(shower, lag_ratio=0.06, scale=0.6), run_time=0.2)
        self.play(
            LaggedStart(*[
                sq.animate.move_to(client.ctx_outline.get_center()
                                   + RIGHT * 0.8)
                for sq in shower
            ], lag_ratio=0.12),
            meter_val.animate.set_value(55000),
            run_time=2.0,
        )
        self.play(FadeOut(shower), Transform(client.ctx_fill, fill_b),
                  run_time=0.4)
        before_tag = Text("before any work", font=UI_FONT, font_size=11,
                          color=MUTED)
        before_tag.next_to(meter_unit, DOWN, buff=0.12, aligned_edge=RIGHT)
        self.play(FadeIn(before_tag), run_time=0.3)
        # Rule-2 tail: the voice ends ~15.0 ("alone" heard 14.3). The ghost
        # servers' exit is the one short settle, starting at voice end.
        self.wait(0.87)

        # The extra servers leave; the cost stays.
        self.play(FadeOut(extras), FadeOut(x5), run_time=0.6)

        # ------------------------------------------------- final hold ----
        # Settle ends ~15.6; static hold 0.9 s.
        self.wait(0.9)
