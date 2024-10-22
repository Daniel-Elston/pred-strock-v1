from __future__ import annotations

from src.api.request_factory import RequestFactory
from config.state_init import StateManager
from utils.execution import TaskExecutor


class RequestPipeline:
    def __init__(self, state: StateManager, exe: TaskExecutor):
        self.state = state
        self.exe = exe
        self.market = state.api_config.market
        self.mode = state.api_config.mode
        self.save_path = state.api_config.data_market

    def main(self):
        """
        Main entry point for the pipeline.
        """
        steps = [
            (RequestFactory(self.state, self.exe).create_market_request(), None, self.save_path),
        ]
        for step, load_path, save_paths in steps:
            self.exe.run_parent_step(step, load_path, save_paths)
