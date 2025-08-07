## TASKS

1. Load a sample .xlsx data into python
2. Store it as a .parquet file for efficient access
3. Maintain modularity and folder structure according the SDLC principles
4. Print the contents of the .xlsx file for verification

4. Create a simple UI to perform the above task:
4a. Tkinter (Standalone)
4b. Streamlit (Web Based)

5. **AI-Powered Data Analysis**
5a. Display all headers and dimensions in the UI
5b. Allow users to input analysis instructions
5c. Generate Python code using Groq AI
5d. Execute the code locally and display results

6. **NEW: Automated Batch Testing**
6a. Read queries from .txt files (e.g., queries.txt)
6b. Execute predefined queries in batch mode
6c. Display results with success/failure tracking
6d. Export results for debugging and analysis

## API Keys / LLM Interface

1. Create a Groq account (free)
2. Get an API key 
3. Store the key safely on your machine
4. Write a "Hello World" program to interface with Groq.
4a. Try a small language model (8b)
4b. Try a large language model (70b)
5. Output inference times
6. Output total token usage

7. **AI Data Analysis**
7a. Generate Python code for data analysis tasks
7b. Execute generated code safely on local data
7c. Display results and performance metrics

8. **NEW: Batch Testing**
8a. Execute multiple queries from text files
8b. Track success rates and performance metrics
8c. Generate detailed execution logs
8d. Export results in JSON format




# XLSX → Parquet + Groq Hello-World + AI Data Analysis + Batch Testing

A powerful toolbox that does four things:

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

4. **NEW: Automated Batch Testing**  
   *Test AI-generated code against predefined queries from text files.*
   Run multiple analysis queries in batch mode with detailed reporting and
   export capabilities.

---

## Directory layout

```text
project_root/
├── data/                 ← auto-created at runtime
│   ├── raw/              ← original Excel files
│   └── processed/        ← generated Parquet files
├── queries/              ← NEW: batch testing queries
│   └── queries.txt       ← predefined analysis queries
├── src/
│   ├── cli.py            ← xlsx → parquet + batch testing from terminal
│   ├── config.py         ← paths for the converter
│   ├── io_utils.py       ← reusable load_/save_ helpers
│   └── llm/              ← Groq demo code lives here
│       ├── __init__.py
│       ├── config.py     ← loads `GROQ_API_KEY`
│       ├── hello.py      ← runs the small / large model
│       ├── data_analyzer.py ← AI data analysis
│       └── batch_analyzer.py ← NEW: batch testing functionality
├── ui/
│   ├── tkinter_app.py    ← desktop UI (enhanced with AI)
│   └── streamlit_app.py  ← web UI (enhanced with AI + batch testing)
├── requirements.txt
├── pyproject.toml
├── .env.example          ← template for secrets (not committed)
├── test_ai_analysis.py   ← test script for AI features
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
#pip install -r .\requirements.txt
```

### 2  Set up your Groq API key

1. Sign up / log in at [https://console.groq.com/](https://console.groq.com/) → **Create API key**
2. Copy `.env.example` to `.env` and paste the key:

   ```env
   GROQ_API_KEY=sk-YOUR_KEY
   ```
(Create a `.env` file in your root directory and paste the key (as above))
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

**FEATURES:**

1. **Data Structure Display**: View all headers, dimensions, and data types
2. **Natural Language Instructions**: Describe what you want to analyze
3. **AI Code Generation**: Groq generates Python code for your analysis
4. **Safe Execution**: Code runs locally on your data
5. **Performance Metrics**: See latency and token usage
6. **NEW: Tabbed Interface**: Separate Interactive Analysis and Unit Tests
7. **NEW: Batch Testing**: Run predefined queries from queries.txt

**Example Usage:**

1. Upload your Excel file
2. Choose your analysis mode:
   - **Interactive Analysis**: Enter custom instructions
   - **Unit Tests**: Run predefined queries from queries.txt
3. Enter instructions like:
   - "Sort by Age in descending order"
   - "Calculate the sum of Salary column"
   - "Show the top 10 rows sorted by Department"
   - "Find the average of all numeric columns"
4. Click "Generate & Execute Analysis" or "Run All Tests"
5. View results, generated code, and performance metrics

**CLI Usage:**

```bash
# Interactive mode
python -m src.cli interactive data/raw/test_data.xlsx

# Batch mode
python -m src.cli batch data/raw/test_data.xlsx queries/queries.txt

# With specific model
python -m src.cli interactive data/raw/test_data.xlsx --model small
```

**Test the AI Analysis:**

```bash
# Test with sample data
python test_ai_analysis.py
```

### Batch Testing

**NEW FEATURES:**

1. **Query File Support**: Read queries from `queries/queries.txt` or upload custom files
2. **File Upload**: Upload your own .txt files containing natural language queries
3. **Section Organization**: Group queries by sections (e.g., [Employee & Work Insights])
4. **Batch Execution**: Run all queries with a single click
5. **Detailed Reporting**: Success/failure tracking with performance metrics
6. **Execution Logging**: Real-time log of batch execution
7. **Result Export**: Export results to JSON for further analysis

**Query File Format:**

```txt
[Employee & Work Insights]
Which department has the highest total hours worked?
What is the average hourly rate for each department?

[Date & Time Analysis]
How many employees started before January 1, 2022?
Which employees worked for less than 30 days?

[Aggregations & Group Comparisons]
Compare the total earnings by department.
Which departments have median hourly rates higher than the overall median?
```

**File Upload Usage:**

1. **Upload Custom Queries**: In the "Unit Tests" tab, use the file uploader to upload your own .txt file
2. **Default Behavior**: If no file is uploaded, the app uses `queries/queries.txt` from the project directory
3. **File Requirements**: Upload .txt files with one query per line, optionally grouped by sections
4. **Sample File**: Download `sample_queries.txt` to see the expected format

**Batch Testing Results Include:**

- **Summary Metrics**: Total queries, success rate, execution time
- **Detailed Results**: Individual query results with generated code and output
- **Performance Tracking**: Latency and token usage per query
- **Error Handling**: Detailed error messages for failed queries
- **Export Capability**: JSON export with all results and logs

---
