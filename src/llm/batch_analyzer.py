"""Batch testing functionality for AI-generated code analysis."""
import time
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from .data_analyzer import analyze_data_with_ai


class BatchAnalyzer:
    """Handles batch execution of queries against datasets."""
    
    def __init__(self, model: str = "large"):
        """
        Initialize the batch analyzer.
        
        Parameters
        ----------
        model : str
            The AI model to use for analysis ("small" or "large")
        """
        self.model = model
        self.results = []
        self.execution_log = []
    
    def load_queries_from_file(self, file_path: Path) -> List[str]:
        """
        Load queries from a text file.
        
        Parameters
        ----------
        file_path : Path
            Path to the queries file
            
        Returns
        -------
        List[str]
            List of queries, one per line
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse queries, handling sections and comments
            queries = []
            current_section = "General"
            
            for line in content.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                # Check for section headers
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    continue
                
                # Skip comment lines (starting with # or //)
                if line.startswith('#') or line.startswith('//'):
                    continue
                
                # Add non-empty lines as queries
                if line:
                    queries.append({
                        'query': line,
                        'section': current_section
                    })
            
            return queries
            
        except Exception as e:
            raise Exception(f"Error loading queries from {file_path}: {str(e)}")
    
    def execute_batch_analysis(self, df: pd.DataFrame, queries: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Execute batch analysis on the given DataFrame.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to analyze
        queries : List[Dict[str, str]]
            List of queries with their sections
            
        Returns
        -------
        Dict[str, Any]
            Batch execution results
        """
        start_time = time.time()
        results = []
        successful = 0
        failed = 0
        
        for i, query_info in enumerate(queries, 1):
            query = query_info['query']
            section = query_info['section']
            
            # Log start of query
            self._log_execution(f"Starting query {i}/{len(queries)}: {query[:50]}...")
            
            try:
                # Execute analysis
                result = analyze_data_with_ai(query, df, self.model)
                
                # Add metadata
                result['query'] = query
                result['section'] = section
                result['query_number'] = i
                result['total_queries'] = len(queries)
                
                if result['success']:
                    successful += 1
                    self._log_execution(f"✅ Query {i} completed successfully")
                else:
                    failed += 1
                    self._log_execution(f"❌ Query {i} failed: {result.get('error', 'Unknown error')}")
                
                results.append(result)
                
            except Exception as e:
                failed += 1
                error_result = {
                    'success': False,
                    'query': query,
                    'section': section,
                    'query_number': i,
                    'total_queries': len(queries),
                    'error': str(e),
                    'code': '',
                    'output': '',
                    'latency_s': 0,
                    'tokens': {'total_tokens': 0}
                }
                results.append(error_result)
                self._log_execution(f"❌ Query {i} failed with exception: {str(e)}")
        
        total_time = time.time() - start_time
        
        return {
            'results': results,
            'summary': {
                'total_queries': len(queries),
                'successful': successful,
                'failed': failed,
                'success_rate': (successful / len(queries)) * 100 if queries else 0,
                'total_time': total_time,
                'average_time': total_time / len(queries) if queries else 0
            },
            'execution_log': self.execution_log
        }
    
    def _log_execution(self, message: str):
        """Add a message to the execution log."""
        timestamp = time.strftime("%H:%M:%S")
        self.execution_log.append(f"[{timestamp}] {message}")
    
    def export_results(self, results: Dict[str, Any], output_path: Optional[Path] = None) -> Path:
        """
        Export batch results to a JSON file.
        
        Parameters
        ----------
        results : Dict[str, Any]
            Batch execution results
        output_path : Optional[Path]
            Output file path. If None, generates a timestamped filename
            
        Returns
        -------
        Path
            Path to the exported file
        """
        if output_path is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = Path(f"batch_results_{timestamp}.json")
        
        # Prepare export data
        export_data = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'model': self.model,
            'summary': results['summary'],
            'execution_log': results['execution_log'],
            'results': []
        }
        
        # Add results (excluding large DataFrames if present)
        for result in results['results']:
            export_result = result.copy()
            # Remove any large objects that might cause serialization issues
            if 'df' in export_result:
                del export_result['df']
            export_data['results'].append(export_result)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return output_path


def run_batch_analysis(df: pd.DataFrame, queries_file: Path, model: str = "large") -> Dict[str, Any]:
    """
    Convenience function to run batch analysis.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to analyze
    queries_file : Path
        Path to the queries file
    model : str
        AI model to use
        
    Returns
    -------
    Dict[str, Any]
        Batch execution results
    """
    analyzer = BatchAnalyzer(model)
    queries = analyzer.load_queries_from_file(queries_file)
    return analyzer.execute_batch_analysis(df, queries) 