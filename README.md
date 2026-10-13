# Javier Peigneux · CV

Personal CV, a one-page PDF and a responsive static website.

- **Website:** https://javierpeigneux.github.io/cv/
- **PDF:** [Download CV](cv-javier-peigneux.pdf)
- **Content:** [Markdown CV](cv-javier-peigneux.md)

## Build the website

Python 3.10+ is sufficient; no JavaScript framework or package installation is needed.

```sh
python3 build_web.py
python3 -m http.server 8000 --directory docs
```

Visit http://localhost:8000. Edit `cv-javier-peigneux.md` for web content and `web/` for layout/styles, then rebuild. The generated `docs/` folder contains only public website assets. GitHub Pages publishes `main:/docs` after a push.

## Build the PDF

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build_cv_pdf.py
python build_web.py
```

The PDF layout and copy live in `build_cv_pdf.py`; keep its text synchronized with the Markdown when editing. The generator checks that both columns fit on one page. `CV_OUTPUT`, `CV_PHOTO` and `CV_FONT_DIR` optionally override the output filename, portrait and font directory.

The alternate PDF filename is retained for compatibility. Lato fonts are bundled with their SIL Open Font License. CV content and portrait are personal materials; no reuse license is granted for those materials.

## Working materials

Alternative portraits and PDF layout previews are preserved in this repository. The original example CV (including its rendered page), Python environments, caches, and the downloaded LinkedIn HTML are excluded. Only `docs/` is served as the website.
