"""Scene 10: the same question, resolved. ~23 s of motion plus a 1 s hold.

The key scene. The LLM searches the semantic model for SMB, gets back one
small fact, sends a short request, and its job ends. The compiler assembles
the SQL from the model's building blocks, permissions included. Nothing
guessed.

Narration (srt + 0.5 s):
  0.55   "Now the same question, through the layer."
  2.66   "The LLM searches the semantic model for the words it doesn't
          know, and gets back only what it needs: SMB is a value of
          segment, on the account."
  11.32  "It sends a short request back, and that's where its job ends."
  14.67  "A compiler, plain code, picks up the building blocks, the join
          and the formulas, and builds the SQL, permissions included."
  21.99  "Nothing guessed."
"""

from manim import *
from common import (
    make_ai_client, make_mcp_server, make_api_box, make_background,
    make_tool_card, make_caption, make_dot_grid, make_bubble,
    make_sem_zone, make_sem_stack, make_object_card, make_compiler,
    make_block, make_lock, ctx_fill_target, make_shadow,
    BG, INK, MUTED, PURPLE, PURPLE_FILL, TEAL, TEAL_DARK, GREY, SLATE,
    ALERT_RED, AMBER, OK_GREEN, PACKET_WHITE,
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


class Scene10Resolved(Scene):
    def construct(self):
        # ------------- reflowed layout, as scene 9 left it ----------------
        bg = make_background()
        grid = make_dot_grid()
        client = make_ai_client()
        cards = VGroup(*[make_tool_card(*s) for s in TOOL_SPECS])
        cards.arrange(RIGHT, buff=0.18)
        cards.scale_to_fit_width(5.1)
        for card, dx in zip(cards, (-1.08, 0.0, 1.08)):
            card.scale(0.6).move_to(
                client.llm.get_center() + DOWN * 0.1 + RIGHT * dx)
        cg = VGroup(client, cards)
        cg.scale(0.62).move_to(UP * 2.25)
        client.ctx_fill.become(ctx_fill_target(client, 0.08))

        server = make_mcp_server().scale(0.65).move_to(UP * 0.6)
        apis = make_api_box().scale(0.7).move_to(DOWN * 2.82)
        apis.endpoints.set_opacity(0.55)
        zone = make_sem_zone().move_to(DOWN * 1.2)
        w1 = Line(client.shell.get_bottom(), server.shell.get_top())
        w2 = Line(server.shell.get_bottom(), zone.shell.get_top())
        w3 = Line(zone.shell.get_bottom(), apis.shell.get_top())
        for w in (w1, w2, w3):
            w.set_stroke(GREY, 2.2, opacity=0.75)

        stack = make_sem_stack(3)
        stack.move_to(zone.shell.get_center() + LEFT * 1.7 + DOWN * 0.08)
        opp = make_object_card("Opportunity", ["status"], width=1.6).scale(0.8)
        acc = make_object_card("Account", ["segment"], width=1.6).scale(0.8)
        opp.move_to(zone.shell.get_center() + RIGHT * 0.55 + UP * 0.08)
        acc.move_to(zone.shell.get_center() + RIGHT * 2.05 + UP * 0.08)
        rel = Line(opp.card.get_right(), acc.card.get_left())
        rel.set_stroke(AMBER, 2.5)
        tag_open = Text("“open”", font=UI_FONT, font_size=12,
                        color=AMBER)
        tag_smb = Text("“SMB”", font=UI_FONT, font_size=12,
                       color=AMBER)
        tag_open.next_to(opp, DOWN, buff=0.1)
        tag_smb.next_to(acc, DOWN, buff=0.1)

        # Packets and data rows travel the full column; keep the card titles
        # and labels above them so nothing drives over text.
        server.title.set_z_index(2)
        apis.title.set_z_index(2)
        client.ctx_label.set_z_index(2)
        stack.label.set_z_index(2)

        self.add(bg, grid, w1, w2, w3, server, apis, zone, cg,
                 stack, opp, acc, rel, tag_open, tag_smb)
        self.wait(0.3)

        # ------ beat 1: the question returns (0.5-2.6 s) ------------------
        bubble = make_bubble("show me my open SMB opportunities", width=4.9)
        bubble.text[12:15].set_color(ALERT_RED)
        bubble.scale(0.8).move_to(UP * 3.6)
        cap = make_caption("Now the same question, through the layer.")
        # Peak sync: the bubble completes at 1.0 s, ON "question"
        # (heard 1.03 s).
        self.play(FadeIn(bubble, shift=DOWN * 0.15), FadeIn(cap),
                  run_time=0.7)
        self.wait(1.3)

        # ------ beat 2: search the model for SMB (2.7-11 s) ---------------
        cap2 = make_caption("It searches the model for the words it doesn't know.")
        self.play(FadeOut(cap), run_time=0.2)
        cap = cap2

        q_lab = Text("SMB?", font=CODE_FONT, font_size=12, color="#FFFFFF")
        q_pill = RoundedRectangle(corner_radius=0.1,
                                  width=q_lab.width + 0.26, height=0.26)
        q_pill.set_stroke(width=0).set_fill(PACKET_WHITE, 1.0)
        q_lab.move_to(q_pill.get_center())
        pkt = VGroup(q_pill, q_lab)
        # The unknown word starts inside the context window: below the LLM
        # box the gap is too narrow and the pill straddled both edges.
        pkt.move_to(client.ctx_outline.get_center())
        self.play(FadeIn(pkt, scale=0.5), FadeIn(cap2), run_time=0.4)
        path = VMobject().set_points_smoothly([
            pkt.get_center(),
            server.shell.get_center(),
            stack.cards.get_top() + UP * 0.15,
        ])
        self.play(MoveAlongPath(pkt, path), run_time=1.0)
        self.play(FadeOut(pkt, scale=0.5), run_time=0.2)

        # The files flip: a quick teal flicker, done by plain code.
        # Peak sync: the flicker runs 4.3-5.2 s, across "the words it
        # doesn't know" (heard 4.8-6.2 s).
        self.wait(0.2)
        self.play(
            LaggedStart(*[
                Indicate(c, color=TEAL, scale_factor=1.06)
                for c in stack.cards
            ], lag_ratio=0.18),
            run_time=0.9,
        )
        top_card = stack.cards[-1]
        self.play(top_card.body.animate.set_fill(AMBER, opacity=0.35),
                  run_time=0.3)
        self.play(top_card.body.animate.set_fill("#FBF3E8", opacity=1.0),
                  run_time=0.3)

        # One small amber fact travels back and lands in the context.
        fact_pkt = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.24)
        fact_pkt.set_stroke(width=0).set_fill(AMBER, 1.0)
        fact_pkt.move_to(stack.cards.get_top() + UP * 0.1)
        # Peak sync: the travel starts at 6.0 s, half its run before
        # "gets back" (heard 6.4 s), so the landing peaks on "only what
        # it needs" instead of arriving a beat late.
        self.play(FadeIn(fact_pkt, scale=0.5), run_time=0.2)
        back = VMobject().set_points_smoothly([
            fact_pkt.get_center(),
            server.shell.get_center() + RIGHT * 0.4,
            client.ctx_outline.get_center(),
        ])
        self.play(MoveAlongPath(fact_pkt, back), run_time=0.8)
        # The fact lands inside the context window: between the LLM box and
        # the bar there is no room, and the text sat across the bar outline.
        fact = Text("SMB = account.segment", font=CODE_FONT, font_size=11,
                    color=AMBER)
        fact.move_to(client.ctx_outline.get_center())
        self.play(FadeTransform(fact_pkt, fact), run_time=0.5)
        self.play(Transform(client.ctx_fill, ctx_fill_target(client, 0.14)),
                  run_time=0.3)
        # The unknown word is unknown no more. The amber ring mirrors the red
        # ring of scene 6: the payoff rhymes with the break.
        # Accent sync: the ring draws 8.1-8.9 s, so it is live ON "SMB"
        # itself (heard 8.28 s), not starting there.
        self.wait(0.5)
        self.play(bubble.text[12:15].animate.set_color(AMBER),
                  Circumscribe(bubble.text[12:15], color=AMBER, buff=0.08),
                  run_time=0.8)
        self.wait(2.05)

        # ------ beat 3: a short request, job ends (11.3-14.6 s) -----------
        cap2 = make_caption("A short request back. The LLM's job ends.")
        self.play(FadeOut(cap), run_time=0.2)
        cap = cap2

        req_tags = VGroup(*[
            Text(t, font=CODE_FONT, font_size=10, color=INK)
            for t in ["opportunities", "status: open", "segment: SMB"]
        ])
        req_tags.arrange(RIGHT, buff=0.18)
        req_card = RoundedRectangle(corner_radius=0.08,
                                    width=req_tags.width + 0.3, height=0.36)
        req_card.set_stroke(PURPLE, 2).set_fill("#FFFFFF", opacity=1.0)
        req_tags.move_to(req_card.get_center())
        req = VGroup(req_card, req_tags)
        req.move_to(fact.get_center())
        # Peak sync: the transform peaks at 11.85 s, on "short request"
        # (heard 11.8-12.5 s); the send-off below then peaks on "back"
        # (heard 12.5 s).
        self.play(FadeTransform(fact, req), FadeIn(cap2), run_time=0.7)
        self.wait(0.25)
        # It stops on the wire just above the layer: inside the zone it would
        # strike through the zone title.
        self.play(req.animate.scale(0.7).move_to([0, -0.08, 0]), run_time=0.9)

        # The purple pulse stops: from here on, everything is teal.
        # Peak sync: the dim runs 13.1-13.7 s, peaking into "job ends"
        # (heard 13.7-14.5 s).
        self.wait(0.1)
        self.play(client.llm.animate.set_stroke(PURPLE, 3, opacity=0.35)
                  .set_fill(PURPLE, opacity=0.02),
                  client.llm_label.animate.set_opacity(0.4),
                  run_time=0.6)
        self.wait(0.55)

        # ------ beat 4: the compiler builds the SQL (14.7-21.9 s) ---------
        cap2 = make_caption("A compiler assembles the SQL. Permissions included.")
        self.play(FadeOut(cap), run_time=0.2)
        cap = cap2

        # The object cards fold back into the model; the compiler steps in.
        self.play(
            FadeOut(tag_open), FadeOut(tag_smb), FadeOut(rel),
            opp.animate.scale(0.25).move_to(stack.cards.get_center()),
            acc.animate.scale(0.25).move_to(stack.cards.get_center()),
            FadeOut(req),
            # The title hands the floor to the compiler, which arrives where
            # it would otherwise collide with it.
            # Fully out, not 0.15: a half-visible title half-hidden behind
            # the compiler read as a bug. The amber stroke still names the
            # zone.
            zone.title.animate.set_opacity(0.0),
            FadeIn(cap2),
            run_time=0.6,
        )
        self.remove(opp, acc)

        compiler = make_compiler()
        compiler.move_to(zone.shell.get_center() + RIGHT * 1.45 + UP * 0.25)
        # Peak sync: the fold peaked on "A compiler" (heard 14.8 s); the
        # compiler itself fades in 15.3-15.8 s, peaking on "plain code"
        # (heard 15.6-16.4 s).
        self.wait(0.25)
        self.play(FadeIn(compiler, scale=0.8), run_time=0.5)

        blocks = VGroup(make_block("join: opp → account"),
                        make_block("count"),
                        make_block("open = not closed"))
        # Spread over the stack rather than superimposed on one point, and
        # fade in rather than popping in a single frame.
        for i, b in enumerate(blocks):
            b.move_to(stack.cards.get_center() + UP * (0.32 * (1 - i)))
        targets = [
            compiler.box.get_bottom() + DOWN * 0.3 + LEFT * 0.75,
            compiler.box.get_bottom() + DOWN * 0.3 + RIGHT * 0.55,
            compiler.box.get_bottom() + DOWN * 0.68 + LEFT * 0.3,
        ]
        self.play(FadeIn(blocks, lag_ratio=0.15, scale=0.6), run_time=0.3)
        # Peak sync: the travel runs 16.1-17.1 s, starting half its run
        # before "picks up" (heard 16.6 s) so it peaks on "building
        # blocks" (heard 17.0-17.9 s).
        self.play(
            LaggedStart(*[
                b.animate.move_to(t) for b, t in zip(blocks, targets)
            ], lag_ratio=0.3),
            run_time=1.0,
        )

        # The blocks snap together into one SQL card with a lock on it.
        sql_lines = VGroup(*[
            Text(s, font=CODE_FONT, font_size=10, color=SLATE)
            for s in ["SELECT count(*) FROM opportunity o",
                      "JOIN account a ON o.account_id = a.id",
                      "WHERE o.status='open' AND a.segment='SMB'"]
        ])
        sql_lines.arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        sql_card = RoundedRectangle(corner_radius=0.08,
                                    width=sql_lines.width + 0.3,
                                    height=sql_lines.height + 0.26)
        sql_card.set_stroke(TEAL, 2).set_fill("#FFFFFF", opacity=1.0)
        sql_lines.move_to(sql_card.get_center())
        sql = VGroup(sql_card, sql_lines)
        sql.move_to(compiler.box.get_bottom() + DOWN * 0.4)
        # Keep the card (and the lock badge on its corner) inside the zone:
        # centred under the compiler it crossed the zone's right border.
        overshoot = sql.get_right()[0] - 2.5
        if overshoot > 0:
            sql.shift(LEFT * overshoot)
        # Peak sync: the blocks hold under the compiler through "the join
        # and the formulas", then snap so the card completes between
        # "builds" and "SQL" (heard 20.1-20.5 s). The wait is 0.3 s short
        # of the arithmetic value: frame rounding at 15 fps accumulates
        # ~0.3 s of drift by this point (verified against rendered
        # frames), and this is where it is paid back.
        self.wait(1.9)
        self.play(FadeTransform(blocks, sql), run_time=0.7)
        # Peak sync: the lock fades in 20.45-20.85 s, landing ON
        # "permissions included" (heard 20.8-21.8 s): the old early-lock
        # compromise is gone. 0.8 was set from rendered frames, not
        # arithmetic: it puts the fade at 20.5-20.9 s actual.
        self.wait(0.8)
        lock = make_lock(0.8)
        lock.move_to(sql_card.get_corner(UR))
        self.play(FadeIn(lock, scale=0.5), run_time=0.4)
        # The SQL card is the proof: it has held since 19.85 s. The run
        # below is compressed (rule 2: no animated tail past the voice)
        # so the "Nothing guessed" accent stays on its words.

        # It runs: down to the systems, rows back up to the client.
        sql_pkt = RoundedRectangle(corner_radius=0.1, width=0.55, height=0.24)
        sql_pkt.set_stroke(width=0).set_fill(TEAL, 1.0)
        sql_pkt.move_to(sql.get_bottom() + DOWN * 0.08)
        # Run_times from here to the check are frame-exact (multiples of
        # 1/15 s): nine chained plays otherwise each round up a frame and
        # push the "Nothing guessed" accent off its words.
        self.play(FadeTransform(sql, sql_pkt), FadeOut(lock), run_time=0.2)
        self.play(sql_pkt.animate.move_to(apis.shell.get_center()),
                  run_time=4 / 15)
        self.play(FadeOut(sql_pkt, scale=0.4),
                  apis.shell.animate.set_stroke(TEAL, 4), run_time=1 / 15)
        self.play(apis.shell.animate.set_stroke("#D8DCE3", 2.5),
                  run_time=1 / 15)

        rows = VGroup(*[
            Rectangle(width=1.0 - 0.12 * i, height=0.07)
            .set_stroke(width=0).set_fill(SLATE, 0.85)
            for i in range(3)
        ])
        rows.arrange(DOWN, buff=0.09, aligned_edge=LEFT)
        rows.move_to(apis.shell.get_top() + UP * 0.15)
        self.play(FadeIn(rows), run_time=1 / 15)
        self.play(rows.animate.move_to(client.ctx_outline.get_center()),
                  run_time=4 / 15)
        self.play(FadeOut(rows),
                  Transform(client.ctx_fill, ctx_fill_target(client, 0.18)),
                  run_time=2 / 15)

        # ------ beat 5: nothing guessed (22 s) ----------------------------
        cap2 = make_caption("Nothing guessed.")
        self.play(FadeOut(cap), run_time=1 / 15)
        check = Text("✓", font_size=34, color=OK_GREEN)
        check.next_to(compiler.box, RIGHT, buff=0.22)
        # Circumscribe, not Indicate: Indicate left the file cards tinted
        # dark amber after it finished.
        # Accent sync: check + ring run 22.3-23.0 s, ON "Nothing guessed"
        # (heard 22.1-22.9 s); the voice ends at 23.06 s, so no animation
        # outlives it (rule 2).
        self.play(FadeIn(cap2), FadeIn(check, scale=0.5),
                  Circumscribe(stack.cards, color=AMBER, buff=0.1),
                  run_time=0.7)

        # ------------------------------------------------- final hold ----
        # Motion ends 22.99 s, voice 23.06 s: a 1.2 s static hold leaves a
        # ~1.1 s silent tail, inside the 0.6-1.2 s window.
        self.wait(1.2)
