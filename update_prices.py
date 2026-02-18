import requests
import os

# Recupera le chiavi dai segreti di GitHub
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def get_yahoo_price(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    # Questo header serve a simulare un browser reale
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    
    try:
        return data['chart']['result'][0]['meta']['regularMarketPrice']
    except (KeyError, TypeError, IndexError):
        print(f"Errore nel recupero del prezzo per {ticker}")
        return None

# Esempio: Aggiorna il BTP
prezzo_btp = get_yahoo_price("IT0005565392.MI")

# Invia a Supabase (Upsert)
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

payload = {
    "nome_asset": "BTP Valore",
    "prezzo_unitario": prezzo_btp
}

requests.post(f"{SUPABASE_URL}/rest/v1/patrimonio", json=payload, headers=headers)
print(f"Aggiornato BTP: {prezzo_btp}")
