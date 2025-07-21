import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz

# Configurazione
FINNHUB_TOKEN = os.getenv("FINNHUB_TOKEN")
TWELVEDATA_TOKEN = os.getenv("TWELVEDATA_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
WATCHLIST = ["GOOG", "LDO.MI", "STLAM.MI", "NEE", "XOM"]

# Timezone
tz = pytz.timezone("Europe/Rome")

# Funzione per invio messaggi su Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Errore Telegram: {e}")

# Funzione per ottenere dati da TwelveData
def get_price_data(symbol, interval="1h", outputsize=100):
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": TWELVEDATA_TOKEN,
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "values" in data:
        df = pd.DataFrame(data["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime")
        df.set_index("datetime", inplace=True)
        df = df.astype(float)
        return df
    else:
        print(f"Dati non disponibili per {symbol}")
        return None
