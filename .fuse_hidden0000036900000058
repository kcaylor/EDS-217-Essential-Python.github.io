# Fixing Jupyter Kernel Issues for EDS 217

If you're getting `ModuleNotFoundError` for packages like seaborn, numpy, or pandas in your notebooks, the issue is likely that your notebook is using the wrong kernel.

## 🔧 Quick Fix

### Step 1: Ensure Environment is Active
```bash
conda activate eds217_2025
```

### Step 2: Reinstall the Kernel
```bash
python -m ipykernel install --user --name eds217_2025 --display-name "Python 3.11 (EDS 217 2025)" --force
```

### Step 3: Restart JupyterLab
```bash
# If JupyterLab is running, stop it (Ctrl+C) and restart
jupyter lab
```

### Step 4: Change Kernel in Notebook
1. Open your notebook in JupyterLab
2. Click on the kernel name in the top-right corner 
3. Select "Python 3.11 (EDS 217 2025)" from the dropdown
4. The notebook will restart with the correct environment

## 🔍 Verify It's Working

Run this in a notebook cell to confirm:
```python
import sys
print(f"Python path: {sys.executable}")

import seaborn as sns
import pandas as pd
import numpy as np
print(f"✅ All packages imported successfully!")
print(f"Seaborn version: {sns.__version__}")
```

## 🚨 Common Issues

- **Wrong kernel selected**: Always check the kernel name in the top-right of your notebook
- **Old kernel cache**: The `--force` flag in Step 2 overwrites any existing kernel registration
- **Environment not activated**: Make sure you're in the `eds217_2025` environment when installing the kernel

## 🔄 Alternative: Recreate Environment

If issues persist, recreate the environment:
```bash
conda env remove -n eds217_2025
mamba env create -f environment-fast.yml
conda activate eds217_2025
python -m ipykernel install --user --name eds217_2025 --display-name "Python 3.11 (EDS 217 2025)"
``` 