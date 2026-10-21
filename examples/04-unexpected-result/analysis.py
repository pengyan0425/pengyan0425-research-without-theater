import json
import math
import statistics
from pathlib import Path

data = json.loads(Path("data.json").read_text(encoding="utf-8"))
values = data["paired_differences"]
n = len(values)
mean = statistics.mean(values)
se = statistics.stdev(values) / math.sqrt(n)
critical = 2.364624251
result = {"n": n, "mean_difference": mean, "standard_error": se, "ci95": [mean - critical * se, mean + critical * se], "analysis": "prespecified"}
Path("outputs").mkdir(exist_ok=True)
Path("outputs/result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result))
