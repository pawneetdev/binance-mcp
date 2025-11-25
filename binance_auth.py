"""
Binance API authentication handler.

Implements HMAC-SHA256 signature authentication for Binance API.
"""

import hmac
import hashlib
import time
from typing import Dict

from adapter import AuthHandler
from adapter.runtime.auth import AuthType


class BinanceAuth(AuthHandler):
    """
    Binance API authentication handler.

    Uses HMAC-SHA256 signature authentication with API key and secret.
    Automatically adds timestamp and signature to requests.
    """

    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize Binance authentication.

        Args:
            api_key: Binance API key
            api_secret: Binance API secret for HMAC signing
        """
        self.api_key = api_key
        self.api_secret = api_secret

    def apply(self, headers: Dict[str, str], params: Dict[str, str]) -> None:
        """
        Apply Binance authentication to the request.

        Adds:
        - X-MBX-APIKEY header with API key
        - timestamp parameter (current time in milliseconds)
        - signature parameter (HMAC-SHA256 of query string)
        """
        # Add API key to headers
        headers["X-MBX-APIKEY"] = self.api_key

        # Add timestamp to params
        timestamp = str(int(time.time() * 1000))
        params["timestamp"] = timestamp

        # Create query string and generate signature
        query_string = "&".join([f"{key}={value}" for key, value in sorted(params.items())])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # Add signature to params
        params["signature"] = signature

    def get_type(self) -> AuthType:
        """Return API_KEY type for Binance auth."""
        return AuthType.API_KEY

    def __repr__(self) -> str:
        return "BinanceAuth(api_key='***')"
