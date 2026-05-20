#!/usr/bin/env python3
"""Patch the pandoc default reference.docx to apply NEXOURA branding.

What this script does (stdlib only — no python-docx):

1. Heading colours: H1/H2/H3/H4/Title/Subtitle re-coloured to the NEXOURA palette
   via w:color in word/styles.xml. (Original behaviour, preserved.)

2. Sora as default Latin font: w:rFonts in Normal/Heading/Title styles set to
   "Sora". Plus the Sora Regular TTF is *embedded* in the package
   (word/fonts/sora.ttf), a w:font entry with <w:embedRegular r:id="..."/> is
   added to word/fontTable.xml, and a corresponding relationship is written
   into word/_rels/fontTable.xml.rels. Content Types gains a Default for the
   ttf extension. This allows Word on machines without Sora installed to render
   the document with the embedded font.

   Caveat: Microsoft's spec describes an optional obfuscation scheme (GUID XOR
   over the first 32 bytes). We store the TTF un-obfuscated and omit the
   w:fontKey attribute. Word and LibreOffice both accept this form for most
   practical fonts; some Word builds may show a font-embedding warning. This
   is documented in SKILL.md §3 honesty paragraph.

3. NEXOURA Pill character styles: 9 character styles (NEXOURAPillVerified,
   NEXOURAPillResolved, NEXOURAPillBlocked, NEXOURAPillWarning, NEXOURAPillP0..P4)
   added to word/styles.xml. Each is bold 11pt Sora, white foreground, w:shd
   shading fill with the per-pill colour.

   Caveat: w:shd cFill draws a flat rectangle behind the run — Word does not
   support rounded-corner shading natively. The HTML output uses real rounded
   pills; the DOCX renders as a flat coloured tag.

4. Gradient tagline footer: word/footer1.xml authored from scratch, image
   word/media/footer-tagline.png copied in, footer relationships file authored,
   Content Types overrides added, document.xml.rels gains a footer relationship,
   sectPr in document.xml gets <w:footerReference w:type="default" r:id="..."/>.

Run via: python3 patch_reference_docx.py
"""
import zipfile, shutil, re, pathlib, sys

HERE = pathlib.Path(__file__).parent
DOCX = HERE / "reference.docx"
BACKUP = HERE / "reference.docx.pandoc-default.bak"
FONT_TTF = HERE / "assets" / "sora-regular.ttf"
FOOTER_PNG = HERE / "assets" / "footer-tagline.png"

# --- Heading palette ---
HEADING_PALETTE = {
    "Heading1": "5B30FF",
    "Heading2": "7861FF",
    "Heading3": "2563FF",
    "Heading4": "475569",
    "Title":    "5B30FF",
    "Subtitle": "7861FF",
}

# --- Status pill palette (hex without #) ---
PILL_PALETTE = {
    "Verified": "00E0FF",
    "Resolved": "2563FF",
    "Blocked":  "7861FF",
    "Warning":  "F59E0B",
    "P0":       "DC2626",
    "P1":       "2563FF",
    "P2":       "F59E0B",
    "P3":       "6B7280",
    "P4":       "6B7280",
}

W_NS = "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\""
R_NS = "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\""


def patch_heading_colour(xml: str, style_id: str, hex_colour: str) -> str:
    pattern = re.compile(
        r'(<w:style\b[^>]*w:styleId="' + re.escape(style_id) + r'"[^>]*>)(.*?)(</w:style>)',
        re.DOTALL,
    )
    def repl(m):
        head, body, tail = m.group(1), m.group(2), m.group(3)
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
            body = body + f"<w:rPr>{colour_el}</w:rPr>"
        return head + body + tail
    return pattern.sub(repl, xml, count=1)


def set_sora_on_style(xml: str, style_id: str) -> str:
    """Force <w:rFonts w:ascii='Sora' w:hAnsi='Sora' w:cs='Sora'/> on a style."""
    pattern = re.compile(
        r'(<w:style\b[^>]*w:styleId="' + re.escape(style_id) + r'"[^>]*>)(.*?)(</w:style>)',
        re.DOTALL,
    )
    fonts_el = '<w:rFonts w:ascii="Sora" w:hAnsi="Sora" w:cs="Sora"/>'
    def repl(m):
        head, body, tail = m.group(1), m.group(2), m.group(3)
        rpr = re.search(r"<w:rPr>(.*?)</w:rPr>", body, re.DOTALL)
        if rpr:
            inner = rpr.group(1)
            if "<w:rFonts" in inner:
                inner_new = re.sub(r'<w:rFonts\b[^/]*/>', fonts_el, inner)
            else:
                inner_new = fonts_el + inner
            body = body.replace(rpr.group(0), f"<w:rPr>{inner_new}</w:rPr>")
        else:
            body = body + f"<w:rPr>{fonts_el}</w:rPr>"
        return head + body + tail
    return pattern.sub(repl, xml, count=1)


def add_sora_to_font_table(xml: str, rid: str) -> str:
    """Append a <w:font w:name='Sora'> entry with embedRegular reference."""
    if 'w:name="Sora"' in xml:
        return xml
    entry = (
        '<w:font w:name="Sora">'
        '<w:panose1 w:val="00000000000000000000"/>'
        '<w:charset w:val="00"/>'
        '<w:family w:val="swiss"/>'
        '<w:pitch w:val="variable"/>'
        f'<w:embedRegular r:id="{rid}"/>'
        '</w:font>'
    )
    return xml.replace("</w:fonts>", entry + "</w:fonts>")


def make_pill_style(name_suffix: str, fill_hex: str) -> str:
    style_id = f"NEXOURAPill{name_suffix}"
    return (
        f'<w:style w:type="character" w:customStyle="1" w:styleId="{style_id}">'
        f'<w:name w:val="NEXOURA Pill {name_suffix}"/>'
        '<w:rPr>'
        '<w:rFonts w:ascii="Sora" w:hAnsi="Sora" w:cs="Sora"/>'
        '<w:b/>'
        '<w:caps/>'
        '<w:color w:val="FFFFFF"/>'
        '<w:sz w:val="22"/>'   # half-points: 22 = 11pt
        f'<w:shd w:val="clear" w:color="auto" w:fill="{fill_hex}"/>'
        '</w:rPr>'
        '</w:style>'
    )


def inject_pill_styles(xml: str) -> str:
    if 'w:styleId="NEXOURAPillVerified"' in xml:
        return xml
    block = "".join(make_pill_style(k, v) for k, v in PILL_PALETTE.items())
    return xml.replace("</w:styles>", block + "</w:styles>")


def add_relationship(rels_xml: str, rid: str, rtype: str, target: str, extra: str = "") -> str:
    rel = f'<Relationship Id="{rid}" Type="{rtype}" Target="{target}"{extra}/>'
    return rels_xml.replace("</Relationships>", rel + "</Relationships>")


FOOTER_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
       xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:p>
    <w:pPr><w:jc w:val="center"/></w:pPr>
    <w:r>
      <w:rPr><w:noProof/></w:rPr>
      <w:drawing>
        <wp:inline distT="0" distB="0" distL="0" distR="0">
          <wp:extent cx="3810000" cy="381000"/>
          <wp:effectExtent l="0" t="0" r="0" b="0"/>
          <wp:docPr id="1" name="FooterTagline" descr="NEXOURA WHERE AI BUILDS"/>
          <wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
          <a:graphic>
            <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:pic>
                <pic:nvPicPr>
                  <pic:cNvPr id="1" name="FooterTagline"/>
                  <pic:cNvPicPr/>
                </pic:nvPicPr>
                <pic:blipFill>
                  <a:blip r:embed="rIdFooterImg"/>
                  <a:stretch><a:fillRect/></a:stretch>
                </pic:blipFill>
                <pic:spPr>
                  <a:xfrm><a:off x="0" y="0"/><a:ext cx="3810000" cy="381000"/></a:xfrm>
                  <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                </pic:spPr>
              </pic:pic>
            </a:graphicData>
          </a:graphic>
        </wp:inline>
      </w:drawing>
    </w:r>
  </w:p>
</w:ftr>
'''

FOOTER_RELS_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rIdFooterImg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/footer-tagline.png"/>
</Relationships>
'''


def patch_sectpr_for_footer(doc_xml: str, rid: str) -> str:
    """Insert <w:footerReference w:type="default" r:id="rid"/> as first child of sectPr."""
    if f'r:id="{rid}"' in doc_xml and "footerReference" in doc_xml:
        return doc_xml
    return re.sub(
        r"<w:sectPr(\b[^>]*)>",
        lambda m: f'<w:sectPr{m.group(1)}><w:footerReference w:type="default" r:id="{rid}"/>',
        doc_xml,
        count=1,
    )


def main():
    if not DOCX.exists():
        sys.exit("reference.docx missing — run `pandoc -o reference.docx --print-default-data-file reference.docx` first")
    if not FONT_TTF.exists():
        sys.exit(f"font missing: {FONT_TTF}")
    if not FOOTER_PNG.exists():
        sys.exit(f"footer image missing: {FOOTER_PNG} — run examples/generation-script.py")

    if not BACKUP.exists():
        shutil.copy(DOCX, BACKUP)

    with zipfile.ZipFile(DOCX, "r") as zf:
        members = {name: zf.read(name) for name in zf.namelist()}

    # --- styles.xml: heading colours, Sora font on body/heading styles, pill styles ---
    styles = members["word/styles.xml"].decode("utf-8")
    for sid, hexc in HEADING_PALETTE.items():
        styles = patch_heading_colour(styles, sid, hexc)
    for sid in ("Normal", "Heading1", "Heading2", "Heading3", "Heading4", "Title", "Subtitle"):
        styles = set_sora_on_style(styles, sid)
    styles = inject_pill_styles(styles)
    members["word/styles.xml"] = styles.encode("utf-8")

    # --- fontTable.xml + relationship + embedded TTF ---
    font_table = members["word/fontTable.xml"].decode("utf-8")
    font_rid = "rIdSora"
    font_table = add_sora_to_font_table(font_table, font_rid)
    members["word/fontTable.xml"] = font_table.encode("utf-8")

    members["word/fonts/sora.ttf"] = FONT_TTF.read_bytes()

    # word/_rels/fontTable.xml.rels — create if absent
    ft_rels_key = "word/_rels/fontTable.xml.rels"
    if ft_rels_key in members:
        ft_rels = members[ft_rels_key].decode("utf-8")
    else:
        ft_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '</Relationships>')
    ft_rels = add_relationship(
        ft_rels, font_rid,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font",
        "fonts/sora.ttf",
    )
    members[ft_rels_key] = ft_rels.encode("utf-8")

    # --- footer1.xml, footer image, footer1.xml.rels ---
    members["word/footer1.xml"] = FOOTER_XML.encode("utf-8")
    members["word/_rels/footer1.xml.rels"] = FOOTER_RELS_XML.encode("utf-8")
    members["word/media/footer-tagline.png"] = FOOTER_PNG.read_bytes()

    # document.xml.rels — add footer relationship
    doc_rels = members["word/_rels/document.xml.rels"].decode("utf-8")
    footer_rid = "rIdFooter1"
    if footer_rid not in doc_rels:
        doc_rels = add_relationship(
            doc_rels, footer_rid,
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer",
            "footer1.xml",
        )
    members["word/_rels/document.xml.rels"] = doc_rels.encode("utf-8")

    # document.xml — inject footerReference in sectPr
    doc = members["word/document.xml"].decode("utf-8")
    doc = patch_sectpr_for_footer(doc, footer_rid)
    members["word/document.xml"] = doc.encode("utf-8")

    # [Content_Types].xml — register footer override, font/png defaults
    ct = members["[Content_Types].xml"].decode("utf-8")
    # png default
    if 'Extension="png"' not in ct:
        ct = ct.replace("</Types>",
                        '<Default Extension="png" ContentType="image/png"/></Types>')
    # ttf default (Word uses application/vnd.openxmlformats-officedocument.obfuscatedFont for
    # obfuscated fonts; for raw TTF use application/x-font-ttf as a pragmatic default)
    if 'Extension="ttf"' not in ct:
        ct = ct.replace("</Types>",
                        '<Default Extension="ttf" ContentType="application/x-font-ttf"/></Types>')
    # footer override
    if '/word/footer1.xml' not in ct:
        ct = ct.replace("</Types>",
                        '<Override PartName="/word/footer1.xml" '
                        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>')
    members["[Content_Types].xml"] = ct.encode("utf-8")

    # --- write back ---
    tmp = DOCX.with_suffix(".docx.tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    tmp.replace(DOCX)

    print(f"patched {DOCX}")
    print(f"  - heading colours: {', '.join(HEADING_PALETTE)}")
    print(f"  - Sora set on Normal/Heading*/Title/Subtitle, TTF embedded ({len(members['word/fonts/sora.ttf'])} bytes)")
    print(f"  - {len(PILL_PALETTE)} NEXOURAPill* character styles injected")
    print(f"  - footer1.xml + footer-tagline.png ({len(members['word/media/footer-tagline.png'])} bytes) wired into sectPr")


if __name__ == "__main__":
    main()
