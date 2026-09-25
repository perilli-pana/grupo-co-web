#!/usr/bin/env python3
"""Arma las placas de Instagram de Grupo Co como HTML y las fotografía con Chrome.
Uso:  python3 build_placas.py      → deja los PNG en _kit/placas/
"""
import os, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent                      # grupo-co-web/
OUT  = HERE / "placas"; OUT.mkdir(exist_ok=True)
HTML = HERE / "_html"; HTML.mkdir(exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

FONT = '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">'
BASE = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--paper:#FAF6F1;--ink:#3F0702;--brown:#73341D;--muted:#9A7B6C;--black:#0B0807}
body{width:%(w)dpx;height:%(h)dpx;overflow:hidden;font-family:Poppins,sans-serif;background:var(--paper);color:var(--ink);-webkit-font-smoothing:antialiased}
.logo{display:block;fill:currentColor;width:auto}
.gc{background:url(%(root)s/logos/grupoco.svg) center/contain no-repeat}
.label{font-size:26px;font-weight:500;letter-spacing:.32em;text-transform:uppercase}
h1{font-weight:600;text-transform:uppercase;letter-spacing:-.02em;line-height:.96}
.marcas{display:flex;gap:44px;align-items:center;justify-content:center;flex-wrap:wrap}
.marcas .logo{height:30px;max-width:170px}
"""

def page(name, w, h, css, body):
    html = f"<!doctype html><html><head><meta charset='utf-8'>{FONT}<style>{BASE % dict(w=w,h=h,root=ROOT.as_uri())}{css}</style></head><body>{body}</body></html>"
    f = HTML / f"{name}.html"; f.write_text(html)
    png = OUT / f"{name}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={w},{h}", "--virtual-time-budget=4000",
                    f"--screenshot={png}", f.as_uri()],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("ok", png.name)

LOCALES = ["thunder","pasta","maryvino","parrilla","bodegon","chinita"]
import re
def svg_inline(name):
    s=open(ROOT/'logos'/f'{name}.svg').read()
    s=re.sub(r'\s(id|width|height)="[^"]*"','',s,count=3)
    return s.replace('<svg ','<svg class="logo" ',1)
marcas_row = "".join(svg_inline(n) for n in LOCALES)

# ── STORY 1 · buscamos personal (crema) ────────────────────────────────
page("story-personal", 1080, 1920, """
body{display:flex;flex-direction:column;justify-content:space-between;padding:120px 96px 110px}
h1{font-size:150px;color:var(--ink)}
.sub{margin-top:52px;font-size:34px;font-weight:500;letter-spacing:.26em;text-transform:uppercase;color:var(--brown)}
.cv{margin-top:120px;font-size:30px;font-weight:400;letter-spacing:.14em;text-transform:uppercase;line-height:1.7;color:var(--ink)}
.cv b{font-weight:600}
.foot{display:flex;flex-direction:column;gap:60px;align-items:center}
.gc{width:300px;height:140px}
.marcas .logo{color:var(--muted);height:26px;max-width:150px}
""", f"""
<div>
  <p class="label" style="color:var(--brown)">Grupo Co · Gastronomía</p>
  <h1 style="margin-top:70px">Buscamos<br>personal</h1>
  <p class="sub">Cocina · Salón · Barra</p>
  <p class="cv">Para cualquiera de los seis locales.<br>Mandá tu CV por <b>mensaje directo</b> & contanos en cuál te gustaría estar.</p>
</div>
<div class="foot">
  <span class="gc"></span>
</div>
""")

# ── STORY 2 · buscamos personal (sobre foto) ───────────────────────────
page("story-personal-foto", 1080, 1920, f"""
body{{background:url({ROOT.as_uri()}/fotos/f79.jpg) center/cover no-repeat;color:#FAF6F1}}
.veil{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,8,7,.55) 0%,rgba(11,8,7,.35) 45%,rgba(11,8,7,.88) 100%)}}
.wrap{{position:relative;height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:120px 96px 110px}}
h1{{font-size:150px}}
.sub{{margin-top:52px;font-size:34px;font-weight:500;letter-spacing:.26em;text-transform:uppercase;opacity:.9}}
.cv{{margin-top:120px;font-size:30px;letter-spacing:.14em;text-transform:uppercase;line-height:1.7}}
.cv b{{font-weight:600}}
.foot{{display:flex;flex-direction:column;gap:60px;align-items:center}}
.gc{{width:300px;height:140px;background-image:url({ROOT.as_uri()}/logos/grupoco.svg);filter:brightness(0) invert(1)}}
.marcas .logo{{height:26px;max-width:150px;opacity:.8}}
""", f"""
<div class="veil"></div>
<div class="wrap">
  <div>
    <p class="label">Grupo Co · Gastronomía</p>
    <h1 style="margin-top:70px">Buscamos<br>personal</h1>
    <p class="sub">Cocina · Salón · Barra</p>
    <p class="cv">Para cualquiera de los seis locales.<br>Mandá tu CV por <b>mensaje directo</b> & contanos en cuál te gustaría estar.</p>
  </div>
  <div class="foot">
    <span class="gc"></span>
  </div>
</div>
""")

# ── STORY 3 · comunicado del grupo (ejemplo: feriado) ──────────────────
page("story-comunicado", 1080, 1920, """
body{display:flex;flex-direction:column;justify-content:space-between;padding:120px 96px 110px;background:var(--black);color:var(--paper)}
h1{font-size:120px}
.sub{margin-top:52px;font-size:34px;font-weight:500;letter-spacing:.26em;text-transform:uppercase;color:#B9A79C}
.lista{margin-top:110px;display:grid;grid-template-columns:1fr auto;gap:26px 40px;font-size:28px;letter-spacing:.1em;text-transform:uppercase;border-top:1px solid #3a2c26;padding-top:40px}
.lista span:nth-child(even){text-align:right;font-weight:600}
.gc{width:300px;height:140px;filter:brightness(0) invert(1);align-self:center}
""", f"""
<div>
  <p class="label" style="opacity:.6">Grupo Co · Gastronomía</p>
  <h1 style="margin-top:70px">Lunes 12<br>de octubre</h1>
  <p class="sub">Feriado · Abrimos todos</p>
  <div class="lista">
    <span>Bodegón Co</span><span>Desde las 12</span>
    <span>Parrilla Co</span><span>Mediodía & noche</span>
    <span>Pasta Co</span><span>Mediodía & noche</span>
    <span>Mar & Vino</span><span>Desde las 20</span>
    <span>Chinita</span><span>Desde las 19</span>
    <span>Thunder</span><span>Todo el día</span>
  </div>
</div>
<span class="gc" style="background-image:url({ROOT.as_uri()}/logos/grupoco.svg)"></span>
""")

# ── FEED · placas de logo (negras, como las del .ai) ───────────────────
for n in LOCALES:
    page(f"feed-logo-{n}", 1080, 1350, """
body{background:var(--black);display:flex;align-items:center;justify-content:center}
.logo{width:760px;height:auto;max-height:320px;color:#FAF6F1}
""", svg_inline(n))

page("feed-logo-grupoco", 1080, 1350, """
body{display:flex;align-items:center;justify-content:center}
.gc{width:640px;height:300px}
""", '<span class="gc"></span>')

# ── FEED · presentación del grupo ───────────────────────────────────────
page("feed-presentacion", 1080, 1350, """
body{padding:110px 96px;display:flex;flex-direction:column;justify-content:space-between}
h1{font-size:104px;text-transform:none;letter-spacing:-.025em;line-height:1}
h1 em{font-style:normal;color:var(--brown)}
.col{display:grid;grid-template-columns:1fr 1fr;gap:64px 80px;align-items:center;margin-top:20px}
.col .logo{width:100%;height:auto;max-height:78px;color:var(--ink)}
.gc{width:220px;height:100px;background-position:left center}
""", f"""
<div>
  <span class="gc"></span>
  <h1 style="margin-top:60px">Seis lugares<br>para comer<br><em>&amp;</em> tomar.</h1>
</div>
<div class="col">{marcas_row}</div>
""")
