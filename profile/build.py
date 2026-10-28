"""Generates the SVGs used by the profile README.

Text is shaped with HarfBuzz and written out as vector glyphs, so the images
look identical everywhere and never depend on a web font loading.

    pip install uharfbuzz fonttools brotli
    npm i @fontsource/schibsted-grotesk @fontsource/martian-mono
    FONT_DIR=./node_modules/@fontsource python3 profile/build.py

Edit the CONTENT section below, rerun, commit the SVGs.
"""

import io
import os
from xml.sax.saxutils import escape

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get("FONT_DIR", "node_modules/@fontsource")

# ---------------------------------------------------------------- palette --

THEMES = {
    "dark": dict(
        ink="#E6EDF3", ink2="#A2ACB8", ink3="#7D8590", rule="#30363D",
        eng="#B392F0", sec="#E3B341", biz="#4FD1C0",
    ),
    "light": dict(
        ink="#1F2328", ink2="#4B5560", ink3="#656D76", rule="#D0D7DE",
        eng="#7A4CC2", sec="#9A6700", biz="#0B7A6E",
    ),
}

INSET = 6  # every image keeps 6 units of air on the sides so edges line up in the grid
LANE_NAME = {"eng": "engineering", "sec": "security", "biz": "business"}

# ------------------------------------------------------------------ fonts --


class Font:
    def __init__(self, path, key):
        tt = TTFont(path)
        tt.flavor = None
        buf = io.BytesIO()
        tt.save(buf)
        data = buf.getvalue()
        self.key = key
        self.tt = TTFont(io.BytesIO(data))
        self.upem = self.tt["head"].unitsPerEm
        self.glyphset = self.tt.getGlyphSet()
        face = hb.Face(data)
        self.hb = hb.Font(face)
        self.hb.scale = (self.upem, self.upem)
        self.order = self.tt.getGlyphOrder()

    def shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": False, "calt": False})
        out, x = [], 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((self.order[info.codepoint], x + pos.x_offset, pos.y_offset))
            x += pos.x_advance
        return out, x

    def width(self, text, size, track=0):
        _, adv = self.shape(text)
        return adv * size / self.upem + track * size * max(len(text) - 1, 0)

    def glyph_path(self, name):
        pen = SVGPathPen(self.glyphset, lambda v: str(int(round(v))))
        self.glyphset[name].draw(pen)
        return pen.getCommands()


class Doc:
    """Collects glyph definitions so every glyph is stored once per SVG."""

    def __init__(self):
        self.defs = {}

    def text(self, font, s, x, y, size, fill, track=0, cls=None, anchor="start"):
        glyphs, adv = font.shape(s)
        tr = track * font.upem
        total = adv + tr * max(len(glyphs) - 1, 0)
        if anchor == "end":
            x -= total * size / font.upem
        sc = size / font.upem
        uses = []
        for i, (name, gx, gy) in enumerate(glyphs):
            gid = f"{font.key}-{name}".replace(".", "_")
            if gid not in self.defs:
                d = font.glyph_path(name)
                self.defs[gid] = d
            if not self.defs[gid]:
                continue  # spaces
            px = int(round(gx + tr * i))
            uses.append(f'<use href="#{gid}" x="{px}" y="{-gy}"/>' if gy else f'<use href="#{gid}" x="{px}"/>')
        c = f' class="{cls}"' if cls else ""
        return (f'<g{c} fill="{fill}" transform="translate({x:.1f} {y:.1f}) '
                f'scale({sc:.5f} {-sc:.5f})">{"".join(uses)}</g>')

    def defs_svg(self):
        return "".join(f'<path id="{k}" d="{v}"/>' for k, v in self.defs.items() if v)


def wrap(font, s, size, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.width(t, size) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def svg(w, h, doc, body, title, style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
        f"<defs>{doc.defs_svg()}</defs>"
        + (f"<style>{style}</style>" if style else "")
        + body + "</svg>"
    )


def load_fonts():
    sg = os.path.join(FONT_DIR, "schibsted-grotesk", "files", "schibsted-grotesk-latin-{}-normal.woff2")
    mm = os.path.join(FONT_DIR, "martian-mono", "files", "martian-mono-latin-{}-normal.woff2")
    return dict(
        regular=Font(sg.format(400), "r"),
        medium=Font(sg.format(500), "m"),
        semibold=Font(sg.format(600), "s"),
        bold=Font(sg.format(700), "b"),
        black=Font(sg.format(800), "k"),
        mono=Font(mm.format(400), "c"),
    )


# ---------------------------------------------------------------- content --

NAME = "Atharva Karekar"
TAGLINE = ("Computer engineer, then about two years as a security analyst for major "
           "banking clients. Now in business school at SDA Bocconi Asia Center, still "
           "building the tools my teams run on.")

# Newest first, like git log. Lane decides the colour.
COMMITS = [
    dict(lane="biz", refs="HEAD -> business",
         title="IMB 9 at SDA Bocconi Asia Center, Mumbai",
         body=["Placement Coordinator for strategy and operations on the placement committee",
               "Lean Six Sigma Green Belt, Grant Thornton Bharat",
               "Case competitions and live consulting projects alongside the coursework"]),
    dict(lane="sec", refs="security",
         title="Security Analyst at ARCON",
         body=["About two years working with major banking clients"]),
    dict(lane="eng", refs="engineering",
         title="B.E. Computer Engineering, Honors in AI/ML",
         body=["A. P. Shah Institute of Technology",
               "Smart India Hackathon national winner; two papers on IEEE Xplore",
               "President of the Deep Learning Cell; Head Mentor at Hackwave",
               "Data Analyst intern at Archytas Innovation Labs"]),
]

FEATURED = dict(
    file="card-placement", lane="biz",
    title="Placement Committee System",
    desc=("A full-stack operations portal for the IMB 9 placement committee: a workspace "
          "for each wing, cross-wing requests, event approvals with email alerts, Excel "
          "import and export, and a log of who changed what. It replaced the separate "
          "Excel trackers the wings used to keep."),
    tags="Node.js, Express, MySQL, plain HTML and JavaScript",
    action="See the code",
)

CARDS = [
    dict(file="card-deadline-dash", lane="biz",
         title="Deadline Dash",
         desc=("A 45-second consulting survival game for our Consulting Day stall. Catch the "
               "chai, dodge the quick calls, climb from Chai Runner to Global Managing Partner."),
         tags="JavaScript, HTML canvas", action="Play the game"),
    dict(file="card-openvpn", lane="sec",
         title="OpenVPN crypto library audit",
         desc=("Smart India Hackathon 2023 with Team BitHeads. Static and dynamic analysis of "
               "the crypto libraries OpenVPN uses for IPsec over IPv6, looking for unknown "
               "vulnerabilities."),
         tags="Snyk, static and dynamic analysis", action="Read the write-up"),
    dict(file="card-freq", lane="eng",
         title="FreQ",
         desc=("Upload past exam papers as PDFs, Word files or scans. FreQ groups repeated "
               "questions using sentence embeddings and ranks them by how often they appear."),
         tags="Python, Flask, Sentence Transformers, OCR", action="See the code"),
    dict(file="card-marketing", lane="eng",
         title="Marketing mix and attribution",
         desc=("Regression and attribution modelling on customer touchpoint data to see which "
               "marketing channels actually earn their ROI, plus launch and seasonal analysis."),
         tags="Python, pandas, statsmodels, scikit-learn", action="See the code"),
]

TOOLKIT = [
    ("eng", ["Python and JavaScript", "Node.js, Express and MySQL", "React, Flask and Streamlit",
             "pandas, NLTK and Transformers", "Jupyter for analysis"]),
    ("sec", ["Static and dynamic code analysis", "Vulnerability scanning with Snyk",
             "Banking client environments", "Crypto library research"]),
    ("biz", ["Lean Six Sigma Green Belt", "Financial modelling and valuation",
             "Go-to-market strategy", "Case interviews and competitions",
             "Excel trackers and dashboards"]),
]

# --------------------------------------------------------------- builders --


def ref_pill(doc, F, label, x, y, color, cls=None):
    """A git ref label like (HEAD -> business). y is the text baseline."""
    size = 11.5
    w = F["mono"].width(label, size)
    pad = 7
    c = f' class="{cls}"' if cls else ""
    return (f'<g{c}><rect x="{x:.1f}" y="{y - 13.5:.1f}" width="{w + 2 * pad:.1f}" height="19" rx="4" '
            f'fill="none" stroke="{color}" stroke-width="1"/>'
            + doc.text(F["mono"], label, x + pad, y, size, color) + "</g>", w + 2 * pad)


def hero(F, t):
    doc = Doc()
    W = 900
    parts = []
    parts.append(doc.text(F["black"], NAME, INSET - 3, 64, 62, t["ink"], track=-0.02))
    y = 108
    for line in wrap(F["regular"], TAGLINE, 19, 760):
        parts.append(doc.text(F["regular"], line, INSET, y, 19, t["ink2"]))
        y += 29

    # graph geometry
    x0, x1, tx = INSET + 20, INSET + 52, INSET + 90
    y += 34
    rows = []
    for i, c in enumerate(COMMITS):
        top = y
        title_y = y + 6
        body_ys = [title_y + 28 + k * 24 for k in range(len(c["body"]))]
        rows.append((c, title_y, body_ys))
        y = (body_ys[-1] if body_ys else title_y) + 44
    H = int(y - 22)

    (c3, y3, _), (c2, y2, _), (c1, y1, _) = rows
    cy3, cy2, cy1 = y3 - 6, y2 - 6, y1 - 6
    eng, sec, biz = t["eng"], t["sec"], t["biz"]

    # lines: draw bottom-up so the animation reads as history being written
    r = 14
    lines = [
        # tail below the first commit
        (f"M{x0} {H} L{x0} {cy1}", eng, "l0"),
        # engineering continues straight up into HEAD
        (f"M{x0} {cy1} L{x0} {cy3}", eng, "l1"),
        # security branches off engineering and merges into HEAD
        (f"M{x0} {cy1} C{x0} {cy1 - r * 2} {x1} {cy1 - r} {x1} {cy1 - r * 3} L{x1} {cy2}", sec, "l2"),
        (f"M{x1} {cy2} L{x1} {cy3 + r * 3} C{x1} {cy3 + r} {x0} {cy3 + r * 2} {x0} {cy3}", sec, "l3"),
    ]
    for d, col, cls in lines:
        parts.append(f'<path class="ln {cls}" d="{d}" fill="none" stroke="{col}" stroke-width="2.5" '
                     f'stroke-linecap="round" pathLength="1"/>')

    def dot(x, yy, col, cls, head=False):
        s = f'<g class="dot {cls}">'
        if head:
            s += f'<circle cx="{x}" cy="{yy}" r="11" fill="none" stroke="{col}" stroke-width="1.5" opacity=".55"/>'
        s += f'<circle cx="{x}" cy="{yy}" r="6.5" fill="{col}"/></g>'
        return s

    parts.append(dot(x0, cy1, eng, "d1"))
    parts.append(dot(x1, cy2, sec, "d2"))
    parts.append(dot(x0, cy3, biz, "d3", head=True))

    for (c, ty, bys), cls in zip(rows, ["c3", "c2", "c1"]):
        col = t[c["lane"]]
        g = [f'<g class="cm {cls}">']
        pill, pw = ref_pill(doc, F, c["refs"], tx, ty, col)
        g.append(pill)
        g.append(doc.text(F["bold"], c["title"], tx + pw + 12, ty + 1, 20, t["ink"]))
        for line, by in zip(c["body"], bys):
            g.append(doc.text(F["regular"], line, tx, by, 16, t["ink2"]))
        g.append("</g>")
        parts.append("".join(g))

    style = """
.ln{stroke-dasharray:1;stroke-dashoffset:0;animation:draw .55s ease-out backwards}
.l0{animation-delay:.05s}.l1{animation-delay:.35s;animation-duration:1.1s}
.l2{animation-delay:.45s}.l3{animation-delay:.95s}
.dot,.cm{animation:pop .45s ease-out backwards}
.d1,.c1{animation-delay:.3s}.d2,.c2{animation-delay:.85s}.d3,.c3{animation-delay:1.4s}
.dot{transform-box:fill-box;transform-origin:center}
@keyframes draw{from{stroke-dashoffset:1}}
@keyframes pop{from{opacity:0}}
@media (prefers-reduced-motion:reduce){.ln,.dot,.cm{animation:none}}
"""
    title = ("Atharva Karekar. Career as a git graph: engineering, then security at ARCON, "
             "merged into business at SDA Bocconi Asia Center.")
    return svg(W, H, doc, "".join(parts), title, style)


def card_layout(F, c, w):
    p = 24
    big = w > 600
    ts = 25 if big else 21
    ty = INSET + p + (48 if big else 44)
    lines = wrap(F["regular"], c["desc"], 15.5, w - 2 * INSET - 2 * p)
    y_after = ty + 30 + len(lines) * 23
    return dict(p=p, ts=ts, ty=ty, lines=lines, min_h=int(y_after + 50 + INSET))


def card(F, t, c, w, h):
    doc = Doc()
    col = t[c["lane"]]
    L = card_layout(F, c, w)
    p, i = L["p"], INSET
    parts = [f'<rect x="{i + .5}" y="{i + .5}" width="{w - 2 * i - 1}" height="{h - 2 * i - 1}" rx="10" '
             f'fill="none" stroke="{t["rule"]}"/>']
    parts.append(f'<circle cx="{i + p + 5}" cy="{i + p + 6}" r="5" fill="{col}"/>')
    parts.append(doc.text(F["mono"], LANE_NAME[c["lane"]], i + p + 18, i + p + 10.5, 11.5, col))
    parts.append(doc.text(F["bold"], c["title"], i + p, L["ty"], L["ts"], t["ink"], track=-0.005))
    y = L["ty"] + 30
    for line in L["lines"]:
        parts.append(doc.text(F["regular"], line, i + p, y, 15.5, t["ink2"]))
        y += 23
    fy = h - i - p + 2
    parts.append(f'<line x1="{i + p}" x2="{w - i - p}" y1="{fy - 24}" y2="{fy - 24}" stroke="{t["rule"]}"/>')
    parts.append(doc.text(F["regular"], c["tags"], i + p, fy, 13.5, t["ink3"]))
    parts.append(doc.text(F["semibold"], c["action"], w - i - p, fy, 14, col, anchor="end"))
    return svg(w, h, doc, "".join(parts), f'{c["title"]}: {c["desc"]}')


def toolkit(F, t):
    doc = Doc()
    W = 900
    parts = []
    rows = max(len(items) for _, items in TOOLKIT)
    H = 44 + rows * 27 + 8
    for i, (lane, items) in enumerate(TOOLKIT):
        x = INSET + i * (W - 2 * INSET) / 3
        col = t[lane]
        parts.append(f'<circle cx="{x + 5}" cy="{14}" r="5" fill="{col}"/>')
        parts.append(doc.text(F["mono"], LANE_NAME[lane], x + 18, 18.5, 11.5, col))
        parts.append(f'<line x1="{x + 5}" x2="{x + 5}" y1="24" y2="{H - 10}" stroke="{col}" stroke-width="1.5" opacity=".45"/>')
        for k, item in enumerate(items):
            parts.append(doc.text(F["medium"], item, x + 18, 50 + k * 27, 15.5, t["ink"]))
    title = "Toolkit. " + " ".join(f"{LANE_NAME[l]}: {', '.join(items)}." for l, items in TOOLKIT)
    return svg(W, H, doc, "".join(parts), title)


def main():
    F = load_fonts()
    out = HERE
    small_h = max(card_layout(F, c, 450)["min_h"] for c in CARDS)
    wide_h = card_layout(F, FEATURED, 900)["min_h"]
    for theme, t in THEMES.items():
        files = {f"hero-{theme}.svg": hero(F, t), f"toolkit-{theme}.svg": toolkit(F, t)}
        files[f'{FEATURED["file"]}-{theme}.svg'] = card(F, t, FEATURED, 900, wide_h)
        for c in CARDS:
            files[f'{c["file"]}-{theme}.svg'] = card(F, t, c, 450, small_h)
        for name, data in files.items():
            with open(os.path.join(out, name), "w") as f:
                f.write(data)
            print(f"{name:32} {len(data) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
