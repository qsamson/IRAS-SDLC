\# Dataset Instructions for IRAS-SDLC



This directory contains the datasets used in the paper. Due to size constraints, most datasets must be downloaded separately.



\---



\## ✅ Included Dataset



\### `iras\_dataset.csv` (Included in Repository)

\- \*\*Size\*\*: 37,729 samples, 1.62 MB

\- \*\*Purpose\*\*: Pre-computed IRAS risk scores for validation and testing

\- \*\*Columns\*\*:

&#x20; - `V`: Vulnerability likelihood \[0, 1] from CodeBERT

&#x20; - `E`: Exploitability score \[0, 1] from CVSS

&#x20; - `I`: Impact score \[0, 1] from CVSS

&#x20; - `R`: Unified risk score = αV + βE + γI

\- \*\*Usage\*\*: Ready to use for reproducing paper results



```python

import pandas as pd

df = pd.read\_csv('data/iras\_dataset.csv')

print(f"Loaded {len(df):,} samples")

```



\---



\## 📥 External Datasets (Download Required)



\### 1. Big-Vul

\*\*Purpose\*\*: Training and testing CodeBERT vulnerability detection model



\- \*\*Source\*\*: https://github.com/ZeoVan/MSR\_20\_Code\_vulnerability\_CSV\_Dataset

\- \*\*Paper\*\*: "A C/C++ Code Vulnerability Dataset with Code Changes and CVE Summaries" (MSR 2020)

\- \*\*File\*\*: `bigvul\_clean\_for\_transformer.csv`

\- \*\*Size\*\*: \~188,000 function-level samples

\- \*\*Version\*\*: Latest commit as of 2024-01-15



\*\*Download Instructions:\*\*

```bash

cd data/

wget https://github.com/ZeoVan/MSR\_20\_Code\_vulnerability\_CSV\_Dataset/raw/master/bigvul\_clean\_for\_transformer.csv

```



\*\*Expected Columns:\*\*

\- `func\_before`: Source code before fix

\- `vul`: Binary label (1 = vulnerable, 0 = secure)

\- `project`: Repository name

\- `commit\_id`: Git commit hash

\- `CWE ID`: Common Weakness Enumeration identifier

\- `CVE ID`: Common Vulnerabilities and Exposures identifier



\---



\### 2. National Vulnerability Database (NVD)

\*\*Purpose\*\*: CVSS exploitability and impact scores (E and I components)



\- \*\*Source\*\*: https://nvd.nist.gov/

\- \*\*API Documentation\*\*: https://nvd.nist.gov/developers/vulnerabilities

\- \*\*File\*\*: `nvd\_master\_2010\_2026.csv` (aggregated from API)

\- \*\*Coverage\*\*: CVE records from 2010-2026

\- \*\*Version\*\*: Downloaded 2024-12-15



\*\*Download Instructions:\*\*

```bash

\# Option 1: Use NVD API (requires API key)

\# Register at: https://nvd.nist.gov/developers/request-an-api-key



\# Option 2: Use our aggregation script

cd scripts/

python download\_nvd\_data.py --start-year 2010 --end-year 2026

```



\*\*Expected Columns:\*\*

\- `CVE\_ID`: CVE identifier

\- `Year`: Publication year

\- `Exploitability\_Score`: CVSS exploitability \[0, 10]

\- `Impact\_Score`: CVSS impact \[0, 10]

\- `Base\_Score`: Overall CVSS score

\- `Severity`: Low/Medium/High/Critical



\*\*Preprocessing\*\*: Normalize scores to \[0, 1] by dividing by 10.0



\---



\### 3. Devign

\*\*Purpose\*\*: Graph-based structural analysis and cross-validation



\- \*\*Source\*\*: https://github.com/epicosy/devign

\- \*\*Paper\*\*: "Devign: Effective Vulnerability Identification by Learning Comprehensive Program Semantics" (NeurIPS 2019)

\- \*\*File\*\*: `devign\_master.csv`

\- \*\*Size\*\*: \~27,000 C functions from QEMU and FFmpeg

\- \*\*Version\*\*: v1.0 (2019-10-01)



\*\*Download Instructions:\*\*

```bash

cd data/

git clone https://github.com/epicosy/devign.git

cp devign/data/devign\_master.csv .

rm -rf devign/  # Remove repo after extracting data

```



\*\*Expected Columns:\*\*

\- `func`: Source code function

\- `target`: Binary label (0 = secure, 1 = vulnerable)

\- `project`: QEMU or FFmpeg



\---



\### 4. Juliet Test Suite (C/C++)

\*\*Purpose\*\*: Cross-domain validation with synthetic test cases



\- \*\*Source\*\*: https://samate.nist.gov/SARD/test-suites/112

\- \*\*Paper\*\*: NIST Software Assurance Reference Dataset (SARD)

\- \*\*File\*\*: `juliet\_c\_function\_level.csv` (preprocessed)

\- \*\*Size\*\*: \~60,000 test cases

\- \*\*Version\*\*: Juliet 1.3 (2017-10-01)



\*\*Download Instructions:\*\*

1\. Download Juliet C/C++ 1.3 from NIST SARD

2\. Extract test cases

3\. Use our preprocessing script:



```bash

cd scripts/

python preprocess\_juliet\_c.py --input /path/to/juliet/ --output ../data/juliet\_c\_function\_level.csv

```



\*\*Expected Columns:\*\*

\- `func`: C/C++ function code

\- `cwe`: CWE identifier

\- `label`: 0 (good) or 1 (bad)



\---



\### 5. Juliet Test Suite (Java)

\*\*Purpose\*\*: Cross-language validation



\- \*\*Source\*\*: https://samate.nist.gov/SARD/test-suites/113

\- \*\*File\*\*: `juliet\_java\_file\_level.csv` (preprocessed)

\- \*\*Size\*\*: \~20,000 test cases

\- \*\*Version\*\*: Juliet 1.3 (2017-10-01)



\*\*Download Instructions:\*\*

Same as Juliet C/C++, but use:

```bash

python preprocess\_juliet\_java.py --input /path/to/juliet-java/ --output ../data/juliet\_java\_file\_level.csv

```



\---



\## 📊 Data Splits \& Reproducibility



\### Train/Validation/Test Split

\- \*\*Big-Vul\*\*: 70% train, 15% validation, 15% test

\- \*\*Random Seed\*\*: 42 (for reproducibility)

\- \*\*Stratification\*\*: Balanced by vulnerability label



```python

from sklearn.model\_selection import train\_test\_split



\# Split Big-Vul

train\_df, temp\_df = train\_test\_split(

&#x20;   bigvul\_df, test\_size=0.3, random\_state=42, stratify=bigvul\_df\['vul']

)

val\_df, test\_df = train\_test\_split(

&#x20;   temp\_df, test\_size=0.5, random\_state=42, stratify=temp\_df\['vul']

)

```



\### Preprocessing Steps

1\. \*\*Text Cleaning\*\*: Remove non-ASCII characters, normalize whitespace

2\. \*\*Code Tokenization\*\*: Use CodeBERT tokenizer (max length: 512)

3\. \*\*CVSS Normalization\*\*: Divide by 10.0 to get \[0, 1] range

4\. \*\*Deduplication\*\*: Remove duplicate functions by hash



\### Expected Outputs

After downloading and preprocessing all datasets, you should have:

data/

├── iras\_dataset.csv                 (37,729 samples) ✓ Included

├── bigvul\_clean\_for\_transformer.csv (188,636 samples)

├── nvd\_master\_2010\_2026.csv         (245,382 CVEs)

├── devign\_master.csv                (27,318 samples)

├── juliet\_c\_function\_level.csv      (61,387 samples)

└── juliet\_java\_file\_level.csv       (28,745 samples)



\---



\## 🔄 Quick Setup Script



Run this to download and preprocess all datasets:



```bash

cd scripts/

python setup\_datasets.py --download --preprocess

```



This will:

1\. Download Big-Vul and Devign

2\. Fetch NVD data via API

3\. Download and preprocess Juliet test suites

4\. Validate data integrity

5\. Create train/val/test splits



\*\*Estimated time\*\*: 30-60 minutes depending on network speed



\---



\## ❓ Troubleshooting



\*\*Q: "NVD API rate limit exceeded"\*\*  

A: The NVD API allows 5 requests per 30 seconds without a key, or 50 requests per 30 seconds with a key. Use `--api-key YOUR\_KEY` when running the download script.



\*\*Q: "Big-Vul download fails"\*\*  

A: The file is large (\~500MB). Try using `git clone` instead of `wget`, or download manually from the GitHub releases page.



\*\*Q: "Juliet preprocessing is slow"\*\*  

A: Juliet has 60K+ test cases. The preprocessing script shows a progress bar. Expect 10-15 minutes on a modern CPU.



\---



\## 📖 Citation



If you use these datasets, please cite the original papers:



\*\*Big-Vul:\*\*

```bibtex

@inproceedings{fan2020msr,

&#x20; title={A C/C++ Code Vulnerability Dataset with Code Changes and CVE Summaries},

&#x20; author={Fan, Jiahao and Li, Yi and Wang, Shaohua and Nguyen, Tien N},

&#x20; booktitle={MSR},

&#x20; year={2020}

}

```



\*\*NVD:\*\* Maintained by NIST - https://nvd.nist.gov/general/faq



\*\*Devign:\*\*

```bibtex

@inproceedings{zhou2019devign,

&#x20; title={Devign: Effective Vulnerability Identification by Learning Comprehensive Program Semantics},

&#x20; author={Zhou, Yaqin and Liu, Shangqing and Siow, Jingkai and Du, Xiaoning and Liu, Yang},

&#x20; booktitle={NeurIPS},

&#x20; year={2019}

}

```



\*\*Juliet:\*\* NIST SARD - https://samate.nist.gov/SARD/

