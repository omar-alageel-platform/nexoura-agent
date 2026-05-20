#!/usr/bin/env python3
"""Build the sample-report HTML and DOCX from sample-report.md.

Re-runs render.py twice (HTML, DOCX) and patches three metric cards into the
HTML — the metric grid is a hand-authored injection point, demonstrating how
production pipelines compose metrics from upstream data.
"""
import pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
PY = sys.executable
SRC = HERE / "examples/sample-report.md"
HTML = HERE / "examples/sample-report.html"
DOCX = HERE / "examples/sample-report.docx"

# --- HTML ---
subprocess.run([PY, str(HERE/"render.py"), str(SRC), str(HTML)], check=True)
p = HTML.read_text()
metrics = (
    '<div class="nx-metric"><div class="label">Findings</div><div class="value">5</div>'
    '<div class="delta">3 verified \u00b7 1 pending \u00b7 1 blocked</div></div>'
    '<div class="nx-metric"><div class="label">Cache hit</div><div class="value">87%</div>'
    '<div class="delta">target \u2265 85%</div></div>'
    '<div class="nx-metric"><div class="label">Failover p50</div><div class="value">4.2s</div>'
    '<div class="delta">SLO \u2264 5.0s</div></div>'
)
p = p.replace('<section class="nx-metrics">\n    \n  </section>',
              '<section class="nx-metrics">\n    '+metrics+'\n  </section>')
HTML.write_text(p)
print(f"rendered {HTML} ({len(p)} bytes)")

# --- DOCX ---
subprocess.run([PY, str(HERE/"render.py"), str(SRC), str(DOCX)], check=True)
print(f"rendered {DOCX} ({DOCX.stat().st_size} bytes)")
