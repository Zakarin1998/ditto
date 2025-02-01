
'''Attraverso API devo collegare due conti dello stesso exchange. 
Ecco la logica: il bot piazza un ordine di acquisto con l'account 1 ad un livello compreso tra lo spread tra bid e ask.
Appena è stato piazzato l'ordine, l'ordine viene colpito interamente dall'account 2. 
A questo punto il bot piazza un ordine di acquisto con l'account 2 ad un livello compreso tra lo spread tra bid e ask.
Appena è stato piazzato l'ordine, l'ordine viene colpito interamente dall'account 1.
Il ciclo si ripete fino a quando non interrompo il bot. 
La size degli ordini deve essere casuale in un range che definisce l'utente. 
La frequenza degli ordine deve essere casuale in un range che definisce l'utente, es. 10 ordini in 1 h distribuiti casualmente. '''

import requests
import time
import random

# Configurazione API Tothemoon
BASE_URL = "https://api.tothemoon.com/v1"

# Credenziali account 1
API_KEY_1 = "your_api_key_account_1"
API_SECRET_1 = "your_api_secret_account_1"

# Credenziali account 2
API_KEY_2 = "your_api_key_account_2"
API_SECRET_2 = "your_api_secret_account_2"

# Configurazione coppia di trading e altri parametri
SYMBOL = "BTC-USDT"
ORDER_SIZE_RANGE = (0.001, 0.005)
ORDER_FREQUENCY_RANGE = (30, 120)

# Funzione per ottenere il prezzo medio tra bid e ask
def get_mid_price():
    response = requests.get(f"{BASE_URL}/market/orderbook", params={"symbol": SYMBOL})
    data = response.json()
    bids = data.get("bids", [])
    asks = data.get("asks", [])
    
    if bids and asks:
        bid = float(bids[0][0])
        ask = float(asks[0][0])
        return (bid + ask) / 2
    return None

# Funzione per creare un ordine
def place_order(api_key, side, amount, price):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    order_data = {
        "symbol": SYMBOL,
        "side": side,
        "type": "limit",
        "quantity": amount,
        "price": price
    }
    response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
    return response.json()

# Funzione principale per il bot ping-pong
def ping_pong_bot():
    print("Avvio del bot PING-PONG...")
    while True:
        try:
            order_size = round(random.uniform(*ORDER_SIZE_RANGE), 6)
            mid_price = get_mid_price()

            if mid_price is None:
                print("Impossibile ottenere il prezzo medio, riprovo...")
                time.sleep(5)
                continue

            price_1 = round(mid_price * random.uniform(0.999, 1.001), 2)
            print(f"Account 1: piazzo ordine di acquisto - Size: {order_size}, Prezzo: {price_1}")
            place_order(API_KEY_1, "buy", order_size, price_1)
            
            #inserire un ritardo di 1-2 secondi per fillare l'ordine 1

            print(f"Account 2: colpisco l'ordine di Account 1 vendendo")
            place_order(API_KEY_2, "sell", order_size, price_1)

            sleep_time = random.randint(*ORDER_FREQUENCY_RANGE)
            print(f"Aspetto {sleep_time} secondi prima del prossimo ciclo...")
            time.sleep(sleep_time)

            price_2 = round(mid_price * random.uniform(0.999, 1.001), 2)
            print(f"Account 2: piazzo ordine di acquisto - Size: {order_size}, Prezzo: {price_2}")
            place_order(API_KEY_2, "buy", order_size, price_2)

            #inserire un ritardo di 1-2 secondi per fillare l'ordine 2
            
            print(f"Account 1: colpisco l'ordine di Account 2 vendendo")
            place_order(API_KEY_1, "sell", order_size, price_2)

            sleep_time = random.randint(*ORDER_FREQUENCY_RANGE)
            print(f"Aspetto {sleep_time} secondi prima del prossimo ciclo...")
            time.sleep(sleep_time)

        except Exception as e:
            print(f"Errore nel bot: {e}")
            time.sleep(5)

# Avviare il bot
if __name__ == "__main__":
    ping_pong_bot()
