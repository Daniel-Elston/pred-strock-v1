from __future__ import annotations

from src.api.request_factory import RequestFactory
from config.state_init import StateManager
from utils.execution import TaskExecutor
from typing import Union
from config.api import CryptoConfig, StockConfig

class RequestPipeline:
    def __init__(self, state: StateManager, exe: TaskExecutor, market_config: Union[CryptoConfig, StockConfig]):
        self.state = state
        self.exe = exe
        self.market_config = market_config
        self.api_config = self.state.api_config
        
        self.market = self.api_config.market
        self.mode = self.api_config.mode
        self.save_path = state.paths.get_path(self.market_config.symbol)

    def main(self):
        """
        Main entry point for the pipeline.
        """
        steps = [
            (RequestFactory(self.state, self.exe, self.market_config).create_market_request(), None, self.save_path),
        ]
        self.exe._execute_steps(steps, stage="parent")
