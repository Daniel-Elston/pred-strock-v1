from __future__ import annotations

from config.state_init import StateManager


class DatabaseFactory:
    """
    Factory for creating and configuring database components based on data type, mode, and stage.
    """
    def __init__(self, state: StateManager, stage: str):
        self.state = state
        self.stage = stage
        self.base_path = f'{state.api_config.symbol}_{state.api_config.mode}'
        
    def create_paths(self):
        if self.stage == 'load1':
            load_path = f'{self.base_path}_transform'
            save_path = None
        elif self.stage == 'load2':
            load_path = None
            save_path = f'{self.base_path}_fetch'
        else:
            raise ValueError(f"Invalid stage: {self.stage}. Expected 'load1' or 'load2'.")
        return load_path, save_path