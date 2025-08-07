"""Command-line interface for the productivity app."""
import argparse
import sys
from pathlib import Path

# Add the project root to the Python path
root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.append(str(root))

from src.io_utils import load_xlsx, save_parquet
from src.llm.data_analyzer import analyze_data_with_ai
from src.llm.batch_analyzer import run_batch_analysis


def interactive_mode(data_file: Path, model: str = "large"):
    """Run interactive analysis mode."""
    print(f"📊 Loading data from {data_file}...")
    df = load_xlsx(data_file)
    
    print(f"✅ Loaded {len(df)} rows × {len(df.columns)} columns")
    print(f"📋 Columns: {', '.join(df.columns.tolist())}")
    print()
    
    while True:
        instruction = input("🤖 Enter analysis instruction (or 'quit' to exit): ").strip()
        
        if instruction.lower() in ['quit', 'exit', 'q']:
            break
        
        if not instruction:
            print("⚠️ Please enter an instruction.")
            continue
        
        print("🚀 Generating analysis...")
        try:
            result = analyze_data_with_ai(instruction, df, model)
            
            if result["success"]:
                print("✅ Analysis completed successfully!")
                print(f"⏱️ Latency: {result['latency_s']}s")
                print(f"🧠 Model: {result['model']}")
                print(f"🔢 Tokens: {result['tokens']['total_tokens']}")
                print()
                
                if result.get("output"):
                    print("📊 Results:")
                    print(result["output"])
                else:
                    print("ℹ️ Analysis completed but no output was generated.")
                
                print()
                print("🔧 Generated Code:")
                print(result["code"])
                print()
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("💡 Make sure your GROQ_API_KEY is set in the .env file")


def batch_mode(data_file: Path, queries_file: Path, model: str = "large"):
    """Run batch testing mode."""
    print(f"📊 Loading data from {data_file}...")
    df = load_xlsx(data_file)
    
    print(f"✅ Loaded {len(df)} rows × {len(df.columns)} columns")
    print(f"📋 Loading queries from {queries_file}...")
    
    try:
        batch_results = run_batch_analysis(df, queries_file, model)
        
        # Display summary
        summary = batch_results['summary']
        print()
        print("📊 Batch Execution Summary")
        print("=" * 40)
        print(f"Total Queries: {summary['total_queries']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Total Time: {summary['total_time']:.2f}s")
        print(f"Average Time/Query: {summary['average_time']:.2f}s")
        print()
        
        # Display detailed results
        print("📋 Detailed Results")
        print("=" * 40)
        for result in batch_results['results']:
            status = "✅ Success" if result['success'] else "❌ Failed"
            print(f"\nQuery {result['query_number']}: {result['query'][:50]}...")
            print(f"Section: {result['section']}")
            print(f"Status: {status}")
            
            if result['success']:
                print(f"Latency: {result['latency_s']}s")
                print(f"Tokens: {result['tokens']['total_tokens']}")
                if result.get('output'):
                    print("Output:")
                    print(result['output'])
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
        
        # Display execution log
        print()
        print("📝 Execution Log")
        print("=" * 40)
        for log_entry in batch_results['execution_log']:
            print(log_entry)
            
    except Exception as e:
        print(f"❌ Batch analysis failed: {str(e)}")
        print("💡 Make sure your GROQ_API_KEY is set in the .env file")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI-powered data analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python -m src.cli interactive data/raw/test_data.xlsx
  
  # Batch mode
  python -m src.cli batch data/raw/test_data.xlsx queries/queries.txt
  
  # With specific model
  python -m src.cli interactive data/raw/test_data.xlsx --model small
        """
    )
    
    subparsers = parser.add_subparsers(dest='mode', help='Analysis mode')
    
    # Interactive mode
    interactive_parser = subparsers.add_parser('interactive', help='Interactive analysis mode')
    interactive_parser.add_argument('data_file', type=Path, help='Path to Excel file')
    interactive_parser.add_argument('--model', choices=['small', 'large'], default='large', 
                                  help='AI model to use (default: large)')
    
    # Batch mode
    batch_parser = subparsers.add_parser('batch', help='Batch testing mode')
    batch_parser.add_argument('data_file', type=Path, help='Path to Excel file')
    batch_parser.add_argument('queries_file', type=Path, help='Path to queries file')
    batch_parser.add_argument('--model', choices=['small', 'large'], default='large',
                             help='AI model to use (default: large)')
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        return
    
    # Validate file paths
    if not args.data_file.exists():
        print(f"❌ Data file not found: {args.data_file}")
        return
    
    if args.mode == 'batch' and not args.queries_file.exists():
        print(f"❌ Queries file not found: {args.queries_file}")
        return
    
    # Run the appropriate mode
    if args.mode == 'interactive':
        interactive_mode(args.data_file, args.model)
    elif args.mode == 'batch':
        batch_mode(args.data_file, args.queries_file, args.model)


if __name__ == "__main__":
    main()