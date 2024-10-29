from __future__ import annotations
import logging
import asyncio
from abc import ABC, abstractmethod
from utils.file_access import save_json, temp_file_reset
from pathlib import Path
from config.state_init import StateManager
from utils.execution import TaskExecutor
import aiohttp
from typing import Union
from config.api import CryptoConfig, StockConfig


class BaseMarketRequest(ABC):
    """
    Base class for all market requests
    """
    def __init__(self, state: StateManager, config: Union[CryptoConfig, StockConfig]):
        self.state = state
        self.config = config
        self.symbol = self.config.symbol
        self.mode = self.config.mode
        self.save_path = state.paths.get_path(f'{self.config.symbol}_{self.config.mode}')

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
    def __init__(self, state: StateManager, config: CryptoConfig):
        super().__init__(state, config)
        self.exchange_name = self.config.exchange_name
        self.currency = self.config.currency

    async def batch_save_helper(self, batch, path: Path):
        """Helper method to save batch data conditionally."""
        logging.debug(f"Saving batch of size {len(batch)} to: {path}")
        await save_json(batch, path)
        batch.clear()


class BaseStockRequest(BaseMarketRequest):
    """
    Base class for all stock requests
    """
    def __init__(self, state: StateManager, config: StockConfig):
        super().__init__(state, config)
        self.api_key = self.config.auth_creds['stock_api_key']
        self.base_url = self.config.base_url
        self.function = self.config.function
        self.outputsize = self.config.outputsize
        self.interval = self.config.interval

    async def perform_request(self):
        """
        Shared request logic for stock data.
        """
        await temp_file_reset(self.save_path)
        params = {
            "apikey": self.api_key,
            "symbol": self.symbol,
            "function": self.function,
            "outputsize": self.outputsize,
            "interval": self.interval
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    await save_json(data, self.save_path)
                    await session.close()
                else:
                    logging.error(f"Failed fetch: {response.status}, {await response.text()}")