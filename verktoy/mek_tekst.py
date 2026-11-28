#!/usr/bin/env python3
"""Lager mek_tekst.js og mek/figur/*.png fra de originale eksamens-PDF-ene (Inspera-utskrift).

For hver deloppgave hentes oppgaveteksten som tekst (formler er satt inn for hånd etter kontroll mot PDF-en)
og figurene som hele, innebygde bilder. Fasitmarkeringene i PDF-en (grønne tall og haker) tas aldri med,
fordi bare tekstlinjer og figurbilder brukes, ikke utsnitt av siden.
Kjør fra repo-roten:  python3 verktoy/mek_tekst.py
"""
import pymupdf as fitz, json, re, subprocess, os, sys
from PIL import Image
import numpy as np

Q = json.loads(subprocess.check_output(['node','-e',"global.window={};require('./bank_mek.js');console.log(JSON.stringify(window.BANK_MEK.questions))"]))
QBY = {q['id']: q for q in Q}
STOY = re.compile(r'^(Format.*|Σ.*|Words: \d+|Skriv .*svar.* her.*|Velg ett alternativ.*|Velg .* du mener er riktig:?|du mener er riktig:?|Velg|Utskrift / PDF|\d+/\d+|Maks poeng: \d+|\(.*\)|Alternativ \w+|ingen av alternativene|Ingen av alternativene|Erstatt.*|Merk at hånd.*|Merk at argumentasjonen.*|Innlevering av hånd.*|.*løse denne oppgaven (må|skal) leveres.*|.*leveres inn\.?:?|inn\.|valgfritt for denne oppgav[ae]n?\.|Du må begrunne svar.*|Oppgaven besvares direkte i Inspera|Rammeoppgave|Fyll inn svaret ditt her.*|For å få full uttelling.*|med ord, eller vise en utregning\.|Største moment|Største bøyespenning|Bøyemoment|i punkt [BC] er lik:|Maks\. (strekk|trykk)kraft =|mm.*|N\.|MPa\.|\.)$')

def hent(ex):
    d = fitz.open(f'mek/pdf/{ex}.pdf'); starts = []
    for pn in range(len(d)):
        for b in d[pn].get_text('dict')['blocks']:
            if b['type']!=0: continue
            t = ' '.join(s['text'] for l in b['lines'] for s in l['spans']).strip()
            m = re.match(r'^(\d)(?:\(([a-z])\))?(\s|$)', t)
            if m and b['bbox'][0] < 45 and not re.match(r'^\d Erstatt', t): starts.append((pn, b['bbox'][1], m.group(1)+(m.group(2) or '')))
    starts.sort(); out = {}
    for i,(pn,y,nr) in enumerate(starts):
        end = starts[i+1][:2] if i+1<len(starts) else (len(d)-1, 9999); bl = []
        for p2 in range(pn, end[0]+1):
            for b in d[p2].get_text('dict')['blocks']:
                by = b['bbox'][1]
                if (p2,by) < (pn,y-1) or (p2,by) >= (end[0], end[1]-1): continue
                if b['type']==1: bl.append({'p':p2,'bbox':b['bbox'],'img':True})
                else:
                    for l in b['lines']:
                        t = ''.join(s['text'] for s in l['spans']).strip()
                        if t: bl.append({'p':p2,'bbox':l['bbox'],'t':t})
        bl.sort(key=lambda b:(b['p'], b['bbox'][1], b['bbox'][0])); out[nr] = bl
    return d, out

# Formler og presiseringer satt inn for hånd, kontrollert mot PDF-en linje for linje
FIX = {
 'mH25-1a': [(r'arealsenter C \( og \)', r'arealsenter C ($y_C$ og $z_C$). Svarene oppgis i mm.')],
 'mH25-1b': [(r'annet areal momenter I_y og I_z', r'annet arealmomenter $I_y$ og $I_z$'), (r'$', r' Svarene oppgis i $10^6\\ \\text{mm}^4$, avrundet til 1 desimal.')],
 'mH25-3a': [(r'jevnt fordelt last over felt BC og ei punktlast i punkt D', r'jevnt fordelt last $q = 1{,}5$ kN/m over felt BC og ei punktlast $F = 2$ kN i punkt D'), (r'talet', 'tallet')],
 'mH25-3c': [(r'bøyemomentet i hjørne B', r'bøyemomentet $M_B$ i hjørne B')],
 'mH25-3d': [(r'normalkraft , skjærkraft og moment mellom B og C\. La løpe', r'normalkraft $N(x)$, skjærkraft $V(x)$ og moment $M(x)$ mellom B og C. La $x$ løpe')],
 'mH25-4a': [(r'last q = 4 kN/m', r'last $q = 4$ kN/m'), (r'f = 355 N/mm \.', r'$f_y = 355\\ \\text{N/mm}^2$.')],
 'mH25-4e': [(r'\(f = 355 N/mm \) \?', r'($f_y = 355\\ \\text{N/mm}^2$)?'), (r'punktlast F ', r'punktlast $F$ '), (r'Punktlasten F vil gi et ekstra bidrag FL \(der L = 6m', r'Punktlasten $F$ vil gi et ekstra bidrag $FL$ (der $L = 6$ m')],
 'mH25-5b': [(r'rotasjonsvinkelen i punkt A', r'rotasjonsvinkelen $\\phi_A$ i punkt A')],
 'mH25-5c': [(r'rotasjonsvinkelen i punkt C', r'rotasjonsvinkelen $\\phi_C$ i punkt C')],
 'mH24-2a': [(r'arealsenter C \( og \)\.', r'arealsenter C ($y_C$ og $z_C$). Svarene oppgis i mm.'), (r'tverrsnitts geometrien', 'tverrsnittsgeometrien')],
 'mH24-2b': [(r'annet areal moment \. Bruk Steiners teorem', r'annet arealmoment $I_y$. Bruk Steiners teorem.'), (r'tverrsnitts geometrien', 'tverrsnittsgeometrien'), (r'nærmeste heltall\.', r'nærmeste heltall (svaret oppgis i $10^6\\ \\text{mm}^4$).')],
 'mH24-1b': [(r'\s+A = A = E =.*$', r' Finn $A_x$, $A_z$ og $E_x$.')],
 'mH24-4b': [(r'uttrykt ved F og a\.', r'uttrykt ved $F$ og $a$: bøyemomentet $M_B$ i punkt B og $M_C$ i punkt C.')],
 'mH24-4c': [(r'Anta F = 250 N og a = 1,0 m', r'Anta $F = 250$ N og $a = 1{,}0$ m')],
 'mH24-4d': [(r'dersom F = 250N og a = 1,0m\.', r'dersom $F = 250$ N og $a = 1{,}0$ m.'), (r'$', r' Svaret $\\sigma^M_{max}$ oppgis i MPa.')],
 'mH24-4e': [(r'punktlastene F kan ha uten at bruddspenningen \(f = 30 MPa\)', r'punktlastene $F$ kan ha uten at bruddspenningen ($f_y = 30$ MPa)'), (r'at a = 1,0 m\.', r'at $a = 1{,}0$ m.')],
}
FIX_INTRO = {
 'H24-4': [(r'punktlaster F angriper', r'punktlaster $F$ angriper'), (r'trematerialet er f = 30 MPa\.\s*y?', r'trematerialet er $f_y = 30$ MPa.')],
 'H24-5': [(r'en kraft i C', r'en kraft $P$ i C'), (r'har lengde og bøyestivhet \.', r'har lengde $L$ og bøyestivhet $EI$.')],
 'H25-5': [(r'en kraft F ved D', r'en kraft $F$ ved D'), (r'bøyestivhet EI og aksialstivhet EA', r'bøyestivhet $EI$ og aksialstivhet $EA$'), (r'har lengde L\.', r'har lengde $L$.'), (r'har lengde 2L\.', r'har lengde $2L$.')],
 'H25-6': [(r'med side L er', r'med side $L$ er'), (r'en kraft F som', r'en kraft $F$ som'), (r'Kraften F beregnes', r'Kraften $F$ beregnes'), (r'vannstanden h som variere fra 0 til 3L', r'vannstanden $h$ som varierer fra $0$ til $3L$')],
}
# Deloppgaver som mangler fellesteksten på sin egen side i PDF-en, får den fra første deloppgave i oppgaven
FELLES_FRA = {'mH25-2c':'mH25-2b', 'mH25-3b':'mH25-3a', 'mH25-3c':'mH25-3a', 'mH25-3d':'mH25-3a', 'mH25-3e':'mH25-3a', 'mH25-3f':'mH25-3a', 'mH25-3g':'mH25-3a',
              'mH25-4b':'mH25-4a', 'mH25-4c':'mH25-4a', 'mH25-4d':'mH25-4a', 'mH25-4e':'mH25-4a', 'mH25-4f':'mH25-4a'}
FELLES_SETN = {'mH25-2b': 2, 'mH25-3a': 1, 'mH25-4a': 3}   # antall setninger i starten som er felles opplysninger

def sig(im):
    g = np.asarray(im.convert('L').resize((24,24)), dtype=float); return g, im.width/im.height
def lik(a, b): return abs(a[1]-b[1])/b[1] < 0.012 and np.abs(a[0]-b[0]).mean() < 12

def rens(linjer, q):
    etik = set()
    for f in q['fields']:
        for l in (f.get('labels') or []): etik.add(re.sub(r'[\$\\{},]', '', l).replace(' ', '').lower())
    ut = []
    for t in linjer:
        if STOY.match(t): continue
        if re.sub(r'[\s,]', '', t).lower() in etik: continue
        if re.match(r'^(ca )?-?\d+([,.]\d+)? ?(kN|kNm|MPa|m|N)?( \(i punkt [AB]\))?$', t) or re.match(r'^[A-F]$', t) or re.match(r'^\d*Fa$', t) or re.match(r'^(Stav|Punkt|Like|Rett|Det er ingen|Bøyespenningen er den samme) ', t) and len(t) < 60: continue
        if re.match(r'^(N|=|AC|AD|BD|CE|CF|DF|x|z|y|\d)$', t): continue
        ut.append(t)
    return ut
def sett(linjer):
    t = re.sub(r'\s+', ' ', ' '.join(linjer)).strip()
    t = re.sub(r'(\s+kN){2,}$', '', t); t = re.sub(r'\s*Maks\. strekkraft = kN Maks\. trykkraft = kN$', '', t)
    t = re.sub(r'\s*(Merk at|Innlevering av håndberegning er)$', '', t)
    return t.strip()
def fiks(t, regler):
    for a, b in regler:
        ny = re.sub(a, b, t); 
        if ny == t and a != r'$': print('   ADVARSEL: regel traff ikke:', a, file=sys.stderr)
        t = ny
    return t

ut = {}; figs_laget = 0
for ex in ['H25', 'H24']:
    d, S = hent(ex)
    # fellestekst og fellesfigurer per oppgave (egne «intro»-avsnitt i PDF-en)
    intro = {}
    for nr, bl in S.items():
        cut = next((i for i,b in enumerate(bl) if 't' in b and re.match(r'^[1-6]$', b['t']) and b['bbox'][0] < 95 and i>0), None)
        if nr in ('4','5'): intro[nr] = bl
        elif cut is not None and len(nr)==2: intro[bl[cut]['t']] = bl[cut:]; S[nr] = bl[:cut]
    def figurer(bl, navn):
        global figs_laget
        res = []
        for k, b in enumerate([b for b in bl if b.get('img') and (b['bbox'][2]-b['bbox'][0]) > 110]):
            r = fitz.Rect(b['bbox']); pm = d[b['p']].get_pixmap(clip=r, dpi=190); im = Image.frombytes('RGB', (pm.width, pm.height), pm.samples)
            res.append({'im': im, 's': sig(im), 'side': b['p']+1})
        return res
    hoved = {}   # oppgavenummer -> fellesfigurer
    for onr, bl in intro.items(): hoved[onr] = figurer(bl, f'{ex}_{onr}')
    lagret = []  # (signatur, filnavn, w, h) for gjenbruk av like figurer
    def lagre(f, navn):
        global figs_laget
        for s, fn, w, h in lagret:
            if lik(f['s'], s): return {'src': fn, 'w': w, 'h': h}
        fn = f'mek/figur/{navn}.png'; f['im'].save(fn, optimize=True); figs_laget += 1; lagret.append((f['s'], fn, f['im'].width, f['im'].height)); return {'src': fn, 'w': f['im'].width, 'h': f['im'].height}
    for nr in sorted(S):
        qid = f'm{ex}-{nr}'
        if qid not in QBY: continue
        q = QBY[qid]; bl = S[nr]; onr = nr[0]
        egne = figurer(bl, qid)
        if onr not in hoved: hoved[onr] = egne[:]          # første deloppgave med figur gir oppgavens fellesfigur
        felles = [] if qid in ('mH25-1b','mH24-2b') else [f for f in hoved.get(onr, []) if not any(lik(f['s'], e['s']) for e in egne)]
        alle = felles + egne
        linjer = rens([b['t'] for b in bl if 't' in b and not re.match(r'^\d(\([a-z]\))?( |$)', b['t']) ] + [], q)
        forste = next((b['t'] for b in bl if 't' in b), '')
        rest = re.sub(r'^\d(\([a-z]\))?\s*', '', forste)
        if rest and not STOY.match(rest): linjer = rens([rest], q) + linjer
        tekst = fiks(sett(linjer), FIX.get(qid, []))
        fellestekst = ''
        if onr in intro:
            il = [b['t'] for b in intro[onr] if 't' in b and not re.match(r'^[1-6]$', b['t'])]
            fellestekst = fiks(sett([t for t in il if not STOY.match(t)]), FIX_INTRO.get(f'{ex}-{onr}', []))
        elif qid in FELLES_FRA:
            kilde = ut[FELLES_FRA[qid]]['tekst']; n = FELLES_SETN[FELLES_FRA[qid]]
            fellestekst = ' '.join(re.split(r'(?<=[.])\s+(?=[A-ZÆØÅ]|[a-g]\) )', kilde)[:n])
        ut[qid] = {'tekst': tekst, 'felles': fellestekst, 'figs': [dict(lagre(f, f'{qid[1:]}_{i+1}'), felles=(f in felles)) for i, f in enumerate(alle)], 'side': q['src']['page']}
json.dump(ut, open('/tmp/mek_tekst.json','w'), ensure_ascii=False, indent=1)
open('mek_tekst.js','w',encoding='utf-8').write('// Laget av verktoy/mek_tekst.py fra de originale eksamens-PDF-ene. Ikke rediger for hånd.\nwindow.MEK_TEKST = ' + json.dumps(ut, ensure_ascii=False) + ';\n')
print('deloppgaver:', len(ut), 'av', len(Q), '| figurfiler:', figs_laget)
for k, v in ut.items(): print(f"\n[{k}] figurer: {[(os.path.basename(f['src']), 'felles' if f['felles'] else 'egen') for f in v['figs']]}\n  FELLES: {v['felles'][:300]}\n  TEKST: {v['tekst'][:600]}")
