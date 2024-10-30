from __future__ import annotations

from config.state_init import StateManager
from utils.execution import TaskExecutor
from config.state_init import StateManager
from src.db.db_factory import DatabaseFactory

class DatabasePipeline:
    """
    ELTL or ETL pipeline for database operations.
    """
    def __init__(self, state: StateManager, exe: TaskExecutor, stage: str):
        self.state = state
        self.exe = exe
        
        # self.stage = state.db_config.stage
        self.stage = stage
        self.market = state.api_config.market
        self.mode = state.api_config.mode
        self.symbol = state.api_config.symbol
        
        self.db_ops = self.state.db_manager.ops
        self.data_handler = self.state.db_manager.handler

        self.load_path, self.save_paths = DatabaseFactory(self.state, self.stage).create_paths()

    def extract_load(self):
        steps = [
            (self._create_table, self.load_path, None),
            (self._insert_data, self.load_path, None),
            # (self._fetch_data, None, self.save_paths),
        ]
        self.exe._execute_steps(steps, stage="parent")

    def _create_table(self, df):
        self.db_ops.create_table_if_not_exists(df)
        return df

    def _insert_data(self, df):
        self.data_handler.insert_batches_to_db(df)
        return df

    def _fetch_data(self):
        query = f"SELECT * FROM {self.state.db_manager.config.schema}.{self.state.db_config.table};"
        return self.data_handler.fetch_data(query)