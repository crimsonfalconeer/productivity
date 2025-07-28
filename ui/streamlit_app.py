"""Enhanced Streamlit UI with AI-powered data analysis."""
from pathlib import Path
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.append(str(root))

import streamlit as st
import pandas as pd
import json

from src.io_utils import load_xlsx, save_parquet
from src.llm.data_analyzer import analyze_data_with_ai

st.set_page_config(
    page_title="📊 XLSX → Parquet Converter & AI Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 XLSX → Parquet Converter & AI Analyzer")

# Sidebar for model selection
with st.sidebar:
    st.header("🤖 AI Settings")
    model_choice = st.selectbox(
        "Choose AI Model",
        ["large", "small"],
        help="Large model is more capable but slower, small model is faster but less capable"
    )
    
    st.markdown("---")
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. Upload your Excel file
    2. View the data preview and headers
    3. Enter your analysis instruction
    4. Let AI generate and execute the code!
    
    **Example instructions:**
    - "Sort by column X in descending order"
    - "Calculate the sum of column Y"
    - "Show the top 10 rows sorted by column Z"
    - "Find the average of numeric columns"
    """)

# File upload
uploaded = st.file_uploader("Choose an .xlsx file", type="xlsx")

if uploaded is not None:
    # Use the system temp dir to avoid hard‑coded /tmp on Windows
    tmp_dir = Path(tempfile.gettempdir())
    tmp_dir.mkdir(exist_ok=True)
    tmp_path = tmp_dir / uploaded.name
    tmp_path.write_bytes(uploaded.getbuffer())

    df = load_xlsx(tmp_path)
    
    # Display file info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Rows", len(df))
    
    with col2:
        st.metric("Columns", len(df.columns))
    
    with col3:
        st.metric("File Size", f"{uploaded.size / 1024:.1f} KB")
    
    # Display headers and dimensions in a text box
    st.subheader("📋 Data Structure")
    
    headers_info = f"""
**Headers ({len(df.columns)} columns):**
{', '.join(df.columns.tolist())}

**Dimensions:** {len(df)} rows × {len(df.columns)} columns

**Data Types:**
"""
    
    for col in df.columns:
        headers_info += f"- {col}: {df[col].dtype}\n"
    
    st.text_area(
        "Data Structure Information",
        value=headers_info,
        height=200,
        disabled=True
    )
    
    # Data preview
    st.subheader("📊 Data Preview")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # AI Analysis Section
    st.markdown("---")
    st.subheader("🤖 AI-Powered Data Analysis")
    
    # User instruction input
    user_instruction = st.text_area(
        "Enter your analysis instruction:",
        placeholder="e.g., 'Sort by column X in descending order' or 'Calculate the sum of column Y'",
        height=100
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        analyze_button = st.button("🚀 Generate & Execute Analysis", type="primary")
    
    with col2:
        if st.button("💾 Save to Parquet"):
            out_path = save_parquet(df, original_path=tmp_path)
            st.success(f"Saved → {out_path.relative_to(Path.cwd())}")
    
    # Execute analysis if button is clicked
    if analyze_button and user_instruction.strip():
        with st.spinner("🤖 Generating analysis code..."):
            try:
                result = analyze_data_with_ai(user_instruction, df, model_choice)
                
                if result["success"]:
                    # Display results in tabs
                    tab1, tab2, tab3 = st.tabs(["📊 Results", "🔧 Generated Code", "📈 Performance"])
                    
                    with tab1:
                        if result.get("output"):
                            st.subheader("Analysis Results")
                            st.code(result["output"], language="text")
                        else:
                            st.info("Analysis completed but no output was generated.")
                    
                    with tab2:
                        st.subheader("Generated Python Code")
                        st.code(result["code"], language="python")
                        
                        # Add a copy button
                        st.button("📋 Copy Code", on_click=lambda: st.write("Code copied to clipboard!"))
                    
                    with tab3:
                        st.subheader("Performance Metrics")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Latency", f"{result['latency_s']}s")
                        
                        with col2:
                            st.metric("Model", result["model"])
                        
                        with col3:
                            st.metric("Total Tokens", result["tokens"]["total_tokens"])
                        
                        # Detailed token usage
                        st.json(result["tokens"])
                
                else:
                    st.error(f"❌ Error during analysis: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Make sure your GROQ_API_KEY is set in the .env file")
    
    elif analyze_button and not user_instruction.strip():
        st.warning("⚠️ Please enter an analysis instruction first.")