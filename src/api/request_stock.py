# stock_requests.py
from __future__ import annotations

import aiohttp

import logging

from config.state_init import StateManager
from utils.file_access import save_json, temp_file_reset
from pathlib import Path

from src.base.base_request import BaseStockRequest

class RequestLiveStock(BaseStockRequest):
    def __init__(self, state: StateManager):
        super().__init__(state)
        self.function = "TIME_SERIES_INTRADAY"
        self.interval = "1min"

    async def fetch_data(self):
        await self.fetch_live_data(
            self.base_url, self.api_key, self.save_path, 
            self.symbol, self.function, self.interval)

    async def fetch_live_data(
        self, base_url: str, api_key: str, live_save_path: Path,
        symbol: str, function: str, interval: str):
        await temp_file_reset(live_save_path)

        params = {
            "apikey": api_key,
            "symbol": symbol,
            "function": function,
            "interval": interval
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        logging.debug(f"Fetched live data. Symbol: {symbol}")
                        await save_json(data, live_save_path)
                    else:
                        logging.error(f"Failed fetch: {response.status}, {await response.text()}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")


class RequestHistoricalStock(BaseStockRequest):
    def __init__(self, state: StateManager):
        super().__init__(state)
        self.function = self.api_conf.function
        self.outputsize = self.api_conf.outputsize

    async def fetch_data(self):
        await self.fetch_historical_data(
            self.base_url, self.api_key, self.save_path, 
            self.symbol, self.function, self.outputsize)

    async def fetch_historical_data(
        self, base_url: str, api_key: str, historical_save_path: Path,
        symbol: str, function: str, outputsize: str):
        await temp_file_reset(historical_save_path)

        params = {
            "apikey": api_key,
            "symbol": symbol,
            "function": function,
            "outputsize": outputsize
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        logging.debug(f"Fetched historical data. Symbol: {symbol}")
                        await save_json(data, historical_save_path)
                    else:
                        logging.error(f"Failed fetch: {response.status}, {await response.text()}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")