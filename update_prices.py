import requests
import os

# Recupera le chiavi dai segreti di GitHub
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def get_yahoo_price(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1d"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data['chart']['result'][0]['meta']['regularMarketPrice']

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
