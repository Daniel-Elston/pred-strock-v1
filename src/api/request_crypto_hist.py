from __future__ import annotations

import asyncio
import logging
import datetime
import ccxt.pro as ccxtpro

from config.state_init import StateManager
from utils.execution import TaskExecutor
from utils.file_access import save_json, temp_file_reset
from pathlib import Path

class RequestHistoricalCrypto:
    def __init__(self, state: StateManager):
        api_conf = state.api_config
        self.exchange_name = api_conf.exchange_name
        self.symbol = api_conf.symbol
        self.currency = api_conf.currency
        self.timeframe = api_conf.timeframe
        self.since = api_conf.since
        self.limit = api_conf.limit
        self.historical_save_path = state.paths.get_path(api_conf.symbol)


    def pipeline(self, df):
        steps = [
            self.run_historical_data_fetch,
        ]
        for step in steps:
            df = TaskExecutor.run_child_step(step, df)
        return df

    async def fetch_historical_data(
        self, historical_save_path:Path, exchange_name:str, symbol:str, currency:str,
        timeframe:str, since:str, limit:int=1000):
        """Fetch historical OHLCV data."""
        exchange = getattr(ccxtpro, exchange_name)()
        await temp_file_reset(historical_save_path)
        
        try:
            since_timestamp = int(datetime.datetime.strptime(since, "%d/%m/%Y").timestamp() * 1000)
            all_data = []
            
            while True:
                logging.debug(f"Fetching historical data for {symbol}/{currency} starting from {since}")
                ohlcv = await exchange.fetch_ohlcv(
                    f'{symbol}/{currency}', timeframe, since=since_timestamp, limit=limit)
                
                if not ohlcv:
                    break
                
                all_data.extend(ohlcv)
                since_timestamp = ohlcv[-1][0] + 60000  # Move the time forward to fetch the next batch

                if len(all_data) >= limit:
                    logging.debug(f"Saving batch of historical data to: {historical_save_path}")
                    await save_json(all_data, historical_save_path)
                    all_data.clear()

            if all_data:
                logging.debug(f"Saving final historical batch to: {historical_save_path}")
                await save_json(all_data, historical_save_path)

        except ccxtpro.NetworkError as e:
            logging.error(f"NetworkError: {e}")
        except ccxtpro.ExchangeError as e:
            logging.error(f"ExchangeError: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        finally:
            await exchange.close()

    async def async_extract_historical(self):
        await self.fetch_historical_data(
            self.historical_save_path, self.exchange_name, self.symbol,
            self.currency, self.timeframe, self.since, self.limit)

    def run_historical_data_fetch(self, _):
        asyncio.run(self.async_extract_historical())
