#!/usr/bin/env python3
"""Lager bank_var.js: nye varianter av eksamensoppgavetypene med fasit.

Hvert svar regnes eksakt med sympy og kontrolleres med en uavhengig numerisk
metode (scipy). Malene for flate og Gauss kontrolleres i tillegg mot tallene i
løsningsforslagene (Ord25 11, Ord25 13, Mai26 12). Feiler én kontroll, stopper
skriptet uten å skrive fila.
"""
import json, math, random, re, sys
import sympy as sp
import numpy as np
from scipy.integrate import quad, dblquad, tplquad

random.seed(20261217)
x, y, z, t, u, v, r, th = sp.symbols('x y z t u v r theta', real=True)
CHECKS = []

def check(name, a, b, rel=1e-6):
    a, b = float(a), float(b)
    ok = abs(a - b) <= rel * max(1.0, abs(b))
    CHECKS.append((name, ok, a, b))
    if not ok:
        print('FEIL I KONTROLL:', name, a, b); sys.exit(1)

def js(e):
    """sympy-uttrykk -> streng som mathjs i plattformen forstår."""
    s = str(sp.simplify(e)) if not isinstance(e, (list, tuple)) else '[' + ', '.join(js(k) for k in e) + ']'
    s = s.replace('**', '^')
    if re.search(r'[A-DF-Za-df-z_]\w*\(', s.replace('sqrt(', '').replace('sin(', '').replace('cos(', '').replace('exp(', '').replace('log(', '').replace('atan(', '')):
        raise ValueError('ukjent funksjon i ' + s)
    return s

def tex(e):
    # Til bruk INNE i matematikk ($...$): ingen egne dollartegn. Vektorer skrives som (a, b, c).
    if isinstance(e, sp.MatrixBase):
        return '\\left(' + ',\\ '.join(sp.latex(sp.simplify(x)) for x in e) + '\\right)'
    return sp.latex(e)

def Lx(e):
    return '$' + sp.latex(e) + '$'

def pretty(e):
    s = str(e).replace('**', '^').replace('*', '·').replace('exp(', 'e^(').replace('-', '−')
    return 'u = ' + s

def fnum(a, d=4):
    return f'{float(a):.{d}f}'

QS, SETS = [], {}

def add_set(key, navn, kort, info):
    SETS[key] = {'navn': navn, 'kort': kort, 'info': info, 'fag': 'matte'}

def q(set_, nr, topic, title, text, fields, steg, explain, komp, refkey, maxp=1):
    QS.append({'id': f'v{set_}q{nr}', 'oving': set_, 'nr': nr, 'status': 'ny', 'maxp': maxp, 'topic': topic, 'title': title,
               'text': text, 'fields': fields, 'hints': [], 'explain': explain, 'komp': komp, 'forel': '',
               'sitat': None, 'refs': [{'key': refkey, 'title': komp, 'start': 0, 'end': 0, 'focus': 0, 'side': 0}],
               'steg': steg, 'fig': None, 'base': None, 'variant': True})

# =====================================================================
# 1) Parametrisk flate a–d  (mal: Ord25 oppg. 11)
# r(u,v) = (v cos u, v sin u, k v^2), 0<=u<=U, a<=v<=b
# =====================================================================
def flate(k, U, a, b):
    R = sp.Matrix([v*sp.cos(u), v*sp.sin(u), k*v**2])
    ru, rv = R.diff(u), R.diff(v)
    N = ru.cross(rv)
    nN = sp.sqrt(sp.simplify(N.dot(N)))
    nN = sp.simplify(sp.factor(nN))
    nN_s = v*sp.sqrt(1 + 4*k**2*v**2)
    check(f'|N| k={k}', sp.N((nN - nN_s).subs(v, 1.37)), 0)
    A = sp.simplify(sp.integrate(nN_s, (v, a, b), (u, 0, U)))
    A_num = dblquad(lambda vv, uu: vv*math.sqrt(1+4*float(k)**2*vv*vv), 0, float(U), float(a), float(b))[0]
    check(f'A k={k} U={U} [{a},{b}]', A, A_num)
    I = sp.integrate(k*v**2*nN_s, (v, a, b), (u, 0, U))
    zbar = sp.simplify(I / A)
    zb_num = dblquad(lambda vv, uu: float(k)*vv*vv*vv*math.sqrt(1+4*float(k)**2*vv*vv), 0, float(U), float(a), float(b))[0] / A_num
    check(f'zbar k={k}', zbar, zb_num)
    V = sp.simplify(sp.integrate(r, (z, 0, k*r**2), (r, a, b), (th, 0, U)))
    V_num = tplquad(lambda zz, rr, tt: rr, 0, float(U), float(a), float(b), 0, lambda tt, rr: float(k)*rr*rr)[0]
    check(f'V k={k}', V, V_num)
    return dict(R=R, ru=ru, rv=rv, N=N, nN=nN_s, A=A, zbar=zbar, V=V, k=k, U=U, a=a, b=b)

# Kontroll mot løsningsforslaget Ord25 11: A = 19π/3, z̄ ≈ 2.832, V ≈ 21.598
F0 = flate(sp.Rational(1, 2), sp.pi, sp.sqrt(3), 2*sp.sqrt(2))
check('Ord25 11b A=19π/3', F0['A'], 19*math.pi/3)
check('Ord25 11c z̄≈2.8316', F0['zbar'], 2.8315789473684223, rel=1e-9)
check('Ord25 11d V≈21.598', F0['V'], 21.59844949342984, rel=1e-9)

FLATE_PAR = [  # (k, U, a, b) – gir pene tall
    (sp.Rational(1, 2), sp.pi, sp.sqrt(3), 2*sp.sqrt(2)),
    (sp.Rational(1, 2), 2*sp.pi, 0, sp.sqrt(3)),
    (sp.Rational(1, 2), sp.pi/2, 0, 2*sp.sqrt(2)),
    (1, 2*sp.pi, 0, 1),
    (sp.Rational(1, 2), sp.pi, 0, sp.sqrt(8)),
    (1, sp.pi, 0, sp.sqrt(2)),
    (sp.Rational(1, 4), 2*sp.pi, 0, 2*sp.sqrt(2)),
    (sp.Rational(1, 2), 2*sp.pi, sp.sqrt(3), sp.sqrt(8)),
]

def flate_steg(F, med_svar=True):
    k, U, a, b = F['k'], F['U'], F['a'], F['b']
    s = [
        {'t': 'Partiellderiverte', 's': f"$\\mathbf r_u = {tex(F['ru'].T)}$ og $\\mathbf r_v = {tex(F['rv'].T)}$. Deriver hver komponent for seg; den andre variabelen holdes fast.", 'ref': '1.9'},
        {'t': 'Normalvektor', 's': f"$\\mathbf N = \\mathbf r_u\\times\\mathbf r_v = {tex(F['N'].T)}$. Bruk determinanten med $\\mathbf i,\\mathbf j,\\mathbf k$ i første rad.", 'ref': '1.9'},
        {'t': 'Lengden av N', 's': f"$|\\mathbf N| = \\sqrt{{N_1^2+N_2^2+N_3^2}} = {tex(F['nN'])}$ (siden $v\\ge 0$). Bruk $\\cos^2u+\\sin^2u=1$.", 'ref': '1.9'},
        {'t': 'Areal', 's': f"$A=\\iint_D |\\mathbf N|\\,dA = \\int_0^{{{tex(U)}}}\\!\\int_{{{tex(a)}}}^{{{tex(b)}}} {tex(F['nN'])}\\,dv\\,du = {tex(F['A'])}$. Substitusjon $w = 1+{tex(4*k**2)}v^2$ gir det indre integralet, eller bruk `sp.integrate`.", 'ref': '1.9'},
        {'t': 'z-koordinaten til tyngdepunktet', 's': f"$\\bar z = \\frac1A\\iint_S z\\,dS = \\frac1A\\iint_D {tex(k*v**2)}\\cdot {tex(F['nN'])}\\,dA \\approx {fnum(F['zbar'])}$. I `dblquad` er første argument den indre variabelen: `f = lambda v, u: ...`.", 'ref': '1.9'},
        {'t': 'Volum i sylinderkoordinater', 's': f"Flaten er $z = {tex(k)}r^2$ i sylinderkoordinater, så $V=\\int_0^{{{tex(U)}}}\\!\\int_{{{tex(a)}}}^{{{tex(b)}}}\\!\\int_0^{{{tex(k)}r^2}} r\\,dz\\,dr\\,d\\theta = {tex(F['V'])}\\approx {fnum(F['V'])}$. Husk Jacobi-faktoren $r$.", 'ref': '1.6'},
    ]
    return s

def flate_kode(F):
    k, U, a, b = F['k'], F['U'], F['a'], F['b']
    pyn = lambda e: str(e).replace('pi', 'np.pi').replace('sqrt', 'np.sqrt')
    A = F['A']
    c = (f"import numpy as np\nfrom scipy.integrate import dblquad, tplquad\n"
         f"A = {pyn(sp.nsimplify(A))}\n"
         f"f = lambda v, u: ({pyn(k)})*v**2 * v*np.sqrt(1 + {pyn(4*k**2)}*v**2) / A\n"
         f"zbar = dblquad(f, 0, {pyn(U)}, {pyn(a)}, {pyn(b)})[0]\n"
         f"V = tplquad(lambda z, r, th: r, 0, {pyn(U)}, {pyn(a)}, {pyn(b)}, 0, lambda th, r: ({pyn(k)})*r**2)[0]\n"
         f"print(zbar, V)")
    env = {}
    exec(c.replace('print(zbar, V)', ''), env)
    check('kode z̄ ' + str((k, U, a, b)), env['zbar'], F['zbar'], rel=1e-8)
    check('kode V ' + str((k, U, a, b)), env['V'], F['V'], rel=1e-8)
    return c

def flate_tekst(F):
    k, U, a, b = F['k'], F['U'], F['a'], F['b']
    return (f"La $S$ være den parametriske flaten gitt ved\n$$\\mathbf r(u,v) = \\big(v\\cos u,\\ v\\sin u,\\ {tex(k*v**2)}\\big),\\quad 0\\le u\\le {tex(U)},\\ {tex(a)}\\le v\\le {tex(b)}.$$\n")

add_set('VF', 'Varianter: parametrisk flate (del 2)', 'VF', 'Løst eksempel → med hull → selv · samme oppgavetype som Ord25 11 og Feb26 13')
nr = 1
for idx, par in enumerate(FLATE_PAR):
    F = flate(*par)
    kode = flate_kode(F)
    steg = flate_steg(F)
    ru, rv, N = js(list(F['ru'])), js(list(F['rv'])), js(list(F['N']))
    nN, A, V = js(F['nN']), js(F['A']), js(F['V'])
    base = flate_tekst(F)
    if idx == 0:   # Løst eksempel
        txt = (base + "\n**Løst eksempel.** Regn gjennom hvert steg selv på ark før du leser videre.\n\n"
               + "\n\n".join(f"**{i+1}. {s['t']}.** {s['s']}" for i, s in enumerate(steg))
               + f"\n\nPython for c) og d):\n```python\n{kode}\n```\n\nNår du har regnet gjennom alt selv: skriv arealet $A$ under.\n\n$A=$ {{{{f1}}}}")
        q('VF', nr, 'flate', 'Løst eksempel: parametrisk flate a–d', txt, [{'i': 1, 'kind': 'expr', 'ans': A}], steg,
          f"A = {Lx(F['A'])}, z̄ ≈ {fnum(F['zbar'])}, V = {Lx(F['V'])} ≈ {fnum(F['V'])}. Samme tall som i løsningsforslaget til Ord25 oppg. 11.", '§1.9 Parametriske flater', '1.9', maxp=9)
    elif idx in (1, 2):  # Med hull: r_u, r_v og N er gitt
        txt = (base + f"\n**Med hull.** Gitt: $\\mathbf r_u = {tex(F['ru'].T)}$, $\\mathbf r_v = {tex(F['rv'].T)}$ og $\\mathbf N = {tex(F['N'].T)}$.\n\n"
               "a) Regn ut $|\\mathbf N|$ (bruk at $v\\ge 0$).\n\n$|\\mathbf N|=$ {{f1}}\n\n"
               "b) Regn ut arealet $A$ eksakt.\n\n$A=$ {{f2}}\n\n"
               "c) Regn ut $z$-koordinaten til tyngdepunktet, $\\bar z = \\frac1A\\iint_S z\\,dS$, med `dblquad` (4 desimaler).\n\n$\\bar z\\approx$ {{f3}}\n\n"
               "d) Regn ut volumet av legemet under flaten og over $xy$-planet med `tplquad` i sylinderkoordinater.\n\n$V\\approx$ {{f4}}")
        q('VF', nr, 'flate', f'Med hull: parametrisk flate ({idx})', txt,
          [{'i': 1, 'kind': 'expr', 'ans': nN}, {'i': 2, 'kind': 'expr', 'ans': A},
           {'i': 3, 'kind': 'expr', 'ans': fnum(F['zbar'], 6), 'tol': 0.002}, {'i': 4, 'kind': 'expr', 'ans': fnum(F['V'], 6), 'tol': 0.002}],
          steg, f"|N| = {Lx(F['nN'])}, A = {Lx(F['A'])}, z̄ ≈ {fnum(F['zbar'])}, V ≈ {fnum(F['V'])}.\n\nKode:\n```python\n{kode}\n```", '§1.9 Parametriske flater', '1.9', maxp=9)
    else:  # Selv
        txt = (base + "\na) Regn ut $\\mathbf r_u$ og $\\mathbf r_v$. Skriv vektorer som `[a, b, c]`.\n\n$\\mathbf r_u=$ {{f1}}\n\n$\\mathbf r_v=$ {{f2}}\n\n"
               "Regn ut $\\mathbf N = \\mathbf r_u\\times\\mathbf r_v$.\n\n$\\mathbf N=$ {{f3}}\n\nRegn ut $|\\mathbf N|$ (bruk at $v\\ge0$).\n\n$|\\mathbf N|=$ {{f4}}\n\n"
               "b) Regn ut arealet $A$ eksakt (for hånd eller med `sp.integrate`).\n\n$A=$ {{f5}}\n\n"
               "c) Regn ut $\\bar z = \\frac1A\\iint_S z\\,dS$ med `dblquad` (4 desimaler).\n\n$\\bar z\\approx$ {{f6}}\n\n"
               "d) Sett opp volumet under flaten og over $xy$-planet i sylinderkoordinater, og regn det ut med `tplquad`.\n\n$V\\approx$ {{f7}}")
        q('VF', nr, 'flate', f'Selv: parametrisk flate ({idx-2})', txt,
          [{'i': 1, 'kind': 'expr', 'ans': ru}, {'i': 2, 'kind': 'expr', 'ans': rv}, {'i': 3, 'kind': 'expr', 'ans': N},
           {'i': 4, 'kind': 'expr', 'ans': nN}, {'i': 5, 'kind': 'expr', 'ans': A},
           {'i': 6, 'kind': 'expr', 'ans': fnum(F['zbar'], 6), 'tol': 0.002}, {'i': 7, 'kind': 'expr', 'ans': fnum(F['V'], 6), 'tol': 0.002}],
          steg, f"$\\mathbf r_u = {tex(F['ru'])}$, $\\mathbf r_v = {tex(F['rv'])}$, $\\mathbf N = {tex(F['N'])}$, |N| = {Lx(F['nN'])}, A = {Lx(F['A'])}, z̄ ≈ {fnum(F['zbar'])}, V ≈ {fnum(F['V'])}.\n\nKode:\n```python\n{kode}\n```", '§1.9 Parametriske flater', '1.9', maxp=9)
    nr += 1

# =====================================================================
# 2) Fluks og Gauss  (maler: Mai26 oppg. 12 og Ord25 oppg. 13)
# =====================================================================
def sylinder(R, H, a, b, c):
    """Sylinder x^2+y^2<=R^2, 0<=z<=H, F=(x+a, y+b, c z). Utoverpekende normal."""
    phi, zz, rr = sp.symbols('phi zz rr', real=True)
    F = lambda X, Y, Z: sp.Matrix([X + a, Y + b, c*Z])
    # direkte flateintegraler
    topp = sp.integrate((F(rr*sp.cos(phi), rr*sp.sin(phi), H).dot(sp.Matrix([0, 0, 1])))*rr, (rr, 0, R), (phi, 0, 2*sp.pi))
    bunn = sp.integrate((F(rr*sp.cos(phi), rr*sp.sin(phi), 0).dot(sp.Matrix([0, 0, -1])))*rr, (rr, 0, R), (phi, 0, 2*sp.pi))
    vegg = sp.integrate(F(R*sp.cos(phi), R*sp.sin(phi), zz).dot(sp.Matrix([sp.cos(phi), sp.sin(phi), 0]))*R, (phi, 0, 2*sp.pi), (zz, 0, H))
    div = sp.diff(x + a, x) + sp.diff(y + b, y) + sp.diff(c*z, z)
    tot = div*sp.pi*R**2*H
    check(f'Gauss sylinder {R,H,a,b,c}', topp + bunn + vegg, tot)
    # uavhengig numerisk kontroll av veggen
    vn = dblquad(lambda p, Z: float((R*math.cos(p) + a)*math.cos(p) + (R*math.sin(p) + b)*math.sin(p))*R, 0, H, 0, 2*math.pi)[0]
    check(f'vegg numerisk {R,H,a,b,c}', vegg, vn)
    return dict(R=R, H=H, a=a, b=b, c=c, topp=sp.simplify(topp), bunn=sp.simplify(bunn), vegg=sp.simplify(vegg), div=div, tot=sp.simplify(tot))

S0 = sylinder(3, 5, 6, 6, 1)
check('Mai26 12 topp = 45π', S0['topp'], 45*math.pi)
check('Mai26 12 bunn = 0', S0['bunn'], 0)
check('Mai26 12 vegg = 90π', S0['vegg'], 90*math.pi)

def paraboloid(h, al, be, ga, de, ka):
    """T: 0<=z<=h-r^2. F=(al x, be x z + ga y, de + ka z). S1 = bunnen (z=0), S2 = paraboloiden."""
    div = al + ga + ka
    V = sp.integrate(r, (z, 0, h - r**2), (r, 0, sp.sqrt(h)), (th, 0, 2*sp.pi))
    phi1 = sp.integrate(-(de + ka*0)*r, (r, 0, sp.sqrt(h)), (th, 0, 2*sp.pi))
    phi2 = div*V - phi1
    # uavhengig kontroll: fluks gjennom paraboloiden direkte, r(r,θ) = (r cos θ, r sin θ, h - r^2)
    rr_, tt_ = sp.symbols('rr tt', positive=True)
    P = sp.Matrix([rr_*sp.cos(tt_), rr_*sp.sin(tt_), h - rr_**2])
    Nn = P.diff(rr_).cross(P.diff(tt_))           # = (2r^2 cosθ, 2r^2 sinθ, r): peker oppover/utover
    Fv = sp.Matrix([al*P[0], be*P[0]*P[2] + ga*P[1], de + ka*P[2]])
    integrand = sp.lambdify((rr_, tt_), sp.simplify(Fv.dot(Nn)), 'math')
    direct = dblquad(lambda R_, T_: integrand(R_, T_), 0, 2*math.pi, 0, math.sqrt(float(h)))[0]
    check(f'paraboloid direkte {h,al,be,ga,de,ka}', phi2, direct, rel=1e-7)
    return dict(h=h, al=al, be=be, ga=ga, de=de, ka=ka, div=div, V=sp.simplify(V), phi1=sp.simplify(phi1), phi2=sp.simplify(phi2))

# Kontroll av malen mot Ord25 13 (der bunnen har et e-ledd): div = 6, V = 9π/2
PT = paraboloid(3, 2, 3, 2, 4, 2)
check('Ord25 13: V = 9π/2', PT['V'], 9*math.pi/2)
check('Ord25 13: div = 6', PT['div'], 6)

add_set('VG', 'Varianter: fluks og Gauss (del 2)', 'VG', 'Løst eksempel → med hull → selv · samme oppgavetype som Mai26 12 og Ord25 13')
gsteg_syl = lambda S: [
    {'t': 'Normalvektorer', 's': 'Topp: $\\hat{\\mathbf N}=\\mathbf k$. Bunn: $\\hat{\\mathbf N}=-\\mathbf k$. Vegg: $\\hat{\\mathbf N}=\\cos\\varphi\\,\\mathbf i+\\sin\\varphi\\,\\mathbf j$ (peker ut fra $z$-aksen).', 'ref': '2.7'},
    {'t': 'Topp og bunn', 's': f"Topp ($z={S['H']}$): $\\mathbf F\\cdot\\mathbf k = {tex(S['c']*S['H'])}$, konstant, så fluksen er ${tex(S['c']*S['H'])}\\cdot\\pi\\cdot{S['R']}^2 = {tex(S['topp'])}$. Bunn ($z=0$): $\\mathbf F\\cdot(-\\mathbf k) = -{tex(S['c'])}\\cdot 0 = 0$.", 'ref': '2.7'},
    {'t': 'Divergens', 's': f"$\\nabla\\cdot\\mathbf F = 1 + 1 + {S['c']} = {S['div']}$.", 'ref': '2.2'},
    {'t': 'Gauss', 's': f"$\\iint_S \\mathbf F\\cdot\\hat{{\\mathbf N}}\\,dS = \\iiint_V \\nabla\\cdot\\mathbf F\\,dV = {S['div']}\\cdot \\pi\\cdot {S['R']}^2\\cdot {S['H']} = {tex(S['tot'])}$.", 'ref': '2.8'},
    {'t': 'Veggen', 's': f"Veggen = total − topp − bunn $= {tex(S['tot'])} - {tex(S['topp'])} - 0 = {tex(S['vegg'])}$. Kontroll direkte: $\\int_0^{{{S['H']}}}\\!\\int_0^{{2\\pi}} ({S['R']} + {S['a']}\\cos\\varphi + {S['b']}\\sin\\varphi)\\,{S['R']}\\,d\\varphi\\,dz = {tex(S['vegg'])}$.", 'ref': '2.8'},
]
SYL_PAR = [(3, 5, 6, 6, 1), (2, 3, 6, 6, 1), (1, 4, 2, 3, 2), (2, 5, 1, 4, 3), (3, 2, 5, 0, 2), (2, 2, 0, 7, 1)]
nr = 1
for idx, par in enumerate(SYL_PAR):
    S = sylinder(*par)
    R_, H_, a_, b_, c_ = par
    Ftex = f"\\mathbf F = \\begin{{pmatrix}} x+{a_} \\\\ y+{b_} \\\\ {'' if c_ == 1 else c_}z \\end{{pmatrix}}"
    base = (f"Flaten $S$ er en lukket sylinder (topp og bunn med) med sentrum langs $z$-aksen, radius ${R_}$, bunn i $xy$-planet og høyde ${H_}$. "
            f"Den er orientert med normalvektor ut av sylinderen. Vektorfeltet er ${Ftex}$.\n\n")
    steg = gsteg_syl(S)
    if idx == 0:
        txt = (base + "**Løst eksempel.** Regn hvert steg selv på ark før du leser videre.\n\n" + "\n\n".join(f"**{i+1}. {s['t']}.** {s['s']}" for i, s in enumerate(steg))
               + "\n\nNår du har regnet gjennom: skriv fluksen gjennom veggen.\n\n$\\iint_{S_{vegg}}\\mathbf F\\cdot\\hat{\\mathbf N}\\,dS=$ {{f1}}")
        q('VG', nr, 'gauss', 'Løst eksempel: fluks ut av sylinder', txt, [{'i': 1, 'kind': 'expr', 'ans': js(S['vegg'])}], steg,
          f"Topp {Lx(S['topp'])}, bunn 0, vegg {Lx(S['vegg'])}, totalt {Lx(S['tot'])}. Samme tall som løsningsforslaget til Mai26 oppg. 12.", '§2.8 Divergenssetningen', '2.8', maxp=9)
    else:
        hull = idx in (1, 2)
        txt = base + ("**Med hull.** Normalvektorene er $\\mathbf k$ (topp), $-\\mathbf k$ (bunn) og $\\cos\\varphi\\,\\mathbf i+\\sin\\varphi\\,\\mathbf j$ (vegg).\n\n" if hull else "") + \
            ("a) Regn ut fluksen gjennom toppen.\n\n{{f1}}\n\nb) Regn ut fluksen gjennom bunnen.\n\n{{f2}}\n\nc) Regn ut $\\nabla\\cdot\\mathbf F$.\n\n{{f3}}\n\n"
             "d) Bruk Gauss til å finne total fluks ut av $S$.\n\n{{f4}}\n\ne) Finn fluksen gjennom veggen.\n\n{{f5}}")
        q('VG', nr, 'gauss', ('Med hull' if hull else 'Selv') + f': fluks ut av sylinder ({idx})', txt,
          [{'i': 1, 'kind': 'expr', 'ans': js(S['topp'])}, {'i': 2, 'kind': 'expr', 'ans': js(S['bunn'])}, {'i': 3, 'kind': 'expr', 'ans': js(S['div'])},
           {'i': 4, 'kind': 'expr', 'ans': js(S['tot'])}, {'i': 5, 'kind': 'expr', 'ans': js(S['vegg'])}], steg,
          f"Topp {Lx(S['topp'])}, bunn {Lx(S['bunn'])}, ∇·F = {S['div']}, totalt {Lx(S['tot'])}, vegg {Lx(S['vegg'])}.", '§2.8 Divergenssetningen', '2.8', maxp=9)
    nr += 1

PAR_PAR = [(3, 2, 3, 2, 4, 2), (4, 1, 1, 2, 3, 3), (1, 2, 5, 1, 2, 1), (2, 3, 2, 1, 1, 2)]
for idx, par in enumerate(PAR_PAR):
    P = paraboloid(*par)
    h, al, be, ga, de, ka = par
    Ftex = f"\\mathbf F = \\begin{{pmatrix}} {al}x \\\\ {be}xz+{ga}y \\\\ {de}+{ka}z \\end{{pmatrix}}"
    steg = [
        {'t': 'Divergens', 's': f"$\\nabla\\cdot\\mathbf F = {al} + {ga} + {ka} = {P['div']}$ (leddet ${be}xz$ deriveres med hensyn på $y$ og gir 0).", 'ref': '2.2'},
        {'t': 'Fluks gjennom bunnen $S_1$', 's': f"Bunnen er disken $x^2+y^2\\le {h}$ i $z=0$ med $\\hat{{\\mathbf N}}_1=-\\mathbf k$. Der er $\\mathbf F\\cdot(-\\mathbf k) = -({de}+{ka}\\cdot 0) = -{de}$, konstant. Arealet er ${h}\\pi$, så $\\Phi_1 = {tex(P['phi1'])}$.", 'ref': '2.7'},
        {'t': 'Volumet', 's': f"I sylinderkoordinater: $V = \\int_0^{{2\\pi}}\\!\\int_0^{{\\sqrt{{{h}}}}}\\!\\int_0^{{{h}-r^2}} r\\,dz\\,dr\\,d\\theta = {tex(P['V'])}$.", 'ref': '1.6'},
        {'t': 'Gauss', 's': f"$\\Phi_1+\\Phi_2 = \\iiint_T\\nabla\\cdot\\mathbf F\\,dV = {P['div']}\\cdot{tex(P['V'])}$, så $\\Phi_2 = {P['div']}\\cdot{tex(P['V'])} - ({tex(P['phi1'])}) = {tex(P['phi2'])}$.", 'ref': '2.8'},
    ]
    txt = (f"Legemet $T$ er avgrenset av paraboloiden $z = {h} - r^2$ (i sylinderkoordinater) og $xy$-planet. Randen i $xy$-planet kaller vi $S_1$, resten av randen $S_2$. "
           f"Begge er orientert med normal bort fra $T$. Vektorfeltet er ${Ftex}$.\n\n"
           "a) Regn ut $\\nabla\\cdot\\mathbf F$.\n\n{{f1}}\n\nb) Regn ut fluksen $\\Phi_1$ gjennom $S_1$.\n\n{{f2}}\n\nc) Regn ut volumet av $T$.\n\n{{f3}}\n\n"
           "d) Bruk Gauss til å finne fluksen $\\Phi_2$ gjennom $S_2$.\n\n{{f4}}")
    q('VG', nr, 'gauss', f'Selv: fluks gjennom paraboloide ({idx+1})', txt,
      [{'i': 1, 'kind': 'expr', 'ans': js(P['div'])}, {'i': 2, 'kind': 'expr', 'ans': js(P['phi1'])}, {'i': 3, 'kind': 'expr', 'ans': js(P['V'])}, {'i': 4, 'kind': 'expr', 'ans': js(P['phi2'])}],
      steg, f"∇·F = {P['div']}, Φ₁ = {Lx(P['phi1'])}, V = {Lx(P['V'])}, Φ₂ = {Lx(P['phi2'])}. Φ₂ er også kontrollert ved å regne flateintegralet direkte.", '§2.8 Divergenssetningen', '2.8', maxp=9)
    nr += 1

# =====================================================================
# 3) PDE-løsning ved innsetting (flervalg)
# =====================================================================
add_set('VP', 'Varianter: PDE-løsning ved innsetting', 'VP', 'Flervalg · sjekk med sp.diff · samme type som Ord25 9, Feb26 9, Mai26 8')
def residual_heat(U_, c):
    return sp.simplify(sp.diff(U_, t) - c*sp.diff(U_, x, 2))
def residual_wave(U_, c2):
    return sp.simplify(sp.diff(U_, t, 2) - c2*sp.diff(U_, x, 2))
nr = 1
for (c, m) in [(4, 3), (2, 1), (9, 2), (3, 2), (5, 1), (1, 3), (2, 3), (6, 1), (3, 4)]:
    lam = c*m**2
    pool = [sp.exp(-c*t)*sp.sin(m*x), sp.exp(-lam*t)*sp.sin((m+1)*x), sp.exp(-m*t)*sp.sin(m*x), sp.exp(lam*t)*sp.sin(m*x),
            sp.sin(m*x*t), sp.exp(-(lam+1)*t)*sp.sin(m*x), sp.exp(-c*m*t)*sp.sin(m*x)]
    good = sp.exp(-lam*t)*sp.sin(m*x)
    cands = [good]
    for cc in pool:  # bare feil alternativer, og ingen duplikater
        if residual_heat(cc, c) != 0 and all(sp.simplify(cc - d) != 0 for d in cands) and len(cands) < 6: cands.append(cc)
    res = [residual_heat(cc, c) == 0 for cc in cands]
    assert res[0] and sum(res) == 1, ('flere/ingen riktige', c, m, res)
    CHECKS.append((f'PDE varme c={c} m={m}: nøyaktig ett riktig alternativ', True, 1, 1))
    opts = [pretty(cc) for cc in cands]
    order = list(range(len(opts))); random.shuffle(order)
    opts_s = [opts[i] for i in order]
    txt = f"Vi har varmelikningen $u_t = {c}\\,u_{{xx}}$. Hvilken funksjon er en løsning?\n\n{{{{f1}}}}"
    steg = [{'t': 'Sett inn', 's': f"For $u = e^{{-\\lambda t}}\\sin(mx)$ er $u_t = -\\lambda u$ og $u_{{xx}} = -m^2 u$. Likningen gir $-\\lambda = -{c}m^2$, altså $\\lambda = {c}m^2$.", 'ref': '3.1'},
            {'t': 'Sjekk med Python', 's': f"`u = sp.exp(-{lam}*t)*sp.sin({m}*x)` og `sp.simplify(sp.diff(u, t) - {c}*sp.diff(u, x, 2))` gir 0.", 'ref': '3.1'}]
    q('VP', nr, 'pde', f'Varmelikning: hvilken er løsning? ({nr})', txt, [{'i': 1, 'kind': 'choice', 'options': opts_s, 'ans': opts[0]}], steg,
      f"Riktig: u = {Lx(cands[0])}, fordi λ = {c}·m² = {c}·{m}² = {lam} for u_t = {c}u_xx. De andre gir rest ≠ 0 når de settes inn.", '§3.1 PDE: løsning ved innsetting', '3.1', maxp=4)
    nr += 1
for (c, m) in [(2, 1), (3, 2), (1, 4), (4, 1)]:
    good = sp.sin(m*x)*sp.cos(c*m*t)
    pool = [sp.sin(m*x)*sp.cos(m*t), sp.sin(m*x)*sp.cos(c**2*m*t), sp.exp(-c*m*t)*sp.sin(m*x), sp.sin(m*x)*sp.cos(c*t), sp.sin(2*m*x)*sp.cos(c*m*t), sp.sin(m*x)*sp.cos((c*m+1)*t)]
    cands = [good]
    for cc in pool:
        if residual_wave(cc, c**2) != 0 and all(sp.simplify(cc - d) != 0 for d in cands) and len(cands) < 5: cands.append(cc)
    res = [residual_wave(cc, c**2) == 0 for cc in cands]
    assert res[0] and sum(res) == 1, ('bølge', c, m, res)
    CHECKS.append((f'PDE bølge c={c} m={m}: nøyaktig ett riktig alternativ', True, 1, 1))
    opts = [pretty(cc) for cc in cands]
    order = list(range(len(opts))); random.shuffle(order)
    txt = f"Vi har bølgelikningen $u_{{tt}} = {c**2}\\,u_{{xx}}$. Hvilken funksjon er en løsning?\n\n{{{{f1}}}}"
    steg = [{'t': 'Sett inn', 's': f"For $u = \\sin(mx)\\cos(\\omega t)$ er $u_{{tt}} = -\\omega^2u$ og $u_{{xx}} = -m^2u$. Likningen gir $\\omega^2 = {c**2}m^2$, altså $\\omega = {c}m$.", 'ref': '3.1'}]
    q('VP', nr, 'pde', f'Bølgelikning: hvilken er løsning? ({nr})', txt, [{'i': 1, 'kind': 'choice', 'options': [opts[i] for i in order], 'ans': opts[0]}], steg,
      f"Riktig: u = {Lx(good)}, fordi ω² = {c**2}·m², så ω = {c}·{m} = {c*m} for u_tt = {c**2}u_xx.", '§3.1 PDE: løsning ved innsetting', '3.1', maxp=4)
    nr += 1

# =====================================================================
# 4) Varmelikningskode: indekser og stabilitet (mal: Ord25 oppg. 12)
# x = linspace(0, L, m+2) -> dx = L/(m+1); t = linspace(0, T, N) -> dt = T/(N-1); stabil når c2*dt/dx^2 < 0.5
# =====================================================================
add_set('VK', 'Varianter: varmelikningskode (indekser og stabilitet)', 'VK', 'Samme type som Ord25 12')
def minN(c2, L, T, m):
    N = 2
    while not (c2*(T/(N-1))/(L/(m+1))**2 < 0.5):
        N += 1
    return N
check('Ord25 12b minste N (m=20) = 46', minN(0.04, 2, 5, 20), 46)
nr = 1
for (L, T, m, N, c2, xi, ti) in [(2, 5, 9, 301, 0.04, 2, 120), (1, 2, 9, 201, 0.01, 3, 50), (4, 10, 19, 501, 0.1, 5, 250), (2, 4, 19, 401, 0.05, 10, 100), (3, 6, 29, 601, 0.02, 12, 300)]:
    dx = sp.Rational(L, m+1); dt = sp.Rational(T, N-1)
    x0 = xi*dx; t0 = ti*dt
    xs = np.linspace(0, L, m+2); ts = np.linspace(0, T, N)
    check(f'dx {L,m}', xs[1]-xs[0], dx); check(f'dt {T,N}', ts[1]-ts[0], dt)
    check(f'x[p] {xi}', xs[xi], x0); check(f't[q] {ti}', ts[ti], t0)
    mm = 2*m
    nmin = minN(c2, L, T, mm)
    stab = sp.Rational(int(c2*1000), 1000)*dt/dx**2
    txt = (f"Koden løser $u_t = {c2}\\,u_{{xx}}$ for $0\\le x\\le {L}$ og $0\\le t\\le {T}$ med\n```python\nx = np.linspace(0, {L}, m + 2)   # m = {m}\nt = np.linspace(0, {T}, N)       # N = {N}\nu = np.zeros((x.size, N))\n```\n"
           f"a) Hva er $\\Delta x$?\n\n{{{{f1}}}}\n\nb) Hva er $\\Delta t$?\n\n{{{{f2}}}}\n\nc) For hvilke indekser $p, q$ er `u[p, q]` løsningen i $x = {tex(x0)}$, $t = {tex(t0)}$?\n\n$p=$ {{{{f3}}}}  $q=$ {{{{f4}}}}\n\n"
           f"d) Stabilitet krever ${c2}\\,\\Delta t/\\Delta x^2 < 0.5$. Hvis $m = {mm}$, hva er minste $N$ som gir stabil løsning?\n\n{{{{f5}}}}")
    steg = [{'t': 'Steglengder', 's': f"`linspace(0, {L}, m+2)` har $m+1$ delintervaller, så $\\Delta x = {L}/(m+1) = {tex(dx)}$. `linspace(0, {T}, N)` har $N-1$ delintervaller, så $\\Delta t = {T}/(N-1) = {tex(dt)}$.", 'ref': '3.3.4'},
            {'t': 'Indekser', 's': f"$p = x/\\Delta x = {tex(x0)}/{tex(dx)} = {xi}$ og $q = t/\\Delta t = {tex(t0)}/{tex(dt)} = {ti}$. Første indeks i `u` er $x$, andre er $t$.", 'ref': '3.3.4'},
            {'t': 'Stabilitet', 's': f"Med $m={mm}$ er $\\Delta x = {L}/{mm+1}$. Krav: ${c2}\\cdot\\frac{{{T}/(N-1)}}{{({L}/{mm+1})^2}} < 0.5 \\iff N-1 > {sp.nsimplify(c2)}\\cdot{T}\\cdot{mm+1}^2/(0.5\\cdot{L}^2)$. Minste heltall er $N = {nmin}$.", 'ref': '3.3.4'}]
    q('VK', nr, 'tidpde', f'Varmelikningskode: indekser og stabilitet ({nr})', txt,
      [{'i': 1, 'kind': 'expr', 'ans': js(dx), 'tol': 1e-6}, {'i': 2, 'kind': 'expr', 'ans': js(dt), 'tol': 1e-6}, {'i': 3, 'kind': 'expr', 'ans': str(xi)}, {'i': 4, 'kind': 'expr', 'ans': str(ti)}, {'i': 5, 'kind': 'expr', 'ans': str(nmin)}],
      steg, f"Δx = {dx}, Δt = {dt}, p = {xi}, q = {ti}, minste N = {nmin} (funnet ved å teste N = 2, 3, … i Python).", '§3.3.4 Eksplisitt Euler og stabilitet', '3.3.4', maxp=9)
    nr += 1

# =====================================================================
# 5) Del 1-typer (kort svar)
# =====================================================================
add_set('VD', 'Varianter: del 1-typer', 'VD', 'Korte oppgaver med nye tall · div/curl, trippel, polar, linjeintegral, kurvelengde, dobbeltintegral')
nr = 1
def d1(topic, title, text, ans_expr, steg, explain, komp, ref, numcheck=None, tol=None):
    global nr
    f = {'i': 1, 'kind': 'expr', 'ans': js(ans_expr) if not isinstance(ans_expr, str) else ans_expr}
    if tol: f['tol'] = tol
    q('VD', nr, topic, title, text, [f], steg, explain, komp, ref, maxp=4); nr += 1
# divergens
for (A_, B_, C_) in [(2, 3, 1), (1, 4, 2), (3, 1, 5), (4, 2, 3), (5, 3, 2), (2, 5, 4)]:
    F = sp.Matrix([A_*x**2*y, B_*y*z, C_*x*z**2])
    d = sp.diff(F[0], x) + sp.diff(F[1], y) + sp.diff(F[2], z)
    check('div numerisk', d.subs({x: 1.3, y: 0.7, z: 2.1}), (A_*2*1.3*0.7) + B_*2.1 + C_*1.3*2*2.1)
    d1('felt', 'Divergens', f"La $\\mathbf F = ({tex(F[0])},\\ {tex(F[1])},\\ {tex(F[2])})$. Regn ut $\\nabla\\cdot\\mathbf F$.\n\n{{{{f1}}}}", d,
       [{'t': 'Divergens', 's': '$\\nabla\\cdot\\mathbf F = \\partial_x F_1 + \\partial_y F_2 + \\partial_z F_3$.', 'ref': '2.2'}], f"∇·F = {Lx(d)}", '§2.2 Divergens', '2.2')
# curl
for (A_, B_) in [(2, 3), (1, 5), (4, 1), (3, 2), (5, 4), (2, 6)]:
    F = sp.Matrix([A_*y*z, B_*x*z, x*y])
    c_ = sp.Matrix([sp.diff(F[2], y) - sp.diff(F[1], z), sp.diff(F[0], z) - sp.diff(F[2], x), sp.diff(F[1], x) - sp.diff(F[0], y)])
    # uavhengig: numerisk derivasjon
    fF = sp.lambdify((x, y, z), list(F), 'math'); h_ = 1e-6; P0 = (0.8, 1.1, 0.6)
    def dd(i, j):
        p1 = list(P0); p2 = list(P0); p1[j] += h_; p2[j] -= h_
        return (fF(*p1)[i] - fF(*p2)[i])/(2*h_)
    cn = [dd(2, 1) - dd(1, 2), dd(0, 2) - dd(2, 0), dd(1, 0) - dd(0, 1)]
    for i in range(3): check('curl numerisk', c_[i].subs({x: P0[0], y: P0[1], z: P0[2]}), cn[i], rel=1e-5)
    d1('felt', 'Curl', f"La $\\mathbf F = ({tex(F[0])},\\ {tex(F[1])},\\ {tex(F[2])})$. Regn ut $\\nabla\\times\\mathbf F$ og skriv svaret som `[a, b, c]`.\n\n{{{{f1}}}}", list(c_),
       [{'t': 'Curl', 's': '$\\nabla\\times\\mathbf F = (\\partial_y F_3-\\partial_z F_2,\\ \\partial_z F_1-\\partial_x F_3,\\ \\partial_x F_2-\\partial_y F_1)$.', 'ref': '2.2'}],
       f"∇×F = ({', '.join(Lx(k) for k in c_)}). Kontroll: hadde alle tre koeffisientene vært 1, ville F = ∇(xyz), og da er curl 0.", '§2.2 Curl', '2.2')
# trippelintegral
for (a_, fexpr) in [(1, x*y*z), (2, x + y + z), (1, z), (2, x*y), (1, x + z), (2, z), (3, x)]:
    I = sp.integrate(fexpr, (z, 0, x + y), (y, 0, x), (x, 0, a_))
    fn = sp.lambdify((z, y, x), fexpr, 'math')
    In = tplquad(lambda zz, yy, xx: fn(zz, yy, xx), 0, a_, 0, lambda xx: xx, 0, lambda xx, yy: xx + yy)[0]
    check(f'trippel {a_} {fexpr}', I, In)
    d1('trippel', 'Trippelintegral', f"Regn ut $\\displaystyle\\int_0^{{{a_}}}\\!\\int_0^{{x}}\\!\\int_0^{{x+y}} {tex(fexpr)}\\,dz\\,dy\\,dx$ eksakt.\n\n{{{{f1}}}}", I,
       [{'t': 'Innenfra og ut', 's': 'Integrer først med hensyn på $z$ (grenser $0$ til $x+y$), så $y$, så $x$.', 'ref': '1.5'},
        {'t': 'Python', 's': f"`sp.integrate({str(fexpr)}, (z, 0, x + y), (y, 0, x), (x, 0, {a_}))`", 'ref': '1.5'}], f"Svaret er {Lx(I)}.", '§1.5 Trippelintegral', '1.5')
# polar
for (R_, kk, vin) in [(2, 1, sp.pi), (3, 0, sp.pi/2), (1, 2, 2*sp.pi), (2, sp.Rational(1, 2), sp.pi), (3, 1, 2*sp.pi), (2, 2, sp.pi/2), (4, 0, sp.pi)]:
    I = sp.integrate((r**2)**kk * r, (r, 0, R_), (th, 0, vin))
    In = dblquad(lambda rr, tt: (rr*rr)**float(kk)*rr, 0, float(vin), 0, R_)[0]
    check(f'polar {R_} {kk}', I, In)
    omr = {sp.pi: 'den øvre halvdisken ($y\\ge0$)', sp.pi/2: 'kvartdisken i første kvadrant', 2*sp.pi: 'hele disken'}[vin]
    ftex = '1' if kk == 0 else ('x^2+y^2' if kk == 1 else ('(x^2+y^2)^2' if kk == 2 else '\\sqrt{x^2+y^2}'))
    d1('polar', 'Polarkoordinater', f"La $D$ være {omr} med radius ${R_}$ og sentrum i origo. Regn ut $\\iint_D {ftex}\\,dA$ eksakt.\n\n{{{{f1}}}}", I,
       [{'t': 'Polarkoordinater', 's': f"$x^2+y^2 = r^2$ og $dA = r\\,dr\\,d\\theta$. Grensene er $0\\le r\\le {R_}$ og $0\\le\\theta\\le {tex(vin)}$.", 'ref': '1.2'}],
       f"Svaret er {Lx(I)}. Husk Jacobi-faktoren r.", '§1.2 Polarkoordinater', '1.2')
# linjeintegral
for (R_, sgn) in [(2, 1), (3, -1), (1, 1), (4, 1), (2, -1), (5, 1)]:
    Fv = lambda X, Y: (sgn*(-Y), sgn*X)
    I = sp.integrate(sum(a*b for a, b in zip(Fv(R_*sp.cos(t), R_*sp.sin(t)), (-R_*sp.sin(t), R_*sp.cos(t)))), (t, 0, 2*sp.pi))
    In = quad(lambda tt: sum(a*b for a, b in zip(Fv(R_*math.cos(tt), R_*math.sin(tt)), (-R_*math.sin(tt), R_*math.cos(tt)))), 0, 2*math.pi)[0]
    check(f'linje {R_} {sgn}', I, In)
    Ftex = '(-y,\\ x)' if sgn == 1 else '(y,\\ -x)'
    d1('arbeid', 'Arbeidsintegral', f"La $\\mathbf F = {Ftex}$ og la $C$ være sirkelen $x^2+y^2={R_}^2$ med positiv orientering (mot klokka). Regn ut $\\oint_C \\mathbf F\\cdot d\\mathbf r$.\n\n{{{{f1}}}}", I,
       [{'t': 'Parametriser', 's': f"$\\mathbf r(t) = ({R_}\\cos t,\\ {R_}\\sin t)$, $0\\le t\\le 2\\pi$, $\\mathbf r'(t) = (-{R_}\\sin t,\\ {R_}\\cos t)$.", 'ref': '2.3'},
        {'t': 'Sett inn', 's': '$\\oint_C \\mathbf F\\cdot d\\mathbf r = \\int_0^{2\\pi}\\mathbf F(\\mathbf r(t))\\cdot\\mathbf r\'(t)\\,dt$.', 'ref': '2.3'}], f"Svaret er {Lx(I)}.", '§2.3 Linjeintegral av vektorfelt', '2.3')
# kurvelengde
for (a_, b_, T_) in [(3, 4, 2*sp.pi), (1, 1, 2), (5, 12, sp.pi), (6, 8, 2), (8, 15, sp.pi/2), (2, 3, 4)]:
    L_ = sp.integrate(sp.sqrt(a_**2 + b_**2), (t, 0, T_))
    Ln = quad(lambda tt: math.sqrt((a_*math.cos(tt))**2 + (a_*math.sin(tt))**2 + b_**2), 0, float(T_))[0]
    check(f'kurve {a_} {b_}', L_, Ln)
    d1('kurve', 'Kurvelengde', f"Finn lengden av kurven $\\mathbf r(t) = ({a_}\\sin t,\\ {b_}t,\\ {a_}\\cos t)$ for $0\\le t\\le {tex(T_)}$.\n\n{{{{f1}}}}", L_,
       [{'t': 'Fart', 's': f"$|\\mathbf r'(t)| = \\sqrt{{{a_}^2\\cos^2t + {b_}^2 + {a_}^2\\sin^2t}} = \\sqrt{{{a_**2 + b_**2}}}$, konstant.", 'ref': '1.8'}],
       f"L = {Lx(L_)}.", '§1.8 Buelengde', '1.8')
# dobbeltintegral med variable grenser
for (a_, fexpr, up) in [(1, x*y, x**2), (2, x + y, x), (1, y, sp.sqrt(x)), (2, x, x**2), (1, x + 2*y, x), (3, y, x), (4, 1, sp.sqrt(x))]:
    I = sp.integrate(fexpr, (y, 0, up), (x, 0, a_))
    fn = sp.lambdify((y, x), fexpr, 'math'); un = sp.lambdify(x, up, 'math')
    In = dblquad(lambda yy, xx: fn(yy, xx), 0, a_, 0, lambda xx: un(xx))[0]
    check(f'dobbel {a_} {fexpr} {up}', I, In)
    d1('dobbel', 'Dobbeltintegral', f"Regn ut $\\displaystyle\\int_0^{{{a_}}}\\!\\int_0^{{{tex(up)}}} {tex(fexpr)}\\,dy\\,dx$ eksakt.\n\n{{{{f1}}}}", I,
       [{'t': 'Indre integral', 's': f"Integrer med hensyn på $y$ fra $0$ til ${tex(up)}$, med $x$ holdt fast. Så integrerer du resultatet fra $0$ til ${a_}$.", 'ref': '1.1'}],
       f"Svaret er {Lx(I)}.", '§1.1 Dobbeltintegral', '1.1')

# =====================================================================
# 6) Prøveeksamener: eget utvalg som ikke brukes i øvingssettene over
# =====================================================================
PROVE = []
def prove(n):
    key = f'PX{n}'
    add_set(key, f'Prøveeksamen {n} (nye tall)', f'P{n}', '4 timer · del 1: 9 oppgaver à 4 p · del 2: 4 oppgaver à 9 p · ta den på tid i prøvemodus')
    global QS
    picks = []
    rnd = random.Random(100 + n)
    # Del 1 i pensumrekkefølge
    def ny(src_set, topic):
        cands = [qq for qq in QS if qq['oving'] == src_set and qq['topic'] == topic and not qq.get('brukt')]
        c = rnd.choice(cands); c['brukt'] = True; return c
    del1 = [('VD', 'kurve'), ('VD', 'dobbel'), ('VD', 'polar'), ('VD', 'felt'), ('VD', 'felt'), ('VD', 'trippel'), ('VD', 'arbeid'), ('VP', 'pde'), ('VP', 'pde')]
    for i, (s_, tp) in enumerate(del1):
        picks.append(ny(s_, tp))
    return key, picks
# Lag egne kopier til prøveeksamenene slik at de ikke deler historikk med øvingssettene
def kopier(qq, key, nr_):
    c = json.loads(json.dumps(qq)); c['id'] = f'v{key}q{nr_}'; c['oving'] = key; c['nr'] = nr_; c.pop('brukt', None); return c

# Ekstra, uavhengige varianter bare for prøveeksamenene (flate, gauss, kode)
EKSTRA = {}
FX = [(sp.Rational(1, 2), sp.pi/2, sp.sqrt(3), 2*sp.sqrt(2)), (1, sp.pi/2, 0, sp.sqrt(2)), (sp.Rational(1, 4), sp.pi, 0, 2*sp.sqrt(2))]
GX = [(3, 4, 2, 5, 1), (1, 3, 4, 4, 2), (2, 4, 3, 1, 1)]
KX = [(2, 5, 4, 101, 0.05, 2, 40), (1, 1, 4, 51, 0.02, 1, 25), (4, 8, 7, 81, 0.1, 6, 30)]
for n in (1, 2, 3):
    key, picks = prove(n)
    out = [kopier(p, key, i+1) for i, p in enumerate(picks)]
    # del 2: 10 utledning (lenke til Ø6.9 i teksten), 11 flate, 12 kode, 13 gauss
    out.append({'id': f'v{key}q10', 'oving': key, 'nr': 10, 'status': 'ny', 'maxp': 9, 'topic': 'bevaring', 'title': 'Utledning av konveksjon–diffusjonslikningen',
                'text': 'Ta oppgaven «Konveksjon–diffusjon som bevaringslov» (øving 6.9) uten hjelpemidler utover formelarket, og marker her når du har fått alle feltene riktige.\n\n[Åpne øving 6.9](#q-o6q9)\n\n{{f1}}',
                'fields': [{'i': 1, 'kind': 'confirm', 'ans': None}], 'hints': [], 'explain': 'Utledningen er lik i Ord25 10, Feb26 10 og Prøve25 14.', 'komp': '§3.2 Bevaringslover', 'forel': '', 'sitat': None,
                'refs': [{'key': '3.2', 'title': 'Bevaringslover', 'start': 0, 'end': 0, 'focus': 0, 'side': 0}], 'steg': [], 'fig': None, 'base': None, 'variant': True})
    F = flate(*FX[n-1]); kode = flate_kode(F)
    out.append({'id': f'v{key}q11', 'oving': key, 'nr': 11, 'status': 'ny', 'maxp': 9, 'topic': 'flate', 'title': 'Parametrisk flate a–d',
                'text': flate_tekst(F) + "\na) $\\mathbf r_u=$ {{f1}}  $\\mathbf r_v=$ {{f2}}  $\\mathbf N=$ {{f3}}  $|\\mathbf N|=$ {{f4}}\n\nb) Arealet eksakt: {{f5}}\n\nc) $\\bar z$ med `dblquad`: {{f6}}\n\nd) Volumet under flaten med `tplquad`: {{f7}}",
                'fields': [{'i': 1, 'kind': 'expr', 'ans': js(list(F['ru']))}, {'i': 2, 'kind': 'expr', 'ans': js(list(F['rv']))}, {'i': 3, 'kind': 'expr', 'ans': js(list(F['N']))}, {'i': 4, 'kind': 'expr', 'ans': js(F['nN'])},
                           {'i': 5, 'kind': 'expr', 'ans': js(F['A'])}, {'i': 6, 'kind': 'expr', 'ans': fnum(F['zbar'], 6), 'tol': 0.002}, {'i': 7, 'kind': 'expr', 'ans': fnum(F['V'], 6), 'tol': 0.002}],
                'hints': [], 'explain': f"A = {Lx(F['A'])}, z̄ ≈ {fnum(F['zbar'])}, V ≈ {fnum(F['V'])}.\n\n```python\n{kode}\n```", 'komp': '§1.9 Parametriske flater', 'forel': '', 'sitat': None,
                'refs': [{'key': '1.9', 'title': '', 'start': 0, 'end': 0, 'focus': 0, 'side': 0}], 'steg': flate_steg(F), 'fig': None, 'base': None, 'variant': True})
    kq = [qq for qq in QS if qq['oving'] == 'VK']  # gjenbruk tekstmal, nye tall
    L, T, m, N, c2, xi, ti = KX[n-1]
    dx = sp.Rational(L, m+1); dt = sp.Rational(T, N-1); mm = 2*m; nmin = minN(c2, L, T, mm)
    xs = np.linspace(0, L, m+2); ts = np.linspace(0, T, N)
    check('PX dx', xs[1]-xs[0], dx); check('PX dt', ts[1]-ts[0], dt); check('PX x', xs[xi], xi*dx); check('PX t', ts[ti], ti*dt)
    out.append({'id': f'v{key}q12', 'oving': key, 'nr': 12, 'status': 'ny', 'maxp': 9, 'topic': 'tidpde', 'title': 'Varmelikningskode',
                'text': f"Koden løser $u_t = {c2}\\,u_{{xx}}$ for $0\\le x\\le {L}$, $0\\le t\\le {T}$ med `x = np.linspace(0, {L}, m + 2)` ($m={m}$) og `t = np.linspace(0, {T}, N)` ($N={N}$).\n\n"
                        f"a) $\\Delta x=$ {{{{f1}}}}  b) $\\Delta t=$ {{{{f2}}}}\n\nc) Indeksene for $x={tex(xi*dx)}$, $t={tex(ti*dt)}$: $p=$ {{{{f3}}}} $q=$ {{{{f4}}}}\n\nd) Minste $N$ for stabilitet (${c2}\\Delta t/\\Delta x^2<0.5$) når $m={mm}$: {{{{f5}}}}",
                'fields': [{'i': 1, 'kind': 'expr', 'ans': js(dx), 'tol': 1e-6}, {'i': 2, 'kind': 'expr', 'ans': js(dt), 'tol': 1e-6}, {'i': 3, 'kind': 'expr', 'ans': str(xi)}, {'i': 4, 'kind': 'expr', 'ans': str(ti)}, {'i': 5, 'kind': 'expr', 'ans': str(nmin)}],
                'hints': [], 'explain': f"Δx = {dx}, Δt = {dt}, p = {xi}, q = {ti}, N = {nmin}.", 'komp': '§3.3.4', 'forel': '', 'sitat': None,
                'refs': [{'key': '3.3.4', 'title': '', 'start': 0, 'end': 0, 'focus': 0, 'side': 0}], 'steg': [], 'fig': None, 'base': None, 'variant': True})
    S = sylinder(*GX[n-1]); R_, H_, a_, b_, c_ = GX[n-1]
    out.append({'id': f'v{key}q13', 'oving': key, 'nr': 13, 'status': 'ny', 'maxp': 9, 'topic': 'gauss', 'title': 'Fluks ut av sylinder',
                'text': f"$S$ er en lukket sylinder om $z$-aksen med radius ${R_}$, bunn i $xy$-planet og høyde ${H_}$, orientert utover. $\\mathbf F = (x+{a_},\\ y+{b_},\\ {c_}z)$.\n\n"
                        "Fluks gjennom toppen: {{f1}}  bunnen: {{f2}}  $\\nabla\\cdot\\mathbf F=$ {{f3}}  total (Gauss): {{f4}}  veggen: {{f5}}",
                'fields': [{'i': 1, 'kind': 'expr', 'ans': js(S['topp'])}, {'i': 2, 'kind': 'expr', 'ans': js(S['bunn'])}, {'i': 3, 'kind': 'expr', 'ans': js(S['div'])}, {'i': 4, 'kind': 'expr', 'ans': js(S['tot'])}, {'i': 5, 'kind': 'expr', 'ans': js(S['vegg'])}],
                'hints': [], 'explain': f"Topp {Lx(S['topp'])}, bunn 0, ∇·F = {S['div']}, total {Lx(S['tot'])}, vegg {Lx(S['vegg'])}.", 'komp': '§2.8', 'forel': '', 'sitat': None,
                'refs': [{'key': '2.8', 'title': '', 'start': 0, 'end': 0, 'focus': 0, 'side': 0}], 'steg': gsteg_syl(S), 'fig': None, 'base': None, 'variant': True})
    EKSTRA[key] = out

QS = [qq for qq in QS if not qq.get('brukt')]
for sk in ('VD', 'VP'):
    for i, qq in enumerate([qq for qq in QS if qq['oving'] == sk]): qq['nr'] = i + 1; qq['id'] = f"v{sk}q{i+1}"
# Rydd i LaTeX: 1x -> x, \sqrt{4} -> 2, + 0\sin -> borte
def rydd(t):
    # t er innholdet i ett matematikkområde (uten dollartegn)
    t = re.sub(r'(?<![\d.\w^}\\])1(?=[a-z]|\\(?:cos|sin|pi)\b)', '', t)
    t = re.sub(r'\\sqrt\{(\d+)\}', lambda k: str(math.isqrt(int(k.group(1)))) if math.isqrt(int(k.group(1)))**2 == int(k.group(1)) else k.group(0), t)
    t = re.sub(r'\s*\+\s*0\\(?:sin|cos)\\varphi', '', t)
    t = re.sub(r'(?<=[=\s])1\\,(?=u_)', '', t)
    return t
def ryddalt(o, k=None):
    if isinstance(o, str):
        if k in ('ans', 'options'): return o
        o = re.sub(r'= 1(u_)', r'= \1', o)  # «u_t = 1u_xx» i ren tekst
        return re.sub(r'(\$\$?)([^$]+)\1', lambda m: m.group(1) + rydd(m.group(2)) + m.group(1), o)
    if isinstance(o, list): return [ryddalt(v, k) for v in o]
    if isinstance(o, dict): return {kk: ryddalt(v, kk) for kk, v in o.items()}
    return o
QS = [ryddalt(qq) for qq in QS]
EKSTRA = {k: [ryddalt(qq) for qq in v] for k, v in EKSTRA.items()}
ALL = QS + [qq for k in EKSTRA for qq in EKSTRA[k]]
# Sett poeng for prøveeksamen: del 1 = 4, del 2 = 9
for qq in ALL:
    if qq['oving'].startswith('PX'):
        qq['maxp'] = 4 if qq['nr'] <= 9 else 9

ids = [qq['id'] for qq in ALL]
assert len(ids) == len(set(ids)), 'duplikate id-er'
out = 'window.BVAR=' + json.dumps({'sets': SETS, 'questions': ALL}, ensure_ascii=False) + ';\n'
open(sys.argv[1] if len(sys.argv) > 1 else 'bank_var.js', 'w', encoding='utf-8').write(out)
json.dump([{'navn': c[0], 'ok': c[1], 'a': c[2], 'b': c[3]} for c in CHECKS], open('/tmp/kontroller.json', 'w'), ensure_ascii=False, indent=0)
print(f'{len(ALL)} oppgaver, {len(CHECKS)} kontroller, alle OK')
