from typing import List
import requests
import time
from app.entities import( 
    TradesApiResponse,
    OrderBookApiResponse,
    OrderPayload,
    OrderApiResponse,
    TradingPairsApiResponse
)

class MoonApi:
    def __init__(self, base_url: str, access_key: str, secret_key: str, nonce=None):
        """
        Initialize the MoonBot client.
        :param base_url: The API base URL (e.g., "https://api.tothemoon.com")
        :param access_key: Your API access key (required for private endpoints)
        :param secret_key: Your API secret key (required for private endpoints)
        :param nonce: Starting nonce value; if None, defaults to the current Unix timestamp
        """
        self.base_url = base_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.nonce = nonce if nonce is not None else int(time.time())

    def _increment_nonce(self):
        """Increment and return the new nonce value."""
        self.nonce += 1
        return self.nonce
    
    def _get_headers(self, private=False):
        """
        Build headers for requests.
        For private endpoints, include Access-Key, Secret-Key, and a unique Nonce.
        """
        headers = {
            "Content-Type": "application/json",
            # "Accept": "application/json",
        }
        if private:
            if not self.access_key or not self.secret_key:
                raise ValueError("Access key and Secret key are required for private endpoints.")
            headers["Access-Key"] = self.access_key
            headers["Secret-Key"] = self.secret_key
            headers["Nonce"] = str(self._increment_nonce())
        return headers

    def _request(
            self, method, endpoint, params=None, json=None, data=None, private=False
        ):
        """
        Generic request handler.
        :param method: "GET" or "POST"
        :param endpoint: API endpoint (e.g., "/v1/private/get-balances")
        :param params: Query parameters (for GET requests)
        :param json_data: JSON body (for POST requests)
        :param private: Boolean flag to indicate if the endpoint is private (needs auth headers)
        :return: Parsed JSON response from the API
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(private=private)
        
        if method.upper() == "GET":
            response = requests.get(
                url, headers=headers, params=params
            )
        elif method.upper() == "POST":
            response = requests.post(
                url, headers=headers, json=json, data=data
            )
        else:
            raise ValueError("Unsupported HTTP method: {}".format(method))
        
        return response.json()
    
    # --------------------- Public Endpoints ---------------------

    def get_trade_pairs(self) -> TradingPairsApiResponse:
        """
        Public endpoint: Retrieve public trade pairs (e.g., "BTC_USD").
        :return: List of TradePair JSON data response from GET /v1/public/get-trade-pairs
        """

        params = {}

        response =  self._request(
            "GET",
            endpoint="/v1/public/get-trade-pairs",
            params=params
        )

        return TradingPairsApiResponse(**response)
    

    def get_trades_v2(self, trade_pair: str) -> TradesApiResponse:
        """
        Public endpoint: Retrieve public trades for a given trading pair.
        :param trade_pair: Trading pair string (e.g., "BTC_USD")
        :return: Raw JSON data response from GET /v1/public/get-trades
        """

        params = {"trade_pair": trade_pair}

        response =  self._request(
            "GET",
            endpoint="/v1/public/get-trades",
            params=params
        )

        return TradesApiResponse(**response)
    
    
    def get_order_book_v2(self, trade_pair: str) -> OrderBookApiResponse:
        """
        Public endpoint: Retrieve public trades for a given trading pair.
        :param trade_pair: Trading pair string (e.g., "BTC_USD")
        :return: Raw JSON data response from GET /v1/public/get-trades
        """

        params = {"trade_pair": trade_pair}

        response =  self._request(
            "GET",
            endpoint="/v1/public/get-order-book",
            params=params
        )

        return OrderBookApiResponse(**response)

    def get_public_trades(self, trade_pair):
        
        params = {"trade_pair": trade_pair}
        
        return self._request(
            "GET", 
            endpoint="/v1/public/get-trades",
            params=params,
            private=False
        )

    # --------------------- Private Endpoints ---------------------
    
    def get_balances(self):
        """
        Get account balances.
        :return: Raw JSON data response from GET /v1/private/get-balances
        """

        return self._request(
            "GET",
            endpoint="/v1/private/get-balances",
            private=True
        )
    

    def get_order(self, order_id):
        """
        Query for order details.
        :param order_id: Order identifier returned by create_order.
        :return: Raw JSON data response from GET /v1/private/get-order
        """
        return self._request(
            "GET",
            endpoint="/v1/private/get-order",
            params={"order_id": order_id},
            private=True
        )
    

    def get_orders(self, trade_pair=None, status=None, limit=100, start_created_at=None, ids=None):
        """
        Retrieve all client orders with optional filters.
        :param trade_pair: Filter by trading pair (optional)
        :param status: Filter by order status (optional)
        :param limit: Maximum number of orders to return (default 100, max 500)
        :param start_created_at: Unix timestamp filter (optional)
        :param ids: Comma separated string of order identifiers (optional)
        :return: Raw JSON data response from GET /v1/private/get-orders
        """
        params = {}
        if trade_pair is not None:
            params["trade_pair"] = trade_pair
        if status is not None:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit
        if start_created_at is not None:
            params["start_created_at"] = start_created_at
        if ids is not None:
            params["ids"] = ids

        return self._request(
            "GET",
            endpoint="/v1/private/get-orders",
            params=params,
            private=True
        )
    

    def get_user_trades(self, trade_pair=None, limit=100, start=None, order_id=None):
        """
        List user trades with optional filters.
        :param trade_pair: Filter by trading pair (optional)
        :param limit: Maximum number of trades to return (default 100, max 500)
        :param start: Unix timestamp filter for trade time (optional)
        :param order_id: Order identifier to filter trades (optional)
        :return: Raw JSON data response from GET /v1/private/get-trades
        """
        params = {}
        if trade_pair is not None:
            params["trade_pair"] = trade_pair
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        if order_id is not None:
            params["order_id"] = order_id
        return self._request(
            "GET", 
            endpoint="/v1/private/get-trades", 
            params=params, 
            private=True)


    def cancel_order(self, order_id):
        """
        Query for cancel an order.
        :param order_id: Order identifier returned by create_order.
        :return: Raw JSON data response from GET /v1/private/get-order
        """
        return self._request(
            "POST",
            endpoint="/v1/private/cancel-order",
            json={"order_id": order_id},
            private=True
        )
    

    def cancel_all_orders(self):
        """
        Cancel all orders with status NEW.
        :return: Raw JSON data response from POST /v1/private/cancel-all-orders
        """
        return self._request(
            "POST",
            endpoint="/v1/private/cancel-all-orders",
            json={},
            private=True
        )
    

    def create_order_v2(
            self,
            payload: OrderPayload
    ) -> OrderApiResponse:
        """
        Public endpoint: Creates an order and retrieves the uid.
        :param payload: Order payload data
        :return: Raw JSON data response from GET /v1/public/get-trades
        """
        
        data = payload.model_dump(exclude_none=True)

        response = self._request(
            "POST",
            endpoint="/v1/private/create-order",
            data=data,
            private=True
        )

        return OrderApiResponse(**response)
    
    def create_order(
            self,
            trade_pair,
            order_type,
            side, amount,
            time_in_force="GTC",
            ttl=None, 
            client_order_id=None, 
            price=None, 
            quote_order_qty=None
        ):
        """
        Create an order.
        :param trade_pair: Trading pair (e.g., "BTC_USD")
        :param order_type: "LIMIT" or "MARKET"
        :param side: "BUY" or "SELL"
        :param amount: Decimal amount value (can be string or number)
        :param time_in_force: Optional; default is "GTC" (other options: IOC, FOK, GTD)
        :param ttl: Only for GTD orders (optional)
        :param client_order_id: Unique client-side order id (optional)
        :param price: Price value as a decimal (required for LIMIT orders)
        :param quote_order_qty: Quote order quantity (required for MARKET orders if amount is not used)
        :return: Raw JSON data response from POST /v1/private/create-order
        """
        payload = {
            "trade_pair": trade_pair,
            "type": order_type,
            "side": side,
            "amount": str(amount)
        }

        if time_in_force:
            payload["time_in_force"] = time_in_force
        if ttl is not None:
            payload["ttl"] = ttl
        if client_order_id is not None:
            payload["client_order_id"] = client_order_id
        if price is not None:
            payload["price"] = str(price)
        if quote_order_qty is not None:
            payload["quote_order_qty"] = str(quote_order_qty)
        
        return self._request(
            "POST", 
            endpoint="/v1/private/create-order",
            json=payload,
            private=True
        )
