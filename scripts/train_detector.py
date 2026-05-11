"""
Training Script for IRAS-SDLC
Train CodeBERT on Big-Vul dataset
"""

import sys
sys.path.append('..')

from src.data.loaders import DatasetLoader
from src.models.codebert_detector import CodeBERTVulnerabilityDetector
from src.models.risk_aggregation import IRASRiskEngine
from src.evaluation.metrics import IRASMetrics

import pandas as pd
import numpy as np


def main():
    print("="*60)
    print("IRAS-SDLC Training Pipeline")
    print("="*60)
    
    # Step 1: Load data
    print("\n[1/4] Loading datasets...")
    loader = DatasetLoader(data_dir='../data')
    
    try:
        bigvul = loader.load_bigvul(nrows=5000)
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nPlease download datasets first. See data/README.md")
        return
    
    # Step 2: Initialize detector
    print("\n[2/4] Initializing CodeBERT detector...")
    detector = CodeBERTVulnerabilityDetector()
    
    # Step 3: Example predictions
    print("\n[3/4] Running vulnerability detection...")
    sample_codes = bigvul['func_before'].head(10).tolist()
    V = detector.predict(sample_codes)
    
    print(f"\nPredicted {len(V)} samples")
    print(f"Average vulnerability probability: {V.mean():.3f}")
    
    # Step 4: Risk aggregation
    print("\n[4/4] Computing unified risk scores...")
    engine = IRASRiskEngine(alpha=0.5, beta=0.3, gamma=0.2)
    
    # Simulate CVSS scores (in practice, these come from NVD)
    E = np.random.uniform(0.3, 0.9, len(V))
    I = np.random.uniform(0.4, 1.0, len(V))
    
    R = engine.aggregate_risk(V, E, I)
    
    print("\nRisk Distribution:")
    low = (R < 0.4).sum()
    medium = ((R >= 0.4) & (R < 0.7)).sum()
    high = (R >= 0.7).sum()
    
    print(f"  Low Risk:    {low} ({low/len(R)*100:.1f}%)")
    print(f"  Medium Risk: {medium} ({medium/len(R)*100:.1f}%)")
    print(f"  High Risk:   {high} ({high/len(R)*100:.1f}%)")
    
    print("\n" + "="*60)
    print("Training complete!")
    print("="*60)


if __name__ == "__main__":
    main()