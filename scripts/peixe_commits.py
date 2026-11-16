"""Gera peixe-commits.svg: um koi que evolui conforme o total de commits no GitHub.

Inspirado na lenda chinesa/japonesa (登龍門): a carpa que nada contra a correnteza
e atravessa o Portão do Dragão se transforma em dragão. Cada commit é uma braçada.

Variáveis de ambiente:
  GITHUB_TOKEN  token para a API GraphQL (no Actions, o GITHUB_TOKEN padrão já serve)
  GH_USER       usuário (padrão: callmekaue)
  COMMITS       força um número (útil para testar os estágios localmente)
  SAIDA         caminho do SVG (padrão: peixe-commits.svg na raiz do repositório)
"""
import datetime as dt
import json
import os
import urllib.request
from pathlib import Path

from koi import koi, petal

USER = os.environ.get("GH_USER", "callmekaue")

# (mínimo de commits, kanji, nome, padrão, nadadeira, cauda, tamanho, escamas brilhantes, aura, dragão)
ESTAGIOS = [
    (0, "稚魚", "Alevino", "alevino", .7, .7, .62, False, False, False),
    (50, "紅白", "Kohaku", "kohaku", 1.0, 1.0, .7, False, False, False),
    (150, "三色", "Sanke", "sanke", 1.25, 1.15, .74, False, False, False),
    (300, "昭和", "Showa Borboleta", "showa", 1.6, 1.4, .76, True, False, False),
    (600, "黄金", "Ogon Dourado", "ogon", 1.75, 1.5, .78, True, True, False),
    (1000, "登龍", "Koi-Dragão", "ogon", 1.9, 1.6, .8, True, True, True),
]


def graphql(query, variables, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "peixe-commits"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def contar_commits():
    if os.environ.get("COMMITS"):
        return int(os.environ["COMMITS"])
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("Defina GITHUB_TOKEN (ou COMMITS para testar).")
    criado = graphql("query($u:String!){user(login:$u){createdAt}}", {"u": USER}, token)["user"]["createdAt"]
    inicio = dt.datetime.fromisoformat(criado.replace("Z", "+00:00"))
    agora = dt.datetime.now(dt.timezone.utc)
    total = 0
    q = ("query($u:String!,$de:DateTime!,$ate:DateTime!){user(login:$u){"
         "contributionsCollection(from:$de,to:$ate){totalCommitContributions restrictedContributionsCount}}}")
    while inicio < agora:
        fim = min(inicio + dt.timedelta(days=365), agora)
        c = graphql(q, {"u": USER, "de": inicio.isoformat(), "ate": fim.isoformat()}, token)
        c = c["user"]["contributionsCollection"]
        total += c["totalCommitContributions"]
        if os.environ.get("INCLUIR_PRIVADOS") == "1":
            total += c["restrictedContributionsCount"]
        inicio = fim
    return total


def svg(n):
    idx = max(i for i, e in enumerate(ESTAGIOS) if n >= e[0])
    minimo, kanji, nome, padrao, fin, cauda, tam, escamas, aura, dragao = ESTAGIOS[idx]
    prox = ESTAGIOS[idx + 1] if idx + 1 < len(ESTAGIOS) else None
    prog = 1.0 if not prox else (n - minimo) / (prox[0] - minimo)
    tam *= 1 + .08 * prog  # cresce um pouco dentro do próprio estágio
    W, H = 1200, 380
    cx, cy, r = 250, 190, 150
    o = []
    A = o.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
      f'aria-label="Koi de commits: {nome}, {n} commits">')
    A('<defs><linearGradient id="fundo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0B1F3A"/>'
      '<stop offset="1" stop-color="#123C69"/></linearGradient>'
      '<radialGradient id="lago" cx=".45" cy=".4" r=".65"><stop offset="0" stop-color="#2A74B5"/>'
      '<stop offset="1" stop-color="#0E2D55"/></radialGradient>'
      '<radialGradient id="aura"><stop offset="0" stop-color="#FFD978" stop-opacity=".55"/>'
      '<stop offset="1" stop-color="#FFD978" stop-opacity="0"/></radialGradient>'
      '<linearGradient id="barra" x1="0" x2="1"><stop offset="0" stop-color="#1D5D9B"/>'
      '<stop offset="1" stop-color="#5CC8FF"/></linearGradient>'
      f'<clipPath id="recorte"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
      '<filter id="borrar" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter></defs>')
    A(f'<rect width="{W}" height="{H}" rx="22" fill="url(#fundo)"/>')
    A(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="21" fill="none" stroke="#4DA3FF" stroke-opacity=".35"/>')

    # lago circular
    A(f'<circle cx="{cx}" cy="{cy}" r="{r + 8}" fill="none" stroke="#5CC8FF" stroke-opacity=".25" stroke-width="2"/>')
    A(f'<g clip-path="url(#recorte)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#lago)"/>')
    for i in range(4):
        A(f'<circle cx="{cx - 50 + i * 35}" cy="{cy + (-1) ** i * 60}" r="2" fill="none" stroke="#CFE6FA" opacity="0">'
          f'<animate attributeName="r" values="2;34" dur="5s" begin="{i * 1.3}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values=".5;0" dur="5s" begin="{i * 1.3}s" repeatCount="indefinite"/></circle>')
    caminho = (f"M{cx + 62},{cy} C{cx + 62},{cy - 60} {cx - 62},{cy - 66} {cx - 62},{cy} "
               f"C{cx - 62},{cy + 66} {cx + 62},{cy + 60} {cx + 62},{cy} Z")
    vel = max(9, 16 - idx * 1.2)
    mov = f'<animateMotion dur="{vel:.1f}s" repeatCount="indefinite" rotate="auto" path="{caminho}"/>'
    A(f'<g transform="translate(10,14)"><g>{mov}<ellipse rx="{62 * tam:.0f}" ry="{16 * tam:.0f}" fill="#06122A" '
      f'opacity=".5" filter="url(#borrar)"/></g></g>')
    corpo = koi("commit", padrao, fin=fin, tail=cauda, tail_dur=max(.7, 1.3 - idx * .1), scales=escamas, dragon=dragao)
    brilho = ""
    if aura:
        brilho = (f'<circle r="{95 * tam:.0f}" fill="url(#aura)"><animate attributeName="opacity" values=".6;1;.6" '
                  f'dur="2.4s" repeatCount="indefinite"/></circle>')
    A(f'<g>{mov}{brilho}<g transform="scale({tam:.3f})">{corpo}</g></g>')
    # pétalas boiando no lago
    for i, (px, py) in enumerate([(-90, -70), (70, -95), (100, 80), (-60, 100), (10, -20)]):
        A(f'<g transform="translate({cx + px},{cy + py})"><g><animateTransform attributeName="transform" type="rotate" '
          f'values="0;360" dur="{18 + i * 4}s" repeatCount="indefinite"/><g transform="scale(1.3)">{petal()}</g></g></g>')
    if dragao:  # brilhos subindo
        for i in range(10):
            x = cx - 120 + i * 26
            A(f'<circle cx="{x}" cy="{cy + 140}" r="2" fill="#FFE9A8"><animate attributeName="cy" values="{cy + 150};{cy - 150}" '
              f'dur="{3 + i % 4}s" begin="{i * .4:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;1;0" dur="{3 + i % 4}s" begin="{i * .4:.1f}s" repeatCount="indefinite"/></circle>')
    A('</g>')

    # textos
    fonte = 'font-family="Segoe UI, Helvetica, Arial, sans-serif"'
    serif = 'font-family="Hiragino Mincho ProN, Yu Mincho, Noto Serif JP, serif"'
    x0 = 470
    A(f'<text x="{x0}" y="70" {fonte} font-size="16" letter-spacing="4" fill="#5CC8FF" font-weight="600">MEU KOI DE COMMITS</text>')
    A(f'<text x="{x0}" y="150" {serif} font-size="66" fill="#F2FAFF">{kanji}</text>')
    A(f'<text x="{x0 + 160}" y="128" {fonte} font-size="30" font-weight="700" fill="#FFFFFF">{nome}</text>')
    A(f'<text x="{x0 + 160}" y="156" {fonte} font-size="17" fill="#C9DDF5">estágio {idx + 1} de {len(ESTAGIOS)}</text>')
    num = f"{n:,}".replace(",", ".")
    A(f'<text x="{x0}" y="214" {fonte} font-size="44" font-weight="700" fill="#FFFFFF">{num}' +
      f'<tspan font-size="20" font-weight="400" fill="#C9DDF5"> commits</tspan></text>')

    bw = 660
    A(f'<rect x="{x0}" y="238" width="{bw}" height="14" rx="7" fill="#0B1F3A" stroke="#4DA3FF" stroke-opacity=".4"/>')
    A(f'<rect x="{x0}" y="238" width="{max(14, bw * prog):.0f}" height="14" rx="7" fill="url(#barra)">'
      f'<animate attributeName="width" from="0" to="{max(14, bw * prog):.0f}" dur="1.6s" fill="freeze"/></rect>')
    if prox:
        falta = prox[0] - n
        legenda = f"faltam {falta} commits para evoluir para {prox[2]} {prox[1]}"
    else:
        legenda = "forma final: o koi atravessou o Portão do Dragão"
    A(f'<text x="{x0}" y="278" {fonte} font-size="16" fill="#C9DDF5">{legenda}</text>')

    # trilha de estágios
    passo = bw / (len(ESTAGIOS) - 1)
    A(f'<line x1="{x0}" y1="322" x2="{x0 + bw}" y2="322" stroke="#4DA3FF" stroke-opacity=".35" stroke-width="2"/>')
    for i, e in enumerate(ESTAGIOS):
        x = x0 + i * passo
        feito = i <= idx
        A(f'<circle cx="{x:.0f}" cy="322" r="{9 if i == idx else 6}" fill="{"#5CC8FF" if feito else "#0B1F3A"}" '
          f'stroke="#5CC8FF" stroke-width="2">' +
          ('<animate attributeName="r" values="8;11;8" dur="1.8s" repeatCount="indefinite"/>' if i == idx else "") +
          '</circle>')
        A(f'<text x="{x:.0f}" y="352" text-anchor="middle" {serif} font-size="15" '
          f'fill="{"#F2FAFF" if feito else "#6F8FB5"}">{e[1]}</text>')
        A(f'<text x="{x:.0f}" y="370" text-anchor="middle" {fonte} font-size="11" '
          f'fill="{"#C9DDF5" if feito else "#6F8FB5"}">{e[0]}+</text>')
    A('</svg>')
    return "".join(o)


if __name__ == "__main__":
    n = contar_commits()
    destino = Path(os.environ.get("SAIDA") or Path(__file__).resolve().parent.parent / "peixe-commits.svg")
    destino.write_text(svg(n), encoding="utf-8")
    print(f"{USER}: {n} commits -> {destino}")
