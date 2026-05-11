"""
Repository Scanner for IRAS-SDLC

Scans entire codebase for vulnerabilities and computes risk scores.
Integrates with CI/CD pipelines.
"""

import sys
import os
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.models.codebert_detector import CodeBERTVulnerabilityDetector
from src.models.risk_aggregation import IRASRiskEngine


def scan_repository(
    repo_path: str,
    config_path: str = None,
    extensions: list = None
):
    """
    Scan repository for vulnerabilities.
    
    Args:
        repo_path: Path to repository root
        config_path: Path to configuration file (optional)
        extensions: File extensions to scan (e.g., ['.py', '.c', '.cpp'])
    """
    if extensions is None:
        extensions = ['.c', '.cpp', '.h', '.hpp', '.py', '.java']
    
    print("=" * 70)
    print("IRAS-SDLC Repository Scanner")
    print("=" * 70)
    print(f"Scanning: {repo_path}")
    print(f"Extensions: {extensions}")
    print()
    
    # Find all code files
    code_files = []
    for ext in extensions:
        code_files.extend(Path(repo_path).rglob(f"*{ext}"))
    
    print(f"Found {len(code_files)} code files")
    
    if len(code_files) == 0:
        print("No code files found. Exiting.")
        return
    
    # Initialize detector and risk engine
    print("Loading CodeBERT model...")
    detector = CodeBERTVulnerabilityDetector()
    
    print("Initializing risk engine...")
    engine = IRASRiskEngine(alpha=0.5, beta=0.3, gamma=0.2)
    
    # Scan files
    vulnerabilities = []
    
    print("\nScanning files...")
    for i, file_path in enumerate(code_files[:10], 1):  # Limit to 10 for demo
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            # Predict vulnerability
            V = detector.predict_single(code)
            
            # Simulate CVSS scores (in production, fetch from NVD)
            E = 0.5
            I = 0.5
            
            # Compute risk
            R = engine.aggregate_risk(V, E, I)
            level, action = engine.classify_risk_level(R)
            
            if level in ['Medium', 'High']:
                vulnerabilities.append({
                    'file': str(file_path),
                    'V': V,
                    'E': E,
                    'I': I,
                    'R': R,
                    'level': level,
                    'action': action
                })
            
            print(f"  [{i}/{min(10, len(code_files))}] {file_path.name}: R={R:.3f} ({level})")
        
        except Exception as e:
            print(f"  Error scanning {file_path}: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("Scan Complete")
    print("=" * 70)
    print(f"Files scanned: {min(10, len(code_files))}")
    print(f"Vulnerabilities found: {len(vulnerabilities)}")
    
    if vulnerabilities:
        print("\nHigh-Priority Issues:")
        for vuln in sorted(vulnerabilities, key=lambda x: x['R'], reverse=True)[:5]:
            print(f"  {vuln['file']}")
            print(f"    Risk: {vuln['R']:.3f} ({vuln['level']}) → {vuln['action']}")
    
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Scan repository for vulnerabilities")
    parser.add_argument('repo_path', help="Path to repository")
    parser.add_argument('--config', help="Path to config file")
    parser.add_argument('--extensions', nargs='+', help="File extensions to scan")
    
    args = parser.parse_args()
    
    scan_repository(args.repo_path, args.config, args.extensions)


if __name__ == "__main__":
    main()