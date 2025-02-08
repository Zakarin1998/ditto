
import random

# Bot logic
TRADE_PAIR = "BTC_USD"

def pair(data):
    return data.get("trading_pair", TRADE_PAIR)

def random_range(tpl_range, precision):
    return round(random.uniform(*tpl_range), precision)

def random_int(tpl_range):
    return random.randint(*tpl_range)

def price_rnd(mid_price):
    return round(mid_price * random_range((0.999, 1.001), 2))

# Mid-price calculation methods
def simple_mid_price(bids, asks):
    best_bid = bids[0][0]
    best_ask = asks[0][0]
    return (best_bid + best_ask) / 2

def volume_weighted_mid_price(bids, asks):
    best_bid_price, best_bid_size = bids[0]
    best_ask_price, best_ask_size = asks[0]
    return ((best_bid_price * best_bid_size) + (best_ask_price * best_ask_size)) / (best_bid_size + best_ask_size)

def order_book_depth_mid_price(bids, asks, depth=3):
    total_bid_value = sum(price * size for price, size in bids[:depth])
    total_ask_value = sum(price * size for price, size in asks[:depth])
    total_bid_size = sum(size for _, size in bids[:depth])
    total_ask_size = sum(size for _, size in asks[:depth])
    return (total_bid_value + total_ask_value) / (total_bid_size + total_ask_size)