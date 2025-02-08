from flask import Blueprint, jsonify, request
import time
import random
from app.moon_api import MoonApi  

bot_blueprint = Blueprint('bot', __name__)
bot_running = False
log_messages = []


TOTHMOON_API_BASE_URL = "https://api.tothemoon.com"

# Credenziali account 2
API_KEY_2 = "your_api_key_account_2"
API_SECRET_2 = "your_api_secret_account_2"

# Initialize API client
moon_api = MoonApi(TOTHMOON_API_BASE_URL, ACCESS_KEY, SECRET_KEY)
account_2 = MoonApi(TOTHMOON_API_BASE_URL, API_KEY_2, API_SECRET_2)


# Bot logic
TRADE_PAIR = "BTC_USD"
ORDER_SIZE_RANGE = (0.001, 0.005)
ORDER_FREQUENCY_RANGE = (30, 120)

def fetch_trades(trading_pair):
    append_log("Fetching latest trades...")
    try:
        trades = moon_api.get_trades_v2(trading_pair)
        if trades.status == "OK":
            for trade in trades.data[:5]:  # Log the latest 5 trades
                append_log(f"Trade ID: {trade.trade_id}, Price: {trade.price}, Amount: {trade.amount}, Time: {trade.time}")
        else:
            append_log(f"Error fetching trades: {trades.error}")
    except Exception as e:
        append_log(f"Exception occurred: {str(e)}")

def fetch_trading_pairs():
    append_log("Fetching trading pairs...")
    
    try:
        trading_pairs = moon_api.get_trade_pairs()
        if trading_pairs.status == "OK":
            for pair in trading_pairs.data:
                append_log(f"Base currency: {pair.base_currency}")
                append_log(f"Quoted currency: {pair.quoted_currency}")
                append_log(f"Trade pair: {pair.trade_pair}")
        else:
            append_log(f"Error fetching trades: {trading_pairs.error}")

    except Exception as e:
        append_log(f"Exception occurred: {str(e)}")

def fetch_account_balance():
    append_log("Fetching account balances...")
    try:
        balances = moon_api.get_balances()
        append_log(f"Account balances: {balances}")
        # if trades.status == "OK":
        #     for trade in trades.data[:5]:  # Log the latest 5 trades
        #         append_log(f"Trade ID: {trade.trade_id}, Price: {trade.price}, Amount: {trade.amount}, Time: {trade.time}")
        # else:
        #     append_log(f"Error fetching trades: {trades.error}")
    except Exception as e:
        append_log(f"Exception occurred: {str(e)}")

def fetch_order_book(trading_pair):
    append_log("Fetching order book...")
    try:
        order_book = moon_api.get_order_book_v2(trading_pair)
        if order_book.status == "OK":
            append_log(f"Bids: {order_book.data.bids}")  
            append_log(f"Asks: {order_book.data.asks}")  
        else:
            append_log(f"Error fetching trades: {order_book.error}")
    except Exception as e:
        append_log(f"Exception occurred: {str(e)}")

def get_order_id(order_data):
    return order_data.get("order_id", "error")

def random_wait(random_time):
    append_log(f"Aspetto {random_time} secondi prima del prossimo ciclo...")
    time.sleep(random_time)

def price_rnd(mid_price):
    return round(mid_price * random.uniform(0.999, 1.001), 2)

def get_mid_price():

    orders = moon_api.get_order_book_v2(TRADE_PAIR)

    bids = orders.get("bids", [])
    asks = orders.get("asks", [])
    
    if bids and asks:
        bid = float(bids[0][0])
        ask = float(asks[0][0])
        return (bid + ask) / 2
    return None

def ping_pong_bot(trading_pair):
    append_log("Avvio del bot PING-PONG...")
    while True:
        try:
            order_size = round(random.uniform(*ORDER_SIZE_RANGE), 6)
            mid_price = get_mid_price()

            if mid_price is None:
                append_log("Impossibile ottenere il prezzo medio, riprovo...")
                time.sleep(5)
                continue
            
            # PING
            price_1 = price_rnd(mid_price)
            append_log(f"BUY - Size: {order_size}, Prezzo: {price_1} STARTED From Account 1: piazzo ordine di acquisto.")
            
            order_data = moon_api.create_order(
                trade_pair=trading_pair, order_type="LIMIT", side="BUY",
                amount=order_size, time_in_force="GTC",  price=price_1,
                # ttl="", # GTD orders only
                # client_order_id = "",
                # quote_order_qty="" # "MARKET" orders only, if amount is not used
            )

            order_id = get_order_id(order_data)
            append_log(f"Order Id: {order_id}")

            random_wait(round(random.randint(111111,211111)/100000,2))
            append_log(f"SELL STARTED From Account 2: colpisco l'ordine di Account 1 vendendo.")

            account_2.create_order(
                trade_pair=trading_pair, order_type="LIMIT", side="SELL",
                amount=order_size, time_in_force="GTC", price=price_1
            )

            random_wait(random.randint(*ORDER_FREQUENCY_RANGE))

            # PONG
            price_2 = price_rnd(mid_price)
            append_log(f"BUY - Size: {order_size}, Prezzo: {price_2} STARTED From Account 2: piazzo ordine di acquisto.")
            
            account_2.create_order(
                trade_pair=trading_pair, order_type="LIMIT", side="BUY",
                amount=order_size, time_in_force="GTC", price=price_2
            )
            time.sleep(round(random.randint(111111,211111)/100000,2)) # Ritardo Casuale

            append_log(f"SELL STARTED From Account 1: colpisco l'ordine di Account 2 vendendo.")
            moon_api.create_order(
                trade_pair=trading_pair, order_type="LIMIT", side="SELL",
                amount=order_size, time_in_force="GTC", price=price_2,
            )
            
            random_wait(random.randint(*ORDER_FREQUENCY_RANGE))

        except Exception as e:
            append_log(f"Errore nel bot: {e}")
            time.sleep(5)

def append_log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_messages.append(f"[{timestamp}] {message}")

def pair(data):
    return data.get("trading_pair", TRADE_PAIR)

@bot_blueprint.route('/start', methods=['POST'])
def start_bot():
    global bot_running
    if not bot_running:
        bot_running = True
        append_log("Bot started.")
        return jsonify({"message": "Bot started."}), 200
    else:
        return jsonify({"message": "Bot already running."}), 400

@bot_blueprint.route('/stop', methods=['POST'])
def stop_bot():
    global bot_running
    if bot_running:
        bot_running = False
        append_log("Bot stopped.")
        return jsonify({"message": "Bot stopped."}), 200
    else:
        return jsonify({"message": "Bot is not running."}), 400

@bot_blueprint.route('/fetch_trades', methods=['POST'])
def fetch_trades_endpoint():
    if not bot_running:
        return jsonify({"message": "Bot is not running. Start the bot first."}), 400

    fetch_trades(pair(request.get_json()))

    return jsonify({"message": "Trades fetched and logged."}), 200

@bot_blueprint.route('/fetch_order_book', methods=['POST'])
def fetch_order_book_endpoint():
    if not bot_running:
        return jsonify({"message": "Bot is not running. Start the bot first."}), 400

    fetch_order_book(pair(request.get_json()))

    return jsonify({"message": "Order book fetched and logged."}), 200

@bot_blueprint.route('/fetch_trading_pairs', methods=['POST'])
def fetch_trading_pairs_endpoint():
    if not bot_running:
        return jsonify({"message": "Bot is not running. Start the bot first."}), 400

    fetch_trading_pairs()

    return jsonify({"message": "Trading pairs and logged."}), 200


@bot_blueprint.route('/ping', methods=['POST'])
def ping_endpoint():
    if not bot_running:
        return jsonify({"message": "Bot is not running. Start the bot first."}), 400

    ping_pong_bot(pair(request.get_json()))

    return jsonify({"message": "Order book fetched and logged."}), 200


@bot_blueprint.route('/fetch_account_balance', methods=['POST'])
def fetch_account_balance_endpoint():
    if bot_running:
        fetch_account_balance()
        return jsonify({"message": "Account balance fetched and logged."}), 200
    else:
        return jsonify({"message": "Bot is not running. Start the bot first."}), 400
    

@bot_blueprint.route('/logs', methods=['GET'])
def get_logs():
    logs = "\n".join(log_messages[-50:])
    return jsonify(logs), 200