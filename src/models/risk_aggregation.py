"""IRAS-SDLC Risk Aggregation Engine"""
import numpy as np

class IRASRiskEngine:
    def __init__(self, alpha=0.5, beta=0.3, gamma=0.2):
        if not np.isclose(alpha + beta + gamma, 1.0):
            raise ValueError("Weights must sum to 1.0")
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
    
    def aggregate_risk(self, V, E, I):
        return self.alpha * V + self.beta * E + self.gamma * I
    
    def classify_risk_level(self, R):
        if R < 0.4:
            return "Low", "Monitor"
        elif R < 0.7:
            return "Medium", "Patch/Mitigate"
        else:
            return "High", "Immediate Fix"