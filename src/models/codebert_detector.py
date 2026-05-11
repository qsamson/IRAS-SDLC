"""
CodeBERT-based Vulnerability Detection Model
Fine-tuned on Big-Vul dataset
"""

import torch
import torch.nn as nn
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from transformers import Trainer, TrainingArguments
from typing import Dict, List, Tuple
import numpy as np


class CodeBERTVulnerabilityDetector:
    """
    CodeBERT model fine-tuned for vulnerability detection
    Binary classification: vulnerable (1) vs. secure (0)
    """
    
    def __init__(self, model_name: str = "microsoft/codebert-base"):
        """
        Initialize CodeBERT detector
        
        Args:
            model_name: Pretrained model identifier
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        # Load tokenizer and model
        self.tokenizer = RobertaTokenizer.from_pretrained(model_name)
        self.model = RobertaForSequenceClassification.from_pretrained(
            model_name,
            num_labels=2
        ).to(self.device)
        
        self.max_length = 512
    
    def tokenize_code(self, code_samples: List[str]) -> Dict:
        """Tokenize code for CodeBERT input"""
        return self.tokenizer(
            code_samples,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        )
    
    def predict(self, code_samples: List[str]) -> np.ndarray:
        """Predict vulnerability probabilities"""
        self.model.eval()
        
        inputs = self.tokenize_code(code_samples)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1)[:, 1]
        
        return probs.cpu().numpy()
    
    def predict_single(self, code: str) -> float:
        """Predict vulnerability probability for single code sample"""
        return self.predict([code])[0]
    
    def save(self, path: str):
        """Save model and tokenizer"""
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        print(f"Model saved to {path}")
    
    def load(self, path: str):
        """Load fine-tuned model"""
        self.model = RobertaForSequenceClassification.from_pretrained(path).to(self.device)
        self.tokenizer = RobertaTokenizer.from_pretrained(path)
        print(f"Model loaded from {path}")