from __future__ import annotations

import asyncio
import logging
import datetime
import aiohttp
import os

from config.state_init import StateManager
from utils.execution import TaskExecutor
from utils.file_access import save_json, temp_file_reset
from pathlib import Path

class RequestHistoricalStock:
    def __init__(self, state: StateManager):
        api_conf = state.api_config
        self.api_key = api_conf.auth_creds['stock_api_key']
        self.symbol = api_conf.stock_symbol
        self.function = api_conf.function
        self.outputsize = api_conf.outputsize
        self.interval = api_conf.interval
        self.base_url = api_conf.base_url
        self.historical_save_path = state.paths.get_path(api_conf.stock_symbol)

    def pipeline(self, df):
        steps = [
            self.run_historical_data_fetch,
        ]
        for step in steps:
            df = TaskExecutor.run_child_step(step, df)
        return df

    def run_historical_data_fetch(self, _):
        asyncio.run(self.async_extract_historical())
        
    async def async_extract_historical(self):
        await self.fetch_historical_data(
            self.base_url, self.api_key,self.historical_save_path, 
            self.symbol, self.function, self.interval, self.outputsize)

    async def fetch_historical_data(
        self, base_url: str, api_key: str, historical_save_path: Path,
        symbol: str, function: str, interval: str, outputsize: str):
        """Fetch historical stock data from Alpha Vantage."""
        await temp_file_reset(self.historical_save_path)

        params = {
            "apikey": api_key,
            "symbol": symbol,
            "function": function,
            "interval": interval,
            "outputsize": outputsize
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    base_url, params=params
                    ) as response:
                    if response.status == 200:
                        data = await response.json()
                        logging.debug(f"Fetched historical. Symbol: {symbol}")
                        await save_json(data, historical_save_path)

                    else:
                        logging.error(f"Failed fetch: {response.status}, {await response.text()}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
