"""Enhanced Tkinter front‑end with AI analysis."""
from pathlib import Path
import sys

# Ensure project root is importable when double‑clicked or executed from any dir
root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.append(str(root))

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import pandas as pd
import threading

from src.io_utils import load_xlsx, save_parquet
from src.llm.data_analyzer import analyze_data_with_ai


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("XLSX → Parquet Converter & AI Analyzer")
        self.geometry("1200x800")

        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Top buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(button_frame, text="Load .xlsx", command=self._open_file).pack(side="left", padx=(0, 10))
        self._save_button = ttk.Button(button_frame, text="Save as .parquet", command=self._save, state="disabled")
        self._save_button.pack(side="left", padx=(0, 10))

        # Model selection
        ttk.Label(button_frame, text="AI Model:").pack(side="left", padx=(20, 5))
        self._model_var = tk.StringVar(value="large")
        model_combo = ttk.Combobox(button_frame, textvariable=self._model_var, values=["large", "small"], state="readonly", width=10)
        model_combo.pack(side="left")

        # Create notebook for tabs
        self._notebook = ttk.Notebook(main_frame)
        self._notebook.pack(fill="both", expand=True)

        # Data preview tab
        self._data_frame = ttk.Frame(self._notebook)
        self._notebook.add(self._data_frame, text="📊 Data Preview")
        
        self._txt = scrolledtext.ScrolledText(self._data_frame, font=("Consolas", 10))
        self._txt.pack(fill="both", expand=True, padx=10, pady=10)

        # AI Analysis tab
        self._ai_frame = ttk.Frame(self._notebook)
        self._notebook.add(self._ai_frame, text="🤖 AI Analysis")

        # AI Analysis controls
        ai_controls = ttk.Frame(self._ai_frame)
        ai_controls.pack(fill="x", padx=10, pady=10)

        ttk.Label(ai_controls, text="Analysis Instruction:").pack(anchor="w")
        self._instruction_text = scrolledtext.ScrolledText(ai_controls, height=4, font=("Consolas", 10))
        self._instruction_text.pack(fill="x", pady=(5, 10))
        self._instruction_text.insert("1.0", "e.g., 'Sort by column X in descending order' or 'Calculate the sum of column Y'")

        ttk.Button(ai_controls, text="🚀 Generate & Execute Analysis", command=self._analyze_data).pack(pady=(0, 10))

        # Results area
        ttk.Label(ai_controls, text="Results:").pack(anchor="w")
        self._results_text = scrolledtext.ScrolledText(ai_controls, height=15, font=("Consolas", 10))
        self._results_text.pack(fill="both", expand=True)

        # Data structure info tab
        self._info_frame = ttk.Frame(self._notebook)
        self._notebook.add(self._info_frame, text="📋 Data Structure")
        
        self._info_text = scrolledtext.ScrolledText(self._info_frame, font=("Consolas", 10))
        self._info_text.pack(fill="both", expand=True, padx=10, pady=10)

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
        self._show_data_info(self._df)
        self._save_button.config(state="normal")

    def _show_df(self, df: pd.DataFrame) -> None:
        """Dump *entire* DataFrame into the scrolled text widget."""
        self._txt.delete("1.0", tk.END)
        with pd.option_context("display.max_rows", None, "display.max_columns", None):
            self._txt.insert(tk.END, df.to_string(index=False))

    def _show_data_info(self, df: pd.DataFrame) -> None:
        """Show data structure information."""
        self._info_text.delete("1.0", tk.END)
        
        info = f"""Headers ({len(df.columns)} columns):
{', '.join(df.columns.tolist())}

Dimensions: {len(df)} rows × {len(df.columns)} columns

Data Types:
"""
        
        for col in df.columns:
            info += f"- {col}: {df[col].dtype}\n"
        
        self._info_text.insert("1.0", info)

    def _save(self):
        if self._df is None:
            messagebox.showerror("Error", "No file loaded!")
            return
        out = save_parquet(self._df, original_path=self._xlsx_path)
        messagebox.showinfo("Saved", f"Parquet saved to: {out}")

    def _analyze_data(self):
        """Run AI analysis in a separate thread to avoid blocking UI."""
        if self._df is None:
            messagebox.showerror("Error", "No file loaded!")
            return
        
        instruction = self._instruction_text.get("1.0", tk.END).strip()
        if not instruction or instruction.startswith("e.g.,"):
            messagebox.showwarning("Warning", "Please enter a valid analysis instruction!")
            return
        
        # Clear previous results
        self._results_text.delete("1.0", tk.END)
        self._results_text.insert("1.0", "🤖 Generating analysis code...\n")
        self._results_text.see("1.0")
        
        # Run analysis in separate thread
        def run_analysis():
            try:
                result = analyze_data_with_ai(instruction, self._df, self._model_var.get())
                
                # Update UI in main thread
                self.after(0, lambda: self._display_results(result))
                
            except Exception as e:
                self.after(0, lambda: self._display_error(str(e)))
        
        threading.Thread(target=run_analysis, daemon=True).start()

    def _display_results(self, result):
        """Display analysis results in the UI."""
        self._results_text.delete("1.0", tk.END)
        
        if result["success"]:
            output = f"""✅ Analysis completed successfully!

📊 RESULTS:
{result.get('output', 'No output generated')}

🔧 GENERATED CODE:
{result['code']}

📈 PERFORMANCE:
- Model: {result['model']}
- Latency: {result['latency_s']}s
- Total Tokens: {result['tokens']['total_tokens']}
- Prompt Tokens: {result['tokens']['prompt_tokens']}
- Completion Tokens: {result['tokens']['completion_tokens']}
"""
        else:
            output = f"❌ Error during analysis: {result.get('error', 'Unknown error')}"
        
        self._results_text.insert("1.0", output)
        self._results_text.see("1.0")

    def _display_error(self, error_msg):
        """Display error message in the UI."""
        self._results_text.delete("1.0", tk.END)
        self._results_text.insert("1.0", f"❌ Error: {error_msg}\n\nMake sure your GROQ_API_KEY is set in the .env file")
        self._results_text.see("1.0")


if __name__ == "__main__":
    App().mainloop()