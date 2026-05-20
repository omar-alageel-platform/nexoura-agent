#!/usr/bin/env python3
"""Render NEXOURA branded reports.

Two outputs from one markdown source:

    python3 render.py <input.md> <output.html>
    python3 render.py <input.md> <output.docx>

Detected by the output extension. HTML uses nexoura-template.html + pandoc body
fragment + placeholder substitution. DOCX uses pandoc --reference-doc=reference.docx,
then a post-processing pass walks word/document.xml and replaces bracketed
status markers ([VERIFIED] / [P0] / ...) with proper runs styled by the
NEXOURAPill* character styles patched into the reference.
"""
import base64
import datetime
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = pathlib.Path(__file__).parent
TEMPLATE = HERE / "nexoura-template.html"
REFERENCE_DOCX = HERE / "reference.docx"
FOOTER_PNG = HERE / "assets" / "footer-tagline.png"

# Map bracketed marker -> (HTML pill class, DOCX character style id)
PILL_MAP = {
    "VERIFIED": ("pill-verified", "NEXOURAPillVerified"),
    "RESOLVED": ("pill-resolved", "NEXOURAPillResolved"),
    "PENDING":  ("pill-pending",  "NEXOURAPillWarning"),
    "BLOCKED":  ("pill-blocked",  "NEXOURAPillBlocked"),
    "WARNING":  ("pill-pending",  "NEXOURAPillWarning"),
    "P0":       ("pill-p0",       "NEXOURAPillP0"),
    "P1":       ("pill-p1",       "NEXOURAPillP1"),
    "P2":       ("pill-p2",       "NEXOURAPillP2"),
    "P3":       ("pill-p3",       "NEXOURAPillP3"),
    "P4":       ("pill-p4",       "NEXOURAPillP4"),
}

PILL_REGEX = re.compile(r"\[(" + "|".join(re.escape(k) for k in PILL_MAP) + r")\]")


def parse_frontmatter(src: str):
    fm = {}
    m = re.match(r"^---\n(.*?)\n---\n", src, flags=re.DOTALL)
    if not m:
        return fm, src
    for line in m.group(1).splitlines():
        mm = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*):\s*"?(.*?)"?\s*$', line)
        if mm:
            fm[mm.group(1)] = mm.group(2)
    return fm, src[m.end():]


def render_html(md_path: pathlib.Path, out_path: pathlib.Path) -> None:
    src = md_path.read_text()
    fm, body_md = parse_frontmatter(src)

    # Drop first H1 (title is in front-matter)
    body_md = re.sub(r"^#\s+.*\n", "", body_md, count=1)

    # Bracketed pill markers -> HTML span (pre-pandoc; safe because we use raw HTML)
    def html_pill(mt):
        marker = mt.group(1)
        cls, _ = PILL_MAP[marker]
        return f'<span class="pill {cls}">{marker}</span>'
    body_md = PILL_REGEX.sub(html_pill, body_md)

    body_html = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html"],
        input=body_md, capture_output=True, text=True, check=True,
    ).stdout

    metrics_html = fm.get("metrics_html", "")

    # Footer image as data URL for self-contained HTML
    footer_img_data_url = ""
    if FOOTER_PNG.exists():
        b64 = base64.b64encode(FOOTER_PNG.read_bytes()).decode("ascii")
        footer_img_data_url = f"data:image/png;base64,{b64}"

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
        .replace("{{FOOTER_TAGLINE_PNG}}", footer_img_data_url)
        .replace("{{TIMESTAMP}}", datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))
    )
    out_path.write_text(out)


# --- DOCX path -----------------------------------------------------------

# Match a <w:r>...<w:t...>[MARKER]</w:t>...</w:r>  (single-run cases — covers
# typical pandoc output). We allow optional surrounding whitespace and
# additional run properties.
DOCX_RUN_PILL_RE = re.compile(
    r'(<w:r\b[^>]*>)(.*?)<w:t(\s[^>]*)?>([^<]*?)\[(' + "|".join(re.escape(k) for k in PILL_MAP) + r')\]([^<]*?)</w:t>(.*?)</w:r>',
    re.DOTALL,
)


def _docx_pill_replace(m):
    open_tag, rpr_etc, t_attrs, before, marker, after, tail = m.groups()
    t_attrs = t_attrs or ""
    _, style_id = PILL_MAP[marker]

    pieces = []
    if before:
        pieces.append(
            f'{open_tag}{rpr_etc}<w:t xml:space="preserve">{before}</w:t>{tail}</w:r>'
        )
    # Pill run with character style applied
    pieces.append(
        f'<w:r><w:rPr><w:rStyle w:val="{style_id}"/></w:rPr>'
        f'<w:t xml:space="preserve"> {marker} </w:t></w:r>'
    )
    if after:
        pieces.append(
            f'{open_tag}{rpr_etc}<w:t xml:space="preserve">{after}</w:t>{tail}</w:r>'
        )
    return "".join(pieces)


def post_process_docx_pills(docx_path: pathlib.Path) -> int:
    """Walk word/document.xml, replace bracketed markers with styled pill runs.
    Returns number of pills inserted."""
    with zipfile.ZipFile(docx_path, "r") as zf:
        members = {name: zf.read(name) for name in zf.namelist()}
    doc = members["word/document.xml"].decode("utf-8")
    count = [0]
    def repl(m):
        count[0] += 1
        return _docx_pill_replace(m)
    new_doc = DOCX_RUN_PILL_RE.sub(repl, doc)
    if new_doc == doc:
        return 0
    members["word/document.xml"] = new_doc.encode("utf-8")
    tmp = docx_path.with_suffix(".docx.tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    tmp.replace(docx_path)
    return count[0]


def render_docx(md_path: pathlib.Path, out_path: pathlib.Path) -> None:
    if not REFERENCE_DOCX.exists():
        raise SystemExit(f"reference.docx missing — run patch_reference_docx.py first")
    subprocess.run(
        ["pandoc", str(md_path), "--reference-doc", str(REFERENCE_DOCX), "-o", str(out_path)],
        check=True,
    )
    n = post_process_docx_pills(out_path)
    print(f"  pills rewritten: {n}")


# -------------------------------------------------------------------------


def render(md_path: pathlib.Path, out_path: pathlib.Path) -> None:
    if out_path.suffix.lower() == ".docx":
        render_docx(md_path, out_path)
    else:
        render_html(md_path, out_path)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    render(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))
    print(f"rendered {sys.argv[2]}")
