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
        
        self.db_factory = DatabaseFactory(self.state, stage)
        self.load_path, self.save_paths = self.db_factory.create_paths()
        self.steps = self.db_factory.create_steps()

    def extract_load(self):
        self.exe._execute_steps(self.steps, stage="parent")
