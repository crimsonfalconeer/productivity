## TASKS

1. Load a sample .xlsx data into python
2. Store it as a .parquet file for efficient access
3. Maintain modularity and folder structure according the SDLC principles
4. Print the contents of the .xlsx file for verification

4. Create a simple UI to perform the above task:
4a. Tkinter (Standalone)
4b. Streamlit (Web Based)

5. **NEW: AI-Powered Data Analysis**
5a. Display all headers and dimensions in the UI
5b. Allow users to input analysis instructions
5c. Generate Python code using Groq AI
5d. Execute the code locally and display results

## API Keys / LLM Interface

1. Create a Groq account (free)
2. Get an API key 
3. Store the key safely on your machine
4. Write a "Hello World" program to interface with Groq.
4a. Try a small language model (8b)
4b. Try a large language model (70b)
5. Output inference times
6. Output total token usage

7. **NEW: AI Data Analysis**
7a. Generate Python code for data analysis tasks
7b. Execute generated code safely on local data
7c. Display results and performance metrics





# XLSX → Parquet + Groq Hello-World + AI Data Analysis

A powerful toolbox that does three things:

1. **Data converter**  
   *Load any `.xlsx`, preview the full sheet, and save it as a
   snappy-compressed `.parquet`* – via CLI, Tkinter desktop app, or
   Streamlit web UI.

2. **Groq LLM demo**  
   A minimal "Hello, world!" that calls Groq's hosted Llama-3 models
   (8 B **instant** & 70 B **versatile**), then prints latency and token
   usage.

3. **AI-Powered Data Analysis**  
   *Upload your spreadsheet, describe what you want to analyze, and let AI
   generate and execute the code for you!* Supports natural language
   instructions like "sort by column X" or "calculate the sum of column Y".

---

## Directory layout

```text
project_root/
├── data/                 ← auto-created at runtime
│   ├── raw/              ← original Excel files
│   └── processed/        ← generated Parquet files
├── src/
│   ├── cli.py            ← xlsx → parquet from the terminal
│   ├── config.py         ← paths for the converter
│   ├── io_utils.py       ← reusable load_/save_ helpers
│   └── llm/              ← Groq demo code lives here
│       ├── __init__.py
│       ├── config.py     ← loads `GROQ_API_KEY`
│       ├── hello.py      ← runs the small / large model
│       └── data_analyzer.py ← NEW: AI data analysis
├── ui/
│   ├── tkinter_app.py    ← desktop UI (enhanced with AI)
│   └── streamlit_app.py  ← web UI (enhanced with AI)
├── requirements.txt
├── pyproject.toml
├── .env.example          ← template for secrets (not committed)
├── test_ai_analysis.py   ← NEW: test script for AI features
└── README.md
```

---

## Quick-start (local)

### 1  Create & activate a virtual environment

```bash
python -m venv .venv
# PowerShell on Windows
. .venv/Scripts/activate
# …or bash/zsh on macOS / Linux
# source .venv/bin/activate

pip install -e
```

### 2  Set up your Groq API key

1. Sign up / log in at [https://console.groq.com/](https://console.groq.com/) → **Create API key**
2. Copy `.env.example` to `.env` and paste the key:

   ```env
   GROQ_API_KEY=sk-YOUR_KEY
   ```

---

## Usage

### Converter

| Mode          | Command                                       |
| ------------- | --------------------------------------------- |
| **CLI**       | `python -m src.cli path/to/file.xlsx`         |
| **Tkinter**   | `python ui/tkinter_app.py`                    |
| **Streamlit** | `streamlit run ui/streamlit_app.py` |

All modes preview the entire sheet; when you confirm, the original file is
copied to **`data/raw/`** and its Parquet twin goes to **`data/processed/`**.

### Groq "Hello, world!"

```bash
# 8-b instant model (default prompt = "Hello, world!")
python -m src.llm.hello --model small

# 70-b versatile model with a custom prompt
python -m src.llm.hello --model large --prompt "Explain transformers in 2 lines"
```

### AI-Powered Data Analysis

**NEW FEATURES:**

1. **Data Structure Display**: View all headers, dimensions, and data types
2. **Natural Language Instructions**: Describe what you want to analyze
3. **AI Code Generation**: Groq generates Python code for your analysis
4. **Safe Execution**: Code runs locally on your data
5. **Performance Metrics**: See latency and token usage

**Example Usage:**

1. Upload your Excel file
2. View the data structure and preview
3. Enter instructions like:
   - "Sort by Age in descending order"
   - "Calculate the sum of Salary column"
   - "Show the top 10 rows sorted by Department"
   - "Find the average of all numeric columns"
4. Click "Generate & Execute Analysis"
5. View results, generated code, and performance metrics

**Test the AI Analysis:**

```bash
# Test with sample data
python test_ai_analysis.py
```

---
