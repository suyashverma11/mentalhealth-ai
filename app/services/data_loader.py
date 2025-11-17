"""
Simple dataset loader for MVP.
- If you have a local CSV: place it in data/ and call load_local_csv('data/myfile.csv')
- Optionally, this can load a Hugging Face dataset if 'datasets' is installed and the dataset name is provided.
"""

import os
from typing import List, Dict

def load_local_csv(path: str) -> List[Dict]:
    """Load a simple CSV with columns 'text' and 'label' into a list of dicts."""
    import csv
    out = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            out.append({'text': row.get('text', ''), 'label': row.get('label', None)})
    return out

def load_hf_dataset(name: str, subset: str = None):
    """Try to load a Hugging Face dataset by name. Requires 'datasets' package."""
    try:
        from datasets import load_dataset
    except Exception as e:
        raise RuntimeError("Install 'datasets' (pip install datasets) to load HF datasets") from e

    if subset:
        return load_dataset(name, subset)
    return load_dataset(name)

if __name__ == "__main__":
    # quick smoke test if run directly:
    print("data folder exists:", os.path.exists("data"))
