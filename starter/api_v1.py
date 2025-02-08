import requests
import time
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

    def get_order_book(self, trade_pair):

        """
        Public endpoint: Retrieve order book asks and bids.
        :param trade_pair: Trading pair string (e.g., "BTC_USD")
        :return: Raw JSON data response from GET /v1/public/get-order-book
        """

        params = {"trade_pair": trade_pair}

        return self._request(
            "GET",
            endpoint="/v1/public/get-order-book",
            params=params
        )