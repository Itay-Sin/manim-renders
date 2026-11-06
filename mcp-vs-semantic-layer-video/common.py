"""Shared visual system for the MCP vs semantic layer explainer.

Colour meaning is strict: purple = AI (reasoning), teal = plain code that
executes, amber = knowledge (semantic model), grey = existing systems.
Red appears only when things break (scenes 6-8).
"""

from manim import *

# ---------------------------------------------------------------- palette ----
BG = "#111318"
INK = "#E8EAF0"          # primary text
MUTED = "#8A91A0"        # secondary text
LIGHT_GREY = "#C7CBD4"   # AI client outline
PURPLE = "#A78BDA"       # the LLM, reasoning
PURPLE_FILL = "#C9B6EE"  # context window fill
TEAL = "#4FD1C5"         # plain code: MCP server, tools, compiler
TEAL_DARK = "#2C8C82"    # compiler shade
AMBER = "#E0AF68"        # knowledge: the semantic model
GREY = "#9AA0A6"         # existing systems
PACKET_WHITE = "#F5F6F8"
ALERT_RED = "#F7768E"
OK_GREEN = "#9ECE6A"

CODE_FONT = "Menlo"

config.background_color = BG


# ----------------------------------------------------------------- actors ----
def _shell(width, height, color, label, label_size=24):
    box = RoundedRectangle(corner_radius=0.18, width=width, height=height)
    box.set_stroke(color, width=2.5)
    tag = Text(label, font_size=label_size, color=color)
    tag.next_to(box.get_top(), DOWN, buff=0.16)
    return box, tag


def make_ai_client():
    """AI client shell with .llm (purple box), .ctx_outline and .ctx_fill."""
    shell, title = _shell(4.6, 5.0, LIGHT_GREY, "AI client")

    llm = RoundedRectangle(corner_radius=0.14, width=2.9, height=2.1)
    llm.set_stroke(PURPLE, 3).set_fill(PURPLE, opacity=0.07)
    llm.move_to(shell.get_center() + UP * 0.75)
    llm_label = Text("LLM", font_size=24, color=PURPLE)
    llm_label.next_to(llm.get_top(), DOWN, buff=0.12)

    ctx_outline = Rectangle(width=3.6, height=0.42)
    ctx_outline.set_stroke(PURPLE, 2)
    ctx_outline.move_to(shell.get_center() + DOWN * 1.15)
    ctx_fill = Rectangle(width=0.001, height=0.32)
    ctx_fill.set_stroke(width=0).set_fill(PURPLE_FILL, 0.9)
    ctx_fill.move_to(ctx_outline.get_left() + RIGHT * 0.05)
    ctx_label = Text("context window", font_size=15, color=MUTED)
    ctx_label.next_to(ctx_outline, DOWN, buff=0.1)

    g = VGroup(shell, title, llm, llm_label, ctx_outline, ctx_fill, ctx_label)
    g.shell, g.title = shell, title
    g.llm, g.llm_label = llm, llm_label
    g.ctx_outline, g.ctx_fill, g.ctx_label = ctx_outline, ctx_fill, ctx_label
    return g


def ctx_fill_target(client, frac):
    """A replacement context-window fill at the given fraction, left-aligned."""
    inner_w = max((client.ctx_outline.width - 0.1) * min(frac, 1.0), 1e-3)
    r = Rectangle(width=inner_w, height=0.32)
    r.set_stroke(width=0).set_fill(PURPLE_FILL, 0.9)
    r.move_to(client.ctx_outline.get_left() + RIGHT * (0.05 + inner_w / 2))
    return r


def make_mcp_server():
    shell, title = _shell(3.3, 5.0, TEAL, "MCP server")
    g = VGroup(shell, title)
    g.shell, g.title = shell, title
    return g


def make_api_box():
    """Grey 'your APIs' box with .endpoints (VGroup of three labels)."""
    shell, title = _shell(3.2, 2.8, GREY, "your APIs")
    endpoints = VGroup(*[
        Text(t, font=CODE_FONT, font_size=15, color=LIGHT_GREY)
        for t in ["GET /opportunities", "GET /accounts", "POST /deals"]
    ])
    endpoints.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    endpoints.move_to(shell.get_center() + DOWN * 0.25)
    g = VGroup(shell, title, endpoints)
    g.shell, g.title, g.endpoints = shell, title, endpoints
    return g


# ------------------------------------------------------------- tool cards ----
def make_tool_card(name, desc, schema, width=2.7, height=0.95):
    card = RoundedRectangle(corner_radius=0.1, width=width, height=height)
    card.set_stroke(TEAL, 1.8).set_fill("#152220", opacity=1.0)
    rows = VGroup(
        Text(name, font=CODE_FONT, font_size=15, color=INK),
        Text(desc, font_size=11, color=MUTED),
        Text(schema, font=CODE_FONT, font_size=11, color=TEAL),
    )
    for t in rows:
        if t.width > width - 0.3:
            t.scale_to_fit_width(width - 0.3)
    rows.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    rows.move_to(card.get_center())
    g = VGroup(card, rows)
    g.card, g.rows = card, rows
    return g


def make_big_tool_card(name, desc, schema, width=6.4, height=3.0):
    """Enlarged card with labelled rows, .rows exposes the three row groups."""
    card = RoundedRectangle(corner_radius=0.14, width=width, height=height)
    card.set_stroke(TEAL, 2.5).set_fill("#152220", opacity=1.0)

    def row(label, value, value_font, value_size, value_color):
        lab = Text(label, font_size=15, color=MUTED)
        val = Text(value, font=value_font or "", font_size=value_size,
                   color=value_color)
        if val.width > width - 0.8:
            val.scale_to_fit_width(width - 0.8)
        r = VGroup(lab, val).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        return r

    rows = VGroup(
        row("name", name, CODE_FONT, 26, INK),
        row("description", desc, None, 20, LIGHT_GREY),
        row("input schema", schema, CODE_FONT, 22, TEAL),
    )
    rows.arrange(DOWN, buff=0.24, aligned_edge=LEFT)
    rows.move_to(card.get_center())
    g = VGroup(card, rows)
    g.card, g.rows = card, rows
    return g


# ------------------------------------------------------- packets and data ----
def make_packet(width=0.55):
    p = RoundedRectangle(corner_radius=0.11, width=width, height=0.24)
    p.set_stroke(width=0).set_fill(PACKET_WHITE, 1.0)
    return p


def make_data_rows(n=3, width=1.4):
    bars = VGroup(*[
        Rectangle(width=width - 0.15 * i, height=0.09)
        .set_stroke(width=0).set_fill(LIGHT_GREY, 0.85)
        for i in range(n)
    ])
    bars.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    return bars


def make_token_meter():
    """Top-right token counter; .num is the Integer to animate."""
    num = Integer(0, font_size=30, color=INK)
    unit = Text("tokens", font_size=16, color=MUTED)
    g = VGroup(num, unit).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    g.num, g.unit = num, unit
    g.to_corner(UR, buff=0.5)
    return g
