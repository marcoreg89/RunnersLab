# Race Calendar Scraper per Runners Lab

Questo repository contiene il "motore backend" del calendario gare dell'app iOS **Runners Lab**.

## Come funziona
Ogni lunedì notte alle 3:00, un server gratuito di GitHub (chiamato GitHub Actions) scarica il codice, esegue lo script `scraper.py` e genera un file `races.json` sempre aggiornato. L'app iOS legge direttamente quel file per mostrare le gare agli utenti.

## Come attivarlo

1. Vai su [GitHub.com](https://github.com/) e crea un nuovo repository PUBBLICO (es. chiamalo `runners-lab-calendar`). Non aggiungere il file README automatico.
2. Apri il terminale del tuo Mac, entra in questa cartella (`cd "/Users/marcoregondi/Desktop/Runners Lab/RaceCalendarScraper"`) e lancia questi comandi:
   ```bash
   git init
   git add .
   git commit -m "Primo commit del motore backend"
   git branch -M main
   git remote add origin https://github.com/TUO-USERNAME/runners-lab-calendar.git
   git push -u origin main
   ```
3. Fatto! Da questo momento, se vai nella scheda "Actions" del tuo repository GitHub, vedrai l'automazione già pronta per partire.
4. Dopo la prima esecuzione, il file `races.json` sarà visibile online a questo link crudo (sostituisci il tuo username):
`https://raw.githubusercontent.com/TUO-USERNAME/runners-lab-calendar/main/races.json`

## Modificare l'App iOS
Una volta che hai il link Raw di GitHub, torna su Xcode, apri `RaceCalendarView.swift` e sostituisci la funzione finta `fetchRaces()` con quella vera che fa la chiamata di rete al tuo nuovo link!
