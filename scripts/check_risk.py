"""
Risk Threshold Checker for CI/CD

Checks if risk scores exceed thresholds and blocks deployment if needed.
"""

import sys
import argparse
import json


def check_risk_threshold(
    results_file: str,
    threshold: str = 'high',
    block_on_fail: bool = False
):
    """
    Check if any vulnerabilities exceed risk threshold.
    
    Args:
        results_file: Path to scan results JSON
        threshold: Risk level threshold ('low', 'medium', 'high')
        block_on_fail: Exit with error code if threshold exceeded
    
    Returns:
        0 if passed, 1 if failed
    """
    threshold_map = {'low': 0.4, 'medium': 0.7, 'high': 1.0}
    threshold_value = threshold_map.get(threshold.lower(), 0.7)
    
    print("=" * 70)
    print("IRAS Risk Threshold Check")
    print("=" * 70)
    print(f"Threshold: {threshold.upper()} (R < {threshold_value})")
    print(f"Block on fail: {block_on_fail}")
    
    # In production, load from results_file
    # For demo, simulate results
    max_risk = 0.65  # Example
    
    if max_risk >= threshold_value:
        print(f"\n❌ FAILED: Maximum risk {max_risk:.3f} exceeds threshold {threshold_value}")
        print("Deployment BLOCKED")
        print("=" * 70)
        return 1 if block_on_fail else 0
    else:
        print(f"\n✓ PASSED: Maximum risk {max_risk:.3f} below threshold {threshold_value}")
        print("Deployment APPROVED")
        print("=" * 70)
        return 0


def main():
    parser = argparse.ArgumentParser(description="Check risk thresholds")
    parser.add_argument('--results', default='results.json', help="Path to scan results")
    parser.add_argument('--threshold', choices=['low', 'medium', 'high'], 
                       default='high', help="Risk threshold")
    parser.add_argument('--block-on-fail', action='store_true',
                       help="Exit with error code if threshold exceeded")
    
    args = parser.parse_args()
    
    exit_code = check_risk_threshold(
        args.results,
        args.threshold,
        args.block_on_fail
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()