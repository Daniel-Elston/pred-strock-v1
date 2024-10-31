from __future__ import annotations

from src.api.request_crypto import RequestLiveCrypto, RequestHistoricalCrypto
from src.api.request_stock import RequestLiveStock, RequestHistoricalStock
from config.state_init import StateManager
from utils.execution import TaskExecutor
from typing import Union
from config.api import CryptoConfig, StockConfig, RequestParams

class RequestFactory:
    """
    Factory class to create market request objects.
    """
    def __init__(self, state: StateManager, exe: TaskExecutor, market_config: Union[CryptoConfig, StockConfig]):
        self.state = state
        self.exe = exe
        self.market_config = market_config

    def create_market_request(self):
        params = RequestParams(
            symbol=getattr(self.market_config, 'symbol', None),
            interval=getattr(self.market_config, 'interval', None),
            outputsize=getattr(self.market_config, 'outputsize', None),
            function=getattr(self.market_config, 'function', None),
            base_url=getattr(self.market_config, 'base_url', None),
            exchange_name=getattr(self.market_config, 'exchange_name', None),
            batch_size=getattr(self.market_config, 'batch_size', None),
            max_items=getattr(self.market_config, 'max_items', None),
            since=getattr(self.market_config, 'since', None),
            limit=getattr(self.market_config, 'limit', None),
            currency=getattr(self.market_config, 'currency', None),
            apikey=self.market_config.auth_creds.get("stock_api_key")
        )
        params = {k: v for k, v in params.__dict__.items() if v is not None}
        
        request_map = {
            ('crypto', 'live'): RequestLiveCrypto,
            ('crypto', 'historical'): RequestHistoricalCrypto,
            ('stock', 'live'): RequestLiveStock,
            ('stock', 'historical'): RequestHistoricalStock
        }
        
        request_class = request_map.get((self.market_config.market, self.market_config.mode))
        if request_class:
            return request_class(self.state, params).pipeline
        raise ValueError(f"Invalid market or mode: {self.market_config.market}, {self.market_config.mode}.")
