# Studieplattform høsten 2026: Matte 3B, Mekanikk 1 og Elementmetoden

(Opprinnelig «Matte 3B Øvingsrom», IMAA3012.)

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

## Studieplattformen (tre fag)
- **Hjem** (`#hjem`): fagkort for MEKA1101, MEPA2314 og IMAA3012 med framdrift, dager til eksamen og neste aktivitet, dagens gjøremål og kommende hendelser fra Canvas (kandidatnummer er utelatt).
- **Kalender** (`#kalender`) og **Gjøremål** (`#gjoremal`): én felles plan, fordelt baklengs fra eksamensdatoene (4.12, 11.12 og 17.12) innenfor studietiden per dag (standard 6 t, kan endres per dag). Ugjorte aktiviteter flyttes til neste dag med ledig kapasitet. Strekker ikke tiden til, tas de lavest prioriterte ut, og det vises hvor mye som gjenstår.
- **Mekanikk 1** (`#fag-mek`): eksamen H25 og H24 deloppgave for deloppgave med originale figurer (klikk for å forstørre), retting mot Inspera-fasiten og LF side for side. Eldre sett (V26 med sensurveiledning, V25 … H18) som PDF med poenglogg.
- **Elementmetoden** (`#fag-fem`): egenlagde spørsmål merket med kilde (forelesning, lysbilde/side): flashcards, flervalg med forklaring på feil alternativ, korte skriftlige svar, figurspørsmål og små beregninger.
- En aktivitet med oppgaver hukes av automatisk når alle feltene er besvart, uansett hvor du svarte. Manuelle aktiviteter hukes av for hånd og lagres i samme historikk.

## Innhold
- `index.html` – hele plattformen (oversikt, gjøremål, øvinger i øvings-/prøvemodus, eksamenssett, kompendium, notater)
- `bank_mek.js`, `bank_fem.js` – oppgavebanker for Mekanikk 1 og Elementmetoden · `mek/`, `fem/` – PDF-er, figurer og LF-sider
- `bank.js` – oppgavebank (matte) med fasit, hint, steg-for-steg og pensumreferanser
- `komp/` – kompendiet som sidebilder · `fig/` – figurer til forklaringene · `eksamen/` – eksamenssett med LF
- `vendor/` – mathjs og MathJax (lokalt, så alt virker uten nett)
- `historikk/` – legg historikkfilene her (valgfritt)

## Regler i historikken
Et svar teller som riktig bare når det ble gitt uten at fasit var vist først. Svar med hint teller 70 %.
Forsøk kan slettes under «Tidligere forsøk» (kan ikke angres).
