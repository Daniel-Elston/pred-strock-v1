from __future__ import annotations

from config.state_init import StateManager
# from api.request_crypto_live import RequestData
from src.api.request_crypto_hist import RequestHistoricalCrypto
from utils.execution import TaskExecutor


class RequestPipeline:
    def __init__(self, state: StateManager, exe: TaskExecutor):
        self.state = state
        self.exe = exe
        self.save_path = self.state.paths.get_path(state.api_config.symbol)

    def main(self):
        steps = [
            # (RequestData(self.state).pipeline, None, self.save_path),
            (RequestHistoricalCrypto(self.state).pipeline, None, self.save_path),
        ]
        for step, load_path, save_paths in steps:
            self.exe.run_parent_step(step, load_path, save_paths)
