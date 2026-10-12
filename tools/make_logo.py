#!/usr/bin/env python3
"""Write the ENPM663 logos, light and dark, into docs/source/_static/images.

The design is the terminal window used by ENPM702 and ENPM818Z: a prompt,
"ENPM" and the course number in UMD red, then a gold block cursor. The
terminal() function is copied from fall2026/ENPM702/rtd/logo-options/
make_options.py, so the three course logos share glyphs, sizes and colors.
Colors from https://brand.umd.edu/visual-identity/colors.

All text is converted to outlines with fontTools, so the SVGs need no fonts.
Usage (from the repo root): /usr/bin/python3 tools/make_logo.py
"""
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

OUT = Path(__file__).resolve().parent.parent / "docs" / "source" / "_static" / "images"
FIRA = "/usr/share/texlive/texmf-dist/fonts/opentype/public/fira/"
RED, GOLD, BLACK, WHITE = "#e21833", "#ffd200", "#000000", "#ffffff"
DGRAY, MGRAY, LGRAY = "#454545", "#7f7f7f", "#e6e6e6"
CAP = 0.689  # Fira cap height, in em

TERM = {
    "dark":  dict(window=BLACK, edge=DGRAY, bar=DGRAY, prompt=MGRAY, enpm=WHITE, gold_edge="none"),
    "light": dict(window=WHITE, edge=MGRAY, bar=LGRAY, prompt=MGRAY, enpm=BLACK, gold_edge=BLACK),
}

_fonts = {}
def font(name):
    if name not in _fonts:
        f = TTFont(FIRA + name)
        _fonts[name] = (f, f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm)
    return _fonts[name]

def text_width(fname, text, size):
    f, gs, cmap, upm = font(fname)
    return sum(f["hmtx"][cmap[ord(c)]][0] for c in text) * size / upm

def text_path(fname, text, size, x, baseline):
    """SVG path data for a line of text, starting at x on the baseline."""
    f, gs, cmap, upm = font(fname)
    s = size / upm
    pen = SVGPathPen(gs)
    cur = x
    for c in text:
        g = cmap[ord(c)]
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cur, baseline)))
        cur += f["hmtx"][g][0] * s
    return pen.getCommands()

def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" '
            f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{label}">\n'
            f'<title>{label}</title>\n{body}\n</svg>\n')

def terminal(theme, number):
    """Terminal-window logo: "> ENPM" plus the course number, in red."""
    c = TERM[theme]
    fn = "FiraMono-Bold.otf"
    size = 54
    pad, bar = 26, 34
    char_w = text_width(fn, " ", size)
    # a third of a character after ">", not a full space
    prompt_w = text_width(fn, ">", size) + 0.35 * char_w
    w_enpm = text_width(fn, "ENPM", size)
    w_num = text_width(fn, number, size)
    cursor_w = text_width(fn, "_", size)
    W = pad + prompt_w + w_enpm + w_num + cursor_w * 1.2 + pad
    H = bar + pad + CAP * size + pad + 6
    base = bar + pad + CAP * size
    x = pad
    dp = text_path(fn, ">", size, x, base); x += prompt_w
    de = text_path(fn, "ENPM", size, x, base); x += w_enpm
    dn = text_path(fn, number, size, x, base); x += w_num
    gold_stroke = "" if c["gold_edge"] == "none" else f' stroke="{c["gold_edge"]}" stroke-width="1.5"'
    body = [
        f'<rect x="1" y="1" width="{W-2:.1f}" height="{H-2:.1f}" rx="14" fill="{c["window"]}" stroke="{c["edge"]}" stroke-width="2"/>',
        f'<path d="M1,{bar} H{W-1:.1f}" stroke="{c["bar"]}" stroke-width="2"/>',
        f'<circle cx="22" cy="{bar/2+0.5}" r="7" fill="{RED}"/>',
        f'<circle cx="44" cy="{bar/2+0.5}" r="7" fill="{GOLD}"{gold_stroke}/>',
        f'<circle cx="66" cy="{bar/2+0.5}" r="7" fill="{MGRAY}"/>',
        f'<path d="{dp}" fill="{c["prompt"]}"/>',
        f'<path d="{de}" fill="{c["enpm"]}"/>',
        f'<path d="{dn}" fill="{RED}"/>',
        # block cursor, one character cell, cap height tall
        f'<rect x="{x + cursor_w*0.15:.1f}" y="{base - CAP*size:.1f}" width="{cursor_w*0.7:.1f}" height="{CAP*size:.1f}" fill="{GOLD}"{gold_stroke}/>',
    ]
    out = OUT / f"enpm{number.lower()}_logo_{theme}.svg"
    out.write_text(svg(W, H, "\n".join(body), "ENPM" + number))
    print("wrote", out.relative_to(OUT.parent.parent.parent.parent))

if __name__ == "__main__":
    for theme in ("dark", "light"):
        terminal(theme, "663")
