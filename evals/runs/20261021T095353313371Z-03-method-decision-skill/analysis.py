import csv
import hashlib
import json
import math
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    data_path = root / "data.csv"
    methods_path = root / "methods.md"
    output_dir = root / "outputs"
    output_dir.mkdir(exist_ok=True)

    with data_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 8 or len({row["unit"] for row in rows}) != 8:
        raise ValueError("The protocol requires eight distinct paired units.")

    missing = []
    differences = []
    for row in rows:
        values = {}
        for field in ("control", "treatment"):
            raw = row[field].strip()
            if raw.upper() in {"", "NA"}:
                missing.append({"unit": row["unit"], "field": field})
                continue
            value = float(raw)
            if not math.isfinite(value):
                raise ValueError(f"Unit {row['unit']} has a nonfinite {field} value.")
            values[field] = value
        if len(values) == 2:
            differences.append(values["treatment"] - values["control"])

    run = {
        "analysis_type": "planned",
        "estimand": "Average treatment-minus-control difference across all eight enrolled units",
        "expected_pairs": 8,
        "observed_pairs": len(rows),
        "complete_pairs": len(differences),
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (data_path, methods_path, Path(__file__).resolve())
        },
    }
    result_path = output_dir / "result.json"
    if missing:
        run.update({
            "status": "blocked_missing_measurement",
            "missing_measurements": missing,
            "decision_required": (
                "Approve a missing-data method or retain the planned analysis as pending. "
                "Excluding an incomplete pair changes the analysis population; "
                "imputation or a missing-data model introduces additional assumptions."
            ),
        })
        result_path.unlink(missing_ok=True)
    else:
        result = {
            "n": len(differences),
            "mean_difference": sum(differences) / len(differences),
        }
        result_path.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        run.update({"status": "completed", "result": result})

    (output_dir / "analysis_status.json").write_text(
        json.dumps(run, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    if missing:
        print("Analysis pending: missing measurements; see outputs/analysis_status.json.", file=sys.stderr)
        return 2
    print(f"Saved the eight-pair result to {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
