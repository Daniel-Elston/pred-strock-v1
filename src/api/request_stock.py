from __future__ import annotations

from config.state_init import StateManager

from src.base.base_request import BaseStockRequest
from config.api import StockConfig


class RequestLiveStock(BaseStockRequest):
    def __init__(self, state: StateManager, config: StockConfig):
        super().__init__(state, config)

    async def fetch_data(self):
        """
        Params:
            base_url: str
            api_key: str
            live_save_path: Path
            symbol: str
            function: str
            interval: str
        """
        await self.perform_request()


class RequestHistoricalStock(BaseStockRequest):
    def __init__(self, state: StateManager, config: StockConfig):
        super().__init__(state, config)

    async def fetch_data(self):
        """
        Params:
            base_url: str
            api_key: str
            historical_save_path: Path
            symbol: str
            function: str
            outputsize: str
        """
        await self.perform_request()
