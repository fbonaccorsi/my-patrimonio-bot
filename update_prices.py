import os
import requests
from bs4 import BeautifulSoup

# Configurazione credenziali dai Secrets di GitHub
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_investing_price(isin):
    # URL specifico per i BTP su Investing.com
    url = f"https://it.investing.com/rates-bonds/{isin.lower()}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cerchiamo il prezzo nel tag HTML usato da Investing
        price_tag = soup.find("div", {"data-test": "instrument-price-last"})
        if price_tag:
            # Puliamo la stringa (es: "104,33" -> 104.33)
            price_str = price_tag.text.replace('.', '').replace(',', '.')
            return float(price_str)
        else:
            print(f"Prezzo non trovato nella pagina per {isin}")
            return None
    except Exception as e:
        print(f"Errore durante il recupero del prezzo: {e}")
        return None

def update_supabase(isin, price):
    url = f"{SUPABASE_URL}/rest/v1/patrimonio?isin=eq.{isin}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    data = {"prezzo_unitario": price}
    
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code in [200, 204] and len(result) > 0:
        print(f"✅ Database aggiornato con successo: {isin} = {price}")
    elif len(result) == 0:
        print(f"⚠️ Attenzione: Supabase dice OK, ma non ha trovato righe con ISIN {isin} o l'RLS blocca l'aggiornamento.")
    else:
        print(f"❌ Errore Supabase: {response.status_code} - {response.text}")
        
    print(f"Risposta SQL di Supabase: {response.status_code}")
if __name__ == "__main__":
    # Inserisci qui il tuo ISIN
    mio_isin = "IT0005583486"
    
    print(f"Avvio recupero prezzo per {mio_isin}...")
    prezzo_attuale = get_investing_price(mio_isin)
    
    if prezzo_attuale:
        update_supabase(mio_isin, prezzo_attuale)
    else:
        print("Impossibile procedere con l'aggiornamento.")
