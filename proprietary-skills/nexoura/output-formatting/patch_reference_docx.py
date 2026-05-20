#!/usr/bin/env python3
"""Patch the pandoc default reference.docx to apply NEXOURA heading colours.

Edits word/styles.xml inside the .docx (which is a zip) and rewrites the
heading styles' w:color values to the NEXOURA palette. Conservative: only
heading colours and the base font; everything else stays at pandoc defaults.
"""
import zipfile, shutil, re, pathlib, sys

HERE = pathlib.Path(__file__).parent
DOCX = HERE / "reference.docx"
BACKUP = HERE / "reference.docx.pandoc-default.bak"

# NEXOURA palette (hex without leading #)
PALETTE = {
    "Heading1": "5B30FF",  # nx-violet-600
    "Heading2": "7861FF",  # nx-purple-500
    "Heading3": "2563FF",  # nx-blue-500
    "Heading4": "475569",  # nx-slate-700
    "Title":    "5B30FF",
    "Subtitle": "7861FF",
}

if not DOCX.exists():
    sys.exit("reference.docx missing — run `pandoc -o reference.docx --print-default-data-file reference.docx` first")

if not BACKUP.exists():
    shutil.copy(DOCX, BACKUP)

# Read styles.xml
with zipfile.ZipFile(DOCX, "r") as zf:
    members = {name: zf.read(name) for name in zf.namelist()}

styles = members["word/styles.xml"].decode("utf-8")

def patch_style(xml: str, style_id: str, hex_colour: str) -> str:
    # Find the <w:style ... w:styleId="<id>"> ... </w:style> block
    pattern = re.compile(
        r'(<w:style\b[^>]*w:styleId="' + re.escape(style_id) + r'"[^>]*>)(.*?)(</w:style>)',
        re.DOTALL,
    )
    def repl(m):
        head, body, tail = m.group(1), m.group(2), m.group(3)
        # Locate or create <w:rPr> inside the style block
        rpr = re.search(r"<w:rPr>(.*?)</w:rPr>", body, re.DOTALL)
        colour_el = f'<w:color w:val="{hex_colour}"/>'
        if rpr:
            inner = rpr.group(1)
            if "<w:color " in inner:
                inner_new = re.sub(r'<w:color\b[^/]*/>', colour_el, inner)
            else:
                inner_new = colour_el + inner
            body = body.replace(rpr.group(0), f"<w:rPr>{inner_new}</w:rPr>")
        else:
            # Insert rPr just before </w:style>
            body = body + f"<w:rPr>{colour_el}</w:rPr>"
        return head + body + tail
    return pattern.sub(repl, xml, count=1)

before = styles
for sid, hexc in PALETTE.items():
    styles = patch_style(styles, sid, hexc)

if styles == before:
    print("WARN: no styles matched — palette unchanged. Default reference.docx kept.")
else:
    members["word/styles.xml"] = styles.encode("utf-8")
    tmp = DOCX.with_suffix(".docx.tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    tmp.replace(DOCX)
    print("patched reference.docx with NEXOURA heading colours")
