"""A paired summary; standard library only."""
import json
import math
from pathlib import Path


def summarize(control, treatment):
    if len(control) != len(treatment) or len(control) < 2:
        raise ValueError("Need at least two complete, matched pairs")
    differences = [t - c for c, t in zip(control, treatment)]
    n = len(differences)
    mean = sum(differences) / n
    squared = sum((value - mean) ** 2 for value in differences)
    sd = math.sqrt(squared / (n - 1))
    return {"n": n, "mean_difference": mean, "sample_sd": sd, "standard_error": sd / math.sqrt(n)}


if __name__ == "__main__":
    data = json.loads(Path("data.json").read_text(encoding="utf-8"))
    result = summarize(data["control"], data["treatment"])
    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
