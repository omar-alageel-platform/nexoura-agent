#!/usr/bin/env python3
"""Render NEXOURA branded reports.

Two outputs from one markdown source:

    # Legacy positional form (still supported, backward compatible):
    python3 render.py <input.md> <output.html>
    python3 render.py <input.md> <output.docx>

    # Theme-aware form:
    python3 render.py <input.md> --theme=dark  --out-dir <dir>
    python3 render.py <input.md> --theme=light --out-dir <dir>
    python3 render.py <input.md> --theme=both  --out-dir <dir>

Detected by the output extension. HTML uses nexoura-template.html + pandoc body
fragment + placeholder substitution. The `{{THEME}}` placeholder controls the
initial `data-theme` attribute (dark | light); a runtime switcher button lets
readers toggle and persists the choice in localStorage. DOCX uses
pandoc --reference-doc=reference.docx (theme-independent — DOCX styling is
defined by reference.docx, not the HTML template), then a post-processing pass
walks word/document.xml and replaces bracketed status markers ([VERIFIED] /
[P0] / ...) with proper runs styled by the NEXOURAPill* character styles
patched into the reference.

`--theme=both` produces TWO files in --out-dir:
    <stem>.dark.html  and  <stem>.light.html
"""
import argparse
import base64
import datetime
import pathlib
import re
import subprocess
import sys
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

VALID_THEMES = ("dark", "light")


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


def _build_body_and_meta(md_path: pathlib.Path):
    """Pandoc + frontmatter + pill substitution. Returns (fm, body_html, metrics_html, footer_data_url)."""
    src = md_path.read_text()
    fm, body_md = parse_frontmatter(src)

    # Drop first H1 (title is in front-matter)
    body_md = re.sub(r"^#\s+.*\n", "", body_md, count=1)

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

    footer_img_data_url = ""
    if FOOTER_PNG.exists():
        b64 = base64.b64encode(FOOTER_PNG.read_bytes()).decode("ascii")
        footer_img_data_url = f"data:image/png;base64,{b64}"

    return fm, body_html, metrics_html, footer_img_data_url


def render_html(md_path: pathlib.Path, out_path: pathlib.Path, theme: str = "dark") -> None:
    if theme not in VALID_THEMES:
        raise SystemExit(f"invalid theme {theme!r} (expected one of {VALID_THEMES})")
    fm, body_html, metrics_html, footer_img_data_url = _build_body_and_meta(md_path)

    tpl = TEMPLATE.read_text()
    out = (
        tpl
        .replace("{{THEME}}", theme)
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
        raise SystemExit("reference.docx missing — run patch_reference_docx.py first")
    subprocess.run(
        ["pandoc", str(md_path), "--reference-doc", str(REFERENCE_DOCX), "-o", str(out_path)],
        check=True,
    )
    n = post_process_docx_pills(out_path)
    print(f"  pills rewritten: {n}")


# -------------------------------------------------------------------------


def render(md_path: pathlib.Path, out_path: pathlib.Path, theme: str = "dark") -> None:
    if out_path.suffix.lower() == ".docx":
        # DOCX styling controlled by reference.docx — theme flag is a no-op here.
        render_docx(md_path, out_path)
    else:
        render_html(md_path, out_path, theme=theme)


def _legacy_two_positional(argv):
    """Returns (input_path, output_path) if argv looks like the old form, else None."""
    if len(argv) == 2 and not argv[0].startswith("-") and not argv[1].startswith("-"):
        return pathlib.Path(argv[0]), pathlib.Path(argv[1])
    return None


def main(argv):
    legacy = _legacy_two_positional(argv)
    if legacy is not None:
        in_path, out_path = legacy
        render(in_path, out_path, theme="dark")
        print(f"rendered {out_path}")
        return 0

    p = argparse.ArgumentParser(
        prog="render.py",
        description="Render NEXOURA branded HTML/DOCX from Markdown.",
    )
    p.add_argument("input", type=pathlib.Path, help="source .md file")
    p.add_argument("output", nargs="?", type=pathlib.Path,
                   help="output path (.html or .docx). Omit when using --theme=both.")
    p.add_argument("--theme", choices=("dark", "light", "both"), default="dark",
                   help="HTML theme. 'both' writes <stem>.dark.html and <stem>.light.html into --out-dir.")
    p.add_argument("--out-dir", type=pathlib.Path, default=None,
                   help="Output directory (required for --theme=both; optional otherwise).")
    args = p.parse_args(argv)

    in_path: pathlib.Path = args.input

    if args.theme == "both":
        out_dir = args.out_dir or (args.output.parent if args.output else in_path.parent)
        out_dir.mkdir(parents=True, exist_ok=True)
        stem = in_path.stem
        dark_path = out_dir / f"{stem}.dark.html"
        light_path = out_dir / f"{stem}.light.html"
        render_html(in_path, dark_path, theme="dark")
        render_html(in_path, light_path, theme="light")
        print(f"rendered {dark_path}")
        print(f"rendered {light_path}")
        return 0

    # Single-theme path
    if args.output is None:
        out_dir = args.out_dir or in_path.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{in_path.stem}.{args.theme}.html"
    else:
        out_path = args.output
        if args.out_dir is not None:
            out_path = args.out_dir / out_path.name
            args.out_dir.mkdir(parents=True, exist_ok=True)

    render(in_path, out_path, theme=args.theme)
    print(f"rendered {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
