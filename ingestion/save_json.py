"""
save_json.py

Save processed documents/chunks into JSON files.
"""

import json
import os
from config import OUTPUT_FOLDER


def save_json(data, filename):
    """
    Save Python data to JSON.
    """

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    filepath = os.path.join(OUTPUT_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(data)} records to {filepath}")