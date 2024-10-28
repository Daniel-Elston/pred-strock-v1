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
    market: str = 'stock'  # 'crypto' or 'stock'
    mode: str = 'historical'  # 'live' or 'historical'
    sleep_interval: int = 60
    auth_creds: dict = field(init=False)
    
    def __post_init__(self):
        self.auth_creds = api_auth()
        logging.debug(f"Initialised general config {self.__class__.__name__}:\n{pformat(self.__dict__)}")

    def load_config(self):
        """Dynamically load the appropriate configuration based on market and mode."""
        if self.market == 'crypto':
            return CryptoConfig(mode=self.mode)
        elif self.market == 'stock':
            return StockConfig(mode=self.mode, auth_creds=self.auth_creds)
        else:
            raise ValueError(f"Invalid market: {self.market}. Please choose 'crypto' or 'stock'.")

@dataclass
class CryptoConfig:
    """Configuration for crypto market requests."""
    mode: str
    symbol: str = "BTC"
    currency: str = "USDT"
    exchange_name: str = "binance"
    interval: str = '15m'
    batch_size: int = 2
    max_items: int = 6
    since: str = '25/10/2024'
    limit: int = 1000

    def __post_init__(self):
        if self.mode == 'historical':
            self.interval = '30m'  # Override default interval for historical mode
        logging.debug(f"Initialised market config {self.__class__.__name__}:\n{pformat(self.__dict__)}")


@dataclass
class StockConfig:
    """Configuration for stock market requests, including API-specific parameters."""
    mode: str
    auth_creds: dict
    symbol: str = 'NVDA'
    base_url: str = "https://www.alphavantage.co/query"
    function: str = field(init=False)
    interval: str = "15m"
    outputsize: str = 'full'

    def __post_init__(self):
        # Set function based on mode
        if self.mode == 'live':
            self.function = "TIME_SERIES_INTRADAY"
            self.interval = "15m"
            self.outputsize = "compact"
        elif self.mode == 'historical':
            self.function = "TIME_SERIES_DAILY"
            self.outputsize = "full"
        logging.debug(f"Initialised market config {self.__class__.__name__}:\n{pformat(self.__dict__)}")
