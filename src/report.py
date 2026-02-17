import json
from datetime import datetime
from pathlib import Path

def save_report(payload: dict, suite: str) -> str:
    Path("outputs").mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"outputs/{suite}_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return path