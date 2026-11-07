"""Scene 4: an easy question. ~12 s of motion plus a 1 s hold.

The question "show me my open opportunities" resolves cleanly because "open"
is a value the tool declares. Ends on the point: the LLM can only ask for
what the tool spells out.

Narration:
  0-4    "Here's an easy question: show me my open opportunities."
  4-8    "The tool lists open as a status value, so the LLM just asks for it."
  8-12   "It can only ask for what the tool spells out."
"""

from manim import *
from common import (
    make_ai_client, make_mcp_server, make_api_box, make_background,
    make_tool_card, make_packet, make_data_rows, make_shadow,
    make_caption, make_title_strip, make_dot_grid, make_bubble,
    ctx_fill_target,
    BG, INK, MUTED, PURPLE, PURPLE_FILL, TEAL, GREY, SLATE, OK_GREEN,
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


class Scene04EasyQuestion(Scene):
    def construct(self):
        # --------------------- base layout, as scene 3 left it ------------
        bg = make_background()
        grid = make_dot_grid()
        client = make_ai_client().move_to(UP * 1.78)
        server = make_mcp_server().move_to(DOWN * 0.75)
        apis = make_api_box().move_to(DOWN * 2.4)

        cards = VGroup(*[make_tool_card(*s) for s in TOOL_SPECS])
        cards.arrange(RIGHT, buff=0.18)
        cards.scale_to_fit_width(5.1)
        cards.move_to(server.shell.get_center() + DOWN * 0.18)

        wire_top = Line(client.shell.get_bottom(), server.shell.get_top())
        wire_bot = Line(server.shell.get_bottom(), apis.shell.get_top())
        for w in (wire_top, wire_bot):
            w.set_stroke(GREY, 2.2, opacity=0.75)

        self.add(bg, grid, wire_top, wire_bot,
                 client, server, apis, cards)

        # ------------- beat 1: the question arrives (0-4 s) ---------------
        # The bubble IS this scene's header: it owns the top zone where other
        # scenes put the title strip (continuity with scene 1 parking it there).
        # Scaled slightly and raised so the bubble body clears the client
        # card's top edge; only the tail tip touches it, pointing at the
        # client the question is being asked of.
        bubble = make_bubble("show me my open opportunities", width=4.6)
        bubble.scale(0.9).move_to(UP * 3.62)
        cap = make_caption("An easy question: show me my open opportunities.")
        self.play(FadeIn(bubble, shift=DOWN * 0.2), FadeIn(cap), run_time=0.8)
        self.wait(0.6)

        # ----- beat 2: "open" is a declared value of the tool (4-8 s) -----
        dim = Rectangle(width=8, height=10)
        dim.set_stroke(width=0).set_fill(BG, opacity=0.65)

        # An enlarged schema view: the status field with its two values.
        panel = RoundedRectangle(corner_radius=0.14, width=5.0, height=2.3)
        panel.set_stroke(TEAL, 2.5).set_fill("#FFFFFF", opacity=1.0)
        panel_shadow = make_shadow(panel)
        p_name = Text("fetch_opportunities", font=CODE_FONT, font_size=22,
                      color=INK)
        p_field = Text("status:", font=CODE_FONT, font_size=20, color=MUTED)
        v_open = Text("open", font=CODE_FONT, font_size=20, color=TEAL)
        v_closed = Text("closed", font=CODE_FONT, font_size=20, color=SLATE)
        v_open_box = SurroundingRectangle(v_open, buff=0.12,
                                          corner_radius=0.08)
        v_open_box.set_stroke(TEAL, 2).set_fill("#EFF9F7", opacity=1.0)
        v_closed_box = SurroundingRectangle(v_closed, buff=0.12,
                                            corner_radius=0.08)
        v_closed_box.set_stroke("#D8DCE3", 2).set_fill("#FFFFFF", opacity=1.0)
        values = VGroup(VGroup(v_open_box, v_open),
                        VGroup(v_closed_box, v_closed))
        values.arrange(RIGHT, buff=0.3)
        inner = VGroup(p_name, VGroup(p_field, values).arrange(RIGHT, buff=0.3))
        inner.arrange(DOWN, buff=0.35)
        inner.move_to(panel.get_center())
        schema_view = VGroup(panel_shadow, panel, inner)
        schema_view.move_to(DOWN * 0.4)

        cap2 = make_caption("The tool lists open as a status value.")
        self.play(FadeOut(cap), run_time=0.2)
        self.play(FadeIn(dim), run_time=0.3)
        self.add(bubble)  # the question stays readable above the dim
        self.play(FadeIn(schema_view, shift=UP * 0.15), FadeIn(cap2),
                  run_time=0.7)
        cap = cap2

        # The word in the question connects to the declared value.
        link = Line(bubble.body.get_bottom() + DOWN * 0.02,
                    v_open_box.get_top() + UP * 0.02)
        link.set_stroke(OK_GREEN, 2.5, opacity=0.9)
        # Above the panel's white fill, so the line visibly reaches the chip —
        # but below the panel's text (z 11), so it passes behind the tool name
        # instead of striking it through.
        link.set_z_index(10)
        inner.set_z_index(11)
        check = Text("✓", font_size=30, color=OK_GREEN)
        # Below the open chip: 0.5 to its right is where the closed chip sits.
        check.next_to(v_open_box, DOWN, buff=0.12)
        check.set_z_index(12)
        self.play(Indicate(bubble.text, color=OK_GREEN, scale_factor=1.03),
                  run_time=0.5)
        self.play(Create(link), run_time=0.5)
        self.play(FadeIn(check, scale=0.5),
                  Indicate(v_open_box, color=OK_GREEN, scale_factor=1.1),
                  run_time=0.6)
        self.wait(0.4)

        # --------- beat 3: so the LLM just asks for it (8-10 s) -----------
        cap2 = make_caption("So the LLM just asks for it.")
        self.play(FadeOut(cap), run_time=0.2)
        self.play(FadeOut(dim), FadeOut(schema_view), FadeOut(link),
                  FadeOut(check), FadeIn(cap2), run_time=0.5)
        cap = cap2

        # Spawns on the wire below the client (UP * 0.15 would sit on the
        # "context window" label) and pauses above the tool card it calls:
        # the server's centre is occupied by the fetch_accounts card here.
        pkt = make_packet().move_to(client.shell.get_bottom() + DOWN * 0.05)
        self.play(FadeIn(pkt, scale=0.4), run_time=0.25)
        p1 = VMobject().set_points_smoothly([
            pkt.get_center(),
            [0, server.shell.get_top()[1] + 0.3, 0],
            [cards[0].get_x(), cards[0].get_top()[1] + 0.16, 0],
        ])
        self.play(MoveAlongPath(pkt, p1), run_time=0.6)
        self.play(server.shell.animate.set_stroke(TEAL, 6), run_time=0.15)
        self.play(server.shell.animate.set_stroke(TEAL, 2.5), run_time=0.2)
        p2 = VMobject().set_points_smoothly([
            pkt.get_center(),
            [apis.endpoints[0].get_x(), apis.shell.get_top()[1] + 0.08, 0],
            apis.endpoints[0].get_center(),
        ])
        self.play(MoveAlongPath(pkt, p2), run_time=0.5)
        self.play(FadeOut(pkt, scale=0.4),
                  apis.endpoints[0].animate.set_color(TEAL), run_time=0.25)
        self.play(apis.endpoints[0].animate.set_color(SLATE), run_time=0.25)

        moving = make_data_rows(3)
        for bar in moving:
            bar.move_to(apis.endpoints[0].get_center()).scale(0.5)
        self.play(
            LaggedStart(*[
                m.animate.move_to(client.ctx_outline.get_center())
                for m in moving
            ], lag_ratio=0.18),
            run_time=0.9,
        )
        fill2 = ctx_fill_target(client, 0.4)
        self.play(FadeOut(moving), Transform(client.ctx_fill, fill2),
                  run_time=0.4)

        # ------ beat 4: only what the tool spells out (10-12 s) -----------
        cap2 = make_caption("It can only ask for what the tool spells out.")
        self.play(FadeOut(cap), run_time=0.2)
        ring = SurroundingRectangle(cards[0], buff=0.07, corner_radius=0.08)
        ring.set_stroke(TEAL, 3)
        shade = Rectangle(width=8, height=10)
        # Added transparent and faded up in the play: a bare self.add() at
        # 0.35 would pop the shade on in a single frame.
        shade.set_stroke(width=0).set_fill(BG, opacity=0.0)
        self.add(shade)
        self.add(cards[0])  # re-adding lifts the spotlighted card above the shade
        self.play(FadeIn(cap2), Create(ring),
                  shade.animate.set_fill(BG, opacity=0.35),
                  run_time=0.7)
        cap = cap2
        self.wait(0.4)
        self.play(FadeOut(shade), FadeOut(ring), run_time=0.4)

        # ------------------------------------------------- final hold ----
        self.wait(1.0)
