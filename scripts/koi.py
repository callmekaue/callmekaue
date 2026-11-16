"""Desenho de carpas (koi) e pétalas de sakura em SVG, no estilo dos banners do perfil.

Cada carpa é desenhada olhando para +x, centrada na origem, com ~130 px de comprimento
na escala 1. As animações usam SMIL (animate/animateTransform/animateMotion), que o
GitHub exibe normalmente dentro de <img>.
"""

BODY = ("M64,0 C64,-15 50,-23 30,-23 C4,-23 -28,-15 -56,-5 "
        "L-56,5 C-28,15 4,23 30,23 C50,23 64,15 64,0 Z")

# Padrões clássicos de nishikigoi: (cor base, manchas, cor das nadadeiras)
PATTERNS = {
    "kohaku": ("#F7F3EC", [(30, -6, 22, 14, "#E2452F"), (-8, 6, 20, 12, "#E2452F"), (-36, -2, 12, 7, "#E2452F")], "#FBE9E2"),
    "tancho": ("#F7F3EC", [(46, 0, 9, 9, "#E2452F")], "#F3F0EA"),
    "sanke": ("#F7F3EC", [(26, -4, 20, 13, "#E2452F"), (-14, 5, 16, 10, "#E2452F"),
                          (4, -12, 6, 4, "#16161E"), (-30, 8, 5, 3.5, "#16161E"), (-6, 14, 4, 3, "#16161E")], "#F8EEE8"),
    "showa": ("#16161E", [(28, -6, 20, 12, "#E2452F"), (-10, 8, 16, 10, "#F7F3EC"), (-30, -4, 12, 7, "#E2452F")], "#2A2A36"),
    "ogon": ("#F2B33D", [(20, 0, 34, 10, "#FFD978")], "#F7C960"),
    "asagi": ("#7FA3C0", [(30, 16, 22, 7, "#E9743A"), (30, -16, 22, 7, "#E9743A"), (-20, 0, 26, 5, "#A9C5DC")], "#B8CFE2"),
    "chagoi": ("#B07A45", [(10, 0, 40, 8, "#C99360")], "#C99360"),
    "alevino": ("#C9D6E2", [(10, 0, 30, 6, "#E1E9F0")], "#DCE6EF"),
}


def koi(uid, pattern="kohaku", fin=1.0, tail=1.0, tail_dur=1.1, scales=False,
        dragon=False, outline="#0B1F3A"):
    base, spots, fin_col = PATTERNS[pattern]
    clip = f"kb{uid}"
    p = []
    p.append(f'<defs><clipPath id="{clip}"><path d="{BODY}"/></clipPath></defs>')

    # nadadeira caudal (animada)
    tl = 44 * tail
    tw = 26 * tail
    p.append(
        f'<g><animateTransform attributeName="transform" type="rotate" '
        f'values="-16 -54 0;16 -54 0;-16 -54 0" dur="{tail_dur}s" repeatCount="indefinite"/>'
        f'<path d="M-52,0 C-64,-6 {-54 - tl * .7:.1f},{-tw:.1f} {-54 - tl:.1f},{-tw * .95:.1f} '
        f'C{-54 - tl * .82:.1f},-8 {-54 - tl * .82:.1f},8 {-54 - tl:.1f},{tw * .95:.1f} '
        f'C{-54 - tl * .7:.1f},{tw:.1f} -64,6 -52,0 Z" fill="{fin_col}" opacity=".82"/>'
        f'<path d="M-56,0 L{-54 - tl * .9:.1f},{-tw * .55:.1f} M-56,0 L{-54 - tl * .95:.1f},0 '
        f'M-56,0 L{-54 - tl * .9:.1f},{tw * .55:.1f}" stroke="{base}" stroke-width="1" opacity=".5"/></g>'
    )

    # nadadeiras peitorais (animadas, alternadas)
    fl = 26 * fin
    for side, begin in ((-1, "0s"), (1, f"{tail_dur / 2:.2f}s")):
        s = side
        p.append(
            f'<g><animateTransform attributeName="transform" type="rotate" '
            f'values="0 30 {s * 18};{s * 22} 30 {s * 18};0 30 {s * 18}" dur="{tail_dur * 1.6:.2f}s" '
            f'begin="{begin}" repeatCount="indefinite"/>'
            f'<path d="M34,{s * 16} C{30 - fl * .2:.1f},{s * (20 + fl):.1f} {10 - fl * .5:.1f},{s * (22 + fl * 1.05):.1f} '
            f'{6 - fl * .55:.1f},{s * (18 + fl * .8):.1f} C{12 - fl * .2:.1f},{s * (20 + fl * .3):.1f} 20,{s * 20} 26,{s * 18} Z" '
            f'fill="{fin_col}" opacity=".78"/></g>'
        )
    # nadadeiras pélvicas pequenas
    for s in (-1, 1):
        p.append(f'<path d="M-14,{s * 12} C-22,{s * (18 + 6 * fin):.1f} -32,{s * (18 + 6 * fin):.1f} -34,{s * 13} Z" '
                 f'fill="{fin_col}" opacity=".7"/>')

    # corpo + manchas
    p.append(f'<path d="{BODY}" fill="{base}"/>')
    p.append(f'<g clip-path="url(#{clip})">')
    for cx, cy, rx, ry, col in spots:
        p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}"/>')
    if scales:
        for i, x in enumerate(range(-44, 48, 9)):
            for y in (-10, 0, 10):
                d = 1.6 + (i % 3) * .4
                p.append(
                    f'<path d="M{x},{y - 4} q4,4 0,8" fill="none" stroke="#FFFFFF" stroke-width="1" opacity=".25">'
                    f'<animate attributeName="opacity" values=".1;.6;.1" dur="{d:.1f}s" begin="{(i * .13) % 1.5:.2f}s" '
                    f'repeatCount="indefinite"/></path>')
    # brilho na lateral
    p.append('<ellipse cx="18" cy="-9" rx="34" ry="5" fill="#FFFFFF" opacity=".22"/>')
    p.append('</g>')
    p.append(f'<path d="{BODY}" fill="none" stroke="{outline}" stroke-opacity=".25" stroke-width="1.2"/>')
    # espinha dorsal (nadadeira vista de cima)
    p.append(f'<path d="M30,0 L-40,0" stroke="{fin_col}" stroke-width="2.4" stroke-linecap="round" opacity=".55"/>')
    # olhos
    for s in (-1, 1):
        p.append(f'<circle cx="52" cy="{s * 10}" r="2.6" fill="#0B0B12"/>'
                 f'<circle cx="52.8" cy="{s * 10 - .8}" r=".8" fill="#FFFFFF"/>')

    if dragon:
        # bigodes longos ondulando e chifres, a lenda do koi que vira dragão
        for s in (-1, 1):
            p.append(
                f'<path d="M62,{s * 5} C80,{s * 10} 92,{s * 30} 108,{s * 26}" fill="none" stroke="#FFD978" '
                f'stroke-width="1.8" stroke-linecap="round">'
                f'<animate attributeName="d" dur="2.4s" repeatCount="indefinite" values="'
                f'M62,{s * 5} C80,{s * 10} 92,{s * 30} 108,{s * 26};'
                f'M62,{s * 5} C82,{s * 2} 96,{s * 20} 112,{s * 34};'
                f'M62,{s * 5} C80,{s * 10} 92,{s * 30} 108,{s * 26}"/></path>')
            p.append(f'<path d="M40,{s * 12} L22,{s * 30} L30,{s * 14} Z" fill="#F2FAFF" stroke="#FFD978" stroke-width="1"/>')

    return "".join(p)


PETAL = "M0,6 C-6,2 -6,-5 -2,-6 L0,-3.6 L2,-6 C6,-5 6,2 0,6 Z"


def petal(fill="#F7B6C8", vein="#FBD7E2"):
    return (f'<path d="{PETAL}" fill="{fill}"/>'
            f'<path d="M0,4.5 L0,-2" stroke="{vein}" stroke-width=".8" opacity=".9"/>')


def blossom(x, y, r=9, fill="#F9C6D3", center="#E8708F"):
    out = [f'<g transform="translate({x:.1f},{y:.1f})">']
    for i in range(5):
        out.append(f'<g transform="rotate({i * 72}) translate(0,{-r * .62:.1f}) scale({r / 9:.2f})">'
                   f'<path d="{PETAL}" fill="{fill}" transform="rotate(180)"/></g>')
    out.append(f'<circle r="{r * .22:.1f}" fill="{center}"/>')
    for i in range(5):
        out.append(f'<circle cx="0" cy="{-r * .38:.1f}" r=".9" fill="#FFF3C4" transform="rotate({i * 72 + 36})"/>')
    out.append('</g>')
    return "".join(out)


def smooth_loop(pts):
    """Catmull-Rom fechado -> path Bézier suave."""
    n = len(pts)
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} "
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} "
    return d + "Z"
