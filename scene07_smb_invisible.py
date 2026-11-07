"""Scene 7: why SMB is invisible. ~11.7 s of motion plus a 1 s hold.

The LLM searches the tool for SMB and finds nothing, then the candidates
appear: deal size on the opportunity, segment or employees on the account,
and three customers who each define it differently.

Narration (srt + 0.5 s):
  0.55   "SMB isn't in the tool or the schema."
  3.05   "It might be deal size on the opportunity, or more likely a
          segment on the account."
  7.48   "Every customer defines it differently, and the LLM can't know
          which."
"""

from manim import *
from common import (
    make_ai_client, make_mcp_server, make_api_box, make_background,
    make_tool_card, make_big_tool_card, make_caption, make_dot_grid,
    make_bubble, make_object_card, ctx_fill_target,
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


class Scene07SmbInvisible(Scene):
    def construct(self):
        # ------------- base layout, dimmed, as scene 6 left it ------------
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

        # ------ beat 1: not in the tool, not in the schema (0.5-3 s) ------
        big = make_big_tool_card(*TOOL_SPECS[0]).move_to(UP * 0.55)
        cap = make_caption("SMB isn't in the tool or the schema.")
        self.play(FadeIn(big, shift=UP * 0.15), FadeIn(cap), run_time=0.6)
        # The row scan is "isn't in the tool..." ("isn't" heard at 1.23);
        # without this hold the first spotlight led the word by 0.33 s.
        self.wait(0.15)

        # A spotlight sweeps each row; nothing matches, a red X per row.
        xs = VGroup()
        for row in big.rows:
            hl = SurroundingRectangle(row, buff=0.08, corner_radius=0.06)
            hl.set_stroke(SLATE, 2)
            x = Text("✗", font_size=24, color=ALERT_RED)
            # In the margin, outside the card: inside it the description row's
            # text runs to the card edge and the mark landed on "status".
            x.next_to(big.card.get_right(), RIGHT, buff=0.12)
            x.match_y(row)
            xs.add(x)
            self.play(Create(hl), run_time=0.2)
            self.play(FadeIn(x, scale=0.6), FadeOut(hl), run_time=0.35)
        self.wait(0.15)

        # ------ beat 2: the candidate fields (3.1-7.4 s) ------------------
        opp = make_object_card("Opportunity", ["amount", "status"])
        acc = make_object_card("Account", ["segment", "employees"])
        opp.move_to(LEFT * 1.55 + UP * 0.75)
        acc.move_to(RIGHT * 1.55 + UP * 0.75)
        rel = Line(opp.card.get_right(), acc.card.get_left())
        rel.set_stroke(GREY, 2, opacity=0.8)

        cap2 = make_caption("Deal size? Or a segment on the account?")
        self.play(FadeOut(cap), run_time=0.2)
        self.play(FadeOut(big), FadeOut(xs),
                  FadeIn(opp), FadeIn(acc), Create(rel), FadeIn(cap2),
                  run_time=0.7)
        cap = cap2

        self.play(Indicate(opp.fields["amount"], color=AMBER,
                           scale_factor=1.3), run_time=0.7)
        # "segment" is heard at 6.12; the old 0.9 s wait pulsed it at 5.35.
        self.wait(1.45)
        self.play(Indicate(acc.fields["segment"], color=AMBER,
                           scale_factor=1.3), run_time=0.7)
        self.play(Indicate(acc.fields["employees"], color=AMBER,
                           scale_factor=1.3), run_time=0.6)
        self.wait(0.4)

        # ------ beat 3: every customer differs (7.5-11.7 s) ---------------
        cap2 = make_caption("Every customer defines it differently.")
        self.play(FadeOut(cap), run_time=0.2)

        tiles = VGroup()
        for i, name in enumerate(["Customer A", "Customer B", "Customer C"]):
            t = Text(name, font=UI_FONT, font_size=14, color=INK)
            box = RoundedRectangle(corner_radius=0.1, width=t.width + 0.4,
                                   height=0.5)
            box.set_stroke("#D8DCE3", 1.8).set_fill("#FFFFFF", opacity=1.0)
            t.move_to(box.get_center())
            tile = VGroup(box, t)
            # Inside the MCP server card's empty body: at DOWN*1.7 the tiles
            # straddled the server card's bottom border and the APIs card's
            # top border.
            tile.move_to(DOWN * 1.15 + RIGHT * (i - 1) * 2.05)
            tiles.add(tile)

        targets = [acc.fields["segment"], acc.fields["employees"],
                   opp.fields["amount"]]
        arrows = VGroup()
        for tile, tgt in zip(tiles, targets):
            a = CurvedArrow(tile.get_top() + UP * 0.05,
                            tgt.get_bottom() + DOWN * 0.08,
                            angle=-0.35, tip_length=0.12)
            a.set_stroke(SLATE, 1.8, opacity=0.75)
            arrows.add(a)

        self.play(
            LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles],
                        lag_ratio=0.2),
            FadeIn(cap2),
            run_time=0.9,
        )
        cap = cap2
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.25),
                  run_time=1.2)

        # The LLM can't know which: a question mark over the tangle.
        q = Text("?", font=UI_FONT, font_size=40, color=PURPLE, weight=BOLD)
        # On a white badge: bare, it sat directly on the dimmed tool card's
        # text inside the LLM.
        badge = Circle(radius=0.3)
        badge.set_stroke(PURPLE, 2).set_fill("#FFFFFF", opacity=0.95)
        q_g = VGroup(badge, q.move_to(badge.get_center()))
        q_g.move_to(UP * 2.1)
        # The badge answers "can't know which" ("can't" heard at 10.51).
        self.wait(0.35)
        self.play(FadeIn(q_g, scale=0.5), run_time=0.5)
        self.wait(1.4)

        # ------------------------------------------------- final hold ----
        self.wait(1.5)
