# Matte 3B Øvingsrom (IMAA3012, NTNU høsten 2026)

Øvingsplattform for egen eksamensforberedelse – **for educational purposes only**.
Oppgavetekstene er fra de obligatoriske øvingene og repetisjonsøvingene i Capquiz, og
kompendiet «Forelesningsnotater Matematikk 3B» (versjon 2. nov 2026) vises side for side. Repoet skal være privat.

## Kom i gang
1. Klon eller last ned repoet.
2. Åpne `index.html` i **Chrome eller Edge** (dobbeltklikk – ingen server eller internett trengs).
3. Trykk **Lagre som …** øverst og opprett din egen historikkfil, f.eks. `historikk/<navn>_historikk.json`.
   Hvert svar lagres automatisk til fila. Neste gang: trykk **Fortsett: <fil>** (eller **Åpne historikk**).

Hver person bruker sin egen historikkfil – da kan flere dele samme repo uten å blande resultater.
Safari/Firefox støtter ikke historikkfil; der ligger historikken i nettleseren (eksport/import under «Om øvingsrommet»).

## Innhold
- `index.html` – hele plattformen (oversikt, gjøremål, øvinger i øvings-/prøvemodus, eksamenssett, kompendium, notater)
- `bank.js` – oppgavebank med fasit, hint, steg-for-steg og pensumreferanser
- `komp/` – kompendiet som sidebilder · `fig/` – figurer til forklaringene · `eksamen/` – eksamenssett med LF
- `vendor/` – mathjs og MathJax (lokalt, så alt virker uten nett)
- `historikk/` – legg historikkfilene her (valgfritt)

## Regler i historikken
Et svar teller som riktig bare når det ble gitt uten at fasit var vist først. Svar med hint teller 70 %.
Forsøk kan slettes under «Tidligere forsøk» (kan ikke angres).
