from __future__ import annotations

import os
import logging
from dataclasses import dataclass, field
from pprint import pformat

def api_auth():
    """Load API authentication credentials from environment variables."""
    return {"stock_api_key": os.getenv("ALPHA_VANTAGE_API")}

@dataclass
class ApiConfig:
    """Base configuration class for market requests (e.g., crypto or stock)."""
    symbol: str = "BTC"
    market: str = "crypto"  # 'crypto' or 'stock'
    mode: str = "live"  # "live" or "historical"
    auth_creds: dict = field(init=False)
    sleep_interval: int = 60

    def __post_init__(self):
        self.auth_creds = api_auth()
        logging.debug(f"Initialized base market config: {pformat(self.__dict__)}")

    def load_config(self):
        """Dynamically load the appropriate configuration based on market and mode."""
        if self.market == 'crypto':
            return CryptoConfig(mode=self.mode)
        elif self.market == 'stock':
            return StockConfig(mode=self.mode)
        else:
            raise ValueError(f"Invalid market: {self.market}. Please choose 'crypto' or 'stock'.")


@dataclass
class CryptoConfig(ApiConfig):
    """Configuration for crypto market requests."""
    currency: str = "USDT"
    exchange_name: str = "binance"
    interval: str = "15m"
    batch_size: int = 2
    max_items: int = 6
    since: str = "31/10/2024"
    limit: int = 1000
    apikey: str = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.mode == "historical":
            self.interval = "30m"
        logging.debug(f"Initialized crypto config: {pformat(self.__dict__)}")

@dataclass
class StockConfig(ApiConfig):
    """Configuration for stock market requests."""
    base_url: str = "https://www.alphavantage.co/query"
    function: str = field(init=False)
    interval: str = "15min"
    outputsize: str = "compact"
    apikey: str = None
    
    def __post_init__(self):
        super().__post_init__()
        self.function = "TIME_SERIES_INTRADAY" if self.mode == "live" else "TIME_SERIES_DAILY"
        if self.mode == "live":
            self.interval = "1min"
        logging.debug(f"Initialized stock config: {pformat(self.__dict__)}")

@dataclass
class RequestParams:
    """Dataclass for storing request-specific parameters."""
    symbol: str
    interval: str = "15min"
    outputsize: str = None
    function: str = None
    base_url: str = None
    exchange_name: str = None
    batch_size: int = None
    max_items: int = None
    since: str = None
    limit: int = None
    currency: str = None
    apikey: str = None
