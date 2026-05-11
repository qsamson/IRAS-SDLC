"""
IRAS-SDLC Risk Aggregation Engine

Implements the unified risk formula: R = αV + βE + γI
where:
    V = Vulnerability likelihood (from ML model)
    E = Exploitability score (from CVSS)
    I = Impact score (from CVSS)
    α, β, γ = Configurable weights
"""

import numpy as np
from typing import Union, Tuple


class IRASRiskEngine:
    """
    Lifecycle Risk Aggregation Engine for IRAS-SDLC.
    
    Combines ML-based vulnerability detection with CVSS metrics
    to produce a unified risk score aligned with RMF guidelines.
    """
    
    def __init__(self, alpha: float = 0.5, beta: float = 0.3, gamma: float = 0.2):
        """
        Initialize the risk aggregation engine.
        
        Args:
            alpha: Weight for vulnerability likelihood (default: 0.5)
            beta: Weight for exploitability (default: 0.3)
            gamma: Weight for impact (default: 0.2)
        
        Raises:
            ValueError: If weights do not sum to 1.0
        """
        if not np.isclose(alpha + beta + gamma, 1.0):
            raise ValueError(
                f"Weights must sum to 1.0, got {alpha + beta + gamma}"
            )
        
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
    
    
    def aggregate_risk(
        self, 
        V: Union[float, np.ndarray],
        E: Union[float, np.ndarray],
        I: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        """
        Compute unified lifecycle risk score.
        
        Args:
            V: Vulnerability likelihood ∈ [0, 1] from ML model
            E: Exploitability score ∈ [0, 1] from CVSS
            I: Impact score ∈ [0, 1] from CVSS
        
        Returns:
            R: Aggregated risk score ∈ [0, 1]
        
        Example:
            >>> engine = IRASRiskEngine(alpha=0.5, beta=0.3, gamma=0.2)
            >>> R = engine.aggregate_risk(V=0.9, E=0.7, I=0.8)
            >>> print(f"Risk: {R:.3f}")
            Risk: 0.845
        """
        R = (self.alpha * V + self.beta * E + self.gamma * I)
        return R
    
    
    def classify_risk_level(self, R: float) -> Tuple[str, str]:
        """
        Map risk score to RMF-aligned risk level and recommended action.
        
        Args:
            R: Risk score ∈ [0, 1]
        
        Returns:
            Tuple of (risk_level, recommended_action)
        
        Risk Thresholds:
            - Low (R < 0.4): Monitor only
            - Medium (0.4 ≤ R < 0.7): Patch in next sprint
            - High (R ≥ 0.7): Immediate fix + block deployment
        """
        if R < 0.4:
            return "Low", "Monitor"
        elif R < 0.7:
            return "Medium", "Patch/Mitigate"
        else:
            return "High", "Immediate Fix"


# Example usage
if __name__ == "__main__":
    # Initialize engine with default weights
    engine = IRASRiskEngine(alpha=0.5, beta=0.3, gamma=0.2)
    
    # Example vulnerability
    V = 0.95  # High ML confidence
    E = 0.70  # Moderate exploitability
    I = 0.80  # High impact
    
    # Compute unified risk
    R = engine.aggregate_risk(V, E, I)
    level, action = engine.classify_risk_level(R)
    
    print("="*50)
    print("IRAS-SDLC Risk Assessment Example")
    print("="*50)
    print(f"Vulnerability Likelihood (V): {V:.2f}")
    print(f"Exploitability (E):           {E:.2f}")
    print(f"Impact (I):                   {I:.2f}")
    print(f"Unified Risk Score (R):       {R:.3f}")
    print(f"Risk Level:                   {level}")
    print(f"Recommended Action:           {action}")
    print("="*50)