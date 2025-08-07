"""Enhanced Streamlit UI with AI-powered data analysis and batch testing."""
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
from src.llm.batch_analyzer import run_batch_analysis, BatchAnalyzer

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
    3. Choose your analysis mode:
       - **Interactive Analysis**: Enter custom instructions
       - **Unit Tests**: Run predefined queries from queries.txt
    
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
    
    # Create tabs for different analysis modes
    tab1, tab2 = st.tabs(["🔍 Interactive Analysis", "🧪 Unit Tests"])
    
    # Tab 1: Interactive Analysis
    with tab1:
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
            analyze_button = st.button("🚀 Generate & Execute Analysis", type="primary", key="interactive_analyze")
        
        with col2:
            if st.button("💾 Save to Parquet", key="interactive_save"):
                out_path = save_parquet(df, original_path=tmp_path)
                st.success(f"Saved → {out_path.relative_to(Path.cwd())}")
        
        # Execute analysis if button is clicked
        if analyze_button and user_instruction.strip():
            with st.spinner("🤖 Generating analysis code..."):
                try:
                    result = analyze_data_with_ai(user_instruction, df, model_choice)
                    
                    if result["success"]:
                        # Display results in tabs
                        result_tab1, result_tab2, result_tab3 = st.tabs(["📊 Results", "🔧 Generated Code", "📈 Performance"])
                        
                        with result_tab1:
                            if result.get("output"):
                                st.subheader("Analysis Results")
                                st.code(result["output"], language="text")
                            else:
                                st.info("Analysis completed but no output was generated.")
                        
                        with result_tab2:
                            st.subheader("Generated Python Code")
                            st.code(result["code"], language="python")
                            
                            # Add a copy button
                            st.button("📋 Copy Code", on_click=lambda: st.write("Code copied to clipboard!"))
                        
                        with result_tab3:
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
    
    # Tab 2: Unit Tests (Batch Mode)
    with tab2:
        st.markdown("---")
        st.subheader("🧪 Batch Testing")
        
        # File upload for custom queries
        st.subheader("📁 Upload Custom Queries")
        uploaded_queries = st.file_uploader(
            "Upload a .txt file with queries (one per line)",
            type="txt",
            help="Upload your own queries file, or leave empty to use the default queries/queries.txt"
        )
        
        # Determine which queries file to use
        if uploaded_queries is not None:
            # Use uploaded file
            st.success(f"✅ Using uploaded file: {uploaded_queries.name}")
            
            # Save uploaded file to temp location
            import tempfile
            temp_dir = Path(tempfile.gettempdir())
            temp_queries_path = temp_dir / uploaded_queries.name
            temp_queries_path.write_bytes(uploaded_queries.getbuffer())
            queries_file = temp_queries_path
            
            # Display uploaded queries content
            queries_content = uploaded_queries.getvalue().decode('utf-8')
            st.subheader("📋 Uploaded Queries")
            st.text_area(
                "Queries from uploaded file",
                value=queries_content,
                height=200,
                disabled=True
            )
            
        else:
            # Use default queries file
            queries_file = Path("queries/queries.txt")
            
            if not queries_file.exists():
                st.error(f"❌ Default queries file not found at {queries_file}")
                st.info("Please either upload a queries file above, or create a queries.txt file in the queries/ directory with one query per line.")
                st.stop()
            else:
                st.info("ℹ️ Using default queries file: queries/queries.txt")
                
                # Display default queries file info
                try:
                    with open(queries_file, 'r', encoding='utf-8') as f:
                        queries_content = f.read()
                    
                    st.subheader("📋 Available Queries")
                    st.text_area(
                        "Queries from queries.txt",
                        value=queries_content,
                        height=200,
                        disabled=True
                    )
                
                except Exception as e:
                    st.error(f"❌ Error reading queries file: {str(e)}")
                    st.stop()
        
        # Batch execution controls (common for both uploaded and default files)
        if 'queries_file' in locals():
            col1, col2 = st.columns([1, 1])
            
            with col1:
                run_batch_button = st.button("🚀 Run All Tests", type="primary", key="batch_run")
            
            with col2:
                if st.button("📊 View Query Stats", key="batch_stats"):
                    try:
                        analyzer = BatchAnalyzer(model_choice)
                        queries = analyzer.load_queries_from_file(queries_file)
                        
                        st.subheader("📊 Query Statistics")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Total Queries", len(queries))
                        
                        with col2:
                            sections = set(q['section'] for q in queries)
                            st.metric("Sections", len(sections))
                        
                        with col3:
                            st.metric("File Size", f"{queries_file.stat().st_size / 1024:.1f} KB")
                        
                        # Show sections breakdown
                        st.subheader("📂 Sections Breakdown")
                        section_counts = {}
                        for query in queries:
                            section = query['section']
                            section_counts[section] = section_counts.get(section, 0) + 1
                        
                        for section, count in section_counts.items():
                            st.write(f"**{section}**: {count} queries")
                            
                    except Exception as e:
                        st.error(f"❌ Error loading queries: {str(e)}")
            
            # Execute batch analysis
            if run_batch_button:
                with st.spinner("🧪 Running batch analysis..."):
                    try:
                        batch_results = run_batch_analysis(df, queries_file, model_choice)
                        
                        # Display summary
                        st.subheader("📊 Batch Execution Summary")
                        summary = batch_results['summary']
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Total Queries", summary['total_queries'])
                        
                        with col2:
                            st.metric("Successful", summary['successful'], delta=f"+{summary['successful']}")
                        
                        with col3:
                            st.metric("Failed", summary['failed'], delta=f"-{summary['failed']}")
                        
                        with col4:
                            st.metric("Success Rate", f"{summary['success_rate']:.1f}%")
                        
                        # Performance metrics
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Total Time", f"{summary['total_time']:.2f}s")
                        
                        with col2:
                            st.metric("Avg Time/Query", f"{summary['average_time']:.2f}s")
                        
                        # Display detailed results
                        st.subheader("📋 Detailed Results")
                        
                        # Create expandable sections for each query
                        for result in batch_results['results']:
                            with st.expander(f"Query {result['query_number']}: {result['query'][:50]}...", expanded=False):
                                col1, col2 = st.columns([1, 1])
                                
                                with col1:
                                    st.write(f"**Section:** {result['section']}")
                                    st.write(f"**Status:** {'✅ Success' if result['success'] else '❌ Failed'}")
                                    
                                    if result['success']:
                                        st.metric("Latency", f"{result['latency_s']}s")
                                        st.metric("Tokens", result['tokens']['total_tokens'])
                                    else:
                                        st.error(f"Error: {result.get('error', 'Unknown error')}")
                                
                                with col2:
                                    if result['success'] and result.get('output'):
                                        st.subheader("Output:")
                                        st.code(result['output'], language="text")
                                    
                                    if result.get('code'):
                                        st.subheader("Generated Code:")
                                        st.code(result['code'], language="python")
                        
                        # Execution log
                        st.subheader("📝 Execution Log")
                        log_text = "\n".join(batch_results['execution_log'])
                        st.text_area("Log", value=log_text, height=200, disabled=True)
                        
                        # Export results
                        if st.button("💾 Export Results", key="export_batch"):
                            try:
                                analyzer = BatchAnalyzer(model_choice)
                                export_path = analyzer.export_results(batch_results)
                                st.success(f"✅ Results exported to: {export_path}")
                            except Exception as e:
                                st.error(f"❌ Export failed: {str(e)}")
                        
                    except Exception as e:
                        st.error(f"❌ Batch analysis failed: {str(e)}")
                        st.info("Make sure your GROQ_API_KEY is set in the .env file")