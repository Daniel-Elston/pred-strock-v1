from __future__ import annotations

from src.api.request_crypto import RequestLiveCrypto, RequestHistoricalCrypto
from src.api.request_stock import RequestLiveStock, RequestHistoricalStock
from config.state_init import StateManager
from utils.execution import TaskExecutor


class RequestFactory:
    """
    Factory class to create market request objects.
    """
    def __init__(self, state: StateManager, exe: TaskExecutor):
        self.state = state
        self.exe = exe
        self.market = state.api_config.market
        self.mode = state.api_config.mode

    def create_market_request(self):
        if self.market == 'crypto' and self.mode == 'live':
            return RequestLiveCrypto(self.state).pipeline
        elif self.market == 'crypto' and self.mode == 'historical':
            return RequestHistoricalCrypto(self.state).pipeline
        elif self.market == 'stock' and self.mode == 'live':
            return RequestLiveStock(self.state).pipeline
        elif self.market == 'stock' and self.mode == 'historical':
            return RequestHistoricalStock(self.state).pipeline
        
        raise ValueError(f"Invalid market or mode: {self.market}, {self.mode}")
