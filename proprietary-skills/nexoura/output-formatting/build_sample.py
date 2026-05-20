#!/usr/bin/env python3
"""Build the sample-report.html from sample-report.md plus inline metric injection."""
import pathlib, subprocess, sys
HERE = pathlib.Path(__file__).parent
subprocess.run([sys.executable, str(HERE/"render.py"), str(HERE/"examples/sample-report.md"), str(HERE/"examples/sample-report.html")], check=True)
out = HERE/"examples/sample-report.html"
p = out.read_text()
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
out.write_text(p)
print("rendered", out, len(p), "bytes")
print(p[:500])
