"""Gera as peças visuais do README em assets/: cabeçalho, títulos, pergaminho,
cards de projeto, botões e rodapé. Tudo em SVG animado (SMIL), na estética ukiyo-e azul.

Uso:  python scripts/gerar_visuais.py
"""
import math
import random
from pathlib import Path

from koi import koi, petal, blossom

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "assets"
ASSETS.mkdir(exist_ok=True)

SERIF = 'font-family="Noto Serif JP, Yu Mincho, Hiragino Mincho ProN, Georgia, serif"'
LATIN = 'font-family="Georgia, Noto Serif, Times New Roman, serif"'
SANS = 'font-family="Segoe UI, Helvetica, Arial, sans-serif"'
NUM = ["一", "二", "三", "四", "五", "六", "七"]
CORES_SAKURA = ["#F9C6D3", "#F7B6C8", "#FBD7E2"]


def salvar(nome, conteudo):
    (ASSETS / nome).write_text(conteudo, encoding="utf-8")
    print(f"ok: assets/{nome}")


def abrir(w, h, rotulo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{rotulo}">')


def defs_comuns():
    return ('<linearGradient id="noite" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06142B"/>'
            '<stop offset=".6" stop-color="#0E2F57"/><stop offset="1" stop-color="#1D5D9B"/></linearGradient>'
            '<linearGradient id="cartao" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0B1F3A"/>'
            '<stop offset="1" stop-color="#123C69"/></linearGradient>'
            '<radialGradient id="brilho"><stop offset="0" stop-color="#F2FAFF" stop-opacity=".5"/>'
            '<stop offset="1" stop-color="#F2FAFF" stop-opacity="0"/></radialGradient>'
            '<filter id="borrar" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>'
            '<g id="escama"><circle r="30" fill="#123C69" stroke="#5CC8FF" stroke-opacity=".55" stroke-width="1.6"/>'
            '<circle r="23" fill="none" stroke="#5CC8FF" stroke-opacity=".4" stroke-width="1.4"/>'
            '<circle r="16" fill="none" stroke="#5CC8FF" stroke-opacity=".35" stroke-width="1.2"/>'
            '<circle r="9" fill="none" stroke="#5CC8FF" stroke-opacity=".3" stroke-width="1.1"/></g>')


def seigaiha(x0, y0, largura, linhas, dur=40):
    """Ondas seigaiha (escamas concêntricas) deslizando devagar."""
    o = [f'<g><animateTransform attributeName="transform" type="translate" values="0 0;-60 0" '
         f'dur="{dur}s" repeatCount="indefinite"/>']
    for r in range(linhas):
        y = y0 + r * 15
        off = 30 if r % 2 else 0
        for x in range(int(x0) - 60 + off, int(x0 + largura) + 120, 60):
            o.append(f'<use href="#escama" x="{x}" y="{y}"/>')
    o.append('</g>')
    return "".join(o)


def hanko(x, y, texto, tam=64, cor="#C8372D"):
    fs = tam * .56 if len(texto) == 1 else tam * .36
    return (f'<g transform="translate({x},{y})"><rect width="{tam}" height="{tam}" rx="{tam * .1:.0f}" fill="{cor}"/>'
            f'<rect x="{tam * .07:.1f}" y="{tam * .07:.1f}" width="{tam * .86:.1f}" height="{tam * .86:.1f}" rx="{tam * .07:.0f}" '
            f'fill="none" stroke="#F7E9DC" stroke-width="1.6"/>'
            f'<text x="{tam / 2}" y="{tam / 2 + fs * .36:.1f}" text-anchor="middle" font-size="{fs:.0f}" fill="#F7E9DC" {SERIF}>{texto}</text></g>')


def petalas_caindo(w, h, n, rnd, xmin=-80):
    o = []
    for _ in range(n):
        x0 = rnd.uniform(xmin, w)
        dur = rnd.uniform(9, 16)
        sw = rnd.uniform(40, 100)
        cam = (f"M{x0:.0f},-20 C{x0 + sw:.0f},{h * .3:.0f} {x0 - sw * .6:.0f},{h * .6:.0f} "
               f"{x0 + sw * 1.5:.0f},{h * .85:.0f} S{x0 + sw * 2:.0f},{h + 10:.0f} {x0 + sw * 2.4:.0f},{h + 30:.0f}")
        e = rnd.uniform(.9, 1.5)
        o.append(f'<g><animateMotion dur="{dur:.1f}s" begin="-{rnd.uniform(0, dur):.1f}s" repeatCount="indefinite" path="{cam}"/>'
                 f'<g><animateTransform attributeName="transform" type="rotate" values="0;{rnd.choice([-1, 1]) * 360}" '
                 f'dur="{rnd.uniform(3, 6):.1f}s" repeatCount="indefinite"/><g><animateTransform attributeName="transform" '
                 f'type="scale" values="{e:.2f} {e:.2f};{e:.2f} {e * .25:.2f};{e:.2f} {e:.2f}" dur="{rnd.uniform(1.4, 2.6):.1f}s" '
                 f'repeatCount="indefinite"/>{petal()}</g></g></g>')
    return "".join(o)


def galho(pontos, larg):
    d = f"M{pontos[0][0]},{pontos[0][1]} " + " ".join(f"Q{a},{b} {c},{e}" for a, b, c, e in pontos[1:])
    return (f'<path d="{d}" fill="none" stroke="#2B1E24" stroke-width="{larg}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#4A3540" stroke-width="{larg * .35:.1f}" stroke-linecap="round" opacity=".6"/>')


def ramo_direita(w, rnd, alcance=380, flores=30, pivo=None):
    pivo = pivo or f"{w} 0"
    o = [f'<g><animateTransform attributeName="transform" type="rotate" values="0 {pivo};-1.2 {pivo};0 {pivo}" '
         f'dur="7s" repeatCount="indefinite"/>']
    o.append(galho([(w + 20, -10), (w - 120, 40, w - 230, 46), (w - 320, 52, w - alcance, 110)], 12))
    o.append(galho([(w - 180, 44), (w - 200, 90, w - 260, 120)], 5))
    o.append(galho([(w - 300, 52), (w - 340, 20, w - 410, 18)], 5))
    for _ in range(flores):
        t = rnd.random()
        o.append(blossom(w - t * alcance + rnd.uniform(-26, 26), 10 + t * 80 + rnd.uniform(-24, 32),
                         rnd.uniform(7, 12), rnd.choice(CORES_SAKURA)))
    o.append('</g>')
    return "".join(o)


def nevoa(y, x, larg, dur, op=.35):
    """Faixas de névoa (kasumi) das gravuras ukiyo-e."""
    return (f'<g opacity="{op}"><animateTransform attributeName="transform" type="translate" values="0 0;90 0;0 0" '
            f'dur="{dur}s" repeatCount="indefinite"/><rect x="{x}" y="{y}" width="{larg}" height="16" rx="8" fill="#CFE6FA"/>'
            f'<rect x="{x + larg * .25:.0f}" y="{y + 22}" width="{larg * .6:.0f}" height="10" rx="5" fill="#CFE6FA"/></g>')


# ---------------------------------------------------------------- cabeçalho
def cabecalho():
    rnd = random.Random(11)
    W, H = 1600, 520
    o = [abrir(W, H, "Kauê Alves: Engenharia de Software, Análise de Dados, TI e IA"), f'<defs>{defs_comuns()}</defs>']
    A = o.append
    A(f'<rect width="{W}" height="{H}" fill="url(#noite)"/>')
    for _ in range(60):
        A(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, 300):.0f}" r="{rnd.uniform(.6, 1.8):.1f}" fill="#F2FAFF">'
          f'<animate attributeName="opacity" values=".2;.9;.2" dur="{rnd.uniform(2, 5):.1f}s" begin="{rnd.uniform(0, 4):.1f}s" '
          f'repeatCount="indefinite"/></circle>')
    # sol vermelho das gravuras
    A('<circle cx="1180" cy="215" r="200" fill="url(#brilho)" opacity=".5"/>')
    A('<circle cx="1180" cy="215" r="118" fill="#D9483B"/><circle cx="1180" cy="215" r="118" fill="none" stroke="#F7B6A8" stroke-opacity=".3" stroke-width="6"/>')
    A(nevoa(150, 900, 420, 26, .4))
    A(nevoa(250, 1180, 360, 32, .3))
    A(nevoa(90, 300, 300, 30, .18))
    # monte distante
    A('<path d="M820,385 L1010,250 L1060,268 L1130,205 L1210,268 L1260,250 L1480,385 Z" fill="#1A4A80" opacity=".85"/>'
      '<path d="M1130,205 L1100,240 L1122,234 L1136,252 L1152,234 L1176,242 Z" fill="#EAF6FF" opacity=".9"/>')
    # mar
    A('<path d="M0,370 C200,345 400,395 600,370 C800,345 1000,395 1200,370 C1400,345 1600,395 1600,370 L1600,520 L0,520 Z" fill="#1D5D9B"/>')
    A('<clipPath id="marclip"><rect y="380" width="1600" height="140"/></clipPath>')
    A(f'<g clip-path="url(#marclip)">{seigaiha(0, 400, W, 9, 36)}</g>')
    # koi saltando
    arco = "M960,420 C1020,190 1220,170 1300,430"
    A('<g opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.04;.36;.4;1" dur="7s" repeatCount="indefinite"/>'
      f'<animateMotion dur="7s" repeatCount="indefinite" rotate="auto" path="{arco}" keyPoints="0;1;1" keyTimes="0;.4;1" calcMode="linear"/>'
      f'<g transform="scale(.95)">{koi("salto", "ogon", fin=1.6, tail=1.4, tail_dur=.5, scales=True)}</g></g>')
    for x, b in ((960, 0), (1300, 2.8)):
        for k in range(2):
            A(f'<ellipse cx="{x}" cy="418" rx="2" ry="1" fill="none" stroke="#EAF6FF" stroke-width="2" opacity="0">'
              f'<animate attributeName="rx" values="2;60" dur="1.6s" begin="{b + k * .3:.1f}s;rep{x}{k}.end+5.4s" id="rep{x}{k}"/>'
              f'<animate attributeName="ry" values="1;14" dur="1.6s" begin="{b + k * .3:.1f}s;rep{x}{k}.end+5.4s"/>'
              f'<animate attributeName="opacity" values=".8;0" dur="1.6s" begin="{b + k * .3:.1f}s;rep{x}{k}.end+5.4s"/></ellipse>')
    A(ramo_direita(W, rnd, 420, 34))
    # textos
    A(hanko(116, 118, "海", 56))
    A(f'<text x="190" y="155" {SERIF} font-size="24" letter-spacing="10" fill="#5CC8FF">カウエ・アルヴェス</text>')
    A(f'<text x="112" y="262" {LATIN} font-size="108" font-weight="700" fill="#F2FAFF">Kauê Alves</text>')
    A('<rect x="118" y="290" width="90" height="4" rx="2" fill="#D9483B"/>')
    A(f'<text x="118" y="336" {SANS} font-size="25" fill="#C9DDF5">Engenharia de Software · Análise de Dados · TI · IA</text>')
    A(petalas_caindo(W, H, 26, rnd))
    A('</svg>')
    salvar("cabecalho.svg", "".join(o))


# ---------------------------------------------------------------- títulos
def titulo(n, texto, kanji, leitura, arquivo, padrao):
    rnd = random.Random(n * 3)
    W, H = 1600, 150
    o = [abrir(W, H, texto), f'<defs>{defs_comuns()}</defs>']
    A = o.append
    A(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="url(#cartao)" stroke="#4DA3FF" stroke-opacity=".35"/>')
    A(f'<clipPath id="tc"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22"/></clipPath><g clip-path="url(#tc)">')
    A(f'<g opacity=".35">{seigaiha(1000, 120, 640, 3, 30)}</g>')
    caminho = "M1020,60 C1140,20 1300,110 1420,60 S1560,40 1640,70"
    A(f'<g><animateMotion dur="{13 + n}s" begin="-{n * 2.7:.1f}s" repeatCount="indefinite" rotate="auto" path="M940,70 C1100,30 1260,110 1420,64 S1600,50 1700,74"/>'
      f'<g transform="scale(.42)">{koi(f"t{n}", padrao, tail_dur=.9)}</g></g>')
    for i in range(3):
        A(f'<g transform="translate({1080 + i * 160},{30 + (i % 2) * 70})"><g><animateTransform attributeName="transform" type="rotate" '
          f'values="0;360" dur="{14 + i * 4}s" repeatCount="indefinite"/><g transform="scale(1.3)">{petal()}</g></g></g>')
    A('</g>')
    A(hanko(44, 38, NUM[n - 1], 74))
    A(f'<text x="150" y="92" fill="#F2FAFF"><tspan {LATIN} font-size="50" font-weight="700">{texto}</tspan>'
      f'<tspan dx="22" {SERIF} font-size="38" fill="#5CC8FF">{kanji}</tspan>'
      f'<tspan dx="14" {SANS} font-size="17" fill="#8FB7DC" font-style="italic">{leitura}</tspan></text>')
    A(f'<path d="M150,114 q20,-8 40,0 t40,0 t40,0 t40,0 t40,0" fill="none" stroke="#D9483B" stroke-width="3" stroke-linecap="round">'
      f'<animate attributeName="stroke-dasharray" values="0 240;240 0" dur="2s" fill="freeze"/></path>')
    A('</svg>')
    salvar(arquivo, "".join(o))


# ---------------------------------------------------------------- pergaminho
def pergaminho():
    rnd = random.Random(5)
    W, H = 1600, 380
    o = [abrir(W, H, "Pergaminho: Kauê Alves, estudante de Engenharia de Software com foco em Análise de Dados"),
         '<defs><linearGradient id="papel" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#F4EBDD"/>'
         '<stop offset="1" stop-color="#E9DCC6"/></linearGradient>'
         '<linearGradient id="vara" x1="0" x2="1"><stop offset="0" stop-color="#2B1E24"/><stop offset=".5" stop-color="#5A4048"/>'
         '<stop offset="1" stop-color="#2B1E24"/></linearGradient></defs>']
    A = o.append
    A('<g><animateTransform attributeName="transform" type="scale" values="0.04 1;1 1" dur="1.2s" fill="freeze" '
      'additive="sum"/><animateTransform attributeName="transform" type="translate" values="768 0;0 0" dur="1.2s" fill="freeze" additive="sum"/>')
    A(f'<rect x="70" y="30" width="{W - 140}" height="{H - 60}" fill="url(#papel)"/>')
    A(f'<rect x="70" y="30" width="{W - 140}" height="18" fill="#123C69"/><rect x="70" y="{H - 48}" width="{W - 140}" height="18" fill="#123C69"/>')
    A(f'<g opacity=".14" transform="translate(1160,0)"><clipPath id="pc"><rect x="0" y="48" width="370" height="{H - 96}"/></clipPath>'
      f'<g clip-path="url(#pc)">{seigaiha(0, 250, 400, 6, 50)}</g></g>')
    linhas = [("名前", "nome", "Kauê Alves"),
              ("学業", "formação", "Engenharia de Software"),
              ("焦点", "foco", "Análise de Dados"),
              ("興味", "interesses", "Desenvolvimento · Infraestrutura de TI · Inteligência Artificial"),
              ("信条", "lema", "do código ao hardware, uma onda de cada vez")]
    for i, (k, rot, val) in enumerate(linhas):
        y = 100 + i * 50
        A(f'<text x="150" y="{y}" {SERIF} font-size="28" fill="#C8372D">{k}</text>')
        A(f'<text x="230" y="{y}" {SANS} font-size="17" fill="#7A6A5C" letter-spacing="2">{rot.upper()}</text>')
        A(f'<text x="390" y="{y}" {LATIN} font-size="27" fill="#1B2A44">{val}</text>')
        A(f'<line x1="150" y1="{y + 14}" x2="1150" y2="{y + 14}" stroke="#C9B89E" stroke-dasharray="2 6"/>')
    A(hanko(1290, 92, "鯉", 92))
    A(f'<text x="1336" y="232" text-anchor="middle" {SERIF} font-size="18" fill="#7A6A5C">callmekaue</text>')
    A('</g>')
    for x in (40, W - 60):
        A(f'<rect x="{x}" y="14" width="20" height="{H - 28}" rx="10" fill="url(#vara)"/>'
          f'<circle cx="{x + 10}" cy="14" r="13" fill="#C8372D"/><circle cx="{x + 10}" cy="{H - 14}" r="13" fill="#C8372D"/>')
    A('</svg>')
    salvar("pergaminho.svg", "".join(o))


# ---------------------------------------------------------------- cards de projeto
def card(n, titulo_, linhas, tags, padrao, arquivo, kanji):
    rnd = random.Random(40 + n)
    W, H = 1600, 300
    o = [abrir(W, H, f"Projeto {n}: {titulo_}"), f'<defs>{defs_comuns()}</defs>']
    A = o.append
    A(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24" fill="url(#cartao)" stroke="#4DA3FF" stroke-opacity=".4"/>')
    A(f'<clipPath id="cc"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24"/></clipPath><g clip-path="url(#cc)">')
    # lago à direita
    A('<ellipse cx="1330" cy="150" rx="250" ry="120" fill="#1D5D9B" opacity=".55"/>')
    A(f'<g opacity=".28">{seigaiha(1060, 240, 560, 4, 34)}</g>')
    for i in range(3):
        A(f'<circle cx="{1230 + i * 90}" cy="{110 + (i % 2) * 70}" r="2" fill="none" stroke="#CFE6FA" stroke-width="1.4" opacity="0">'
          f'<animate attributeName="r" values="2;36" dur="5s" begin="{i * 1.6}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values=".5;0" dur="5s" begin="{i * 1.6}s" repeatCount="indefinite"/></circle>')
    cam = "M1180,150 C1180,80 1480,70 1480,150 C1480,230 1180,220 1180,150 Z"
    sentido = "" if n % 2 else ' keyPoints="1;0" keyTimes="0;1" calcMode="linear"'
    rot = "auto" if n % 2 else "auto-reverse"
    mov = f'<animateMotion dur="{12 + n}s" repeatCount="indefinite" rotate="{rot}" path="{cam}"{sentido}/>'
    A(f'<g transform="translate(8,12)"><g>{mov}<ellipse rx="44" ry="12" fill="#06122A" opacity=".5" filter="url(#borrar)"/></g></g>')
    A(f'<g>{mov}<g transform="scale(.7)">{koi(f"p{n}", padrao, fin=1.3, tail=1.2, tail_dur=1)}</g></g>')
    for i in range(4):
        A(f'<g transform="translate({1120 + i * 120},{60 + (i * 53) % 180})"><g><animateTransform attributeName="transform" '
          f'type="rotate" values="0;360" dur="{16 + i * 3}s" repeatCount="indefinite"/><g transform="scale(1.3)">{petal()}</g></g></g>')
    A(f'<text x="1560" y="{H - 26}" text-anchor="end" {SERIF} font-size="120" fill="#5CC8FF" opacity=".08">{kanji}</text>')
    A('</g>')
    A(hanko(52, 52, NUM[n - 1], 78))
    A(f'<text x="164" y="104" {LATIN} font-size="50" font-weight="700" fill="#F2FAFF">{titulo_}</text>')
    for i, l in enumerate(linhas):
        A(f'<text x="166" y="{150 + i * 34}" {SANS} font-size="25" fill="#C9DDF5">{l}</text>')
    x = 166
    for t in tags:
        w = len(t) * 12 + 34
        A(f'<rect x="{x}" y="{214}" width="{w}" height="38" rx="19" fill="#0B1F3A" stroke="#5CC8FF" stroke-opacity=".6"/>'
          f'<text x="{x + w / 2}" y="{239}" text-anchor="middle" {SANS} font-size="18" fill="#8FD8FF">{t}</text>')
        x += w + 12
    A(f'<text x="{x + 20}" y="240" {SANS} font-size="18" fill="#6F8FB5">ver repositório ↗</text>')
    A('</svg>')
    salvar(arquivo, "".join(o))


# ---------------------------------------------------------------- botões
def botao(rotulo, kanji, sub, arquivo):
    W, H = 520, 120
    o = [abrir(W, H, rotulo), f'<defs>{defs_comuns()}</defs>']
    A = o.append
    A(f'<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="20" fill="url(#cartao)" stroke="#5CC8FF" stroke-width="2"/>')
    A(f'<clipPath id="bc"><rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="20"/></clipPath>'
      f'<g clip-path="url(#bc)" opacity=".3">{seigaiha(300, 90, 260, 3, 24)}</g>')
    A(hanko(24, 24, kanji, 72))
    A(f'<text x="122" y="66" {LATIN} font-size="34" font-weight="700" fill="#F2FAFF">{rotulo}</text>')
    A(f'<text x="124" y="94" {SANS} font-size="17" fill="#8FB7DC">{sub}</text>')
    A(f'<text x="{W - 34}" y="72" text-anchor="end" {SANS} font-size="30" fill="#5CC8FF">↗'
      f'<animate attributeName="opacity" values=".4;1;.4" dur="2s" repeatCount="indefinite"/></text>')
    A('</svg>')
    salvar(arquivo, "".join(o))


# ---------------------------------------------------------------- rodapé
def rodape():
    rnd = random.Random(21)
    W, H = 1600, 420
    o = [abrir(W, H, "Obrigado por visitar meu perfil: duas carpas nadando em círculo"),
         f'<defs>{defs_comuns()}<radialGradient id="lagoR" cx=".5" cy=".45" r=".6"><stop offset="0" stop-color="#2A74B5"/>'
         '<stop offset="1" stop-color="#0B1F3A"/></radialGradient></defs>']
    A = o.append
    A(f'<rect width="{W}" height="{H}" fill="url(#lagoR)"/>')
    for i in range(5):
        A(f'<circle cx="800" cy="170" r="20" fill="none" stroke="#CFE6FA" stroke-width="1.5" opacity="0">'
          f'<animate attributeName="r" values="40;260" dur="8s" begin="{i * 1.6}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values=".35;0" dur="8s" begin="{i * 1.6}s" repeatCount="indefinite"/></circle>')
    circ = "M880,170 A80,80 0 1,1 720,170 A80,80 0 1,1 880,170 Z"
    for i, (pat, beg) in enumerate((("kohaku", "0s"), ("showa", "-5s"))):
        mov = f'<animateMotion dur="10s" begin="{beg}" repeatCount="indefinite" rotate="auto-reverse" path="{circ}" keyPoints="1;0" keyTimes="0;1" calcMode="linear"/>'
        A(f'<g transform="translate(10,14)"><g>{mov}<ellipse rx="56" ry="15" fill="#06122A" opacity=".5" filter="url(#borrar)"/></g></g>')
        A(f'<g>{mov}<g transform="scale(.85)">{koi(f"r{i}", pat, fin=1.4, tail=1.3, tail_dur=.9)}</g></g>')
    for x, y, r in ((1420, 250, 40), (190, 250, 34)):
        a1, a2 = -.3, .2
        A(f'<g transform="translate({x},{y})"><path d="M0,0 L{r * math.cos(a2):.1f},{r * math.sin(a2):.1f} '
          f'A{r},{r} 0 1 1 {r * math.cos(a1):.1f},{r * math.sin(a1):.1f} Z" fill="#2F7D6B"/>'
          f'<circle r="{r * .15:.1f}" fill="#3E8E78"/></g>')
    for _ in range(18):
        A(f'<g transform="translate({rnd.uniform(0, W):.0f},{rnd.uniform(20, 380):.0f})"><g><animateTransform attributeName="transform" '
          f'type="rotate" values="0;{rnd.choice([-1, 1]) * 360}" dur="{rnd.uniform(16, 30):.0f}s" repeatCount="indefinite"/>'
          f'<g transform="scale({rnd.uniform(1, 1.4):.2f})">{petal()}</g></g></g>')
    A(ramo_direita(W, rnd, 360, 26))
    A(f'<g transform="scale(-1,1) translate(-{W},0)">{ramo_direita(W, rnd, 300, 22)}</g>')
    A('<rect y="300" width="1600" height="120" fill="#0B1F3A" opacity=".55"/>')
    A(f'<text x="800" y="340" text-anchor="middle" {SERIF} font-size="34" letter-spacing="14" fill="#F2FAFF">ありがとう</text>')
    A(f'<text x="800" y="384" text-anchor="middle" {LATIN} font-size="26" fill="#C9DDF5">obrigado por visitar meu perfil</text>')
    A('</svg>')
    salvar("rodape.svg", "".join(o))


if __name__ == "__main__":
    cabecalho()
    titulo(1, "Sobre mim", "波", "nami · a onda", "titulo-sobre.svg", "tancho")
    titulo(2, "Tecnologias", "海", "umi · o mar", "titulo-tecnologias.svg", "asagi")
    titulo(3, "Projetos", "潮", "shio · a maré", "titulo-projetos.svg", "kohaku")
    titulo(4, "Lago das carpas", "鯉", "koi · a carpa", "titulo-lago.svg", "ogon")
    titulo(5, "Painel de programação", "龍", "ryū · o dragão", "titulo-painel.svg", "showa")
    pergaminho()
    projetos = [
        ("Difeecult: Sistema ERP", ["ERP para uma empresa parceira de moda esportiva: estoque,",
                                   "vendas, contas a receber, a pagar e muito mais."],
         ["Node.js", "Express", "SQLite", "PostgreSQL", "JavaScript"], "ogon", "帳"),
        ("PACORA: Gestor de Turmas", ["Sistema para gerir turmas e muitos alunos sem dificuldade."],
         ["HTML", "JavaScript", "SQL", "Cloudflare"], "kohaku", "学"),
        ("The Cure", ["Projeto em JavaScript, feito com amor de fã da Olivia Rodrigo."],
         ["HTML", "JavaScript", "JSON"], "showa", "音"),
        ("Pokédex", ["Projeto para registrar e pesquisar pokémons."],
         ["HTML", "CSS", "JavaScript"], "sanke", "図"),
        ("Login Riot", ["Interface de login inspirada na Riot Games."],
         ["HTML", "CSS", "JavaScript"], "tancho", "門"),
        ("Agrotech", ["Sensores Arduino e análise de dados em Python", "para apoiar a agricultura familiar."],
         ["Arduino", "Python", "Dados"], "chagoi", "農"),
        ("Star Wars: Jogo da Memória", ["Jogo da memória com personagens de A Guerra dos Clones."],
         ["HTML", "CSS", "JavaScript"], "asagi", "星"),
    ]
    for i, (t, l, tg, p, k) in enumerate(projetos, 1):
        card(i, t, l, tg, p, f"projeto-{i}.svg", k)
    botao("Portfólio", "作", "currículo online e projetos", "botao-portfolio.svg")
    botao("LinkedIn", "縁", "vamos nos conectar", "botao-linkedin.svg")
    rodape()
