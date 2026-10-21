"""Calculate the planned paired mean; run from this directory."""
import csv
import json
from pathlib import Path

rows = list(csv.DictReader(Path("data.csv").open(encoding="utf-8")))
differences = [float(row["treatment"]) - float(row["control"]) for row in rows]
result = {"n": len(differences), "mean_difference": sum(differences) / len(differences)}
Path("outputs").mkdir(exist_ok=True)
Path("outputs/result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result))
