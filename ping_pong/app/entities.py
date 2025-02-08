"""Module for ToTheMoon entities."""

from pydantic import BaseModel
from typing import List, Optional, Tuple

class TradeData(BaseModel):
    trade_id: int
    price: str
    amount: str
    time: float

class OrderBookData(BaseModel):
    bids: List[Tuple[float, float]]
    asks: List[Tuple[float, float]]

class TradePairData(BaseModel):
    trade_pair: str
    base_currency: str
    quoted_currency: str

class ApiResponse(BaseModel):
    status: str
    error: Optional[str]

class ErrorCodes(str):
    INSUFFICIENT_FUND = "INSUFFICIENT_FUND"
    INVALID_REQUEST = "INVALID_REQUEST"
    INVALID_KEY = "INVALID_KEY"
    INVALID_TIMESTAMP = "INVALID_TIMESTAMP"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"
    DUPLICATE_CLIENT_ORDER_ID = "DUPLICATE_CLIENT_ORDER_ID"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"

class OrderNature(str):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(str):
    PENDING = "PENDING"
    NEW = "NEW"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"

class TimeInForce(str):
    GTC = "GTC"
    GTD = "GTD"
    FOK = "FOK"
    IOC = "IOC"

class PaymentStatus(str):
    INITIALIZED = "INITIALIZED"
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"
    DECLINED = "DECLINED"

class OrderBookType(str):
    AGGREGATED = "AGGREGATED"
    BEST = "BEST"  # Currently not supported
    FULL = "FULL"  # Currently not supported

class CandlesInterval(str):
    M1 = "M1"
    M20 = "M20"
    H1 = "H1"
    H6 = "H6"
    D1 = "D1"
    
class OrderPayload(BaseModel):
    trade_pair: str
    order_type: str
    side: str
    amount: float
    price: Optional[float] = None,
    time_in_force: str = "GTC",
    ttl: Optional[int] = None,
    client_order_id: Optional[int] = None,
    quote_order_qty: Optional[float] = None

class OrderId(BaseModel):
    order_id: str

class TradesApiResponse(ApiResponse):
    data: List[TradeData]

class OrderApiResponse(ApiResponse):
    data: OrderId

class TradingPairsApiResponse(ApiResponse):
    data: List[TradePairData]

class OrderBookApiResponse(ApiResponse): 
    data: OrderBookData
