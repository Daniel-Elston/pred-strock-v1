from __future__ import annotations

import asyncio
import logging

import ccxt.pro as ccxtpro

from config.state_init import StateManager
from utils.file_access import save_json, temp_file_reset
from pathlib import Path

from src.base.base_request import BaseCryptoRequest

from datetime import datetime

class RequestLiveCrypto(BaseCryptoRequest):
    def __init__(self, state: StateManager):
        super().__init__(state)
        self.batch_size = self.api_conf.batch_size
        self.max_items = self.api_conf.max_items

    async def fetch_data(self):
        await self.ticker(
            self.save_path, self.exchange_name, self.symbol, 
            self.currency, self.batch_size, self.max_items)

    async def ticker(
        self, live_save_path: Path, exchange_name:str, symbol:str,
        currency:str, batch_size:int, max_items:int):
        await temp_file_reset(live_save_path)
        batch = []

        async with getattr(ccxtpro, exchange_name)() as exchange:
            try:
                while len(batch) < max_items:
                    ticker_symbol = f'{symbol}/{currency}'
                    ticker = await exchange.fetch_ticker(ticker_symbol)
                    batch.append(ticker)

                    if len(batch) % batch_size == 0 or len(batch) >= max_items:
                        logging.debug(f"Saving batch of size {len(batch)} to: {live_save_path}")
                        await save_json(batch, live_save_path)

                    await asyncio.sleep(1)

            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
            finally:
                if batch:
                    logging.debug(f"Saving final batch to: {live_save_path}")
                    await save_json(batch, live_save_path)


class RequestHistoricalCrypto(BaseCryptoRequest):
    def __init__(self, state: StateManager):
        super().__init__(state)
        self.interval = self.api_conf.interval
        self.since = self.api_conf.since
        self.limit = self.api_conf.limit

    async def fetch_data(self):
        await self.fetch_historical_data(
            self.save_path, self.exchange_name, self.symbol,
            self.currency, self.interval, self.since, self.limit)

    async def fetch_historical_data(
        self, historical_save_path:Path, exchange_name:str, crypto_symbol:str,
        currency:str, interval:str, since:str, limit:int=1000):
        exchange = getattr(ccxtpro, exchange_name)()
        await temp_file_reset(historical_save_path)
        
        try:
            since_timestamp = int(datetime.strptime(since, "%d/%m/%Y").timestamp() * 1000)
            all_data = []
            
            while True:
                logging.debug(f"Fetching historical data for {crypto_symbol}/{currency} starting from {since}")
                ohlcv = await exchange.fetch_ohlcv(
                    f'{crypto_symbol}/{currency}',
                    interval,
                    since=since_timestamp,
                    limit=limit)
                
                if not ohlcv:
                    break
                
                all_data.extend(ohlcv)
                since_timestamp = ohlcv[-1][0] + 60000  # Move time forward to fetch next batch

                if len(all_data) >= limit:
                    logging.debug(f"Saving batch of historical data to: {historical_save_path}")
                    await save_json(all_data, historical_save_path)
                    all_data.clear()

            if all_data:
                logging.debug(f"Saving final historical batch to: {historical_save_path}")
                await save_json(all_data, historical_save_path)

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        finally:
            await exchange.close()