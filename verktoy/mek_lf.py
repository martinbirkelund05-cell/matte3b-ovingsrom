#!/usr/bin/env python3
"""Klipper løsningsforslagene (mek/pdf/H25_LF.pdf, H24_LF.pdf) til ett utsnitt per deloppgave -> mek/lfd/ og mek_lf.js.
Hver rad: (side, fra %, til %, felles). «felles» = mellomregning som deles med andre deloppgaver og vises sammenslått.
Utsnittene er satt for hånd etter gjennomsyn av hver side. Kjør fra repo-roten: python3 verktoy/mek_lf.py
"""
import pymupdf as fitz, json
from PIL import Image
K = {
 'mH25-1a': [(2,0,39.3)], 'mH25-1b': [(2,39.3,99)],
 'mH25-2a': [(3,0,52)], 'mH25-2b': [(3,53,99),(4,7,24)], 'mH25-2c': [(4,25,94)],
 'mH25-3a': [(5,4,47)], 'mH25-3b': [(5,4,47)], 'mH25-3c': [(5,4,34),(5,50,98)], 'mH25-3d': [(6,4,90)],
 'mH25-3e': [(8,5,34),(7,6,94,1)], 'mH25-3f': [(8,34,69),(7,6,94,1)], 'mH25-3g': [(8,68,99),(7,6,94,1)],
 'mH25-4a': [(9,38.5,57)], 'mH25-4b': [(9,58,100),(10,6,13.5)], 'mH25-4c': [(9,58,100),(10,6,13.5)], 'mH25-4d': [(10,13.5,46)],
 'mH25-4e': [(10,46.5,100),(11,8,28)], 'mH25-4f': [(10,46.5,100),(11,8,28)],
 'mH25-5a': [(12,53,100)], 'mH25-5b': [(13,3,66)], 'mH25-5c': [(13,3,66)],
 'mH25-5d': [(13,70,79.5),(13,3,66,1)], 'mH25-5e': [(13,79.5,88.5),(13,3,66,1)], 'mH25-5f': [(13,88.5,97),(13,3,66,1)],
 'mH25-6': [(15,2,90)],
 'mH24-1a': [(2,0,20.6)], 'mH24-1b': [(2,20.6,53.2)], 'mH24-1c': [(2,54.2,61.5)], 'mH24-1d': [(2,62,99)],
 'mH24-2a': [(3,7,59)], 'mH24-2b': [(3,63,99)],
 'mH24-3a': [(4,0,95)], 'mH24-3b': [(5,2,96)],
 'mH24-3c': [(8,42,62),(6,8,94,1),(7,62,96,1),(8,0,42,1)], 'mH24-3d': [(8,62,82.5),(6,8,94,1),(7,62,96,1),(8,0,42,1)], 'mH24-3e': [(8,82.5,99),(6,8,94,1),(7,62,96,1),(8,0,42,1)],
 'mH24-4a': [(9,55,99),(10,3,43)], 'mH24-4b': [(10,44,53)], 'mH24-4c': [(10,55,93.5)], 'mH24-4d': [(11,3,9.5),(10,58,82,1)], 'mH24-4e': [(11,10,43)],
 'mH24-5a': [(12,52,98)], 'mH24-5b': [(13,9,21),(13,31,50)], 'mH24-5c': [(13,20.5,31),(13,31,50)], 'mH24-5d': [(13,53,80)],
 'mH24-6a': [(14,0,100)], 'mH24-6b': [(15,2,56)],
}
ut = {}; cache = {}
for qid, rader in K.items():
    ex = qid[1:4]; d = fitz.open(f'mek/pdf/{ex}_LF.pdf'); ut[qid] = []
    for r in rader:
        side, a, b = r[:3]; felles = len(r) > 3
        key = (ex, side, a, b)
        if key not in cache:
            pg = d[side-1]; R = pg.rect; pm = pg.get_pixmap(clip=fitz.Rect(0, R.height*a/100, R.width, R.height*b/100), dpi=135)
            im = Image.frombytes('RGB', (pm.width, pm.height), pm.samples)
            # fjern hvite marger på sidene
            import numpy as np
            g = np.asarray(im.convert('L')); kol = np.where((g < 245).sum(axis=0) > 0)[0]; rad = np.where((g < 245).sum(axis=1) > 0)[0]
            if len(kol) and len(rad): im = im.crop((max(0,kol[0]-12), max(0,rad[0]-8), min(im.width,kol[-1]+12), min(im.height,rad[-1]+8)))
            fn = f'mek/lfd/{ex}_s{side}_{str(a).replace(".","_")}-{str(b).replace(".","_")}.png'; im.save(fn, optimize=True); cache[key] = (fn, im.width, im.height)
        fn, w, h = cache[key]; ut[qid].append({'src': fn, 'side': side, 'w': w, 'h': h, **({'felles': 1} if felles else {})})
open('mek_lf.js','w',encoding='utf-8').write('// Laget av verktoy/mek_lf.py. Ikke rediger for hånd.\nwindow.MEK_LF = ' + json.dumps(ut, ensure_ascii=False) + ';\n')
print(len(ut), 'deloppgaver,', len(cache), 'utsnitt')
