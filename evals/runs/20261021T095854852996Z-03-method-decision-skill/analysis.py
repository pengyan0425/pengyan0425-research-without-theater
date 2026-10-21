import csv
import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent
with (base_dir / "data.csv").open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))

if len(rows) != 8 or len({row["unit"] for row in rows}) != 8:
    raise SystemExit("methods.md requires all eight enrolled units, each appearing once.")

missing = [
    f"unit {row['unit']} ({field})"
    for row in rows
    for field in ("control", "treatment")
    if row[field].strip().upper() in {"", "NA"}
]
if missing:
    raise SystemExit(
        "Planned eight-pair mean cannot be computed: missing measurement(s) for "
        + ", ".join(missing)
        + ". methods.md approves no exclusion, imputation, or missing-data model. "
        "A complete set of measurements or an approved missing-data approach is required. "
        "No numerical result was written."
    )

differences = [float(row["treatment"]) - float(row["control"]) for row in rows]
output_dir = base_dir / "outputs"
output_dir.mkdir(exist_ok=True)
(output_dir / "result.json").write_text(
    json.dumps({"n": len(differences), "mean_difference": sum(differences) / len(differences)}),
    encoding="utf-8",
)
