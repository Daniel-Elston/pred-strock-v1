from __future__ import annotations

import asyncio
import logging

import ccxt.pro as ccxtpro

from config.state_init import StateManager
from utils.file_access import temp_file_reset

from src.base.base_request import BaseCryptoRequest

from datetime import datetime

class RequestLiveCrypto(BaseCryptoRequest):
    def __init__(self, state: StateManager):
        super().__init__(state)
        self.batch_size = self.api_conf.batch_size

    async def fetch_data(self):
        """
        Params:
            save_path: Path
            exchange_name: str
            symbol: str
            currency: str
            batch_size: int
        """
        await temp_file_reset(self.save_path)
        batch = []
        async with getattr(ccxtpro, self.exchange_name)() as exchange:
            while len(batch) < self.batch_size:
                ticker_symbol = f'{self.symbol}/{self.currency}'
                ticker = await exchange.fetch_ticker(ticker_symbol)
                batch.append(ticker)
            await self.batch_save_helper(batch, self.save_path)
            await asyncio.sleep(1)


class RequestHistoricalCrypto(BaseCryptoRequest):
    def __init__(self, state: StateManager):
        super().__init__(state)
        self.interval = self.api_conf.interval
        self.since = self.api_conf.since
        self.limit = self.api_conf.limit

    async def fetch_data(self):
        """
        Params:
            save_path: Path
            exchange_name: str
            symbol: str
            currency: str
            interval: str
            since: str
            limit: int
        """
        exchange = getattr(ccxtpro, self.exchange_name)()
        await temp_file_reset(self.save_path)
        try:
            since_timestamp = int(datetime.strptime(self.since, "%d/%m/%Y").timestamp() * 1000)
            batch = []
            while True:
                logging.debug(
                    f"Fetching historical data for {self.symbol}/{self.currency} starting from {self.since}")
                ohlcv = await exchange.fetch_ohlcv(
                    f'{self.symbol}/{self.currency}',
                    self.interval,
                    since=since_timestamp,
                    limit=self.limit)
                if not ohlcv:
                    break
                batch.extend(ohlcv)
                since_timestamp = ohlcv[-1][0] + 60000  # Move time forward to fetch next batch
                await self.batch_save_helper(batch, self.save_path)
        finally:
            await exchange.close()
