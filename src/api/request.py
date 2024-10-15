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
        self.state = state
        self.s_ac = state.api_config
        self.symbol = state.api_config.symbol
        self.exchange_name = state.api_config.exchange_name
        self.batch_size = state.api_config.batch_size
        self.max_items = state.api_config.max_items
        self.save_path = self.state.paths.get_path("response")
        self.historical_save_path = self.state.paths.get_path("historical")

    def pipeline(self, df):
        steps = [
            self.handle,
        ]
        for step in steps:
            df = TaskExecutor.run_child_step(step, df)
        return df

    # async def ticker(self, symbol="BTC/USDT", exchange_name="binance", batch_size=2, max_items=4):
    async def ticker(self, symbol:str, exchange_name:str, batch_size:int, max_items:int):
        """Watch the ticker for a specific symbol."""
        await temp_file_reset(self.save_path)
        batch = []

        # Use context manager to ensure exchange closes properly
        async with getattr(ccxtpro, exchange_name)() as exchange:
            try:
                while len(batch) < max_items:
                    ticker = await exchange.fetch_ticker(symbol)
                    batch.append(ticker)

                    if len(batch) % batch_size == 0 or len(batch) >= max_items:
                        logging.debug(f"Saving batch of size {len(batch)} to: {self.save_path}")
                        await save_json(batch, self.save_path)

                    await asyncio.sleep(1)

            except ccxtpro.NetworkError as e:
                logging.error(f"NetworkError: {e}")
            except ccxtpro.ExchangeError as e:
                logging.error(f"ExchangeError: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
            finally:
                # Ensure last partial batch is saved
                if batch:
                    logging.debug(f"Saving final batch to: {self.save_path}")
                    await save_json(batch, self.save_path)

    async def async_extract_live(self):
        await self.ticker(self.symbol, self.exchange_name, self.batch_size, self.max_items)

    def run_async_extract_live(self, _):
        asyncio.run(self.async_extract_live())
