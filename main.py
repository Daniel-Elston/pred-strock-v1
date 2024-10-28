from __future__ import annotations

import logging

from config.state_init import StateManager
from utils.execution import TaskExecutor
from utils.project_setup import init_project
from src.pipelines.request_pipeline import RequestPipeline


class MainPipeline:
    def __init__(self, state: StateManager, exe: TaskExecutor):
        self.state = state
        self.exe = exe
        self.market_config = self.state.api_config.load_config()  # Load the specific market configuration
        
        self.save_path = state.paths.get_path(self.market_config.symbol)

    def run(self):
        steps = [
            (RequestPipeline(self.state, self.exe, self.market_config).main, None, self.save_path),
        ]
        self.exe._execute_steps(steps, stage="main")

if __name__ == "__main__":
    project_dir, project_config, state_manager, exe = init_project()
    try:
        MainPipeline(state_manager, exe).run()
    except Exception as e:
        logging.error(f"Pipeline terminated due to unexpected error: {e}", exc_info=False)
