"""Data analysis code generation using Groq."""
import time
import json
import pandas as pd
from typing import List, Dict, Any
from .config import API_KEY
import groq
import pdb # for live runtime debugging

MODELS = {
    "small": "llama-3.1-8b-instant",
    "large": "llama-3.3-70b-versatile",
}

def generate_analysis_code(user_instruction: str, headers: List[str], model: str = "large") -> Dict[str, Any]:
    """
    Generate Python code to analyze data based on user instruction.
    
    Parameters
    ----------
    user_instruction : str
        User's instruction for data analysis
    headers : List[str]
        List of column headers from the spreadsheet
    model : str
        Groq model to use ("small" or "large")
    
    Returns
    -------
    Dict[str, Any]
        Dictionary containing generated code, metadata, and execution results
    """
    client = groq.Groq(api_key=API_KEY)
    
    # Create a comprehensive prompt for code generation
    prompt = f"""
You are a Python data analysis expert. Given a pandas DataFrame with the following columns:
{headers}

The user wants to: {user_instruction}

Generate ONLY Python code that:
1. Uses pandas to perform the requested analysis
2. Assumes the DataFrame is called 'df'
3. Returns or prints the results clearly
4. Handles potential errors gracefully
5. Uses only the headers provided (don't assume other columns exist)
6. I'm already using the necessary imports (e.g. import pandas as pd), so do not generate these lines in your code.

Return ONLY the Python code, no explanations or markdown formatting.
"""
   # Added more context so LLM generates code stubs only (instruction 6 above) ^^

    tic = time.perf_counter()
    
    try:
        resp = client.chat.completions.create(
            model=MODELS[model],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # Lower temperature for more consistent code generation
        )
        
        toc = time.perf_counter()
        
        generated_code = resp.choices[0].message.content.strip()
        
        # Clean up the code (remove markdown if present)
        if generated_code.startswith("```python"):
            generated_code = generated_code[9:]
        if generated_code.endswith("```"):
            generated_code = generated_code[:-3]
        generated_code = generated_code.strip()
        
        return {
            "code": generated_code,
            "latency_s": round(toc - tic, 3),
            "tokens": {
                "prompt_tokens": resp.usage.prompt_tokens,
                "completion_tokens": resp.usage.completion_tokens,
                "total_tokens": resp.usage.total_tokens,
            },
            "model": model,
            "success": True
        }
        
    except Exception as e:
        return {
            "code": "",
            "error": str(e),
            "success": False
        }

def execute_analysis_code(code: str, df: pd.DataFrame) -> Dict[str, Any]:
    """
    Safely execute the generated analysis code.
    
    Parameters
    ----------
    code : str
        Python code to execute
    df : pd.DataFrame
        DataFrame to analyze
    
    Returns
    -------
    Dict[str, Any]
        Dictionary containing execution results and any output
    """
    # Create a safe execution environment
    local_vars = {
        'df': df.copy(),  # Use a copy to avoid modifying original
        'pd': pd,
        'print': print,
    }
    
    try:
        # Capture stdout to get print output
        import io
        import sys
        from contextlib import redirect_stdout
        
        output = io.StringIO()
        
        # pdb.set_trace() # for live runtime debugging

        with redirect_stdout(output):
            exec(code, globals(), local_vars)
        
        captured_output = output.getvalue()
        
        return {
            "success": True,
            "output": captured_output,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }

def analyze_data_with_ai(user_instruction: str, df: pd.DataFrame, model: str = "large") -> Dict[str, Any]:
    """
    Complete workflow: generate code and execute it.
    
    Parameters
    ----------
    user_instruction : str
        User's instruction for data analysis
    df : pd.DataFrame
        DataFrame to analyze
    model : str
        Groq model to use
    
    Returns
    -------
    Dict[str, Any]
        Complete analysis results including code generation and execution
    """
    headers = list(df.columns)
    
    # Generate code
    generation_result = generate_analysis_code(user_instruction, headers, model)
    
    if not generation_result["success"]:
        return generation_result
    
    # Execute code
    execution_result = execute_analysis_code(generation_result["code"], df)
    
    # Combine results
    return {
        **generation_result,
        **execution_result
    } 