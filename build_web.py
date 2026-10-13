"""Build the static CV website from its Markdown source (standard library only)."""
from html import escape
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "docs"


def inline(text):
    text = escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def content():
    lines = (ROOT / "cv-javier-peigneux.md").read_text().splitlines()
    output = []
    section = False
    listing = False
    company = False
    team = False
    started = False
    for line in lines:
        if line.startswith("## "):
            started = True
        if not started or not line.strip():
            continue
        if listing and not line.startswith("- "):
            output.append("</ul>")
            listing = False
        if line.startswith("## "):
            if team:
                output.append("</div>")
                team = False
            if company:
                output.append("</article>")
                company = False
            if section:
                output.append("</section>")
            title = line[3:]
            identifier = title.lower().replace(" ", "-")
            output.append(f'<section id="{identifier}" aria-labelledby="{identifier}-title"><h2 id="{identifier}-title">{inline(title)}</h2>')
            section = True
        elif line.startswith("### "):
            if team:
                output.append("</div>")
                team = False
            if company:
                output.append("</article>")
            output.append(f'<article class="company"><h3>{inline(line[4:])}</h3>')
            company = True
        elif line.startswith("#### "):
            if team:
                output.append("</div>")
            output.append(f'<div class="team"><h4>{inline(line[5:])}</h4>')
            team = True
        elif line.startswith("- "):
            if not listing:
                output.append("<ul>")
                listing = True
            output.append(f"<li>{inline(line[2:])}</li>")
        else:
            date_class = ' class="dates"' if re.search(r"\b20\d{2}\b", line) else ""
            output.append(f"<p{date_class}>{inline(line)}</p>")
    if listing:
        output.append("</ul>")
    if team:
        output.append("</div>")
    if company:
        output.append("</article>")
    if section:
        output.append("</section>")
    return "\n".join(output)


def main():
    SITE.mkdir(exist_ok=True)
    template = (ROOT / "web" / "template.html").read_text()
    (SITE / "index.html").write_text(template.replace("{{CONTENT}}", content()))
    shutil.copyfile(ROOT / "web" / "styles.css", SITE / "styles.css")
    shutil.copyfile(ROOT / "linkedin-photo.jpg", SITE / "portrait.jpg")
    shutil.copyfile(ROOT / "cv-javier-peigneux.pdf", SITE / "cv-javier-peigneux.pdf")
    shutil.copytree(ROOT / "assets" / "fonts", SITE / "fonts", dirs_exist_ok=True)
    (SITE / ".nojekyll").touch()
    print(SITE / "index.html")


if __name__ == "__main__":
    main()
