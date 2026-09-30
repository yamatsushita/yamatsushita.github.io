#!/usr/bin/env python3
"""Regenerate publications.html and assets/publications.bib from publications.json.

Optional helper. The generated HTML is plain, hand-editable markup, so you can
equally well edit publications.html directly and never run this script.

    python3 tools/build_publications.py
"""

import html
import json
import os
import re
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "tools", "publications.json")
OUT_HTML = os.path.join(ROOT, "publications.html")
OUT_BIB = os.path.join(ROOT, "assets", "publications.bib")

# Venue strings -> short badge. Patterns cover both full names and the
# abbreviated forms DBLP uses (e.g. "IEEE Trans. Pattern Anal. Mach. Intell.").
VENUE_BADGES = [
    (r"Computer Vision and Pattern Recognition|\bCVPR\b", "CVPR"),
    (r"International Conference on Computer Vision\b|\bICCV\b", "ICCV"),
    (r"European Conference on Computer Vision|\bECCV\b", "ECCV"),
    (r"Asian Conference on Computer Vision|\bACCV\b", "ACCV"),
    (r"Winter Conference on Applications of Computer Vision|\bWACV\b", "WACV"),
    (r"British Machine Vision Conference|\bBMVC\b", "BMVC"),
    (r"Neural Information Processing Systems|NeurIPS|\bNIPS\b", "NeurIPS"),
    (r"International Conference on Machine Learning\b|\bICML\b", "ICML"),
    (r"Learning Representations|\bICLR\b", "ICLR"),
    (r"Pattern Anal\.? Mach\.? Intell|Pattern Analysis and Machine Intelligence|\bPAMI\b", "TPAMI"),
    (r"Int\.? J\.? Comput\.? Vis|International Journal of Computer Vision|\bIJCV\b", "IJCV"),
    (r"Trans\.? Image Process|Transactions on Image Processing", "TIP"),
    (r"SIGGRAPH", "SIGGRAPH"),
    (r"\b3DV\b|3D Vision|3DIMPVT", "3DV"),
    (r"Computational Photography|\bICCP\b", "ICCP"),
    (r"International Conference on Image Processing|\bICIP\b", "ICIP"),
    (r"International Conference on Pattern Recognition|\bICPR\b", "ICPR"),
    (r"Robotics and Automation|\bICRA\b", "ICRA"),
    (r"Intelligent Robots and Systems|\bIROS\b", "IROS"),
    (r"Comput\.? Vis\.? Image Underst|Computer Vision and Image Understanding", "CVIU"),
    (r"Mach\.? Vis\.? Appl|Machine Vision and Applications|\bMVA\b", "MVA"),
    (r"Vis\.? Comput|The Visual Computer", "TVC"),
    (r"IPSJ Trans\.? Comput\.? Vis\.? Appl", "IPSJ CVA"),
    (r"Pattern Recognit|^Pattern Recognition$", "PR"),
    (r"画像の認識・理解シンポジウム|\bMIRU\b", "MIRU"),
    (r"人工知能学会", "JSAI"),
    (r"Pacific Graphics|\bPG\b", "PG"),
    (r"arXiv|CoRR", "arXiv"),
]

# Within a year: journals first, then conferences, then preprints.
TYPE_RANK = {"article": 0, "inproceedings": 1, "conference": 1, "misc": 2}


def badge_for(venue):
    for pattern, short in VENUE_BADGES:
        if re.search(pattern, venue, re.I):
            return short
    return None


def format_authors(raw):
    """'A and B and C' (or comma separated) -> HTML with my name emphasised."""
    if not raw:
        return ""
    parts = re.split(r"\s+and\s+", raw) if " and " in raw else raw.split(",")
    names = [re.sub(r"^[,\s]+|[,\s]+$", "", p) for p in parts]
    names = [n for n in names if n]
    out = []
    for n in names:
        if "matsushita" in n.lower():
            out.append('<span class="me">%s</span>' % html.escape(n))
        else:
            out.append(html.escape(n))
    return ", ".join(out)


def venue_of(entry):
    venue = entry.get("booktitle") or entry.get("journal") or entry.get("howpublished") or ""
    bits = [venue.strip()]
    if entry.get("volume"):
        bits.append("vol. %s" % entry["volume"])
    if entry.get("number"):
        bits.append("no. %s" % entry["number"])
    if entry.get("pages"):
        bits.append("pp. %s" % entry["pages"])
    return ", ".join(b for b in bits if b)


def label_for(url):
    u = url.lower()
    if "arxiv.org" in u:
        return "arXiv"
    if "github.com" in u:
        return "Code"
    if "doi.org" in u or "/doi/" in u:
        return "DOI"
    if u.endswith(".pdf"):
        return "PDF"
    if "youtube" in u or "youtu.be" in u:
        return "Video"
    return "Link"


def render(entries):
    by_year = OrderedDict()
    for e in entries:
        by_year.setdefault(e.get("year", "Other"), []).append(e)

    chunks = []
    for year in sorted(by_year, key=lambda y: (y.isdigit(), y), reverse=True):
        group = sorted(by_year[year],
                       key=lambda e: (TYPE_RANK.get(e.get("_type"), 1), e.get("title", "").lower()))
        chunks.append('      <section class="year-group">')
        chunks.append("        <h2>%s</h2>" % html.escape(year))
        chunks.append('        <ul class="pub-list">')
        for e in group:
            chunks.append('          <li class="pub">')
            chunks.append('            <span class="pub-title">%s</span>' % html.escape(e.get("title", "")))
            chunks.append('            <span class="pub-authors">%s</span>' % format_authors(e.get("author", "")))

            meta = []
            venue = venue_of(e)
            badge = badge_for(venue)
            if badge:
                meta.append('<span class="badge">%s</span>' % badge)
            if venue:
                meta.append("<span>%s</span>" % html.escape(venue))
            if meta:
                chunks.append('            <span class="pub-meta">%s</span>' % "".join(meta))

            urls = [u for u in re.split(r"\s+", e.get("url", "")) if u.startswith("http")]
            if urls:
                links = "".join(
                    '<a href="%s" rel="noopener">%s</a>' % (html.escape(u), label_for(u)) for u in urls
                )
                chunks.append('            <span class="pub-links">%s</span>' % links)
            chunks.append("          </li>")
        chunks.append("        </ul>")
        chunks.append("      </section>")
    return "\n".join(chunks), len(entries)


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Publications &middot; Yasuyuki Matsushita</title>
<meta name="description" content="Publications by Yasuyuki Matsushita in computer vision, machine learning, and Embodied AI.">
<link rel="canonical" href="https://yamatsushita.github.io/publications.html">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">Yasuyuki Matsushita</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" hidden>Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="publications.html" aria-current="page">Publications</a></li>
        <li><a href="activities.html">Activities</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="main">
  <div class="wrap">
    <h1>Publications</h1>
    <p class="lead">%(count)d entries. Filter by title, co-author, venue, or year.</p>

    <div class="pub-tools">
      <input class="pub-search" type="search" placeholder="Filter publications&hellip;" aria-label="Filter publications">
      <span class="pub-count" role="status"></span>
    </div>
    <p class="empty-state" hidden>No publications match that filter.</p>

%(body)s

    <p class="note">All entries are also available as BibTeX:
      <a href="assets/publications.bib">assets/publications.bib</a>.</p>
  </div>
</main>

<footer class="site-footer">
  <div class="wrap">
    <span>&copy; 2026 Yasuyuki Matsushita</span>
  </div>
</footer>

<script src="assets/js/main.js"></script>
</body>
</html>
"""


def main():
    with open(DATA, encoding="utf-8") as f:
        entries = json.load(f)
    body, count = render(entries)

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(PAGE % {"body": body, "count": count})

    with open(OUT_BIB, "w", encoding="utf-8") as f:
        f.write("%% Publications of Yasuyuki Matsushita (%d entries)\n\n" % count)
        for e in entries:
            f.write("@%s{%s,\n" % (e["_type"], e["_key"]))
            for k in ("title", "author", "booktitle", "journal", "volume",
                      "number", "pages", "year", "url", "doi"):
                if e.get(k):
                    f.write("  %s = {%s},\n" % (k, e[k]))
            f.write("}\n\n")

    print("wrote %s (%d entries)\nwrote %s" % (OUT_HTML, count, OUT_BIB))


if __name__ == "__main__":
    main()
