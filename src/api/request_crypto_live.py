from __future__ import annotations

import asyncio
import logging

import ccxt.pro as ccxtpro

from config.state_init import StateManager
from utils.execution import TaskExecutor
from utils.file_access import save_json, temp_file_reset
from pathlib import Path


class RequestData:
    def __init__(self, state: StateManager):
        api_conf = state.api_config
        self.save_path = state.paths.get_path("response")
        self.historical_save_path = state.paths.get_path("historical")
        self.symbol = api_conf.symbol
        self.exchange_name = api_conf.exchange_name
        self.batch_size = api_conf.batch_size
        self.max_items = api_conf.max_items

    def pipeline(self, df):
        steps = [
            self.run_async_extract_live,
        ]
        for step in steps:
            df = TaskExecutor.run_child_step(step, df)
        return df

    def run_async_extract_live(self, _):
        asyncio.run(self.async_extract_live())
        
    async def async_extract_live(self):
        await self.ticker(
            self.exchange_name, self.symbol, self.batch_size, self.max_items)

    async def ticker(self, exchange_name:str, symbol:str, batch_size:int, max_items:int):
        """Watch the ticker for a specific symbol."""
        await temp_file_reset(self.save_path)
        batch = []

        async with getattr(ccxtpro, exchange_name)() as exchange:
            try:
                while len(batch) < max_items:
                    ticker = await exchange.fetch_ticker(symbol)
                    batch.append(ticker)

                    if len(batch) % batch_size == 0 or len(batch) >= max_items:
                        logging.debug(f"Saving batch of size {len(batch)} to: {self.save_path}")
                        await save_json(batch, self.save_path)

                    await asyncio.sleep(1)

            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
            finally:
                # Ensure last partial batch is saved
                if batch:
                    logging.debug(f"Saving final batch to: {self.save_path}")
                    await save_json(batch, self.save_path)
