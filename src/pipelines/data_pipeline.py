from __future__ import annotations

from config.state_init import StateManager
from src.data.make_dataset import MakeDataset
from utils.execution import TaskExecutor


class DataPipeline:
    def __init__(self, state: StateManager, exe: TaskExecutor):
        self.state = state
        self.exe = exe

    def main(self):
        steps = [
            (MakeDataset(self.state), "raw", "sdo"),
        ]
        self.exe._execute_steps(steps, stage="parent")
