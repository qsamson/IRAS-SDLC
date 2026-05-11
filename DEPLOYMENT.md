\# IRAS-SDLC Industry Deployment Guide



\## Overview



This guide helps organizations integrate IRAS-SDLC into their Software Development Lifecycle (SDLC) for AI-powered vulnerability detection and risk-based prioritization.



\---



\## Table of Contents



1\. \[Quick Start](#quick-start)

2\. \[Deployment Architecture](#deployment-architecture)

3\. \[Integration Scenarios](#integration-scenarios)

4\. \[Configuration Examples](#configuration-examples)

5\. \[API Integration](#api-integration)

6\. \[Production Checklist](#production-checklist)



\---



\## Quick Start



\### Prerequisites



\- Python 3.8+

\- GPU (optional, recommended for CodeBERT)

\- Access to code repositories (GitHub, GitLab, Bitbucket)

\- (Optional) NVD API key for real-time CVSS data



\### Installation



```bash

┌─────────────────────────────────────────────────────────┐

│                    Development Phase                     │

├─────────────────────────────────────────────────────────┤

│  Code Commit → CodeBERT Scan → V (Vulnerability Score)  │

└────────────────────┬────────────────────────────────────┘

│

┌────────────────────▼────────────────────────────────────┐

│                   CVSS Integration                       │

├─────────────────────────────────────────────────────────┤

│      NVD Database → E (Exploitability) + I (Impact)     │

└────────────────────┬────────────────────────────────────┘

│

┌────────────────────▼────────────────────────────────────┐

│              Risk Aggregation Engine                     │

├─────────────────────────────────────────────────────────┤

│            R = αV + βE + γI                             │

│     (Configurable weights based on org priorities)      │

└────────────────────┬────────────────────────────────────┘

│

┌────────────────────▼────────────────────────────────────┐

│                 Decision Engine                          │

├─────────────────────────────────────────────────────────┤

│  Low (R<0.4)    → Monitor                               │

│  Medium (R<0.7) → Patch in next sprint                  │

│  High (R≥0.7)   → Immediate fix + block deployment      │

└─────────────────────────────────────────────────────────┘



\---



\## Integration Scenarios



\### Scenario 1: \*\*Security-Critical Applications\*\* (Banking, Healthcare)

\*\*Priority: High Impact Prevention\*\*



```python

\# config/security\_critical.py

from src.models.risk\_aggregation import IRASRiskEngine



\# Weight impact heavily

engine = IRASRiskEngine(

&#x20;   alpha=0.3,  # Vulnerability likelihood

&#x20;   beta=0.2,   # Exploitability

&#x20;   gamma=0.5   # IMPACT (highest weight)

)



\# Stricter thresholds

RISK\_THRESHOLDS = {

&#x20;   'low': 0.3,      # Lower threshold

&#x20;   'medium': 0.5,   # More conservative

&#x20;   'high': 0.7

}



\# Block deployment on Medium+ risk

BLOCK\_DEPLOYMENT = \['medium', 'high']

```



\*\*Use Case:\*\* Prevents high-impact vulnerabilities (data breaches, PHI exposure) even if exploitability is low.



\---



\### Scenario 2: \*\*High-Traffic Public Services\*\* (E-commerce, SaaS)

\*\*Priority: Prevent Easy Exploits\*\*



```python

\# config/high\_traffic.py

from src.models.risk\_aggregation import IRASRiskEngine



\# Weight exploitability heavily

engine = IRASRiskEngine(

&#x20;   alpha=0.3,  # Vulnerability likelihood

&#x20;   beta=0.5,   # EXPLOITABILITY (highest weight)

&#x20;   gamma=0.2   # Impact

)



\# Standard thresholds

RISK\_THRESHOLDS = {

&#x20;   'low': 0.4,

&#x20;   'medium': 0.7,

&#x20;   'high': 0.85

}



\# Block only critical exploits

BLOCK\_DEPLOYMENT = \['high']

```



\*\*Use Case:\*\* Focuses on preventing easily exploitable vulnerabilities that attackers target first (SQL injection, XSS, CSRF).



\---



\### Scenario 3: \*\*Balanced Approach\*\* (General Enterprise)

\*\*Priority: Comprehensive Coverage\*\*



```python

\# config/balanced.py

from src.models.risk\_aggregation import IRASRiskEngine



\# Equal weighting

engine = IRASRiskEngine(

&#x20;   alpha=0.4,  # Vulnerability likelihood

&#x20;   beta=0.3,   # Exploitability  

&#x20;   gamma=0.3   # Impact

)



\# Standard RMF-aligned thresholds

RISK\_THRESHOLDS = {

&#x20;   'low': 0.4,

&#x20;   'medium': 0.7,

&#x20;   'high': 0.85

}



BLOCK\_DEPLOYMENT = \['high']

```



\*\*Use Case:\*\* Balances all risk factors for general software projects.



\---



\### Scenario 4: \*\*AI-First Detection\*\* (Early-Stage Startups)

\*\*Priority: Trust ML Model\*\*



```python

\# config/ai\_first.py

from src.models.risk\_aggregation import IRASRiskEngine



\# Heavy CodeBERT reliance

engine = IRASRiskEngine(

&#x20;   alpha=0.7,  # VULNERABILITY LIKELIHOOD (highest)

&#x20;   beta=0.15,  # Exploitability

&#x20;   gamma=0.15  # Impact

)



\# Aggressive ML-based blocking

RISK\_THRESHOLDS = {

&#x20;   'low': 0.5,

&#x20;   'medium': 0.75,

&#x20;   'high': 0.9

}



BLOCK\_DEPLOYMENT = \['high']

```



\*\*Use Case:\*\* Startups without historical CVSS data can rely on CodeBERT's detection.



\---



\## Configuration Examples



\### Example 1: CI/CD Pipeline Integration (GitHub Actions)



Create `.github/workflows/iras-scan.yml`:



```yaml

name: IRAS Vulnerability Scan



on: \[push, pull\_request]



jobs:

&#x20; security-scan:

&#x20;   runs-on: ubuntu-latest

&#x20;   steps:

&#x20;     - uses: actions/checkout@v3

&#x20;     

&#x20;     - name: Set up Python

&#x20;       uses: actions/setup-python@v4

&#x20;       with:

&#x20;         python-version: '3.9'

&#x20;     

&#x20;     - name: Install IRAS-SDLC

&#x20;       run: |

&#x20;         pip install -r requirements.txt

&#x20;     

&#x20;     - name: Run Vulnerability Scan

&#x20;       run: |

&#x20;         python scripts/scan\_repository.py --config config/balanced.py

&#x20;     

&#x20;     - name: Check Risk Threshold

&#x20;       run: |

&#x20;         python scripts/check\_risk.py --threshold high --block-on-fail

```



\---



\### Example 2: Pre-Commit Hook



Create `.git/hooks/pre-commit`:



```bash

\#!/bin/bash

\# IRAS-SDLC Pre-Commit Hook



echo "Running IRAS vulnerability scan..."



python scripts/scan\_staged\_files.py



if \[ $? -ne 0 ]; then

&#x20;   echo "❌ High-risk vulnerability detected. Commit blocked."

&#x20;   echo "Run: python scripts/view\_findings.py"

&#x20;   exit 1

fi



echo "✅ No high-risk vulnerabilities detected."

exit 0

```



\---



\### Example 3: API Integration



```python

\# integration/api\_example.py

from src.models.codebert\_detector import CodeBERTVulnerabilityDetector

from src.models.risk\_aggregation import IRASRiskEngine

import requests



\# Initialize IRAS components

detector = CodeBERTVulnerabilityDetector()

engine = IRASRiskEngine(alpha=0.5, beta=0.3, gamma=0.2)



def scan\_code\_snippet(code: str, cve\_id: str = None):

&#x20;   """

&#x20;   Scan a code snippet and return risk assessment

&#x20;   

&#x20;   Args:

&#x20;       code: Source code to scan

&#x20;       cve\_id: Optional CVE ID to fetch CVSS scores

&#x20;   

&#x20;   Returns:

&#x20;       dict: Risk assessment results

&#x20;   """

&#x20;   # Step 1: Get vulnerability likelihood from CodeBERT

&#x20;   V = detector.predict\_single(code)

&#x20;   

&#x20;   # Step 2: Get CVSS scores (if CVE provided)

&#x20;   if cve\_id:

&#x20;       nvd\_response = requests.get(

&#x20;           f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve\_id}"

&#x20;       )

&#x20;       cvss\_data = nvd\_response.json()

&#x20;       E = cvss\_data\['exploitabilityScore'] / 10.0  # Normalize to \[0,1]

&#x20;       I = cvss\_data\['impactScore'] / 10.0

&#x20;   else:

&#x20;       # Use defaults if no CVE

&#x20;       E = 0.5

&#x20;       I = 0.5

&#x20;   

&#x20;   # Step 3: Aggregate risk

&#x20;   R = engine.aggregate\_risk(V, E, I)

&#x20;   level, action = engine.classify\_risk\_level(R)

&#x20;   

&#x20;   return {

&#x20;       'vulnerability\_likelihood': float(V),

&#x20;       'exploitability': float(E),

&#x20;       'impact': float(I),

&#x20;       'unified\_risk': float(R),

&#x20;       'risk\_level': level,

&#x20;       'recommended\_action': action

&#x20;   }



\# Example usage

vulnerable\_code = """

char buffer\[10];

strcpy(buffer, user\_input);  // Buffer overflow

"""



result = scan\_code\_snippet(vulnerable\_code)

print(result)

```



\---



\## Production Checklist



\### Before Deployment



\- \[ ] \*\*Data Preparation\*\*

&#x20; - \[ ] Download Big-Vul dataset

&#x20; - \[ ] Download NVD data (or set up API access)

&#x20; - \[ ] Prepare organization-specific training data (optional)



\- \[ ] \*\*Model Training\*\*

&#x20; - \[ ] Fine-tune CodeBERT on your codebase (optional)

&#x20; - \[ ] Validate accuracy on test set

&#x20; - \[ ] Save trained model to `models/`



\- \[ ] \*\*Configuration\*\*

&#x20; - \[ ] Choose risk weighting strategy (α, β, γ)

&#x20; - \[ ] Set risk thresholds (low, medium, high)

&#x20; - \[ ] Define deployment blocking rules



\- \[ ] \*\*Integration\*\*

&#x20; - \[ ] Set up CI/CD pipeline hooks

&#x20; - \[ ] Configure pre-commit hooks (optional)

&#x20; - \[ ] Integrate with issue tracking (Jira, GitHub Issues)



\- \[ ] \*\*Testing\*\*

&#x20; - \[ ] Run on historical vulnerabilities

&#x20; - \[ ] Validate false positive rate

&#x20; - \[ ] Test performance on large codebases



\### Monitoring \& Maintenance



\- \[ ] \*\*Runtime Monitoring\*\*

&#x20; - \[ ] Track detection accuracy over time

&#x20; - \[ ] Monitor false positive/negative rates

&#x20; - \[ ] Log all risk assessments for audit



\- \[ ] \*\*Model Updates\*\*

&#x20; - \[ ] Retrain CodeBERT quarterly with new vulnerabilities

&#x20; - \[ ] Update NVD data monthly

&#x20; - \[ ] Adjust risk weights based on incident feedback



\- \[ ] \*\*Compliance\*\*

&#x20; - \[ ] Map to RMF controls (NIST SP 800-53)

&#x20; - \[ ] Document for SOC 2 / ISO 27001 audits

&#x20; - \[ ] Maintain risk assessment logs



\---



\## Support



For deployment assistance:

\- \*\*GitHub Issues\*\*: https://github.com/qsamson/IRAS-SDLC/issues

\- \*\*Email\*\*: squaye@hawk.illinoistech.edu



\---



\## Citation



```bibtex

@article{quaye2026iras,

&#x20; title={IRAS-SDLC: Lifecycle Risk Aggregation for Secure AI-Augmented Software Assurance Under RMF and Zero Trust},

&#x20; author={Quaye, Samson and Dawson, Maurice and Ben Ayed, Ahmed},

&#x20; journal={Systems},

&#x20; year={2026},

&#x20; publisher={MDPI}

}

```

