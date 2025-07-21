"""Simple Streamlit UI."""
from pathlib import Path
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.append(str(root))

import streamlit as st
import pandas as pd

from src.io_utils import load_xlsx, save_parquet

st.title("📊 XLSX → Parquet Converter")

uploaded = st.file_uploader("Choose an .xlsx file", type="xlsx")

if uploaded is not None:
    # Use the system temp dir to avoid hard‑coded /tmp on Windows
    tmp_dir = Path(tempfile.gettempdir())
    tmp_dir.mkdir(exist_ok=True)
    tmp_path = tmp_dir / uploaded.name
    tmp_path.write_bytes(uploaded.getbuffer())

    df = load_xlsx(tmp_path)

    st.subheader("Preview (full DataFrame)")
    st.dataframe(df, use_container_width=True, hide_index=True)

    if st.button("Save to data/processed as Parquet"):
        out_path = save_parquet(df, original_path=tmp_path)
        st.success(f"Saved → {out_path.relative_to(Path.cwd())}")