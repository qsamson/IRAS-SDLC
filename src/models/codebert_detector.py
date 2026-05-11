"""
CodeBERT-based Vulnerability Detection Model

Fine-tuned transformer model for binary vulnerability classification.
Uses Microsoft's CodeBERT pre-trained on code and natural language.
"""

import torch
import torch.nn as nn
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from typing import List
import numpy as np


class CodeBERTVulnerabilityDetector:
    """
    CodeBERT model fine-tuned for vulnerability detection.
    
    Binary classification: vulnerable (1) vs. secure (0)
    """
    
    def __init__(self, model_name: str = "microsoft/codebert-base"):
        """
        Initialize CodeBERT vulnerability detector.
        
        Args:
            model_name: Pretrained model identifier from Hugging Face
        """
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        print(f"Using device: {self.device}")
        
        # Load tokenizer and model
        self.tokenizer = RobertaTokenizer.from_pretrained(model_name)
        self.model = RobertaForSequenceClassification.from_pretrained(
            model_name,
            num_labels=2  # Binary: vulnerable vs. secure
        ).to(self.device)
        
        self.max_length = 512  # CodeBERT max sequence length
    
    
    def tokenize_code(self, code_samples: List[str]) -> dict:
        """
        Tokenize source code for CodeBERT input.
        
        Args:
            code_samples: List of source code strings
            
        Returns:
            Dictionary with input_ids and attention_mask tensors
        """
        return self.tokenizer(
            code_samples,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        )
    
    
    def predict(self, code_samples: List[str]) -> np.ndarray:
        """
        Predict vulnerability probabilities for code samples.
        
        Args:
            code_samples: List of source code strings
            
        Returns:
            Array of vulnerability probabilities ∈ [0, 1]
        
        Example:
            >>> detector = CodeBERTVulnerabilityDetector()
            >>> code = ["strcpy(dest, src);"]
            >>> probs = detector.predict(code)
            >>> print(f"Vulnerability probability: {probs[0]:.3f}")
        """
        self.model.eval()
        
        # Tokenize
        inputs = self.tokenize_code(code_samples)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1)[:, 1]  # P(vulnerable)
        
        return probs.cpu().numpy()
    
    
    def predict_single(self, code: str) -> float:
        """
        Predict vulnerability probability for a single code sample.
        
        Args:
            code: Source code string
            
        Returns:
            Vulnerability probability ∈ [0, 1]
        """
        return self.predict([code])[0]
    
    
    def save(self, path: str):
        """
        Save fine-tuned model and tokenizer to disk.
        
        Args:
            path: Directory path to save model
        """
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        print(f"✓ Model saved to {path}")
    
    
    def load(self, path: str):
        """
        Load fine-tuned model from disk.
        
        Args:
            path: Directory path containing saved model
        """
        self.model = RobertaForSequenceClassification.from_pretrained(
            path
        ).to(self.device)
        self.tokenizer = RobertaTokenizer.from_pretrained(path)
        print(f"✓ Model loaded from {path}")


# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = CodeBERTVulnerabilityDetector()
    
    # Example vulnerable code (buffer overflow)
    vulnerable_code = """
    void copy_data(char *dest, char *src) {
        strcpy(dest, src);  // Vulnerable: no bounds checking
    }
    """
    
    # Example secure code
    secure_code = """
    void copy_data(char *dest, char *src, size_t size) {
        strncpy(dest, src, size - 1);
        dest[size - 1] = '\\0';  // Secure: bounds checked
    }
    """
    
    # Predict vulnerability probabilities
    vuln_prob = detector.predict_single(vulnerable_code)
    secure_prob = detector.predict_single(secure_code)
    
    print("="*50)
    print("CodeBERT Vulnerability Detection Example")
    print("="*50)
    print(f"Vulnerable code probability: {vuln_prob:.3f}")
    print(f"Secure code probability:     {secure_prob:.3f}")
    print("="*50)