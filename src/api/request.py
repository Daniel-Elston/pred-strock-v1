from __future__ import annotations

import asyncio
import logging

import ccxt.pro as ccxtpro

from config.state_init import StateManager
from utils.execution import TaskExecutor
from utils.file_access import save_json, temp_file_reset


class RequestData:
    def __init__(self, state: StateManager):
        self.state = state
        self.save_path = self.state.paths.get_path("response")

    def pipeline(self, df):
        steps = [
            self.handle,
        ]
        for step in steps:
            df = TaskExecutor.run_child_step(step, df)
        return df

    async def ticker(self, symbol="BTC/USDT", exchange_name="binance", batch_size=2, max_items=4):
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

    async def async_extract(
        self, symbol="BTC/USDT", exchange_name="binance", batch_size=2, max_items=4
    ):
        await self.ticker(symbol, exchange_name, batch_size, max_items)

    def handle(self, *args, **kwargs):
        symbol = kwargs.get("symbol", "BTC/USDT")
        exchange_name = kwargs.get("exchange_name", "binance")
        batch_size = kwargs.get("batch_size", 2)
        max_items = kwargs.get("max_items", 4)

        asyncio.run(self.async_extract(symbol, exchange_name, batch_size, max_items))
