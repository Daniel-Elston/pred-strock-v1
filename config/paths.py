from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Union

paths_store = {
    "BTC_live": Path("data/request/live/BTC.json"),
    "BTC_historical": Path("data/request/historical/BTC.json"),
    "NVDA_live": Path("data/request/live//NVDA.json"),
    "NVDA_historical": Path("data/request/historical//NVDA.json"),
    
    'BTC_live_transform': Path("data/processed/BTC_live_transform.csv"),
    'BTC_historical_transform': Path("data/processed/BTC_historical_transform.csv"),
    'NVDA_live_transform': Path("data/processed/NVDA_live_transform.csv"),
    'NVDA_historical_transform': Path("data/processed/NVDA_historical_transform.csv"),

}


@dataclass
class PathsConfig:
    paths: Dict[str, Path] = field(default_factory=dict)

    def __post_init__(self):
        self.paths = {k: Path(v) for k, v in paths_store.items()}

    def get_path(self, key: Optional[Union[str, Path]]) -> Optional[Path]:
        if key is None:
            return None
        if isinstance(key, Path):
            return key
        return self.paths.get(key)

    def validate_paths(self):
        for name, path in self.paths.items():
            if not path.exists():
                logging.warning(f"Path {name} does not exist: {path}")
