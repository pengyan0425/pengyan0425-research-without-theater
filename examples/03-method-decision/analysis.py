import csv
import json
from pathlib import Path

rows = list(csv.DictReader(Path("data.csv").open(encoding="utf-8")))
differences = [float(row["treatment"]) - float(row["control"]) for row in rows]
Path("outputs").mkdir(exist_ok=True)
Path("outputs/result.json").write_text(json.dumps({"n": len(differences), "mean_difference": sum(differences) / len(differences)}), encoding="utf-8")
