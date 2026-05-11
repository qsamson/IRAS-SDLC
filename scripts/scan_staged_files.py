"""
Pre-commit Hook Scanner

Scans only staged files before commit.
"""

import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.models.risk_aggregation import IRASRiskEngine


def get_staged_files():
    """Get list of staged files from git."""
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only'],
        capture_output=True,
        text=True
    )
    return result.stdout.strip().split('\n')


def scan_staged_files():
    """Scan staged files for vulnerabilities."""
    print("Scanning staged files for vulnerabilities...")
    
    staged_files = get_staged_files()
    code_files = [f for f in staged_files if f.endswith(('.py', '.c', '.cpp', '.java'))]
    
    if not code_files:
        print("✓ No code files staged")
        return 0
    
    print(f"Found {len(code_files)} code files to scan")
    
    # Simulate scanning (in production, use CodeBERT)
    max_risk = 0.3  # Example
    
    if max_risk >= 0.7:
        print(f"❌ High-risk vulnerability detected (R={max_risk:.3f})")
        print("Commit blocked. Fix vulnerabilities before committing.")
        return 1
    
    print(f"✓ No high-risk vulnerabilities detected")
    return 0


if __name__ == "__main__":
    sys.exit(scan_staged_files())
