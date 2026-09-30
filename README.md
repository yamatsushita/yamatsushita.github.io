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
| `activities.html` | Editorial roles, conference organisation, memberships |
| `cv.html` | Education, appointments, awards |
| `404.html` | Not-found page |
| `assets/css/style.css` | All styling; colours live in the `:root` block |
| `assets/js/main.js` | Mobile nav and publication filter (progressive enhancement) |
| `assets/img/profile.jpg` | Portrait |
| `assets/publications.bib` | BibTeX export of the publication list |
| `tools/publications.json` | Structured publication data |
| `tools/build_publications.py` | Optional regenerator for `publications.html` |

## Editing

Most edits are direct HTML edits — open the file and change the text.

- **News**: edit the `<section id="news">` list in `index.html`.
- **Activities / CV**: edit the `<ul class="cv-list">` blocks.
- **Colours and fonts**: edit the custom properties at the top of `assets/css/style.css`.
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

The 154 entries were imported from the teachPress-backed list on the previous
homepage at `cvl.ist.osaka-u.ac.jp`, filtered to entries with Matsushita as an
author. One source record with a swapped title and venue was corrected against
DOI `10.1145/3641519.3657473`. Papers published before 2004 are not in that
source and are not yet listed here.
