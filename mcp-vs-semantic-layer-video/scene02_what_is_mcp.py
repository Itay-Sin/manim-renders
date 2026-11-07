"""Scene 2: what MCP is. ~12 s of motion plus a 1 s hold.

The USB-C idea: one MCP server with one port, many AI clients plugging into
the same socket, one by one. Ends on the one-client base layout.

Narration:
  0-5    "MCP, the Model Context Protocol, is like a USB-C port for AI."
  5-12   "You build one MCP server for your product, and any compatible AI
          client, like Claude or ChatGPT, can connect to it."
"""

from manim import *
from common import (
    make_background, make_dot_grid, make_caption, make_title_strip,
    make_shadow,
    BG, INK, MUTED, PURPLE, TEAL, GREY, UI_FONT,
)


def small_client(label):
    box = RoundedRectangle(corner_radius=0.14, width=1.72, height=0.92)
    box.set_stroke("#D8DCE3", 2).set_fill("#FFFFFF", opacity=1.0)
    t = Text(label, font=UI_FONT, font_size=15, color=INK)
    if t.width > 1.5:
        t.scale_to_fit_width(1.5)
    t.move_to(box.get_center())
    g = VGroup(make_shadow(box), box, t)
    g.box, g.label = box, t
    return g


class Scene02WhatIsMCP(Scene):
    def construct(self):
        bg = make_background()
        grid = make_dot_grid()
        strip = make_title_strip("MCP", "One port, any client")
        self.add(bg, grid)

        # The MCP server, lower middle, with a USB-C-like socket on top.
        shell = RoundedRectangle(corner_radius=0.18, width=5.6, height=1.7)
        shell.set_stroke(TEAL, 2.5).set_fill("#FFFFFF", opacity=1.0)
        shell.move_to(DOWN * 1.6)
        server_title = Text("MCP server", font=UI_FONT, font_size=26,
                            color=TEAL, weight=BOLD)
        server_title.move_to(shell.get_center() + DOWN * 0.3)
        port = RoundedRectangle(corner_radius=0.07, width=0.78, height=0.18)
        port.set_stroke(TEAL, 2.5).set_fill("#EFF9F7", opacity=1.0)
        port.move_to(shell.get_top())
        server = VGroup(make_shadow(shell), shell, server_title, port)

        cap = make_caption("MCP is like a USB-C port for AI.")
        self.play(FadeIn(strip), FadeIn(server), FadeIn(cap), run_time=0.8)

        # On "USB-C port", the socket pulses once.
        self.play(Indicate(port, color=TEAL, scale_factor=1.35), run_time=0.9)
        # Holds are sized so the scene runs just past its 12.6 s narration.
        self.wait(1.4)

        # Three AI clients appear in a row above.
        clients = VGroup(small_client("Claude"),
                         small_client("ChatGPT"),
                         small_client("any AI client"))
        clients.arrange(RIGHT, buff=0.35)
        clients.move_to(UP * 1.9)

        cap2 = make_caption("One server. Any compatible AI client connects.")
        self.play(FadeOut(cap), run_time=0.2)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in clients],
                              lag_ratio=0.25),
                  FadeIn(cap2), run_time=1.1)
        cap = cap2

        # Each client extends a cable into the same port, with a click flash.
        plug_point = port.get_top() + UP * 0.02
        cables = VGroup()
        for c in clients:
            start = c.box.get_bottom()
            ctrl1 = start + DOWN * 1.2
            ctrl2 = plug_point + UP * 1.2
            cable = CubicBezier(start, ctrl1, ctrl2, plug_point)
            cable.set_stroke(GREY, 2.6, opacity=0.85)
            cables.add(cable)
            self.play(Create(cable), run_time=0.75)
            self.play(Flash(port, color=TEAL, line_length=0.14, num_lines=8),
                      run_time=0.3)

        self.wait(1.5)

        # Two clients leave; one stays: the base layout for the next scenes.
        keeper = clients[2]
        self.play(
            FadeOut(clients[0]), FadeOut(clients[1]),
            FadeOut(cables[0]), FadeOut(cables[1]),
            run_time=0.7,
        )
        # The curved cable straightens into the vertical wire of the base
        # layout as the remaining client takes centre stage.
        wire = Line([0, 1.9, 0] + DOWN * 0.62, port.get_top())
        wire.set_stroke(GREY, 2.2, opacity=0.75)
        self.play(keeper.animate.scale(1.35).move_to(UP * 1.9),
                  ReplacementTransform(cables[2], wire), run_time=0.8)

        # ------------------------------------------------- final hold ----
        self.wait(2.2)
