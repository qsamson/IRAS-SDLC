"""
Evaluation Metrics for IRAS-SDLC
Precision, Recall, F1, AUC-ROC, Cost Reduction
"""

from sklearn.metrics import (
    precision_score, recall_score, f1_score, 
    accuracy_score, roc_auc_score, confusion_matrix
)
import numpy as np
from typing import Dict, Tuple


class IRASMetrics:
    """Comprehensive metrics for vulnerability detection and risk assessment"""
    
    @staticmethod
    def compute_classification_metrics(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: np.ndarray = None
    ) -> Dict[str, float]:
        """
        Compute standard classification metrics
        
        Args:
            y_true: Ground truth labels (0/1)
            y_pred: Predicted labels (0/1)
            y_prob: Predicted probabilities (optional, for AUC)
            
        Returns:
            Dictionary of metrics
        """
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1': f1_score(y_true, y_pred, zero_division=0),
        }
        
        if y_prob is not None:
            metrics['auc_roc'] = roc_auc_score(y_true, y_prob)
        
        return metrics
    
    @staticmethod
    def compute_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, int]:
        """
        Compute confusion matrix components
        
        Returns:
            Dictionary with TP, TN, FP, FN
        """
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        
        return {
            'true_positives': int(tp),
            'true_negatives': int(tn),
            'false_positives': int(fp),
            'false_negatives': int(fn)
        }
    
    @staticmethod
    def compute_cost_reduction(
        baseline_cost: float,
        iras_cost: float
    ) -> Tuple[float, float]:
        """
        Compute cost reduction achieved by IRAS
        
        Args:
            baseline_cost: Cost without IRAS
            iras_cost: Cost with IRAS
            
        Returns:
            (reduction_ratio, percentage_saved)
        """
        reduction = baseline_cost - iras_cost
        ratio = baseline_cost / iras_cost if iras_cost > 0 else float('inf')
        percentage = (reduction / baseline_cost) * 100 if baseline_cost > 0 else 0
        
        return ratio, percentage
    
    @staticmethod
    def print_metrics(metrics: Dict[str, float]):
        """Pretty print metrics"""
        print("\n" + "="*50)
        print("IRAS-SDLC Evaluation Metrics")
        print("="*50)
        
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"{key.replace('_', ' ').title():.<30} {value:.4f}")
            else:
                print(f"{key.replace('_', ' ').title():.<30} {value}")
        
        print("="*50 + "\n")


# Example usage
if __name__ == "__main__":
    # Simulated predictions
    y_true = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 1])
    y_pred = np.array([1, 0, 1, 0, 0, 1, 0, 1, 1, 1])
    y_prob = np.array([0.9, 0.1, 0.85, 0.6, 0.2, 0.95, 0.15, 0.55, 0.88, 0.92])
    
    metrics_calc = IRASMetrics()
    
    # Classification metrics
    metrics = metrics_calc.compute_classification_metrics(y_true, y_pred, y_prob)
    metrics_calc.print_metrics(metrics)
    
    # Confusion matrix
    cm = metrics_calc.compute_confusion_matrix(y_true, y_pred)
    print("Confusion Matrix:")
    print(cm)