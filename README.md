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

## Plattform v2 (én motor for alle fag)
- **Hjem** spør først «Hvor mye tid har du i dag?» (eller «Etter nattevakt»), og viser så én stor **Fortsett**-knapp for det viktigste neste. Fagkortene viser forventet poeng (matte) og hvor mye som sitter (mekanikk, FEM), ikke avkryssing.
- **Plan** (`#gjoremal`): én motor planlegger alle fagene fra eksamensdatoene. Matten legges inn som økter der Økt-motoren velger oppgavene, prøveeksamenene legges inn 5.12, 9.12 og 13.12, og repetisjon av det du bommet på kommer først. Du kan legge til egne oppgaver.
- **Diagnose** (`#diagnose`): én kort testoppgave eller selvvurdering per oppgavetype i matte setter startnivået.
- **Prøv først**: fasiten åpnes etter et forsøk eller to hint (eller «Jeg har regnet den» for papiroppgaver). Ved feil svar velger du årsak rett ved feltet.
- **Øktslutt**: kvittering med tid, riktige, endring i forventet poeng og neste repetisjon.
- **Prøveeksamen** i Inspera-stil: nedtelling fra 4 timer, del 1/del 2, «Merk», poeng av 72 og selvretting av del 2-oppgaver som ikke rettes automatisk.
- **Mobil**: bunnmeny (Hjem, Økt, Plan, Mer), øktknappene nederst.
- **Synk** (`#om`): historikken lagres i `historikk/<navn>.json` på grenen `historikk` i dette repoet og flettes automatisk mellom enheter. Krever et fine-grained token med bare *Contents: Read and write* på dette repoet, lagt inn én gang per enhet (lagres bare i nettleseren).

### Felles motor og struktur (28.11)
- Økt finnes for alle tre fagene (`#okt`, `#okt-mek`, `#okt-fem`) med samme temavelger: andel av eksamen, mestring, nivå (prøvd, løst selv, bekreftet) og tid igjen.
- Planen legger øvingen i alle fag som økter, deler lange aktiviteter og legger aldri mer på en dag enn studietiden. Innleveringer med frist står i planen.
- «Tren på feilene mine» på Økt-siden, og «Prøvemuntlig» (`#muntlig`) for Elementmetoden.
- Én meny: Hjem, Plan, de tre fagene og Mer. Hvert fag har fanene Økt og Oversikt.
- Mekanikk bruker bare emnets egne øvinger (med løsningsforslag) og tidligere eksamener med fasit. Øvingene ligger som oppgaver i øktene («Gjør øving 4»), og Oppgavesamlingen er tatt ut av planen. Poeng per oppgave fra PDF-eksamenene kan føres inn under «Etterarbeid».

### Øktløp, temavalg og pensumdekning (28.11)
- Økt-siden viser én anbefalt økt (tittel, tid, oppgaver og deloppgaver, pensumreferanse, hvilket gjøremål den bidrar til) og øktløpet gruppert etter gjøremål. En økt er en fast liste med oppgaver.
- «Velg tema»: anbefalt + to alternativer med begrunnelse og tid. «Pensum fram mot eksamen»: fire statuser per tema (klarer selv, trenger mer trening, planlagt, uten planlagt økt).
- Oversikt: neste økt, pensum, og søylediagrammet «Dette går igjen på eksamen».
- Tid anslås per oppgave ut fra innholdet og justeres med aktiv tid (pauser telles ikke). Øvinger med frist planlegges før fristen, og underskudd vises som «Mangler ca. X min før fristen».
- Pause og «Avslutt for i dag»: oppgave, utkast i svarfeltene og aktiv tid tas vare på.

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
