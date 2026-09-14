"""Profile loader — selects source-LZ profile module at import time.

Selection order:
1. env var `CONVERTER_PROFILE` (module name under `converter.src.profiles`)
2. default: `thailand`

Each profile module must define, at minimum:
    ACCELERATOR_PREFIX: str
    HOME_REGION: str
    SOURCE_DIR: pathlib.Path  # absolute path to source LZ's CFN dir
    OUT_DIR: pathlib.Path     # absolute path to write UC config to

Plus domain-specific constants consumed by mappers. See
`converter/src/profiles/thailand.py` for the reference profile.
"""
from __future__ import annotations

import importlib
import os

_name = os.environ.get("CONVERTER_PROFILE", "thailand")
_mod = importlib.import_module(f"converter.src.profiles.{_name}")

# Re-export everything the profile module defines. Mappers do
# `from ..profile import ACCELERATOR_PREFIX, ...`
globals().update({k: v for k, v in _mod.__dict__.items() if not k.startswith("_")})
