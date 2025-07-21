"""Tiny Tkinter front‑end."""
from pathlib import Path
import sys

# Ensure project root is importable when double‑clicked or executed from any dir
root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.append(str(root))

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd

from src.io_utils import load_xlsx, save_parquet


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("XLSX → Parquet Converter")
        self.geometry("900x600")

        tk.Button(self, text="Load .xlsx", command=self._open_file).pack(pady=10)
        self._txt = scrolledtext.ScrolledText(self, font=("Consolas", 10))
        self._txt.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Button(self, text="Save as .parquet", command=self._save, state="disabled").pack(pady=10)

        self._df: pd.DataFrame | None = None
        self._xlsx_path: Path | None = None

    # ---------- helpers ----------
    def _open_file(self) -> None:
        file_path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if not file_path:
            return
        self._xlsx_path = Path(file_path)
        self._df = load_xlsx(self._xlsx_path)
        self._show_df(self._df)
        self.children["!button2"].config(state="normal")

    def _show_df(self, df: pd.DataFrame) -> None:
        """Dump *entire* DataFrame into the scrolled text widget."""
        self._txt.delete("1.0", tk.END)
        with pd.option_context("display.max_rows", None, "display.max_columns", None):
            self._txt.insert(tk.END, df.to_string(index=False))

    def _save(self):
        if self._df is None:
            messagebox.showerror("Error", "No file loaded!")
            return
        out = save_parquet(self._df, original_path=self._xlsx_path)
        messagebox.showinfo("Saved", f"Parquet saved to: {out}")


if __name__ == "__main__":
    App().mainloop()