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
    sleep_interval: int = 60
    api_creds: dict = field(init=False)
    api_params: dict = field(init=False)
    
    symbol: str = "BTC/USDT"
    exchange_name: str = "binance"
    batch_size: int = 2
    max_items: int = 6
    fetch_historical: bool = True
    date_from = 1704067200000
    
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
