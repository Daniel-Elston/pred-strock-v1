from __future__ import annotations

import logging

from config.state_init import StateManager
from utils.execution import TaskExecutor
from utils.project_setup import init_project
from src.pipelines.request_pipeline import RequestPipeline
from src.pipelines.db_pipeline import DatabasePipeline
from src.pipelines.data_pipeline import DataPipeline

class MainPipeline:
    def __init__(self, state: StateManager, exe: TaskExecutor):
        self.state = state
        self.exe = exe
        self.market_config = self.state.api_config.load_config()
        self.db_stage = self.state.db_config.stage
        
        base_path = f'{state.api_config.symbol}_{state.api_config.mode}'
        self.extract_path = state.paths.get_path(base_path)
        self.transform_path = state.paths.get_path(f'{base_path}_transform')

    def run(self):
        """ETL pipeline main entry point."""
        steps = [
            (RequestPipeline(self.state, self.exe, self.market_config).main, None, self.extract_path),
            (DataPipeline(self.state, self.exe).main, self.extract_path, self.transform_path),
            (DatabasePipeline(self.state, self.exe, self.db_stage).load_fetch, self.transform_path, None),
        ]
        self.exe._execute_steps(steps, stage="main")

if __name__ == "__main__":
    project_dir, project_config, state_manager, exe = init_project()
    try:
        logging.info(f"Beginning Top-Level Pipeline from ``main.py``...\n{"="*125}")
        MainPipeline(state_manager, exe).run()
    except Exception as e:
        logging.error(f"Pipeline terminated due to unexpected error: {e}", exc_info=False)
