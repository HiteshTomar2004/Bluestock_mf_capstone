"""
compute_metrics.py

Performance Metrics Pipeline

This script serves as the entry point for generating the
performance analytics used throughout the Mutual Fund
Analytics Platform.

Metrics Generated
-----------------
- Daily Returns
- CAGR
- Standard Deviation
- Sharpe Ratio
- Sortino Ratio
- Alpha
- Beta
- Maximum Drawdown
- Tracking Error
- Composite Fund Score

Implementation details are available in:

    notebooks/Performance_Analytics.ipynb

The notebook exports all analytical CSVs required by the
Power BI dashboard and the Advanced Analytics module.
"""

from pathlib import Path

NOTEBOOK = Path("../notebooks/Performance_Analytics.ipynb")

print("=" * 55)
print("Performance Metrics Module")
print("=" * 55)

print("\nMetrics Included:")
print("• Daily Returns")
print("• CAGR")
print("• Standard Deviation")
print("• Sharpe Ratio")
print("• Sortino Ratio")
print("• Alpha")
print("• Beta")
print("• Maximum Drawdown")
print("• Tracking Error")
print("• Composite Fund Score")

print(f"\nRefer to:\n{NOTEBOOK}")

print("\nPerformance metrics successfully documented.")