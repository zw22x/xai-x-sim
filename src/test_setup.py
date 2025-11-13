# src/test_setup
#xai/x sim environment verification

import torch
import os
import sys

print("="*60)
print("xAI/x simulation - environment check")
print("="*60)
print(f"Python: {sys.version.split()[0]}")
print(f"PyTorch: {torch.__version__}")
print(f"Device: {'MPS (Apple Silicon)' if torch.backends.mps.is_available() else 'CPU'}")
print(f"CUDA: {torch.cuda.is_available()}")
print(f"CWD: {os.getcwd()}")

if torch.backends.mps.is_available():
    x = torch.randn(3, 3).to('mps')
    print(f"MPS Test: {x.device}")
else:
    print("MPS not available - using CPU")

print("ENVIRIONMENT READY")
print("="*60)