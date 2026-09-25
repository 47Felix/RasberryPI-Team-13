#!/usr/bin/env python3
"""Build the Ice Truck Team 13 deck as a real .pptx (python-pptx, no node/soffice available)."""
import re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from pptx.enum.text import MSO_AUTO_SIZE

EMU_IN = 914400

# ---------- palette ----------
PEOPLE = {
    "team":  dict(p="1C6E8C", dark="124A5E", light="EAF4F7"),
    "anton": dict(p="C2650A", dark="7A4308", light="FDF1E3"),
    "felix": dict(p="1F8A4C", dark="145C33", light="E8F7EE"),
    "dogan": dict(p="9333C9", dark="5B1F86", light="F5ECFC"),
    "erik":  dict(p="2F6FB0", dark="1F4E7D", light="EAF2FA"),
}
FG = "1C1F22"
MUTED = "6B6F73"
CODE_BG = "F4F7F8"
WHITE = "FFFFFF"
HILITE_BG = "FFE066"
HILITE_FG = "5C4400"
BODY_FONT = "Calibri"
HEAD_FONT = "Century Schoolbook"

prs = Presentation()
prs.slide_width = Emu(13.333 * EMU_IN)
prs.slide_height = Emu(7.5 * EMU_IN)
BLANK = prs.slide_layouts[6]

def rgb(hexstr):
    return RGBColor.from_string(hexstr)

def add_slide():
    return prs.slides.add_slide(BLANK)

def set_bg(slide, hexcolor):
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = rgb(hexcolor)

def add_rect(slide, x, y, w, h, fill=None, line=None, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=None):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.shadow.inherit = False
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = rgb(fill)
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = rgb(line)
        sp.line.width = Pt(line_w)
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE and radius is not None:
        try:
            sp.adjustments[0] = radius
        except Exception:
            pass
    return sp

def add_oval(slide, x, y, w, h, fill, line=None, line_w=1.0):
    sp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.shadow.inherit = False
    sp.fill.solid()
    sp.fill.fore_color.rgb = rgb(fill)
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = rgb(line)
        sp.line.width = Pt(line_w)
    return sp

def add_line(slide, x1, y1, x2, y2, color, width_pt=1.5, dash=None):
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    conn.line.color.rgb = rgb(color)
    conn.line.width = Pt(width_pt)
    if dash:
        ln = conn.line._get_or_add_ln()
        d = ln.makeelement(qn('a:prstDash'), {'val': dash})
        ln.append(d)
    return conn

def set_bullet_char(paragraph, color_hex, char="●", indent=0.22):
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set('marL', str(int(indent * EMU_IN)))
    pPr.set('indent', str(-int(indent * EMU_IN)))
    buClr = pPr.makeelement(qn('a:buClr'), {})
    srgb = buClr.makeelement(qn('a:srgbClr'), {'val': color_hex})
    buClr.append(srgb)
    pPr.append(buClr)
    buFont = pPr.makeelement(qn('a:buFont'), {'typeface': 'Arial'})
    pPr.append(buFont)
    buChar = pPr.makeelement(qn('a:buChar'), {'char': char})
    pPr.append(buChar)

def no_bullet(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set('marL', '0')
    pPr.set('indent', '0')
    pPr.append(pPr.makeelement(qn('a:buNone'), {}))

INLINE_RE = re.compile(r'(\*\*.*?\*\*|`[^`]*?`)')

def add_runs(paragraph, text, size=14, color=FG, code_color="124A5E", font=BODY_FONT):
    for part in INLINE_RE.split(text):
        if not part:
            continue
        run = paragraph.add_run()
        if part.startswith('**') and part.endswith('**'):
            run.text = part[2:-2]
            run.font.bold = True
            run.font.color.rgb = rgb(color)
            run.font.name = font
        elif part.startswith('`') and part.endswith('`'):
            run.text = part[1:-1]
            run.font.name = "Consolas"
            run.font.color.rgb = rgb(code_color)
        else:
            run.text = part
            run.font.color.rgb = rgb(color)
            run.font.name = font
        run.font.size = Pt(size)

def add_text(slide, x, y, w, h, text, size=14, color=FG, bold=False, italic=False,
             align=PP_ALIGN.LEFT, font=BODY_FONT, anchor=MSO_ANCHOR.TOP, wrap=True,
             line_spacing=None, shrink=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    if shrink:
        tf.auto_size = MSO_AUTO_SIZE.NONE
    lines = text.split('\n')
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line_spacing:
            p.line_spacing = line_spacing
        no_bullet(p)
        add_runs(p, line, size=size, color=color, font=font)
        if bold:
            for r in p.runs:
                r.font.bold = True
        if italic:
            for r in p.runs:
                r.font.italic = True
    return tb

def add_bullets(slide, x, y, w, h, items, size=14, color=FG, bullet_color=None,
                 line_spacing=1.12, space_after=8, sub_size_ratio=0.86):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    first = True
    for item in items:
        if isinstance(item, tuple):
            txt, level = item
        else:
            txt, level = item, 0
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        this_size = size if level == 0 else round(size * sub_size_ratio)
        indent = 0.22 if level == 0 else 0.5
        char = "●" if level == 0 else "–"
        set_bullet_char(p, bullet_color or MUTED, char=char, indent=indent)
        add_runs(p, txt, size=this_size, color=color)
    return tb

def icon_circle(slide, cx, cy, r, person, on_dark=False):
    """Small truck+snowflake icon inside a colored circle — the deck's repeated motif."""
    col = PEOPLE[person]
    circle_fill = WHITE if not on_dark else col["dark"]
    add_oval(slide, cx - r, cy - r, 2 * r, 2 * r, fill=circle_fill)
    ic = col["p"] if not on_dark else WHITE
    s = r * 0.62
    ox, oy = cx - s, cy - s * 0.55
    add_rect(slide, ox, oy, s * 0.62, s * 0.62, fill=None, line=ic, line_w=1.6,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.25)
    add_rect(slide, ox + s * 0.62, oy + s * 0.18, s * 0.38, s * 0.42, fill=None, line=ic, line_w=1.6,
              shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.3)
    wr = s * 0.13
    add_oval(slide, ox + s * 0.14 - wr, oy + s * 0.62 + s * 0.28 - wr, 2 * wr, 2 * wr, fill=circle_fill, line=ic, line_w=1.6)
    add_oval(slide, ox + s * 0.88 - wr, oy + s * 0.62 + s * 0.28 - wr, 2 * wr, 2 * wr, fill=circle_fill, line=ic, line_w=1.6)

def chip(slide, x, y, text, person, align_right_edge=None):
    col = PEOPLE[person]
    w = 0.35 + 0.115 * len(text)
    xx = align_right_edge - w if align_right_edge else x
    sp = add_rect(slide, xx, y, w, 0.34, fill=col["light"], line=col["p"], line_w=1.0,
                  shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    tf = sp.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.06); tf.margin_right = Inches(0.06)
    tf.margin_top = 0; tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = rgb(col["dark"]); r.font.name = BODY_FONT
    return w

def demo_badge(slide, x, y):
    w, h = 1.55, 0.34
    sp = add_rect(slide, x, y, w, h, fill=HILITE_BG, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    tf = sp.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.08); tf.margin_right = Inches(0.08)
    tf.margin_top = 0; tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "\U0001F449 Live-Demo"
    r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = rgb(HILITE_FG); r.font.name = BODY_FONT
    return h

def page_number(slide, n, total, person):
    add_text(slide, 12.0, 7.08, 1.1, 0.3, f"{n:02d} / {total}", size=11, color=PEOPLE[person]["p"],
              align=PP_ALIGN.RIGHT, bold=True)

def code_block(slide, x, y, w, h, code_text, person):
    col = PEOPLE[person]
    add_rect(slide, x, y, w, h, fill=CODE_BG, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    tb = slide.shapes.add_textbox(Inches(x + 0.3), Inches(y + 0.12), Inches(w - 0.5), Inches(h - 0.24))
    tf = tb.text_frame
    tf.word_wrap = False
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    for i, line in enumerate(code_text.split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        no_bullet(p)
        r = p.add_run(); r.text = line
        r.font.name = "Consolas"; r.font.size = Pt(12.5); r.font.color.rgb = rgb(FG)

def simple_table(slide, x, y, w, rows, col_widths, person, row_h=0.5, header=True, font_size=12):
    col = PEOPLE[person]
    n_rows = len(rows)
    h = row_h * n_rows
    gtbl = slide.shapes.add_table(n_rows, len(col_widths), Inches(x), Inches(y), Inches(w), Inches(h))
    table = gtbl.table
    for ci, cw in enumerate(col_widths):
        table.columns[ci].width = Inches(cw)
    for ri, row in enumerate(rows):
        table.rows[ri].height = Inches(row_h)
        for ci, val in enumerate(row):
            cell = table.cell(ri, ci)
            cell.margin_left = Inches(0.1); cell.margin_right = Inches(0.1)
            cell.margin_top = Inches(0.04); cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            no_bullet(p)
            is_header = header and ri == 0
            add_runs(p, val, size=font_size, color=col["dark"] if is_header else FG)
            if is_header:
                for r in p.runs:
                    r.font.bold = True
            if is_header:
                cell.fill.solid(); cell.fill.fore_color.rgb = rgb(col["light"])
            else:
                cell.fill.solid(); cell.fill.fore_color.rgb = rgb(WHITE)
    return gtbl

# ================= slide builders =================
TOTAL = 29

def lead_slide(n, person, title, subtitle, icon=True, extra=None, eyebrow=None):
    col = PEOPLE[person]
    s = add_slide()
    set_bg(s, col["light"])
    if icon:
        icon_circle(s, 6.667, 2.35, 0.55, person)
    if eyebrow:
        add_text(s, 0, 3.15, 13.333, 0.4, eyebrow, size=15, color=col["p"], bold=True,
                 align=PP_ALIGN.CENTER, font=HEAD_FONT, italic=True)
    add_text(s, 1.2, 3.55, 10.933, 1.1, title, size=34, color=FG, bold=True,
             align=PP_ALIGN.CENTER, font=HEAD_FONT)
    add_text(s, 1.2, 4.55, 10.933, 0.6, subtitle, size=20, color=col["p"], bold=True,
             align=PP_ALIGN.CENTER, font=HEAD_FONT, italic=True)
    if extra:
        add_text(s, 1.2, 5.25, 10.933, 0.5, extra, size=13, color=MUTED, align=PP_ALIGN.CENTER)
    page_number(s, n, TOTAL, person)
    return s

def content_header(s, person, n, chip_text, eyebrow, title):
    col = PEOPLE[person]
    icon_circle(s, 0.75, 0.72, 0.32, person)
    if chip_text:
        chip(s, 0, 0.42, chip_text, person, align_right_edge=12.75)
    if eyebrow:
        add_text(s, 1.25, 0.42, 10.5, 0.32, eyebrow, size=12, color=col["p"], bold=True, italic=True, font=HEAD_FONT)
    add_text(s, 1.25, 0.72, 10.9, 0.7, title, size=28, color=FG, bold=True, font=HEAD_FONT)
    page_number(s, n, TOTAL, person)
    return 1.62  # y where body content should start

def content_slide(n, person, chip_text, eyebrow, title, bullets=None, badge=False, note=None,
                   table=None, code=None, table_widths=None, table_caption=None):
    s = add_slide()
    set_bg(s, WHITE)
    body_y = content_header(s, person, n, chip_text, eyebrow, title)
    y = body_y + 0.12
    if badge:
        h = demo_badge(s, 0.75, y)
        y += h + 0.14
    if table:
        if table_caption:
            add_text(s, 0.75, y, 11.8, 0.35, table_caption, size=13, color=FG)
            y += 0.4
        simple_table(s, 0.75, y, 11.8, table, table_widths, person, row_h=0.55)
        y += 0.55 * len(table) + 0.2
    if code:
        code_text, code_h = code
        code_block(s, 0.75, y, 11.8, code_h, code_text, person)
        y += code_h + 0.2
    if bullets:
        add_bullets(s, 0.75, y, 11.8, 6.7 - y, bullets, size=15, bullet_color=PEOPLE[person]["p"])
    if note:
        add_text(s, 0.75, 6.55, 11.8, 0.5, note, size=13, color=MUTED, italic=True)
    return s

def diagram_box(slide, x, y, w, h, title, lines, person, filled=False):
    col = PEOPLE[person]
    if filled:
        add_rect(slide, x, y, w, h, fill=col["p"], line=None, radius=0.12)
        title_color, body_color = WHITE, col["light"]
    else:
        add_rect(slide, x, y, w, h, fill=col["light"], line=col["p"], line_w=1.25, radius=0.12)
        title_color, body_color = col["dark"], "333333"
    add_text(slide, x + 0.18, y + 0.1, w - 0.36, 0.3, title, size=13, color=title_color, bold=True)
    if lines:
        add_text(slide, x + 0.18, y + 0.42, w - 0.36, h - 0.5, "\n".join(lines), size=10.5, color=body_color,
                  line_spacing=1.15)

def diagram_arrow_h(slide, x1, x2, y, color, label=None):
    add_line(slide, x1, y, x2, y, color, width_pt=1.75)
    add_text(slide, x1, y - 0.32, x2 - x1, 0.26, "▶", size=11, color=color, align=PP_ALIGN.RIGHT)
    if label:
        add_text(slide, x1, y - 0.32, x2 - x1, 0.26, label, size=10, color=color, align=PP_ALIGN.CENTER, bold=True)

def diagram_arrow_v(slide, x, y1, y2, color, label=None, label_side="right"):
    add_line(slide, x, y1, x, y2, color, width_pt=1.75)
    add_text(slide, x - 0.12, y2 - 0.2, 0.24, 0.2, "▼", size=10, color=color, align=PP_ALIGN.CENTER)
    if label:
        lx = x + 0.15 if label_side == "right" else x - 3.0
        add_text(slide, lx, (y1 + y2) / 2 - 0.13, 2.85, 0.26, label, size=10, color=color,
                  align=PP_ALIGN.LEFT if label_side == "right" else PP_ALIGN.RIGHT)

print("helpers ready")
