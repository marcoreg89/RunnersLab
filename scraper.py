import json
import uuid
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_fidal():
    url = "https://www.fidal.it/calendario.php"
    year = datetime.now().year
    
    # Parametri di ricerca sul sito FIDAL (tipo=6 è 'Strada')
    params = {
        'anno': year,
        'mese': 0,
        'livello': 0,
        'tipo': 6, 
        'submit': 'Invia'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    races = []
    
    # Analizza tutte le righe della tabella del calendario
    rows = soup.find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 6:
            date_str = cols[1].text.strip() # Es. "02/06"
            level = cols[2].text.strip() # "N" (Nazionale), "I" (Internazionale)
            
            name_col = cols[3]
            name = name_col.find('a').text.strip() if name_col.find('a') else name_col.text.strip()
            
            distance_font = name_col.find('font')
            distance = distance_font.text.strip().lower() if distance_font else ""
            
            location = cols[5].text.strip()
            
            # Filtro intelligente per individuare Maratone e Mezze
            is_marathon = "marathon" in name.lower() or "maratona" in name.lower() or "42.195" in distance or "42 km" in distance
            is_half = "half" in name.lower() or "mezza" in name.lower() or "21.097" in distance or "21 km" in distance
            
            # Se la parola 'mezza' o 'half' è presente, vince su 'maratona'
            if is_half:
                is_marathon = False
                
            if is_marathon or is_half:
                try:
                    # Formatta la data nel formato atteso dall'App iOS (yyyy-MM-dd)
                    day, month = date_str.split('/')
                    # Alcune gare durano due giorni, es "11-12/04", teniamo solo il primo giorno
                    if '-' in day:
                        day = day.split('-')[0]
                    
                    race_date = f"{year}-{month}-{day}"
                except:
                    continue
                    
                race_type = "Maratona" if is_marathon else "Mezza Maratona"
                is_intl = (level == "I" or level == "INT")
                
                races.append({
                    "id": str(uuid.uuid4()),
                    "date": race_date,
                    "name": name,
                    "location": location,
                    "type": race_type,
                    "status": "Confermata",
                    "isInternational": is_intl
                })
                
    return races

def main():
    print("Avvio scraper FIDAL ufficiale...")
    races = scrape_fidal()
    
    # Rimuovi eventuali duplicati
    unique_races = []
    seen = set()
    for r in races:
        key = (r['date'], r['name'])
        if key not in seen:
            seen.add(key)
            unique_races.append(r)
            
    # Ordina cronologicamente
    unique_races.sort(key=lambda x: x['date'])
    
    with open('races.json', 'w', encoding='utf-8') as f:
        json.dump(unique_races, f, ensure_ascii=False, indent=2)
        
    print(f"Completato! Estratte {len(unique_races)} gare dal sito ufficiale FIDAL.")

if __name__ == '__main__':
    main()
