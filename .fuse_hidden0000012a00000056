# EDS 217 Fast Environment Setup

Conda is notoriously slow at dependency resolution. Here are faster alternatives:

## Option 1: Use Mamba (Fastest!)

Mamba is a drop-in replacement for conda that's much faster:

```bash
# Install mamba if you don't have it
conda install mamba -n base -c conda-forge

# Create environment with mamba (much faster!)
mamba env create -f environment-fast.yml

# Or create manually with mamba
mamba create -n eds217_2025 python=3.11 numpy pandas matplotlib seaborn jupyter jupyterlab ipykernel -c conda-forge

# Activate and register
conda activate eds217_2025
python -m ipykernel install --user --name eds217_2025 --display-name "Python 3.11 (EDS 217 2025)"
```

## Option 2: Step-by-Step Installation

Create the environment first, then add packages:

```bash
# Create basic environment (fast)
conda create -n eds217_2025 python=3.11 -c conda-forge

# Activate it
conda activate eds217_2025

# Install core packages in batches (faster than all at once)
conda install numpy pandas -c conda-forge
conda install matplotlib seaborn -c conda-forge  
conda install jupyter jupyterlab ipykernel -c conda-forge

# Register with Jupyter
python -m ipykernel install --user --name eds217_2025 --display-name "Python 3.11 (EDS 217 2025)"
```

## Option 3: Minimal + Install as Needed

Start with just the essentials and add packages when you need them:

```bash
# Super minimal environment (very fast)
conda create -n eds217_2025 python=3.11 pandas matplotlib jupyter jupyterlab -c conda-forge

# Activate and register
conda activate eds217_2025
python -m ipykernel install --user --name eds217_2025 --display-name "Python 3.11 (EDS 217 2025)"

# Add other packages as needed during the course
# conda install seaborn scipy scikit-learn -c conda-forge
```

## Option 4: If All Else Fails - Cancel and Retry

If conda is stuck:

```bash
# Cancel the current operation (Ctrl+C)
# Then try with just conda-forge channel:
conda create -n eds217_2025 python=3.11 -c conda-forge
conda activate eds217_2025
conda install numpy pandas matplotlib seaborn jupyter jupyterlab ipykernel -c conda-forge
```

## Why This Happens

Conda gets slow because:
- Multiple channels can create conflicts
- Too many packages at once = exponential complexity
- No version constraints = huge search space
- Some packages have complex dependency trees

## Recommended Approach

1. **Try mamba first** (if you can install it)
2. **Use conda-forge only** (avoid defaults channel)
3. **Install core packages first**, add extras later
4. **Specify versions** if you know what works

The minimal environment with the core packages will work for 90% of the course. You can always add more packages later! 