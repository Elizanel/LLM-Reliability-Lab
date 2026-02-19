import json
from datetime import datetime
from pathlib import Path


def save_report(payload: dict, suite: str) -> str:
    # Ensure outputs folder exists.
    Path("outputs").mkdir(exist_ok=True)

    # Timestamp so reports never overwrite each other.
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Construct filename.
    path = f"outputs/{suite}_{ts}.json"

    # Save JSON with indentation for readability.
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    return path
