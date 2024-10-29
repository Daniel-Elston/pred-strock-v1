from __future__ import annotations

from dataclasses import dataclass, field
import os
from pprint import pformat
import logging

def api_auth():
    """Load API authentication credentials from environment variables."""
    return {"stock_api_key": os.getenv("ALPHA_VANTAGE_API")}

@dataclass
class ApiConfig:
    """
    General API configuration class. Loads market-specific configurations based on the market and mode.
    """
    auth_creds: dict = field(init=False)
    symbol: str = 'BTC'
    market: str = 'crypto'  # 'crypto' or 'stock'
    mode: str = 'live'  # 'live' or 'historical'
    sleep_interval: int = 60
    
    def __post_init__(self):
        self.auth_creds = api_auth()
        logging.debug(f"Initialised general config {self.__class__.__name__}:\n{pformat(self.__dict__)}\n")

    def load_config(self):
        """Dynamically load the appropriate configuration based on market and mode."""
        if self.market == 'crypto':
            return CryptoConfig(mode=self.mode)
        elif self.market == 'stock':
            return StockConfig(mode=self.mode)#, auth_creds=self.auth_creds)
        else:
            raise ValueError(f"Invalid market: {self.market}. Please choose 'crypto' or 'stock'.")

@dataclass
class CryptoConfig(ApiConfig):
    """Configuration for crypto market requests."""
    mode: str
    symbol: str
    currency: str = "USDT"
    exchange_name: str = "binance"
    interval: str = '15m'
    batch_size: int = 2
    max_items: int = 6
    since: str = '25/10/2024'
    limit: int = 1000

    def __post_init__(self):
        if self.mode == 'historical':
            self.interval = '30m'
        logging.debug(f"Initialised market config {self.__class__.__name__}:\n{pformat(self.__dict__)}\n")


@dataclass
class StockConfig(ApiConfig):
    """Configuration for stock market requests, including API-specific parameters."""
    auth_creds: dict
    mode: str
    symbol: str
    base_url: str = "https://www.alphavantage.co/query"
    function: str = field(init=False)
    interval: str = "15min"
    outputsize: str = 'full'

    def __post_init__(self):
        # Set function based on mode
        if self.mode == 'live':
            self.function = "TIME_SERIES_INTRADAY"
            self.interval = "1min"
            self.outputsize = "compact"
        elif self.mode == 'historical':
            self.function = "TIME_SERIES_DAILY"
            self.outputsize = "full"
        logging.debug(f"Initialised market config {self.__class__.__name__}:\n{pformat(self.__dict__)}\n")
