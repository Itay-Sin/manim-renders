"""Scene 8: two bad options. ~11.6 s of motion plus a 1 s hold.

Option 1: stuff every field into the descriptions and the context explodes.
Option 2: let the LLM explore and write the query, and it's still guessing.
Stacked panels for the vertical frame; both end outlined in red.

Narration (srt + 0.5 s):
  0.55   "That leaves two bad options."
  2.27   "Put every field and value in the tool descriptions, and your
          context explodes."
  7.14   "Or let the LLM explore and write the query itself, and it's
          still guessing."
"""

from manim import *
from common import (
    make_ai_client, make_mcp_server, make_api_box, make_background,
    make_tool_card, make_caption, make_dot_grid, make_bubble,
    make_packet, ctx_fill_target, make_shadow,
    BG, INK, MUTED, PURPLE, PURPLE_FILL, TEAL, GREY, SLATE, ALERT_RED,
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

FIELD_NAMES = ["segment", "region", "tier", "industry",
               "employees", "country", "stage", "owner"]


def panel(label):
    box = RoundedRectangle(corner_radius=0.16, width=5.9, height=2.55)
    box.set_stroke("#D8DCE3", 2).set_fill("#FFFFFF", opacity=1.0)
    tag_text = Text(label, font=UI_FONT, font_size=14, color="#FFFFFF",
                    weight=BOLD)
    tag = RoundedRectangle(corner_radius=0.12, width=tag_text.width + 0.34,
                           height=0.32)
    tag.set_stroke(width=0).set_fill(SLATE, 1.0)
    tag_text.move_to(tag.get_center())
    tag_g = VGroup(tag, tag_text)
    tag_g.move_to(box.get_corner(UL) + RIGHT * (tag.width / 2 + 0.2)
                  + DOWN * 0.32)
    g = VGroup(make_shadow(box), box, tag_g)
    g.box = box
    return g


class Scene08TwoBadOptions(Scene):
    def construct(self):
        # ------------- base layout, dimmed, as scene 7 left it ------------
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

        # ------------- beat 1: two panels appear (0.5-2.2 s) --------------
        p1 = panel("option 1").move_to(UP * 1.62)
        p2 = panel("option 2").move_to(DOWN * 1.38)
        cap = make_caption("That leaves two bad options.")
        self.play(FadeIn(p1, shift=UP * 0.1), FadeIn(p2, shift=UP * 0.1),
                  FadeIn(cap), run_time=0.7)
        self.wait(0.9)

        # ------------- beat 2, option 1: context explodes (2.3-6.6) -------
        cap2 = make_caption("Describe every field, and the context explodes.")
        self.play(FadeOut(cap), run_time=0.2)
        cap = cap2

        tool = make_tool_card(*TOOL_SPECS[0]).scale(0.85)
        tool.move_to(p1.box.get_center() + LEFT * 1.55 + DOWN * 0.15)
        bar_out = Rectangle(width=1.9, height=0.34).set_stroke(PURPLE, 2)
        bar_out.move_to(p1.box.get_center() + RIGHT * 1.55 + DOWN * 0.15)
        bar_fill = Rectangle(width=1.2, height=0.24)
        bar_fill.set_stroke(width=0).set_fill(PURPLE_FILL, 0.9)
        bar_fill.move_to(bar_out.get_left() + RIGHT * (0.05 + 0.6))
        bar_tag = Text("context", font=UI_FONT, font_size=12, color=MUTED)
        bar_tag.next_to(bar_out, DOWN, buff=0.08)

        chips = VGroup()
        for i, name in enumerate(FIELD_NAMES):
            t = Text(name, font=CODE_FONT, font_size=11, color=SLATE)
            # Two staggered spawn rows, so the chips never sit on each other.
            t.move_to(p1.box.get_top() + DOWN * (0.32 + 0.34 * (i // 4))
                      + RIGHT * (2.15 - 0.85 * (i % 4)))
            chips.add(t)

        self.play(FadeIn(tool), FadeIn(bar_out), FadeIn(bar_fill),
                  FadeIn(bar_tag), FadeIn(cap2), run_time=0.5)
        # Fade the chips in at their spawn grid, then fly them one after the
        # other on fanned arcs: all eight flying at once crossed each other
        # as overlapping text.
        self.play(FadeIn(chips, lag_ratio=0.08), run_time=0.3)
        self.play(
            LaggedStart(*[
                c.animate(path_arc=-0.45).scale(0.4)
                .move_to(tool.get_center())
                for c in chips
            ], lag_ratio=0.22),
            run_time=1.3,
        )
        self.play(FadeOut(chips), tool.animate.scale(1.18), run_time=0.3)

        # The bar bursts its outline: the fill grows past the right edge.
        spill = Rectangle(width=2.15, height=0.24)
        spill.set_stroke(width=0).set_fill(ALERT_RED, 0.75)
        spill.move_to(bar_out.get_left() + RIGHT * (0.05 + 1.075))
        self.play(Transform(bar_fill, spill), run_time=0.6)
        self.play(bar_out.animate.set_stroke(ALERT_RED, 2.5), run_time=0.3)
        self.wait(1.4)

        # ------------- beat 3, option 2: explore and guess (7.1-10.6) -----
        cap2 = make_caption("Or the LLM explores, and it's still guessing.")
        self.play(FadeOut(cap), run_time=0.2)
        cap = cap2

        llm_mini = RoundedRectangle(corner_radius=0.1, width=1.0, height=0.6)
        llm_mini.set_stroke(PURPLE, 2.5).set_fill(PURPLE, opacity=0.07)
        llm_tag = Text("LLM", font=UI_FONT, font_size=13, color=PURPLE)
        llm_tag.move_to(llm_mini.get_center())
        llm_g = VGroup(llm_mini, llm_tag)
        llm_g.move_to(p2.box.get_center() + LEFT * 2.0 + UP * 0.35)
        data_box = RoundedRectangle(corner_radius=0.1, width=1.4, height=0.6)
        data_box.set_stroke(GREY, 2).set_fill("#FFFFFF", opacity=1.0)
        data_tag = Text("your data", font=UI_FONT, font_size=12, color=SLATE)
        data_tag.move_to(data_box.get_center())
        data_g = VGroup(data_box, data_tag)
        data_g.move_to(p2.box.get_center() + RIGHT * 1.9 + UP * 0.35)

        self.play(FadeIn(llm_g), FadeIn(data_g), FadeIn(cap2), run_time=0.4)

        for probe in ["list objects", "list fields", "sample values"]:
            lab = Text(probe, font=CODE_FONT, font_size=10, color="#FFFFFF")
            pill = RoundedRectangle(corner_radius=0.09,
                                    width=lab.width + 0.24, height=0.26)
            pill.set_stroke(width=0).set_fill(SLATE, 1.0)
            lab.move_to(pill.get_center())
            pkt = VGroup(pill, lab)
            pkt.move_to(llm_g.get_right() + RIGHT * 0.2)
            self.play(FadeIn(pkt, scale=0.6), run_time=0.15)
            self.play(pkt.animate.next_to(data_g, LEFT, buff=0.1),
                      run_time=0.35)
            self.play(pkt.animate.move_to(llm_g.get_right() + RIGHT * 0.2)
                      .scale(0.7), run_time=0.3)
            self.play(FadeOut(pkt, scale=0.3), run_time=0.15)

        # Then it writes the query itself: a guessed join, dashed and wobbly.
        q_opp = Text("Opportunity", font=UI_FONT, font_size=13, color=INK)
        q_acc = Text("Account", font=UI_FONT, font_size=13, color=INK)
        q_opp.move_to(p2.box.get_center() + LEFT * 1.6 + DOWN * 0.75)
        q_acc.move_to(p2.box.get_center() + RIGHT * 1.6 + DOWN * 0.75)
        wob = VMobject()
        wob.set_points_smoothly([
            q_opp.get_right() + RIGHT * 0.15,
            p2.box.get_center() + DOWN * 0.62,
            p2.box.get_center() + DOWN * 0.9 + RIGHT * 0.7,
            q_acc.get_left() + LEFT * 0.15,
        ])
        wobbly = DashedVMobject(wob, num_dashes=14)
        wobbly.set_stroke(ALERT_RED, 2)
        qmark = Text("?", font=UI_FONT, font_size=22, color=ALERT_RED,
                     weight=BOLD)
        qmark.move_to(p2.box.get_center() + DOWN * 0.45)
        self.play(FadeIn(q_opp), FadeIn(q_acc), run_time=0.3)
        self.play(Create(wobbly), FadeIn(qmark, scale=0.6), run_time=0.6)

        # ------------- both are dead ends ---------------------------------
        self.play(p1.box.animate.set_stroke(ALERT_RED, 2.5),
                  p2.box.animate.set_stroke(ALERT_RED, 2.5),
                  run_time=0.5)

        # ------------------------------------------------- final hold ----
        self.wait(1.5)
