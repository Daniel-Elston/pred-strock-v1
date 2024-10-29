# from __future__ import annotations

# from config.db import CryptoConfig, StockConfig
# from src.db.db_components import DatabaseOperations, DataHandler
# from typing import Union
# from config.state_init import StateManager

# class DatabaseFactory:
#     """
#     Factory for creating and configuring database components based on data type, mode, and stage.
#     """
#     @staticmethod
#     def create_table_config(state: StateManager, market: str, mode: str, symbol: str, stage: str):
#         # Load the appropriate configuration based on data type and mode
#         if market == "crypto":
#             table_config = CryptoConfig(mode=mode, symbol=symbol)
#         elif market == "stock":
#             table_config = StockConfig(mode=mode, symbol=symbol)
#         else:
#             raise ValueError(f"Invalid data type: {market}. Expected 'crypto' or 'stock'.")

#         # Determine table name and paths based on stage
#         if stage == "load1":
#             load_path = "load1"
#             table_name = table_config.table_name + "_load1"
#         elif stage == "load2":
#             load_path = "load2"
#             table_name = table_config.table_name + "_load2"
#         else:
#             raise ValueError(f"Invalid stage: {stage}. Expected 'load1' or 'load2'.")

#         # Configure DatabaseOperations and DataHandler with the specified schema and table
#         db_ops = DatabaseOperations(state.db_manager.conn, table_config.schema, table_name)
#         data_handler = DataHandler(state.db_manager.conn, table_config.schema, table_name, table_config.batch_size)

#         return db_ops, data_handler, load_path, table_name


from __future__ import annotations

from typing import Union
from config.api import CryptoConfig, StockConfig
from config.state_init import StateManager
from utils.execution import TaskExecutor
import pandas as pd


class DatabaseFactory:
    """
    Factory for creating and configuring database components based on data type, mode, and stage.
    """
    @staticmethod
    def create_paths(stage: str, symbol: str, mode: str):
        print(stage)
        if stage == 'load1':
            load_path = f'{symbol}_{mode}'
        elif stage == 'load2':
            load_path = 'load2'
        else:
            raise ValueError(f"Invalid stage: {stage}. Expected 'load1' or 'load2'.")

        return load_path