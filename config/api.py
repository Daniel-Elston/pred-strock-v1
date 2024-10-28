from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pprint import pformat

def api_auth():
    auth_creds = {
        "stock_api_key": os.getenv("ALPHA_VANTAGE_API")
    }
    return auth_creds

@dataclass
class ApiConfig:
    market: str = 'crypto'  # 'crypto' or 'stock'
    mode: str = 'historical'  # 'live' or 'historical'
    sleep_interval: int = 60
    
    # Cross Configs
    interval: str = '15m'
    
    # Stock Market Config
    auth_creds: dict = field(init=False)
    base_url: str = "https://www.alphavantage.co/query"
    outputsize: str = 'full'  # 'compact' or 'full'
    function: str = 'TIME_SERIES_DAILY'
    stock_symbol: str = 'NVDA'
    
    # Crypto Market Config
    crypto_symbol: str = "BTC"
    currency: str = "USDT"
    exchange_name: str = "binance"
    batch_size: int = 4
    max_items: int = 6
    since: str = '27/10/2024'
    limit: int = 1000

    def __post_init__(self):
        self.auth_creds = api_auth()
        post_init_dict = self.__dict__
        
        # Remove fields that are not initialized yet
        post_init_dict = {k: v for k, v in post_init_dict.items() if v is not None}
        
        post_init_dict['ALPHA_VANTAGE_API'] = os.getenv("ALPHA_VANTAGE_API")
        logging.debug(f"Initialized API ConnConfig:\n{pformat(post_init_dict)}")

    def __repr__(self):
        return pformat(self.__dict__)

    @property
    def data_market(self):
        """Dynamically return the correct symbol based on request type."""
        if self.market=='crypto':
            return self.crypto_symbol
        elif self.market=='stock':
            return self.stock_symbol
        else:
            raise ValueError(f"Invalid market: {self.market}. Please select either 'crypto' or 'stock'")

# BTC and NVDA/AMD - companies produce GPUs used in crypto mining
# ETH and MSF - Ethereum-based projects and blockchain developmen
# SOL and general tech companies - high-performance blockchain, Solana's performance can be indicative of overall tech sector health
# Cardano (ADA) and tech innovation: Its development is closely watched as an indicator of blockchain technology advancement.
# Block (SQ) directly deals with Bitcoin transactions and holdings, making it closely tied to crypto markets.