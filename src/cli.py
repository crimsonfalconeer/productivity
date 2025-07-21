"""Example command‑line usage:
$ python -m src.cli path/to/file.xlsx
"""
import argparse
from pathlib import Path

from .io_utils import load_xlsx, save_parquet


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert .xlsx -> .parquet")
    parser.add_argument("xlsx", type=Path, help="Path to the .xlsx file")
    args = parser.parse_args()

    df = load_xlsx(args.xlsx)
    print("\n--- File preview (entire DataFrame) ---\n")
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(df)

    if input("\nSave to .parquet? [y/N] ").lower().startswith("y"):
        out = save_parquet(df, original_path=args.xlsx)
        print(f"Saved → {out.relative_to(Path.cwd())}")


if __name__ == "__main__":
    import pandas as pd  # local import so pandas option is available

    main()