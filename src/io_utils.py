"""Small helpers for I/O."""
from pathlib import Path
from typing import Union

import pandas as pd
from . import config

PathLike = Union[str, Path]


def load_xlsx(path: PathLike) -> pd.DataFrame:
    """Read an .xlsx file into a DataFrame (no row/col truncation)."""
    return pd.read_excel(path, engine="openpyxl")


def save_parquet(df: pd.DataFrame, name: str | None = None, *, original_path: PathLike | None = None) -> Path:
    """Save *df* to the processed folder (snappy‑compressed parquet).

    Parameters
    ----------
    df : DataFrame
    name : explicit filename (without extension) OR None to derive from original_path stem
    original_path : path to original .xlsx file (used only to derive name if *name* is None)
    """
    if name is None:
        if original_path is None:
            raise ValueError("Either name or original_path must be given")
        name = Path(original_path).stem

    out_path = config.DATA_PROCESSED / f"{name}.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False, engine="pyarrow", compression="snappy")
    return out_path