"""
Quick Test for IRAS-SDLC
Tests core functionality without requiring datasets
"""

import sys
import numpy as np

print("="*60)
print("Testing IRAS-SDLC Components")
print("="*60)

# Test 1: Risk Aggregation Engine
print("\n[Test 1] Risk Aggregation Engine...")
try:
    from src.models.risk_aggregation import IRASRiskEngine
    
    engine = IRASRiskEngine(alpha=0.5, beta=0.3, gamma=0.2)
    
    # Test case
    V = 0.95  # High vulnerability likelihood
    E = 0.70  # Moderate exploitability
    I = 0.80  # High impact
    
    R = engine.aggregate_risk(V, E, I)
    level, action = engine.classify_risk_level(R)
    
    print(f"  V={V:.2f}, E={E:.2f}, I={I:.2f}")
    print(f"  R={R:.3f} → {level} → {action}")
    print("  ✓ PASSED")
    
except Exception as e:
    print(f"  ✗ FAILED: {e}")

# Test 2: Evaluation Metrics
print("\n[Test 2] Evaluation Metrics...")
try:
    from src.evaluation.metrics import IRASMetrics
    
    metrics_calc = IRASMetrics()
    
    y_true = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 1])
    y_pred = np.array([1, 0, 1, 0, 0, 1, 0, 1, 1, 1])
    y_prob = np.array([0.9, 0.1, 0.85, 0.6, 0.2, 0.95, 0.15, 0.55, 0.88, 0.92])
    
    metrics = metrics_calc.compute_classification_metrics(y_true, y_pred, y_prob)
    
    print(f"  Accuracy: {metrics['accuracy']:.3f}")
    print(f"  Precision: {metrics['precision']:.3f}")
    print(f"  Recall: {metrics['recall']:.3f}")
    print(f"  F1: {metrics['f1']:.3f}")
    print("  ✓ PASSED")
    
except Exception as e:
    print(f"  ✗ FAILED: {e}")

# Test 3: Data Loader (structure only)
print("\n[Test 3] Data Loader Structure...")
try:
    from src.data.loaders import DatasetLoader
    
    loader = DatasetLoader(data_dir='data')
    print("  DatasetLoader initialized")
    print("  ✓ PASSED")
    
except Exception as e:
    print(f"  ✗ FAILED: {e}")

print("\n" + "="*60)
print("All Core Tests Complete!")
print("="*60)
print("\nNext Steps:")
print("1. Download datasets (see data/README.md)")
print("2. Install dependencies: pip install -r requirements.txt")
print("3. Run: python scripts/train_detector.py")