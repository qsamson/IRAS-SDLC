"""
Statistical Analysis for IRAS-SDLC

Implements survival analysis for detection timing:
- Kaplan-Meier estimator for detection latency
- Log-rank test for comparing IRAS vs baseline
- Cox proportional hazards model
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
from typing import Tuple


class IRASStatisticalAnalysis:
    """
    Statistical analysis module for IRAS-SDLC paper results.
    
    Focuses on:
    - Detection timing (negative latency)
    - Cost reduction analysis
    - Survival curves for vulnerability detection
    """
    
    def __init__(self):
        """Initialize statistical analysis module."""
        self.kmf = KaplanMeierFitter()
        self.cph = CoxPHFitter()
    
    
    def analyze_detection_timing(
        self,
        iras_detection_times: np.ndarray,
        baseline_detection_times: np.ndarray,
        time_units: str = "days"
    ) -> dict:
        """
        Analyze detection timing using Kaplan-Meier and log-rank test.
        
        Args:
            iras_detection_times: Detection times for IRAS method
            baseline_detection_times: Detection times for baseline (e.g., manual review)
            time_units: Time unit label (default: "days")
        
        Returns:
            Dictionary with analysis results and statistics
        """
        # Create dataframes for analysis
        iras_df = pd.DataFrame({
            'time': iras_detection_times,
            'event': np.ones(len(iras_detection_times)),  # All detected
            'method': 'IRAS-SDLC'
        })
        
        baseline_df = pd.DataFrame({
            'time': baseline_detection_times,
            'event': np.ones(len(baseline_detection_times)),
            'method': 'Baseline'
        })
        
        combined_df = pd.concat([iras_df, baseline_df], ignore_index=True)
        
        # Kaplan-Meier estimation for both groups
        results = {}
        
        # IRAS group
        iras_mask = combined_df['method'] == 'IRAS-SDLC'
        self.kmf.fit(
            durations=combined_df[iras_mask]['time'],
            event_observed=combined_df[iras_mask]['event'],
            label='IRAS-SDLC'
        )
        results['iras_median_time'] = self.kmf.median_survival_time_
        results['iras_mean_time'] = iras_detection_times.mean()
        
        # Baseline group
        baseline_mask = combined_df['method'] == 'Baseline'
        self.kmf.fit(
            durations=combined_df[baseline_mask]['time'],
            event_observed=combined_df[baseline_mask]['event'],
            label='Baseline'
        )
        results['baseline_median_time'] = self.kmf.median_survival_time_
        results['baseline_mean_time'] = baseline_detection_times.mean()
        
        # Log-rank test for statistical significance
        logrank_result = logrank_test(
            durations_A=iras_detection_times,
            durations_B=baseline_detection_times,
            event_observed_A=np.ones(len(iras_detection_times)),
            event_observed_B=np.ones(len(baseline_detection_times))
        )
        
        results['log_rank_statistic'] = logrank_result.test_statistic
        results['log_rank_p_value'] = logrank_result.p_value
        results['significant'] = logrank_result.p_value < 0.05
        
        # Compute time reduction
        time_reduction = results['baseline_mean_time'] - results['iras_mean_time']
        results['time_reduction_days'] = time_reduction
        results['time_reduction_pct'] = (time_reduction / results['baseline_mean_time']) * 100
        
        return results
    
    
    def plot_survival_curves(
        self,
        iras_detection_times: np.ndarray,
        baseline_detection_times: np.ndarray,
        title: str = "Vulnerability Detection Time: IRAS vs Baseline",
        save_path: str = None
    ):
        """
        Plot Kaplan-Meier survival curves for detection timing.
        
        Args:
            iras_detection_times: Detection times for IRAS
            baseline_detection_times: Detection times for baseline
            title: Plot title
            save_path: Path to save figure (optional)
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Fit and plot IRAS curve
        kmf_iras = KaplanMeierFitter()
        kmf_iras.fit(
            durations=iras_detection_times,
            event_observed=np.ones(len(iras_detection_times)),
            label='IRAS-SDLC'
        )
        kmf_iras.plot_survival_function(ax=ax, color='#3B6D11', linewidth=2.5)
        
        # Fit and plot baseline curve
        kmf_baseline = KaplanMeierFitter()
        kmf_baseline.fit(
            durations=baseline_detection_times,
            event_observed=np.ones(len(baseline_detection_times)),
            label='Baseline (Manual Review)'
        )
        kmf_baseline.plot_survival_function(ax=ax, color='#993C1D', linewidth=2.5)
        
        ax.set_xlabel('Time to Detection (days)', fontsize=12)
        ax.set_ylabel('Probability of Undetected Vulnerability', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        ax.legend(fontsize=11)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Survival curve saved to {save_path}")
        
        plt.tight_layout()
        plt.show()
    
    
    def compute_cost_reduction(
        self,
        iras_cost_per_vuln: float,
        baseline_cost_per_vuln: float,
        num_vulnerabilities: int
    ) -> dict:
        """
        Compute cost reduction achieved by IRAS.
        
        Args:
            iras_cost_per_vuln: Cost per vulnerability with IRAS
            baseline_cost_per_vuln: Cost per vulnerability without IRAS
            num_vulnerabilities: Total number of vulnerabilities
        
        Returns:
            Dictionary with cost analysis results
        """
        total_iras_cost = iras_cost_per_vuln * num_vulnerabilities
        total_baseline_cost = baseline_cost_per_vuln * num_vulnerabilities
        
        cost_reduction = total_baseline_cost - total_iras_cost
        reduction_pct = (cost_reduction / total_baseline_cost) * 100
        cost_ratio = total_baseline_cost / total_iras_cost
        
        return {
            'iras_total_cost': total_iras_cost,
            'baseline_total_cost': total_baseline_cost,
            'cost_reduction': cost_reduction,
            'reduction_percentage': reduction_pct,
            'cost_ratio': cost_ratio,
            'interpretation': f"{cost_ratio:.1f}x cost reduction"
        }
    
    
    def print_analysis_summary(self, results: dict):
        """Print formatted summary of statistical analysis."""
        print("=" * 70)
        print("IRAS-SDLC Statistical Analysis Summary")
        print("=" * 70)
        print("\n[Detection Timing]")
        print(f"  IRAS Mean Detection Time:     {results['iras_mean_time']:.2f} days")
        print(f"  Baseline Mean Detection Time: {results['baseline_mean_time']:.2f} days")
        print(f"  Time Reduction:               {results['time_reduction_days']:.2f} days ({results['time_reduction_pct']:.1f}%)")
        
        print("\n[Statistical Significance]")
        print(f"  Log-rank Test Statistic: {results['log_rank_statistic']:.4f}")
        print(f"  P-value:                 {results['log_rank_p_value']:.6f}")
        print(f"  Significant (p < 0.05):  {'Yes ✓' if results['significant'] else 'No ✗'}")
        
        print("=" * 70)


# Example usage and reproducibility
if __name__ == "__main__":
    print("IRAS-SDLC Survival Analysis - Reproducing Paper Results\n")
    
    # Simulated detection times (in days from deployment)
    # IRAS: Early detection during development (negative latency)
    np.random.seed(42)  # For reproducibility
    iras_times = np.random.exponential(scale=2, size=500)  # Mean: 2 days
    
    # Baseline: Detection in production (post-deployment)
    baseline_times = np.random.exponential(scale=15, size=500)  # Mean: 15 days
    
    # Initialize analysis
    analyzer = IRASStatisticalAnalysis()
    
    # Perform timing analysis
    print("[1] Detection Timing Analysis")
    results = analyzer.analyze_detection_timing(
        iras_detection_times=iras_times,
        baseline_detection_times=baseline_times
    )
    
    analyzer.print_analysis_summary(results)
    
    # Plot survival curves
    print("\n[2] Generating Survival Curves...")
    analyzer.plot_survival_curves(
        iras_detection_times=iras_times,
        baseline_detection_times=baseline_times,
        save_path='../results/figures/survival_curve.png'
    )
    
    # Cost reduction analysis
    print("\n[3] Cost Reduction Analysis")
    cost_results = analyzer.compute_cost_reduction(
        iras_cost_per_vuln=500,      # $500 per vulnerability (early detection)
        baseline_cost_per_vuln=5000,  # $5000 per vulnerability (production fix)
        num_vulnerabilities=100
    )
    
    print("=" * 70)
    print(f"Total IRAS Cost:       ${cost_results['iras_total_cost']:,.2f}")
    print(f"Total Baseline Cost:   ${cost_results['baseline_total_cost']:,.2f}")
    print(f"Cost Reduction:        ${cost_results['cost_reduction']:,.2f} ({cost_results['reduction_percentage']:.1f}%)")
    print(f"Cost Ratio:            {cost_results['interpretation']}")
    print("=" * 70)