"""Shared visual system for the MCP vs semantic layer explainer.

Colour meaning is strict: purple = AI (reasoning), teal = plain code that
executes, amber = knowledge (semantic model), grey = existing systems.
Red appears only when things break (scenes 6-8).
"""

from manim import *

# ---------------------------------------------------------------- palette ----
# Light theme (operator decision 2026-11-07): white background, sleek, modern.
BG = "#FBFBFD"
INK = "#16181D"          # primary text
MUTED = "#6B7280"        # secondary text
LIGHT_GREY = "#7D8594"   # AI client outline, secondary marks (mid grey on white)
PURPLE = "#6F4FC3"       # the LLM, reasoning
PURPLE_FILL = "#C7B5F0"  # context window fill
TEAL = "#0D9488"         # plain code: MCP server, tools, compiler
TEAL_DARK = "#0A6B62"    # compiler shade
AMBER = "#B45309"        # knowledge: the semantic model
GREY = "#8A9099"         # existing systems
PACKET_WHITE = "#16181D" # the travelling packet: near-black so it pops on white
ALERT_RED = "#DC4C64"
OK_GREEN = "#2F9E44"

CODE_FONT = "Menlo"
UI_FONT = "Avenir Next"   # modern geometric sans, ships with macOS
SLATE = "#4B5563"         # endpoint labels, readable on white at mobile size

config.background_color = BG

# 4:5 vertical master (1080x1350): LinkedIn's recommended vertical feed ratio,
# also Facebook's feed spec. Frame coords: x in [-3.2, 3.2], y in [-4, 4].
config.frame_height = 8.0
config.frame_width = 6.4


# ----------------------------------------------------------------- actors ----
def make_shadow(box):
    """Two stacked offset copies fake a soft drop shadow under a card."""
    s1 = box.copy().set_stroke(width=0).set_fill("#101828", opacity=0.10)
    s1.shift(0.045 * RIGHT + 0.065 * DOWN)
    s2 = box.copy().set_stroke(width=0).set_fill("#101828", opacity=0.05)
    s2.shift(0.09 * RIGHT + 0.13 * DOWN)
    return VGroup(s2, s1)


def _shell(width, height, color, label, label_size=26, title_color=None):
    """White elevated card: soft shadow, hairline or accent stroke, bold title."""
    box = RoundedRectangle(corner_radius=0.18, width=width, height=height)
    box.set_stroke(color, width=2.5).set_fill("#FFFFFF", opacity=1.0)
    shadow = make_shadow(box)
    tag = Text(label, font=UI_FONT, font_size=label_size,
               color=title_color or color, weight=BOLD)
    tag.next_to(box.get_top(), DOWN, buff=0.18)
    return shadow, box, tag


def make_background():
    """Soft vertical gradient page behind everything, so the white cards pop
    instead of sitting white-on-white."""
    r = Rectangle(width=8, height=10)
    r.set_stroke(width=0)
    r.set_fill(color=["#ECEFF5", "#F9FAFC", "#EAEDF4"], opacity=1.0)
    r.set_sheen_direction(DOWN)
    return r


def make_ai_client():
    """AI client shell with .llm (purple box), .ctx_outline and .ctx_fill.

    Sized for the stacked 4:5 layout: wide and short, LLM row on top,
    context window bar beneath it."""
    shadow, shell, title = _shell(5.6, 3.0, "#D8DCE3", "AI client",
                                  title_color=INK)

    # 3.1 x 1.05, raised: narrower and shorter than the first cut so the
    # token meter fits in the gap between the LLM box and the context bar
    # (operator note 2026-11-07).
    llm = RoundedRectangle(corner_radius=0.14, width=3.1, height=1.05)
    llm.set_stroke(PURPLE, 3).set_fill(PURPLE, opacity=0.07)
    llm.move_to(shell.get_center() + UP * 0.30)
    llm_label = Text("LLM", font=UI_FONT, font_size=18, color=PURPLE)
    llm_label.next_to(llm.get_top(), DOWN, buff=0.08)

    ctx_outline = Rectangle(width=4.6, height=0.42)
    ctx_outline.set_stroke(PURPLE, 2)
    ctx_outline.move_to(shell.get_center() + DOWN * 1.0)
    ctx_fill = Rectangle(width=0.001, height=0.32)
    ctx_fill.set_stroke(width=0).set_fill(PURPLE_FILL, 0.9)
    ctx_fill.move_to(ctx_outline.get_left() + RIGHT * 0.05)
    ctx_label = Text("context window", font=UI_FONT, font_size=15, color=MUTED)
    ctx_label.next_to(ctx_outline, DOWN, buff=0.08)

    g = VGroup(shadow, shell, title, llm, llm_label,
               ctx_outline, ctx_fill, ctx_label)
    g.shell, g.title = shell, title
    g.llm, g.llm_label = llm, llm_label
    g.ctx_outline, g.ctx_fill, g.ctx_label = ctx_outline, ctx_fill, ctx_label
    return g


def ctx_fill_target(client, frac):
    """A replacement context-window fill at the given fraction, left-aligned.

    Sizes derive from the outline as it currently is, so the target stays
    inside the bar even after the client card has been scaled."""
    pad = client.ctx_outline.width * 0.011
    inner_w = max((client.ctx_outline.width - 2 * pad) * min(frac, 1.0), 1e-3)
    r = Rectangle(width=inner_w, height=client.ctx_outline.height * 0.76)
    r.set_stroke(width=0).set_fill(PURPLE_FILL, 0.9)
    r.move_to(client.ctx_outline.get_left() + RIGHT * (pad + inner_w / 2))
    return r


def make_mcp_server():
    shadow, shell, title = _shell(5.6, 1.6, TEAL, "MCP server")
    g = VGroup(shadow, shell, title)
    g.shell, g.title = shell, title
    return g


def make_api_box():
    """'your APIs' card with .endpoints (VGroup of three labels)."""
    shadow, shell, title = _shell(5.6, 1.15, "#D8DCE3", "your APIs",
                                  title_color=INK, label_size=20)
    endpoints = VGroup(*[
        Text(t, font=CODE_FONT, font_size=14, color=SLATE)
        for t in ["GET /opportunities", "GET /accounts", "POST /deals"]
    ])
    endpoints.arrange(RIGHT, buff=0.32)
    if endpoints.width > 5.2:
        endpoints.scale_to_fit_width(5.2)
    endpoints.move_to(shell.get_center() + DOWN * 0.22)
    g = VGroup(shadow, shell, title, endpoints)
    g.shell, g.title, g.endpoints = shell, title, endpoints
    return g


# ------------------------------------------------------------- tool cards ----
def make_tool_card(name, desc, schema, width=2.7, height=0.95):
    card = RoundedRectangle(corner_radius=0.1, width=width, height=height)
    card.set_stroke(TEAL, 1.8).set_fill("#EFF9F7", opacity=1.0)
    rows = VGroup(
        Text(name, font=CODE_FONT, font_size=15, color=INK),
        Text(desc, font=UI_FONT, font_size=11, color=MUTED),
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


def make_big_tool_card(name, desc, schema, width=5.4, height=2.9):
    """Enlarged card with labelled rows, .rows exposes the three row groups."""
    card = RoundedRectangle(corner_radius=0.14, width=width, height=height)
    card.set_stroke(TEAL, 2.5).set_fill("#FFFFFF", opacity=1.0)
    shadow = make_shadow(card)

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
        row("description", desc, UI_FONT, 20, LIGHT_GREY),
        row("input schema", schema, CODE_FONT, 22, TEAL),
    )
    rows.arrange(DOWN, buff=0.24, aligned_edge=LEFT)
    rows.move_to(card.get_center())
    g = VGroup(shadow, card, rows)
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


def make_caption(text):
    """Caption placeholder: same geometry, rendered fully transparent.

    Captions are no longer drawn by the scenes. They are burned in at mux
    time from the narration's own word timings, so a caption can never
    drift against the voice and never drags a visual with it. The scenes
    still create and fade these placeholders so every play keeps its exact
    run_time; only the pixels are gone. The plate style lives on in
    caption_track.py, which must match this geometry.
    """
    t = Text(text, font=UI_FONT, font_size=25, color=INK)
    if t.width > 5.5:
        t.scale_to_fit_width(5.5)
    plate = RoundedRectangle(corner_radius=0.19,
                             width=t.width + 0.5, height=0.6)
    plate.set_stroke(width=0).set_fill("#FFFFFF", opacity=0.0)
    t.set_fill(opacity=0.0).set_stroke(width=0, opacity=0.0)
    t.move_to(plate.get_center())
    g = VGroup(plate, t)
    g.to_edge(DOWN, buff=0.18)
    return g


def make_title_strip(kicker, title, pill_color=TEAL):
    """Top header band for the vertical frame: accent kicker pill + title."""
    pill_text = Text(kicker, font=UI_FONT, font_size=15, color="#FFFFFF",
                     weight=BOLD)
    pill = RoundedRectangle(corner_radius=0.16,
                            width=pill_text.width + 0.42, height=0.36)
    pill.set_stroke(width=0).set_fill(pill_color, 1.0)
    pill_text.move_to(pill.get_center())
    head = Text(title, font=UI_FONT, font_size=24, color=INK, weight=BOLD)
    g = VGroup(VGroup(pill, pill_text), head).arrange(RIGHT, buff=0.22)
    if g.width > 5.9:
        g.scale_to_fit_width(5.9)
    g.to_edge(UP, buff=0.22)
    return g


def make_dot_grid():
    """Faint dot grid filling the page behind the cards, so no zone is dead."""
    dots = VGroup()
    x = -3.0
    while x <= 3.01:
        y = -3.9
        while y <= 3.91:
            dots.add(Dot([x, y, 0], radius=0.016, color="#C9CFD9")
                     .set_opacity(0.55))
            y += 0.55
        x += 0.55
    return dots


def make_bubble(text, width=None, font_size=17):
    """Speech bubble: white rounded card with a tail, for the user's question."""
    t = Text(text, font=UI_FONT, font_size=font_size, color=INK)
    w = width or (t.width + 0.6)
    if t.width > w - 0.5:
        t.scale_to_fit_width(w - 0.5)
    body = RoundedRectangle(corner_radius=0.22, width=w, height=t.height + 0.5)
    body.set_stroke("#D8DCE3", 2).set_fill("#FFFFFF", opacity=1.0)
    tail = Polygon([-0.14, 0, 0], [0.14, 0, 0], [0, -0.22, 0])
    tail.set_stroke("#D8DCE3", 2).set_fill("#FFFFFF", opacity=1.0)
    tail.move_to(body.get_bottom() + LEFT * (w / 2 - 0.55) + DOWN * 0.1)
    shadow = make_shadow(body)
    t.move_to(body.get_center())
    g = VGroup(shadow, tail, body, t)
    g.body, g.text = body, t
    return g


def make_chip(label, color, fill):
    """Big concept chip (scene 1): tinted rounded card with bold colored text."""
    t = Text(label, font=UI_FONT, font_size=30, color=color, weight=BOLD)
    card = RoundedRectangle(corner_radius=0.24,
                            width=t.width + 0.7, height=t.height + 0.55)
    card.set_stroke(color, 2.5).set_fill(fill, opacity=1.0)
    shadow = make_shadow(card)
    t.move_to(card.get_center())
    g = VGroup(shadow, card, t)
    g.card, g.text = card, t
    return g


def make_sem_zone(width=5.6, height=1.9):
    """The semantic layer zone: amber card that slides in between the MCP
    server and your systems. .shell and .title exposed like the other actors."""
    shadow, shell, title = _shell(width, height, AMBER, "semantic layer",
                                  label_size=22)
    g = VGroup(shadow, shell, title)
    g.shell, g.title = shell, title
    return g


def make_sem_card(width=1.15, height=0.7):
    """One amber file card of the semantic model: index-card look with a tab."""
    body = RoundedRectangle(corner_radius=0.07, width=width, height=height)
    body.set_stroke(AMBER, 1.8).set_fill("#FBF3E8", opacity=1.0)
    tab = RoundedRectangle(corner_radius=0.04, width=width * 0.38, height=0.14)
    tab.set_stroke(AMBER, 1.8).set_fill("#FBF3E8", opacity=1.0)
    tab.move_to(body.get_corner(UL) + RIGHT * (width * 0.19) + UP * 0.055)
    lines = VGroup(*[
        Line(ORIGIN, RIGHT * (width - 0.3)).set_stroke(AMBER, 1.2, opacity=0.5)
        for _ in range(2)
    ])
    lines.arrange(DOWN, buff=0.12)
    lines.move_to(body.get_center() + DOWN * 0.05)
    g = VGroup(tab, body, lines)
    g.body = body
    return g


def make_sem_stack(n=4, label=True):
    """A small stack of semantic-model file cards, slightly offset, with an
    optional label underneath. .cards and .label exposed."""
    cards = VGroup()
    for i in range(n):
        c = make_sem_card()
        c.shift(UP * 0.13 * i + RIGHT * 0.07 * i)
        cards.add(c)
    g = VGroup(cards)
    g.cards = cards
    g.label = None
    if label:
        tag = Text("semantic model", font=UI_FONT, font_size=14, color=AMBER)
        tag.next_to(cards, DOWN, buff=0.12)
        g.add(tag)
        g.label = tag
    return g


def make_object_card(name, fields, color=GREY, width=1.9):
    """A data-object card (Opportunity, Account): name header + field rows.
    .fields maps field name -> its Text mobject, for targeted highlights."""
    rows = VGroup(Text(name, font=UI_FONT, font_size=16, color=INK,
                       weight=BOLD))
    field_map = {}
    for f in fields:
        t = Text(f, font=CODE_FONT, font_size=12, color=SLATE)
        field_map[f] = t
        rows.add(t)
    rows.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    card = RoundedRectangle(corner_radius=0.1, width=width,
                            height=rows.height + 0.4)
    card.set_stroke(color, 1.8).set_fill("#FFFFFF", opacity=1.0)
    rows.move_to(card.get_center())
    g = VGroup(make_shadow(card), card, rows)
    g.card, g.fields, g.name_row = card, field_map, rows[0]
    return g


def make_compiler():
    """The compiler: darker teal box with a gear-like square symbol."""
    box = RoundedRectangle(corner_radius=0.1, width=1.5, height=0.78)
    box.set_stroke(TEAL_DARK, 2.2).set_fill("#E6F3F1", opacity=1.0)
    gear_outer = Square(0.26).set_stroke(TEAL_DARK, 2).rotate(PI / 4)
    gear_inner = Square(0.26).set_stroke(TEAL_DARK, 2)
    gear = VGroup(gear_outer, gear_inner)
    label = Text("compiler", font=UI_FONT, font_size=14, color=TEAL_DARK,
                 weight=BOLD)
    inner = VGroup(gear, label).arrange(RIGHT, buff=0.14)
    inner.move_to(box.get_center())
    g = VGroup(make_shadow(box), box, inner)
    g.box, g.gear = box, gear
    return g


def make_block(text, width=None):
    """A small teal building block the compiler assembles SQL from."""
    t = Text(text, font=CODE_FONT, font_size=11, color="#FFFFFF")
    w = width or (t.width + 0.3)
    if t.width > w - 0.2:
        t.scale_to_fit_width(w - 0.2)
    r = RoundedRectangle(corner_radius=0.06, width=w, height=0.3)
    r.set_stroke(width=0).set_fill(TEAL, 1.0)
    t.move_to(r.get_center())
    g = VGroup(r, t)
    g.box, g.text = r, t
    return g


def make_lock(scale=1.0):
    """A small padlock: body square plus shackle arc."""
    body = RoundedRectangle(corner_radius=0.04, width=0.26, height=0.2)
    body.set_stroke(INK, 2).set_fill("#FFFFFF", opacity=1.0)
    shackle = Arc(radius=0.085, start_angle=0, angle=PI)
    shackle.set_stroke(INK, 2)
    shackle.move_to(body.get_top() + UP * 0.045)
    g = VGroup(shackle, body).scale(scale)
    return g


def make_token_meter():
    """Top-right token counter; .num is the Integer to animate."""
    num = Integer(0, font_size=30, color=INK)
    unit = Text("tokens", font_size=16, color=MUTED)
    g = VGroup(num, unit).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    g.num, g.unit = num, unit
    g.to_corner(UR, buff=0.5)
    return g
