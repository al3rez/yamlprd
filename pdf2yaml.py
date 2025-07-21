#!/usr/bin/env python3
"""
Convert PDF PRDs to YAML format using pdf2markdown4llm
"""

import argparse
import sys
from pathlib import Path
from pdf2markdown4llm import PDF2Markdown4LLM


def progress_callback(progress):
    """Callback function to handle progress"""
    print(f"\rPhase: {progress.phase.value}, Page {progress.current_page}/{progress.total_pages}, Progress: {progress.percentage:.1f}%", end="", flush=True)
    if progress.percentage >= 100:
        print()  # New line when complete


def pdf_to_markdown(pdf_path, remove_headers=False, skip_empty_tables=True):
    """Convert PDF to Markdown"""
    converter = PDF2Markdown4LLM(
        remove_headers=remove_headers,
        skip_empty_tables=skip_empty_tables,
        table_header="### Table",
        progress_callback=progress_callback
    )
    
    print(f"Converting {pdf_path} to Markdown...")
    markdown_content = converter.convert(str(pdf_path))
    return markdown_content


def markdown_to_yaml_template(markdown_content):
    """Convert Markdown to YAML PRD template"""
    yaml_template = """# YAML PRD - Generated from PDF
# Review and edit this template to match your needs

prd:
  title: "TODO: Extract title from document"
  purpose: "TODO: Extract purpose/objective from document"
  
  features:
    # TODO: Extract user stories/features from the markdown content
    - id: F1
      user_story: "As a [user], I can [action] so that [benefit]"
    - id: F2
      user_story: "..."
  
  metrics:
    # TODO: Extract success metrics/KPIs
    - metric: Metric_Name
      target: "Target value"
  
  constraints:
    # TODO: Extract constraints, limitations, and requirements
    - "Constraint 1"
    - "Constraint 2"

# Optional sections (uncomment as needed):
# technical_specs:
#   api:
#     - endpoint: /api/v1/resource
#       method: POST
#   database:
#     table_name:
#       column: type
# 
# dependencies:
#   - name: service_name
#     version: ">=1.0"
# 
# testing:
#   coverage: 80
#   scenarios:
#     - name: scenario_name

# === Original Markdown Content ===
# Use this content to fill in the YAML structure above
---
{}
""".format(markdown_content)
    
    return yaml_template


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF PRDs to YAML format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdf2yaml input.pdf                    # Convert to input.yaml
  pdf2yaml input.pdf -o output.yaml     # Specify output file
  pdf2yaml input.pdf -m                 # Save markdown only
  pdf2yaml input.pdf --keep-headers     # Keep PDF headers/footers
        """
    )
    
    parser.add_argument("pdf_file", help="Path to input PDF file")
    parser.add_argument("-o", "--output", help="Output file path (default: input_name.yaml)")
    parser.add_argument("-m", "--markdown-only", action="store_true", 
                        help="Output markdown only without YAML template")
    parser.add_argument("--keep-headers", action="store_true",
                        help="Keep PDF headers and footers")
    parser.add_argument("--include-empty-tables", action="store_true",
                        help="Include empty tables in output")
    
    args = parser.parse_args()
    
    # Validate input file
    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"Error: File '{pdf_path}' not found")
        sys.exit(1)
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"Error: File '{pdf_path}' is not a PDF")
        sys.exit(1)
    
    # Determine output file
    if args.output:
        output_path = Path(args.output)
    else:
        suffix = ".md" if args.markdown_only else ".yaml"
        output_path = pdf_path.with_suffix(suffix)
    
    try:
        # Convert PDF to Markdown
        markdown_content = pdf_to_markdown(
            pdf_path,
            remove_headers=not args.keep_headers,
            skip_empty_tables=not args.include_empty_tables
        )
        
        # Generate output
        if args.markdown_only:
            output_content = markdown_content
            print(f"\nMarkdown saved to: {output_path}")
        else:
            output_content = markdown_to_yaml_template(markdown_content)
            print(f"\nYAML PRD template saved to: {output_path}")
            print("\nNext steps:")
            print("1. Open the YAML file and review the generated template")
            print("2. Extract relevant information from the markdown section")
            print("3. Fill in the TODO sections with actual content")
            print("4. Remove the markdown section once extraction is complete")
        
        # Save to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_content)
        
    except Exception as e:
        print(f"\nError converting PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()