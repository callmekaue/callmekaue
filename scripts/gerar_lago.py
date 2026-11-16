"""Gera lago-koi.svg: lago visto de cima com carpas, vitórias-régias e pétalas de sakura.

Uso:  python scripts/gerar_lago.py   (gera lago-koi.svg na raiz do repositório)
"""
import math
import random
from pathlib import Path

from koi import koi, petal, blossom, smooth_loop

W, H = 1600, 460
random.seed(7)
out = []
A = out.append

A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  f'role="img" aria-label="Lago japonês com carpas nadando e pétalas de sakura caindo">')
A('<defs>'
  '<radialGradient id="agua" cx=".45" cy=".5" r=".75">'
  '<stop offset="0" stop-color="#2A74B5"/><stop offset=".55" stop-color="#1A4F86"/>'
  '<stop offset="1" stop-color="#0B1F3A"/></radialGradient>'
  '<radialGradient id="borda" cx=".5" cy=".5" r=".72">'
  '<stop offset=".7" stop-color="#0B1F3A" stop-opacity="0"/><stop offset="1" stop-color="#06122A" stop-opacity=".85"/></radialGradient>'
  '<radialGradient id="folha" cx=".4" cy=".4" r=".7">'
  '<stop offset="0" stop-color="#3E8E78"/><stop offset="1" stop-color="#1D5A56"/></radialGradient>'
  '<radialGradient id="luz" ><stop offset="0" stop-color="#F2FAFF" stop-opacity=".35"/>'
  '<stop offset="1" stop-color="#F2FAFF" stop-opacity="0"/></radialGradient>'
  '<filter id="sombra" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
  '<filter id="desfoque" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.5"/></filter>'
  '</defs>')

# água
A(f'<rect width="{W}" height="{H}" fill="url(#agua)"/>')
A('<ellipse cx="520" cy="150" rx="420" ry="160" fill="url(#luz)"/>')

# pedras no fundo
for _ in range(26):
    x, y = random.uniform(0, W), random.choice([random.uniform(380, 470), random.uniform(-10, 60)])
    A(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{random.uniform(18, 46):.0f}" ry="{random.uniform(10, 24):.0f}" '
      f'fill="#0A1A33" opacity="{random.uniform(.35, .6):.2f}" filter="url(#desfoque)"/>')

# reflexos de luz (cáusticas) deslizando
for i in range(9):
    y = 40 + i * 48
    d = " ".join(f"q40,{(-1) ** k * 8} 80,0" for k in range(26))
    A(f'<path d="M-200,{y} {d}" fill="none" stroke="#CFE6FA" stroke-width="1.4" opacity="{.06 + (i % 3) * .03:.2f}">'
      f'<animateTransform attributeName="transform" type="translate" values="0 0;160 0;0 0" '
      f'dur="{18 + i * 3}s" repeatCount="indefinite"/></path>')

# carpas: (padrão, escala, sentido, duração)
cardume = [
    ("kohaku", 1.0, 1, 38), ("ogon", .9, -1, 46), ("showa", .95, 1, 52), ("tancho", .8, -1, 34),
    ("sanke", .9, 1, 44), ("asagi", .85, -1, 56), ("kohaku", .7, 1, 30), ("chagoi", .8, -1, 60),
]
for i, (pat, esc, sentido, dur) in enumerate(cardume):
    cx, cy = random.uniform(380, 1220), random.uniform(170, 290)
    rx, ry = random.uniform(260, 620), random.uniform(90, 150)
    rx = min(rx, (cx - 110) / 1.1, (W - 110 - cx) / 1.1)
    pts = []
    n = 7
    for k in range(n):
        a = 2 * math.pi * k / n + random.uniform(-.2, .2)
        rr = random.uniform(.75, 1.1)
        pts.append((cx + math.cos(a) * rx * rr, cy + math.sin(a) * ry * rr))
    caminho = smooth_loop(pts)
    begin = f"-{random.uniform(0, dur):.1f}s"
    rev = ' keyPoints="1;0" keyTimes="0;1" calcMode="linear"' if sentido < 0 else ""
    rot = "auto-reverse" if sentido < 0 else "auto"
    mov = f'<animateMotion dur="{dur}s" begin="{begin}" repeatCount="indefinite" rotate="{rot}" path="{caminho}"{rev}/>'
    # sombra no fundo
    A(f'<g transform="translate(12,16)"><g>{mov}<ellipse rx="{70 * esc:.0f}" ry="{18 * esc:.0f}" '
      f'fill="#06122A" opacity=".55" filter="url(#sombra)"/></g></g>')
    A(f'<g>{mov}<g transform="scale({esc})">{koi(f"lago{i}", pat, fin=1.15, tail_dur=round(random.uniform(.9, 1.4), 2), scales=pat == "ogon")}</g></g>')

# ondulações na superfície
for i in range(12):
    x, y = random.uniform(60, W - 60), random.uniform(40, H - 40)
    d = random.uniform(4, 7)
    b = random.uniform(0, 8)
    for j in range(2):
        A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2" fill="none" stroke="#CFE6FA" stroke-width="1.4" opacity="0">'
          f'<animate attributeName="r" values="2;42" dur="{d:.1f}s" begin="{b + j * .9:.1f}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values=".55;0" dur="{d:.1f}s" begin="{b + j * .9:.1f}s" repeatCount="indefinite"/></circle>')

# vitórias-régias
folhas = [(150, 360, 44), (230, 410, 30), (1380, 90, 40), (1460, 140, 28), (90, 80, 34), (1250, 400, 36), (720, 420, 26)]
for i, (x, y, r) in enumerate(folhas):
    a1, a2 = math.radians(random.uniform(0, 360)), 0
    a2 = a1 + math.radians(28)
    x1, y1 = r * math.cos(a1), r * math.sin(a1)
    x2, y2 = r * math.cos(a2), r * math.sin(a2)
    veias = "".join(f'<path d="M0,0 L{r * .9 * math.cos(a2 + k * .8):.1f},{r * .9 * math.sin(a2 + k * .8):.1f}" '
                    f'stroke="#5FA98C" stroke-width="1" opacity=".5"/>' for k in range(1, 8))
    A(f'<g transform="translate({x},{y})"><ellipse cx="6" cy="8" rx="{r}" ry="{r * .9:.0f}" fill="#06122A" opacity=".4" filter="url(#sombra)"/>'
      f'<g><animateTransform attributeName="transform" type="rotate" values="-4;4;-4" dur="{9 + i}s" repeatCount="indefinite"/>'
      f'<path d="M0,0 L{x2:.1f},{y2:.1f} A{r},{r} 0 1 1 {x1:.1f},{y1:.1f} Z" fill="url(#folha)"/>{veias}</g></g>')
# flores de lótus em duas folhas
for x, y in ((150, 360), (1380, 90)):
    pet = "".join(f'<ellipse cx="0" cy="-11" rx="6" ry="12" fill="#F9C6D3" stroke="#E8708F" stroke-width=".8" '
                  f'transform="rotate({k * 45})"/>' for k in range(8))
    A(f'<g transform="translate({x + 8},{y - 6})">{pet}<circle r="5" fill="#FFE08A"/></g>')

# pétalas boiando
for i in range(22):
    x, y = random.uniform(0, W), random.uniform(20, H - 20)
    dx = random.uniform(60, 180)
    dur = random.uniform(16, 30)
    A(f'<g opacity=".9"><animateTransform attributeName="transform" type="translate" '
      f'values="{x:.0f} {y:.0f};{x + dx:.0f} {y + random.uniform(-14, 14):.0f};{x:.0f} {y:.0f}" dur="{dur:.0f}s" repeatCount="indefinite"/>'
      f'<g><animateTransform attributeName="transform" type="rotate" values="0;{random.choice([-1, 1]) * 360}" dur="{dur * 1.5:.0f}s" repeatCount="indefinite"/>'
      f'<g transform="scale({random.uniform(.9, 1.4):.2f})">{petal()}</g></g></g>')

# galhos de sakura
def galho(pontos, larg):
    d = f"M{pontos[0][0]},{pontos[0][1]} " + " ".join(f"Q{a},{b} {c},{e}" for a, b, c, e in pontos[1:])
    return (f'<path d="{d}" fill="none" stroke="#2B1E24" stroke-width="{larg}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#4A3540" stroke-width="{larg * .35:.1f}" stroke-linecap="round" opacity=".6"/>')

A('<g>')
A('<animateTransform attributeName="transform" type="rotate" values="0 1600 0;-1.2 1600 0;0 1600 0" dur="7s" repeatCount="indefinite"/>')
A(galho([(1620, -10), (1500, 40, 1380, 46), (1290, 52, 1210, 110)], 13))
A(galho([(1420, 44), (1400, 90, 1340, 120)], 6))
A(galho([(1530, 26), (1520, 80, 1480, 110)], 6))
A(galho([(1300, 52), (1250, 20, 1180, 18)], 5))
for _ in range(34):
    t = random.random()
    bx = 1600 - t * 400 + random.uniform(-30, 30)
    by = 10 + t * 80 + random.uniform(-26, 34)
    A(blossom(bx, by, random.uniform(7, 12), random.choice(["#F9C6D3", "#F7B6C8", "#FBD7E2"])))
A('</g><g>')
A('<animateTransform attributeName="transform" type="rotate" values="0 0 0;1.4 0 0;0 0 0" dur="8s" repeatCount="indefinite"/>')
A(galho([(-20, -10), (80, 30, 170, 30), (240, 30, 300, 70)], 11))
A(galho([(150, 30), (170, 70, 140, 100)], 5))
for _ in range(22):
    t = random.random()
    A(blossom(t * 300 + random.uniform(-20, 20), 10 + t * 50 + random.uniform(-20, 30), random.uniform(7, 11),
              random.choice(["#F9C6D3", "#F7B6C8", "#FBD7E2"])))
A('</g>')

# pétalas caindo
for i in range(34):
    x0 = random.uniform(-100, W)
    dur = random.uniform(9, 17)
    begin = -random.uniform(0, dur)
    sway = random.uniform(40, 110)
    caminho = (f"M{x0:.0f},-20 C{x0 + sway:.0f},{H * .25:.0f} {x0 - sway * .6:.0f},{H * .55:.0f} "
               f"{x0 + sway * 1.6:.0f},{H * .8:.0f} S{x0 + sway * 2.2:.0f},{H + 10:.0f} {x0 + sway * 2.6:.0f},{H + 30:.0f}")
    esc = random.uniform(.9, 1.6)
    A(f'<g><animateMotion dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite" path="{caminho}"/>'
      f'<g><animateTransform attributeName="transform" type="rotate" values="0;{random.choice([-1, 1]) * 360}" '
      f'dur="{random.uniform(3, 6):.1f}s" repeatCount="indefinite"/>'
      f'<g><animateTransform attributeName="transform" type="scale" values="{esc:.2f} {esc:.2f};{esc:.2f} {esc * .25:.2f};{esc:.2f} {esc:.2f}" '
      f'dur="{random.uniform(1.4, 2.6):.1f}s" repeatCount="indefinite"/>{petal()}</g></g></g>')

# vinheta e selo (hanko)
A(f'<rect width="{W}" height="{H}" fill="url(#borda)"/>')
A('<g transform="translate(1510,384)"><rect width="56" height="56" rx="6" fill="#C8372D" opacity=".9"/>'
  '<rect x="4" y="4" width="48" height="48" rx="4" fill="none" stroke="#F7E9DC" stroke-width="1.5"/>'
  '<text x="28" y="38" text-anchor="middle" font-size="30" fill="#F7E9DC" '
  'font-family="Hiragino Mincho ProN, Yu Mincho, Noto Serif JP, serif">鯉</text></g>')
A('</svg>')

destino = Path(__file__).resolve().parent.parent / "lago-koi.svg"
destino.write_text("".join(out), encoding="utf-8")
print(f"ok: {destino} ({destino.stat().st_size // 1024} KB)")
