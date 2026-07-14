## Preprocessing Module

This package contains reusable components for dataset preprocessing.  
It refactors the original notebook into modular Python scripts.

## Files
- `__init__.py` → initializes the package
- `config.py` → dataset configs and `get_config()` function
- `loader.py` → file loading functions (CSV, Excel, JSON)
- `preprocess.py` → preprocessing logic (scaling, encoding, splitting)
- `validate.py` → validation helpers (shapes, distributions, missing values)

##  How to Use
1. Import functions in your notebook or script:
   ```python
   from preprocessing.loader import load
   from preprocessing.config import get_config, configs
   from preprocessing.preprocess import preprocess_data
   from preprocessing.validate import validate_split

2. Run the pipeline end‑to‑end using main.py at the project root:
``` python 
  main.py
```

# Purpose

- Makes preprocessing modular and reusable
- Separates logic from notebooks for clean project structure
- Provides validation checks for data splits, scaling, and encoding