# from __future__ import annotations

# import asyncio
# import logging
# import datetime
# import aiohttp
# import os

# from config.state_init import StateManager
# from utils.execution import TaskExecutor
# from utils.file_access import save_json, temp_file_reset
# from pathlib import Path


# class RequestHistoricalDataAlphaVantage:
#     def __init__(self, state: StateManager):
#         api_conf = state.api_config
#         self.api_key = api_conf.alpha_api_key
#         self.symbol = api_conf.symbol
#         self.function = api_conf.function
#         self.outputsize = api_conf.outputsize
#         self.historical_save_path = state.paths.get_path(api_conf.symbol)
#         self.interval = api_conf.interval

#     def pipeline(self, df):
#         steps = [
#             self.run_historical_data_fetch,
#         ]
#         for step in steps:
#             df = TaskExecutor.run_child_step(step, df)
#         return df

#     async def fetch_historical_data(
#         self, historical_save_path: Path, symbol: str, api_key: str,
#         function: str, interval: str, outputsize: str):
#         """Fetch historical stock data from Alpha Vantage."""
#         await temp_file_reset(historical_save_path)

#         base_url = f"https://www.alphavantage.co/query"
#         params = {
#             "function": function,  # "TIME_SERIES_INTRADAY" or "TIME_SERIES_DAILY"
#             "symbol": symbol,
#             "interval": interval,  # e.g., "5min" or "60min"
#             "apikey": api_key,
#             "outputsize": outputsize  # "compact" or "full"
#         }

#         async with aiohttp.ClientSession() as session:
#             try:
#                 async with session.get(base_url, params=params) as response:
#                     if response.status == 200:
#                         data = await response.json()
#                         logging.debug(f"Fetched historical data for {symbol}: {data}")

#                         # Save the JSON response
#                         await save_json(data, historical_save_path)

#                     else:
#                         logging.error(f"Failed to fetch data: {response.status}, {await response.text()}")
#             except Exception as e:
#                 logging.error(f"An unexpected error occurred: {e}")

#     async def async_extract_historical(self):
#         await self.fetch_historical_data(
#             self.historical_save_path, self.symbol,
#             self.api_key, self.function, self.interval, self.outputsize)

#     def run_historical_data_fetch(self, _):
#         asyncio.run(self.async_extract_historical())
