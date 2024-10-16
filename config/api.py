from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pprint import pformat


@dataclass
class ApiConfig:
    # alpha_api_key: str = os.getenv("ALPHA_API_KEY")
    sleep_interval: int = 60
    
    symbol: str = "BTC"
    currency: str = "USDT"
    exchange_name: str = "binance"
    batch_size: int = 2
    max_items: int = 6
    
    timeframe: str = '15m'
    since: str = '15/10/2024'
    limit: int = 1000


    def __post_init__(self):
        post_init_dict = self.__dict__
        
        # Remove fields that are not initialized yet
        post_init_dict = {k: v for k, v in post_init_dict.items() if v is not None}
        logging.debug(f"Initialized API ConnConfig:\n{pformat(post_init_dict)}")

    def __repr__(self):
        return pformat(self.__dict__)


# BTC and NVDA/AMD - companies produce GPUs used in crypto mining
# ETH and MSF - Ethereum-based projects and blockchain developmen
# SOL and general tech companies - high-performance blockchain, Solana's performance can be indicative of overall tech sector health
# Cardano (ADA) and tech innovation: Its development is closely watched as an indicator of blockchain technology advancement.
# Block (SQ) directly deals with Bitcoin transactions and holdings, making it closely tied to crypto markets.