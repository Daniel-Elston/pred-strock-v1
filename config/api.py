from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pprint import pformat


def auth_manager():
    api_creds = {
        "USERNAME": os.getenv("USERNAME"),
        "PASSWORD": os.getenv("PASSWORD"),
    }
    api_params = {
        "BASE_URL": os.getenv("BASE_URL"),
    }
    return api_creds, api_params


@dataclass
class ApiConfig:
    # alpha_api_key: str = os.getenv("ALPHA_API_KEY")
    api_creds: dict = field(init=False)
    api_params: dict = field(init=False)
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
        self.api_creds, self.api_params = auth_manager()

        post_init_dict = {
            "api_creds": self.api_creds,
            "api_params": self.api_params,
        }
        logging.debug(f"Initialized API ConnConfig:\n{pformat(post_init_dict)}")

    def __repr__(self):
        return pformat(self.__dict__)


# BTC and NVDA/AMD - companies produce GPUs used in crypto mining
# ETH and MSF - Ethereum-based projects and blockchain developmen
# SOL and general tech companies - high-performance blockchain, Solana's performance can be indicative of overall tech sector health
# Cardano (ADA) and tech innovation: Its development is closely watched as an indicator of blockchain technology advancement.
# Block (SQ) directly deals with Bitcoin transactions and holdings, making it closely tied to crypto markets.