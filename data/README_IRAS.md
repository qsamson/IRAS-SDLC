# IRAS Dataset

This directory contains the pre-computed IRAS dataset with vulnerability assessments.

## Files

### `iras_dataset.csv`
Pre-computed risk scores from the IRAS-SDLC framework.

**Columns:**
- `V`: Vulnerability likelihood [0, 1] from CodeBERT model
- `E`: Exploitability score [0, 1] from CVSS metrics
- `I`: Impact score [0, 1] from CVSS metrics
- `R`: Unified risk score = αV + βE + γI

**Sample:**
```csv
V,E,I,R
0.022350114,0.12235011,0.22235012,0.00060802506
0.90982693,1.0,1.0,0.90982693
0.017475989,0.11747599,0.217476,0.0004464802
```

**Usage:**
```python
import pandas as pd

# Load IRAS dataset
df = pd.read_csv('data/iras_dataset.csv')

# Filter high-risk samples
high_risk = df[df['R'] >= 0.7]
print(f"High-risk vulnerabilities: {len(high_risk)}")
```

## Additional Datasets (Not Included)

For full reproducibility, download these datasets separately:

1. **Big-Vul** - Training data for CodeBERT
2. **NVD** - CVSS scores for E and I
3. **Devign** - Graph-based validation
4. **Juliet** - Cross-domain testing

See main `data/README.md` for download instructions.
