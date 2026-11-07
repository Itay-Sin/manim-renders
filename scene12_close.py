"""Scene 12: close. ~17.7 s of motion plus a 1.5 s hold.

Two different tools, side by side: MCP acts on your systems, the semantic
layer understands your data, and sometimes you need both.

Narration (srt + 0.5 s):
  0.55   "So, these are two different tools."
  2.47   "MCP reaches your systems and acts on them."
  5.27   "The semantic layer understands your data."
  7.35   "Simple actions need MCP."
  9.37   "Open questions in your business's own words need the semantic
          layer."
  13.00  "And sometimes you need both: the layer finds the records, and an
          MCP tool acts on them."
"""

from manim import *
from common import (
    make_background, make_caption, make_dot_grid, make_sem_card,
    make_shadow,
    BG, INK, MUTED, PURPLE, TEAL, GREY, SLATE, AMBER, OK_GREEN,
    PACKET_WHITE, CODE_FONT, UI_FONT,
)


def tool_card(label, color, fill, icon):
    box = RoundedRectangle(corner_radius=0.16, width=2.6, height=1.9)
    box.set_stroke(color, 2.5).set_fill("#FFFFFF", opacity=1.0)
    icon.move_to(box.get_center() + UP * 0.25)
    tag = Text(label, font=UI_FONT, font_size=18, color=color, weight=BOLD)
    tag.move_to(box.get_center() + DOWN * 0.55)
    g = VGroup(make_shadow(box), box, icon, tag)
    g.box, g.icon, g.tag = box, icon, tag
    return g


def plug_icon():
    body = RoundedRectangle(corner_radius=0.08, width=0.62, height=0.44)
    body.set_stroke(TEAL, 2.5).set_fill("#EFF9F7", opacity=1.0)
    prongs = VGroup(*[
        Line(ORIGIN, UP * 0.18).set_stroke(TEAL, 3)
        for _ in range(2)
    ])
    prongs[0].move_to(body.get_top() + UP * 0.09 + LEFT * 0.14)
    prongs[1].move_to(body.get_top() + UP * 0.09 + RIGHT * 0.14)
    cord = Line(ORIGIN, DOWN * 0.22).set_stroke(TEAL, 3)
    cord.move_to(body.get_bottom() + DOWN * 0.11)
    return VGroup(cord, body, prongs)


def stack_icon():
    cards = VGroup(*[
        make_sem_card(width=0.8, height=0.5).shift(UP * 0.1 * i
                                                   + RIGHT * 0.06 * i)
        for i in range(3)
    ])
    return cards


class Scene12Close(Scene):
    def construct(self):
        bg = make_background()
        grid = make_dot_grid()
        self.add(bg, grid)
        self.wait(0.3)

        # ------ beat 1: two tools, side by side (0.5-2.4 s) ---------------
        mcp = tool_card("MCP", TEAL, "#EFF9F7", plug_icon())
        sem = tool_card("semantic layer", AMBER, "#FBF3E8", stack_icon())
        mcp.move_to(LEFT * 1.5 + UP * 2.3)
        sem.move_to(RIGHT * 1.5 + UP * 2.3)

        systems = RoundedRectangle(corner_radius=0.14, width=3.4, height=0.9)
        systems.set_stroke(GREY, 2.5).set_fill("#FFFFFF", opacity=1.0)
        sys_tag = Text("your systems", font=UI_FONT, font_size=17, color=SLATE)
        sys_tag.move_to(systems.get_center())
        sys_g = VGroup(make_shadow(systems), systems, sys_tag)
        sys_g.move_to(DOWN * 2.55)

        # The cards sit above the travelling packets, so a packet entering a
        # card slides behind it instead of driving over its icon and label.
        for g in (mcp, sem, sys_g):
            g.set_z_index(1)

        # Faint wires from each tool down to the systems card, so the middle
        # of the frame never reads empty between beats.
        wire_m = Line(mcp.box.get_bottom(), systems.get_top() + LEFT * 0.8)
        wire_s = Line(sem.box.get_bottom(), systems.get_top() + RIGHT * 0.8)
        for w in (wire_m, wire_s):
            w.set_stroke(GREY, 2, opacity=0.45)

        cap = make_caption("Two different tools.")
        self.play(FadeIn(mcp, shift=UP * 0.15), FadeIn(sem, shift=UP * 0.15),
                  FadeIn(sys_g), FadeIn(wire_m), FadeIn(wire_s), FadeIn(cap),
                  run_time=0.8)
        self.wait(1.0)

        # ------ beat 2: MCP acts (2.5-5.2 s) ------------------------------
        cap2 = make_caption("MCP reaches your systems and acts.")
        self.play(FadeOut(cap), run_time=0.2)
        # A scale-pop with a stroke pulse, not Indicate: Indicate's colour
        # flooded the white card solid teal at the flash peak.
        # Each card's role sticks as a small label, so the roles survive the
        # caption swaps and the last frame summarises itself.
        mcp_role = Text("acts on your systems", font=UI_FONT, font_size=14,
                        color=TEAL)
        mcp_role.next_to(mcp, DOWN, buff=0.14)
        mcp_role.set_z_index(1)
        self.play(FadeIn(cap2), FadeIn(mcp_role, shift=UP * 0.08),
                  mcp.box.animate(rate_func=there_and_back)
                  .scale(1.04).set_stroke(TEAL, 4),
                  run_time=0.6)
        cap = cap2
        pkt = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.22)
        pkt.set_stroke(width=0).set_fill(PACKET_WHITE, 1.0)
        pkt.move_to(mcp.box.get_bottom() + DOWN * 0.1)
        self.play(FadeIn(pkt, scale=0.5), run_time=0.2)
        self.play(pkt.animate.move_to(systems.get_top() + UP * 0.05),
                  run_time=0.7)
        self.play(FadeOut(pkt, scale=0.4),
                  systems.animate.set_stroke(TEAL, 4), run_time=0.25)
        self.play(systems.animate.set_stroke(GREY, 2.5), run_time=0.25)
        self.wait(0.8)

        # ------ beat 3: the layer understands (5.3-7.3 s) -----------------
        cap2 = make_caption("The semantic layer understands your data.")
        self.play(FadeOut(cap), run_time=0.2)
        # Same scale-pop treatment: Indicate flooded the card solid amber.
        sem_role = Text("understands your data", font=UI_FONT, font_size=14,
                        color=AMBER)
        sem_role.next_to(sem, DOWN, buff=0.14)
        sem_role.set_z_index(1)
        self.play(FadeIn(cap2), FadeIn(sem_role, shift=UP * 0.08),
                  sem.box.animate(rate_func=there_and_back)
                  .scale(1.04).set_stroke(AMBER, 4),
                  run_time=0.7)
        cap = cap2
        self.wait(1.3)

        # ------ beat 4: simple actions, MCP (7.4-9.3 s) -------------------
        cap2 = make_caption("Simple actions: MCP.")
        self.play(FadeOut(cap), run_time=0.2)
        act = Text("update_deal", font=CODE_FONT, font_size=13, color=INK)
        act_box = RoundedRectangle(corner_radius=0.08,
                                   width=act.width + 0.26, height=0.34)
        act_box.set_stroke(TEAL, 1.8).set_fill("#EFF9F7", opacity=1.0)
        act.move_to(act_box.get_center())
        act_g = VGroup(act_box, act)
        act_g.move_to(mcp.box.get_top() + UP * 0.35)
        self.play(FadeIn(act_g, shift=DOWN * 0.15), FadeIn(cap2),
                  run_time=0.5)
        cap = cap2
        path = VMobject().set_points_smoothly([
            act_g.get_center(),
            mcp.box.get_center(),
            systems.get_top() + UP * 0.05,
        ])
        self.play(MoveAlongPath(act_g, path), run_time=0.9)
        self.play(FadeOut(act_g, scale=0.4), run_time=0.2)
        self.wait(0.3)

        # ------ beat 5: open questions, the layer (9.4-12.9 s) ------------
        cap2 = make_caption("Open questions: the semantic layer.")
        self.play(FadeOut(cap), run_time=0.2)
        q = Text("open SMB opportunities?", font=UI_FONT, font_size=13,
                 color=INK)
        q_box = RoundedRectangle(corner_radius=0.14,
                                 width=q.width + 0.3, height=0.4)
        q_box.set_stroke("#D8DCE3", 1.8).set_fill("#FFFFFF", opacity=1.0)
        q.move_to(q_box.get_center())
        q_g = VGroup(q_box, q)
        q_g.set_z_index(2)  # rides on top of the card, unlike the packets
        q_g.move_to(sem.box.get_top() + UP * 0.35)
        self.play(FadeIn(q_g, shift=DOWN * 0.15), FadeIn(cap2), run_time=0.5)
        cap = cap2
        self.play(q_g.animate.scale(0.8).move_to(sem.box.get_center()
                                                 + DOWN * 0.1),
                  run_time=0.7)
        # Circumscribe, not Indicate: Indicate flooded the file-card icon
        # solid dark amber mid-flash.
        self.play(Circumscribe(sem.icon, color=AMBER, buff=0.08),
                  FadeOut(q_g), run_time=0.6)
        self.wait(1.5)

        # ------ beat 6: sometimes both (13-17 s) --------------------------
        cap2 = make_caption("Sometimes both: the layer finds, MCP acts.")
        self.play(FadeOut(cap), run_time=0.2)
        cap = cap2

        rows = VGroup(*[
            Rectangle(width=2.0, height=0.16)
            .set_stroke(width=0).set_fill(SLATE, 0.5)
            for _ in range(3)
        ])
        rows.arrange(DOWN, buff=0.16)
        rows.move_to(DOWN * 0.45)
        self.play(FadeIn(rows), FadeIn(cap2), run_time=0.5)

        # The layer finds the records...
        ring = SurroundingRectangle(rows, buff=0.14, corner_radius=0.1)
        ring.set_stroke(AMBER, 2.5)
        finder = RoundedRectangle(corner_radius=0.08, width=0.4, height=0.18)
        finder.set_stroke(width=0).set_fill(AMBER, 1.0)
        finder.move_to(sem.box.get_bottom() + DOWN * 0.1)
        # Fade in before moving, so the pill doesn't pop in a single frame.
        self.play(Succession(
            FadeIn(finder, scale=0.5, run_time=0.2),
            ApplyMethod(finder.move_to, rows.get_top() + UP * 0.2,
                        run_time=0.4),
        ))
        self.play(FadeOut(finder, scale=0.4), Create(ring), run_time=0.5)

        # ...and an MCP tool acts on them.
        actor = RoundedRectangle(corner_radius=0.08, width=0.4, height=0.18)
        actor.set_stroke(width=0).set_fill(TEAL, 1.0)
        actor.move_to(mcp.box.get_bottom() + DOWN * 0.1)
        # Fades in before moving, and parks above the ring: at UP*0.2 it
        # landed on the ring's border.
        self.play(Succession(
            FadeIn(actor, scale=0.5, run_time=0.2),
            ApplyMethod(actor.move_to, rows.get_top() + UP * 0.35,
                        run_time=0.4),
        ))
        self.play(FadeOut(actor, scale=0.4),
                  rows.animate.set_fill(TEAL, 0.8), run_time=0.4)
        self.play(rows.animate.set_fill(SLATE, 0.5),
                  ring.animate.set_stroke(OK_GREEN, 2.5), run_time=0.4)
        self.wait(0.6)

        # ------ final: two different tools --------------------------------
        # The caption swaps too: holding "sometimes both" under a "two
        # different tools" title would leave two competing closing lines.
        closing = Text("two different tools", font=UI_FONT, font_size=24,
                       color=INK, weight=BOLD)
        dot_t = Dot(radius=0.06, color=TEAL)
        dot_a = Dot(radius=0.06, color=AMBER)
        lockup = VGroup(dot_t, closing, dot_a).arrange(RIGHT, buff=0.22)
        lockup.move_to(UP * 0.3)  # clear air below the role labels
        cap2 = make_caption("Two different tools. Sometimes both.")
        self.play(FadeOut(cap), run_time=0.2)
        self.play(FadeOut(rows), FadeOut(ring), FadeIn(lockup), FadeIn(cap2),
                  run_time=0.5)

        # ------------------------------------------------- final hold ----
        self.wait(2.6)
