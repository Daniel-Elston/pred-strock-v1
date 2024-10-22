from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod

from config.state_init import StateManager
from utils.execution import TaskExecutor

class BaseMarketRequest(ABC):
    """
    Base class for all market requests
    """
    def __init__(self, state: StateManager):
        self.api_conf = state.api_config
        self.symbol = self.api_conf.data_market
        self.mode = self.api_conf.mode
        self.save_path = state.paths.get_path(self.api_conf.data_market)

    @abstractmethod
    async def fetch_data(self):
        """Abstract method to fetch data"""
        pass

    def pipeline(self, df):
        steps = [
            self.run_data_fetch,
        ]
        for step in steps:
            df = TaskExecutor.run_child_step(step, df)
        return df

    def run_data_fetch(self, _):
        asyncio.run(self.fetch_data())

class BaseCryptoRequest(BaseMarketRequest):
    """
    Base class for all crypto requests
    """
    def __init__(self, state: StateManager):
        super().__init__(state)
        self.exchange_name = self.api_conf.exchange_name
        self.currency = self.api_conf.currency

class BaseStockRequest(BaseMarketRequest):
    """
    Base class for all stock requests
    """
    def __init__(self, state: StateManager):
        super().__init__(state)
        self.api_key = self.api_conf.auth_creds['stock_api_key']
        self.base_url = self.api_conf.base_url
