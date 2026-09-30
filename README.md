# yamatsushita.github.io

Personal academic homepage for Yasuyuki Matsushita, served by GitHub Pages at
<https://yamatsushita.github.io>.

Plain static HTML and CSS — no build step, no dependencies. Push to `main` and
GitHub Pages publishes within a minute.

## Layout

| Path | Purpose |
| --- | --- |
| `index.html` | Home: bio, research interests, news, contact |
| `publications.html` | Full publication list with a client-side filter |
| `activities.html` | Editorial roles, conference organization, area chairing |
| `404.html` | Not-found page |
| `assets/css/style.css` | All styling; colors live in the `:root` block |
| `assets/js/main.js` | Mobile nav and publication filter (progressive enhancement) |
| `assets/img/profile.jpg` | Portrait |
| `assets/publications.bib` | BibTeX export of the publication list |
| `tools/publications.json` | Structured publication data |
| `tools/build_publications.py` | Optional regenerator for `publications.html` |

## Editing

Most edits are direct HTML edits — open the file and change the text.

- **News**: edit the `<section id="news">` list in `index.html`.
- **Activities**: edit the `<ul class="cv-list">` blocks.
- **Colors and fonts**: edit the custom properties at the top of `assets/css/style.css`.
  Dark mode follows the visitor's system setting automatically.

### Publications

`publications.html` is ordinary hand-editable HTML; copy an existing
`<li class="pub">` block and change the fields.

To regenerate it from structured data instead, edit `tools/publications.json` and run:

```sh
python3 tools/build_publications.py
```

That rewrites both `publications.html` and `assets/publications.bib`.

## Local preview

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Publication data provenance

The 207 entries in `tools/publications.json` come from three sources:

1. **DBLP** (primary) — 200 records covering 2000&ndash;2026. Conference papers,
   journal articles, the book, and reference-work entries are all included.
   arXiv/CoRR preprints are included only when no published version exists;
   preprints duplicating a published paper are dropped.
2. **Japanese-language papers** — 13 MIRU (画像の認識・理解シンポジウム) entries
   matched on the author string 松下康之 from the previous homepage's
   teachPress list, which DBLP does not index.
3. **Previous homepage** — 8 remaining entries DBLP does not carry (domestic
   Japanese conferences, a Microsoft technical report, an ICIP tutorial), plus
   the hosted paper PDFs linked throughout the list.

DOIs and open-access PDF links were added by matching titles against OpenAlex
author `A5033986386` (verified via ORCID `0000-0002-1935-4752`).

Proceedings that Matsushita edited are deliberately excluded from the
publication list; those roles appear on `activities.html` instead.

Entries are deduplicated on title **and** year, because a conference paper and
its later journal extension share a title but are distinct publications.
