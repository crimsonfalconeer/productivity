## TASKS

1. Load a sample .xlsx data into python
2. Store it as a .parquet file for efficient access
3. Maintain modularity and folder structure according the SDLC principles
4. Print the contents of the .xlsx file for verification

4. Create a simple UI to perform the above task:
4a. Tkinter (Standalone)
4b. Streamlit (Web Based)


## API Keys / LLM Interface

1. Create a Groq account (free)
2. Get an API key 
3. Store the key safely on your machine 
4. Write a "Hello World" program to interface with Groq.
4a. Try a small language model (8b)
4b. Try a large language model (70b)
5. Output inference times
6. Output total token usage




````markdown
# XLSX → Parquet + Groq Hello-World 🛠️

A tiny toolbox that does two things:

1. **Data converter**  
   *Load any `.xlsx`, preview the full sheet, and save it as a
   snappy-compressed `.parquet`* – via CLI, Tkinter desktop app, or
   Streamlit web UI.

2. **Groq LLM demo**  
   A minimal “Hello, world!” that calls Groq’s hosted Llama-3 models
   (8 B **instant** & 70 B **versatile**), then prints latency and token
   usage.

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
│       └── hello.py      ← runs the small / large model
├── ui/
│   ├── tkinter_app.py    ← desktop UI
│   └── streamlit_app.py  ← web UI
├── requirements.txt
├── pyproject.toml
├── .env.example          ← template for secrets (not committed)
└── README.md
````

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

### Groq “Hello, world!”

```bash
# 8-b instant model (default prompt = "Hello, world!")
python -m src.llm.hello --model small

# 70-b versatile model with a custom prompt
python -m src.llm.hello --model large --prompt "Explain transformers in 2 lines"
```

Example output:

```json
{
  "model": "large",
  "latency_s": 0.41,
  "tokens": {
    "prompt_tokens": 7,
    "completion_tokens": 24,
    "total_tokens": 31
  }
}

--- assistant ---
Transformers treat text as sequences of tokens and learn to relate every
token to every other via self-attention, capturing context in parallel.
They stack many such attention layers, enabling massive models to reason,
translate, and generate human-like language.
```

---
