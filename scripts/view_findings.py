"""
View IRAS Scan Findings

Display scan results in a formatted report.
"""

import json
import argparse


def view_findings(results_file: str = 'scan_results.json'):
    """Display scan findings in formatted report."""
    print("=" * 70)
    print("IRAS-SDLC Scan Findings Report")
    print("=" * 70)
    
    # In production, load from results_file
    # For demo, show example
    print("\n[High Risk - Immediate Action Required]")
    print("  1. src/auth/login.c")
    print("     Risk: 0.85 | SQL Injection vulnerability")
    print("     Action: Fix immediately before deployment")
    
    print("\n[Medium Risk - Schedule for Next Sprint]")
    print("  2. src/api/handler.py")
    print("     Risk: 0.65 | Missing input validation")
    
    print("\n[Low Risk - Monitor]")
    print("  3. src/utils/parser.c")
    print("     Risk: 0.35 | Potential buffer overflow (low probability)")
    
    print("\n" + "=" * 70)
    print("Total Issues: 3 (1 High, 1 Medium, 1 Low)")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="View scan findings")
    parser.add_argument('--file', default='scan_results.json',
                       help="Path to results file")
    args = parser.parse_args()
    view_findings(args.file)


if __name__ == "__main__":
    main()
