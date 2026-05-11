"""
Data Loading Module for IRAS-SDLC
Handles Big-Vul, NVD, Devign, and Juliet datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class DatasetLoader:
    """Unified dataset loader for IRAS-SDLC experiments"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize dataset loader
        
        Args:
            data_dir: Base directory containing datasets
        """
        self.data_dir = Path(data_dir)
        
    def load_bigvul(self, nrows: Optional[int] = None) -> pd.DataFrame:
        """
        Load Big-Vul dataset for vulnerability detection
        
        Args:
            nrows: Number of rows to load (None = all)
            
        Returns:
            DataFrame with columns: func_before, vul, project, commit_id, CWE ID, CVE ID, Score
        """
        file_path = self.data_dir / "bigvul_clean_for_transformer.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(
                f"Big-Vul dataset not found at {file_path}\n"
                "Download from: https://github.com/ZeoVan/MSR_20_Code_vulnerability_CSV_Dataset"
            )
        
        df = pd.read_csv(file_path, nrows=nrows)
        print(f"✓ Loaded Big-Vul: {len(df):,} samples")
        print(f"  Columns: {df.columns.tolist()}")
        print(f"  Vulnerable: {df['vul'].sum():,} ({df['vul'].mean()*100:.1f}%)")
        
        return df
    
    def load_nvd(self, year_start: int = 2010, year_end: int = 2026) -> pd.DataFrame:
        """
        Load National Vulnerability Database (NVD) with CVSS metrics
        
        Args:
            year_start: Start year filter
            year_end: End year filter
            
        Returns:
            DataFrame with CVSS exploitability and impact scores
        """
        file_path = self.data_dir / "nvd_master_2010_2026.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(
                f"NVD dataset not found at {file_path}\n"
                "Download from: https://nvd.nist.gov/"
            )
        
        df = pd.read_csv(file_path)
        
        # Filter by year
        if 'Year' in df.columns:
            df = df[(df['Year'] >= year_start) & (df['Year'] <= year_end)]
        
        print(f"✓ Loaded NVD: {len(df):,} CVE records ({year_start}-{year_end})")
        print(f"  Columns: {df.columns.tolist()}")
        
        return df
    
    def load_devign(self, nrows: Optional[int] = None) -> pd.DataFrame:
        """
        Load Devign dataset for graph-based analysis
        
        Args:
            nrows: Number of rows to load (None = all)
            
        Returns:
            DataFrame with code and label columns
        """
        file_path = self.data_dir / "devign_master.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(
                f"Devign dataset not found at {file_path}\n"
                "Download from: https://github.com/epicosy/devign"
            )
        
        df = pd.read_csv(file_path, nrows=nrows)
        print(f"✓ Loaded Devign: {len(df):,} samples")
        
        return df
    
    def load_juliet_c(self, nrows: Optional[int] = None) -> pd.DataFrame:
        """Load Juliet Test Suite - C/C++ (function-level)"""
        file_path = self.data_dir / "juliet_c_function_level.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(
                f"Juliet-C dataset not found at {file_path}\n"
                "Download from: https://samate.nist.gov/SARD/test-suites"
            )
        
        df = pd.read_csv(file_path, nrows=nrows)
        print(f"✓ Loaded Juliet-C: {len(df):,} samples")
        
        return df
    
    def load_juliet_java(self, nrows: Optional[int] = None) -> pd.DataFrame:
        """Load Juliet Test Suite - Java (file-level)"""
        file_path = self.data_dir / "juliet_java_file_level.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(
                f"Juliet-Java dataset not found at {file_path}\n"
                "Download from: https://samate.nist.gov/SARD/test-suites"
            )
        
        df = pd.read_csv(file_path, nrows=nrows)
        print(f"✓ Loaded Juliet-Java: {len(df):,} samples")
        
        return df
    
    def merge_bigvul_nvd(self) -> pd.DataFrame:
        """
        Merge Big-Vul with NVD to get V, E, I components
        
        Returns:
            Merged DataFrame with func_before, vul, Exploitability_Score, Impact_Score
        """
        bigvul = self.load_bigvul()
        nvd = self.load_nvd()
        
        # Clean CVE IDs
        bigvul['CVE ID'] = bigvul['CVE ID'].astype(str).str.strip()
        nvd['CVE_ID'] = nvd['CVE_ID'].astype(str).str.strip()
        
        # Merge
        merged = bigvul.merge(
            nvd,
            left_on='CVE ID',
            right_on='CVE_ID',
            how='inner'
        )
        
        print(f"\n✓ Merged Big-Vul + NVD: {len(merged):,} samples")
        print(f"  Matched CVEs: {merged['CVE ID'].nunique():,}")
        
        return merged


# Example usage
if __name__ == "__main__":
    loader = DatasetLoader()
    
    # Load individual datasets
    bigvul = loader.load_bigvul(nrows=1000)
    nvd = loader.load_nvd()
    
    # Merge for IRAS
    merged = loader.merge_bigvul_nvd()
    print(f"\nSample columns: {merged.columns.tolist()}")
