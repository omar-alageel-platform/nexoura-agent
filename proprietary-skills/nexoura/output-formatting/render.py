#!/usr/bin/env python3
"""Render a NEXOURA branded report by substituting placeholders in nexoura-template.html.

Usage:
    python3 render.py <input.md> <output.html>

Honest scope: This is a thin renderer used to produce the sample. Production
pipelines can wrap pandoc directly (see SKILL.md §5); this script demonstrates
the placeholder-substitution path which works without pandoc native templating.
"""
import re
import subprocess
import sys
import pathlib
import datetime

HERE = pathlib.Path(__file__).parent
TEMPLATE = HERE / "nexoura-template.html"


def render(md_path: pathlib.Path, out_path: pathlib.Path) -> None:
    src = md_path.read_text()

    # Parse YAML front-matter (minimal: key: "value" or key: value)
    fm = {}
    m = re.match(r"^---\n(.*?)\n---\n", src, flags=re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*):\s*"?(.*?)"?\s*$', line)
            if mm:
                fm[mm.group(1)] = mm.group(2)
        body_md = src[m.end():]
    else:
        body_md = src

    # Drop first H1 (title is in front-matter)
    body_md = re.sub(r"^#\s+.*\n", "", body_md, count=1)

    # Convert status markers to pill spans
    def pill(mt):
        s = mt.group(1).lower()
        return f'<span class="pill pill-{s}">{mt.group(1)}</span>'
    body_md = re.sub(r"\[(VERIFIED|RESOLVED|PENDING|BLOCKED)\]", pill, body_md)

    # Pandoc: markdown -> HTML body fragment
    body_html = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html"],
        input=body_md, capture_output=True, text=True, check=True,
    ).stdout

    # Metrics HTML is optional and orthogonal — pass via env or stub.
    metrics_html = fm.get("metrics_html", "")

    tpl = TEMPLATE.read_text()
    out = (
        tpl
        .replace("{{TITLE}}", fm.get("title", ""))
        .replace("{{KICKER}}", fm.get("kicker", "NEXOURA · STUDIO"))
        .replace("{{SUBTITLE}}", fm.get("subtitle", ""))
        .replace("{{DATE}}", fm.get("date", ""))
        .replace("{{AUTHOR_PROFILE}}", fm.get("author_profile", ""))
        .replace("{{METRICS_HTML}}", metrics_html)
        .replace("{{BODY_HTML}}", body_html)
        .replace("{{TIMESTAMP}}", datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))
    )
    out_path.write_text(out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    render(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))
    print(f"rendered {sys.argv[2]}")
