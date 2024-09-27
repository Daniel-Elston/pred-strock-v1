from __future__ import annotations

import logging

from config.state_init import StateManager
from src.pipelines.api_pipeline import RequestPipeline
from src.pipelines.data_pipeline import DataPipeline
from src.pipelines.db_pipeline import DatabasePipeline
from utils.execution import TaskExecutor
from utils.project_setup import init_project


class MainPipeline:
    def __init__(self, state: StateManager, exe: TaskExecutor):
        self.state = state
        self.exe = exe

        self.api_pipeline = RequestPipeline(self.state, self.exe)
        # self.data_pipeline = DataPipeline(self.state, self.exe)
<<<<<<< HEAD
        self.database_pipeline = DatabasePipeline(self.state, self.exe, stage="raw")
=======
        # self.database_pipeline = DatabasePipeline(self.state, self.exe, stage="raw")
>>>>>>> 9589f0df0ac95942337e101a24e1d5af30d28c1d

    def run(self):
        logging.info(
            f"INITIATING {self.__class__.__name__} from top-level script: ``{__file__.split('/')[-1]}``...\n"
        )
        steps = [
            # (self.data_pipeline.main, 'raw', 'sdo'),
            # (self.database_pipeline.insert_load, 'raw', None),
            (RequestPipeline(self.state, self.exe).main, None, 'response'),
        ]
        self.exe._execute_steps(steps, stage="main")
        logging.info(
            f'Completed {self.__class__.__name__} from top-level script: ``{__file__.split("/")[-1]}`` SUCCESSFULLY.\n'
        )

if __name__ == "__main__":
    project_dir, project_config, state_manager, exe = init_project()
    try:
        MainPipeline(state_manager, exe).run()
    except Exception as e:
        logging.error(f"Pipeline terminated due to unexpected error: {e}", exc_info=False)
