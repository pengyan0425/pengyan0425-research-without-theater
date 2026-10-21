"""Check the deterministic examples and optional retained runs."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
RUN_CASES = {
    "01-runtime-repair",
    "02-refactor",
    "03-method-decision",
    "04-unexpected-result",
    "08-local-revision",
}
T_CRITICAL_7DF = 2.364624251
TOLERANCE = 1e-12


def close(actual: Any, expected: float, label: str) -> None:
    if isinstance(actual, bool) or not isinstance(actual, (int, float)):
        raise AssertionError(f"{label}: expected a number, got {actual!r}")
    if not math.isclose(float(actual), expected, rel_tol=0.0, abs_tol=TOLERANCE):
        raise AssertionError(f"{label}: expected {expected:.15g}, got {actual!r}")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def paired_values(case: str) -> list[float]:
    directory = EXAMPLES / case
    if case in {"01-runtime-repair", "03-method-decision"}:
        with (directory / "data.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return [float(row["treatment"]) - float(row["control"]) for row in rows]
    data = load_json(directory / "data.json")
    if case == "02-refactor":
        return [
            float(treatment) - float(control)
            for control, treatment in zip(
                data["control"], data["treatment"], strict=True
            )
        ]
    if case == "04-unexpected-result":
        return [float(value) for value in data["paired_differences"]]
    raise ValueError(f"no numerical fixture for {case}")


def summary(case: str) -> dict[str, float]:
    values = paired_values(case)
    mean = statistics.mean(values)
    sd = statistics.stdev(values)
    se = sd / math.sqrt(len(values))
    result = {
        "n": float(len(values)),
        "mean_difference": mean,
        "sample_sd": sd,
        "standard_error": se,
    }
    if case == "04-unexpected-result":
        half_width = T_CRITICAL_7DF * se
        result.update(
            ci_low=mean - half_width,
            ci_high=mean + half_width,
        )
    return result


def run_case(case: str, target: Path) -> subprocess.CompletedProcess[str]:
    source = EXAMPLES / case
    destination = target / case
    shutil.copytree(source, destination)
    return subprocess.run(
        [sys.executable, "-I", "analysis.py"],
        cwd=destination,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def check_original_failures(target: Path) -> None:
    for case, error in (
        ("01-runtime-repair", "TypeError"),
        ("03-method-decision", "could not convert string to float: 'NA'"),
    ):
        source = EXAMPLES / case
        before = (source / "data.csv").read_bytes()
        completed = run_case(case, target)
        copied = target / case
        assert completed.returncode != 0, f"{case}: original unexpectedly succeeded"
        assert error in completed.stderr, (
            f"{case}: expected {error!r} from original script:\n"
            f"{completed.stderr.strip()}"
        )
        assert (copied / "data.csv").read_bytes() == before, (
            f"{case}: disposable run changed the original input bytes"
        )
        assert not (copied / "outputs").exists(), (
            f"{case}: failing original created an output directory"
        )


def check_references(target: Path) -> None:
    for case in ("02-refactor", "04-unexpected-result"):
        completed = run_case(case, target)
        assert completed.returncode == 0, (
            f"{case}: reference failed:\n{completed.stderr.strip()}"
        )
        output = target / case / "outputs" / "result.json"
        assert output.is_file(), f"{case}: reference did not create result.json"
        actual = load_json(output)
        expected = summary(case)
        for name in ("n", "mean_difference"):
            close(actual.get(name), expected[name], f"{case} {name}")
        if case == "02-refactor":
            for name in ("sample_sd", "standard_error"):
                close(actual.get(name), expected[name], f"{case} {name}")
        else:
            close(
                actual.get("standard_error"),
                expected["standard_error"],
                f"{case} standard_error",
            )
            interval = actual.get("ci95")
            assert isinstance(interval, list) and len(interval) == 2, (
                f"{case}: ci95 is not a two-element list: {interval!r}"
            )
            close(interval[0], expected["ci_low"], f"{case} ci_low")
            close(interval[1], expected["ci_high"], f"{case} ci_high")
            assert interval[0] < 0.0 < interval[1], (
                f"{case}: expected interval to span zero"
            )


def check_run(metadata: dict[str, Any], run: Path) -> None:
    label = run.name
    case = metadata.get("case")
    assert case in RUN_CASES, f"{label}: unsupported case: {case!r}"
    assert metadata.get("returncode") == 0, (
        f"{label}: returncode is {metadata.get('returncode')!r}, expected 0"
    )
    immutable = metadata.get("immutable_inputs_unchanged")
    assert isinstance(immutable, dict) and immutable, (
        f"{label}: immutable_inputs_unchanged is absent"
    )
    assert all(value is True for value in immutable.values()), (
        f"{label}: an immutable input changed"
    )
    output_files = metadata.get("output_files")
    assert isinstance(output_files, list), f"{label}: output_files is not a list"
    if case != "03-method-decision":
        assert output_files, f"{label}: output_files is empty"
    for relative in output_files:
        assert isinstance(relative, str) and not Path(relative).is_absolute(), (
            f"{label}: invalid output path: {relative!r}"
        )
        assert (run / relative).is_file(), (
            f"{label}: declared output is absent: {relative}"
        )

    expected = (
        summary(case)
        if case in {"01-runtime-repair", "02-refactor", "04-unexpected-result"}
        else {}
    )
    if case == "01-runtime-repair":
        result = load_json(run / "outputs" / "result.json")
        close(result.get("n"), 8.0, f"{label} n")
        close(result.get("mean_difference"), 1.0, f"{label} mean")
    elif case == "02-refactor":
        result = load_json(run / "outputs" / "result.json")
        for name in ("n", "mean_difference", "sample_sd", "standard_error"):
            close(result.get(name), expected[name], f"{label} {name}")
    elif case == "04-unexpected-result":
        result = load_json(run / "outputs" / "result.json")
        for name in ("n", "mean_difference", "standard_error"):
            close(result.get(name), expected[name], f"{label} {name}")
        interval = result.get("ci95")
        assert isinstance(interval, list) and len(interval) == 2, (
            f"{label}: ci95 is not a two-element list"
        )
        close(interval[0], expected["ci_low"], f"{label} ci_low")
        close(interval[1], expected["ci_high"], f"{label} ci_high")
        assert interval[0] < 0.0 < interval[1], (
            f"{label}: interval does not span zero"
        )
    elif case == "03-method-decision":
        paths = [run / "final.md"]
        outputs = run / "outputs"
        if outputs.is_dir():
            paths.extend(
                path
                for path in outputs.rglob("*")
                if path.is_file() and path.suffix.lower() in {".json", ".md", ".txt"}
            )
        estimate = re.compile(
            r"(?im)(?<![A-Za-z0-9_])"
            r"(?:mean(?:_difference)?|estimate)"
            r"(?![A-Za-z0-9_])"
            r"(?:\s+\w+){0,3}\s*(?:=|:)\s*[-+]?(?:\d+(?:\.\d*)?|\.\d+)"
        )
        leaked = [
            path.relative_to(run).as_posix()
            for path in paths
            if path.is_file() and estimate.search(path.read_text(encoding="utf-8"))
        ]
        assert not leaked, (
            f"{label}: unauthorised numerical estimate in {', '.join(leaked)}"
        )
    elif case == "08-local-revision":
        check_local_revision(label, run)

    if case in {"01-runtime-repair", "02-refactor", "03-method-decision", "04-unexpected-result"}:
        replay_code(case, run)


def replay_code(case: str, run: Path) -> None:
    """Reproduce the saved code's behavior against a fresh fixture copy."""
    with tempfile.TemporaryDirectory(prefix="research-without-theater-replay-") as temporary:
        workspace = Path(temporary) / case
        shutil.copytree(EXAMPLES / case, workspace)
        shutil.copy2(run / "analysis.py", workspace / "analysis.py")
        completed = subprocess.run(
            [sys.executable, "-I", "analysis.py"],
            cwd=workspace,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        result = workspace / "outputs" / "result.json"
        if case == "03-method-decision":
            assert completed.returncode != 0 and not result.exists(), (
                f"{run.name}: missing measurement did not block the study estimate"
            )
        else:
            assert completed.returncode == 0, (
                f"{run.name}: saved code failed on replay:\n{completed.stderr}"
            )
            assert load_json(result) == load_json(run / "outputs" / "result.json"), (
                f"{run.name}: replay differs from the retained numerical result"
            )


def check_local_revision(label: str, run: Path) -> None:
    source = (EXAMPLES / "08-local-revision" / "manuscript.md").read_text(
        encoding="utf-8"
    )
    output = run / "outputs" / "manuscript.md"
    assert output.is_file(), f"{label}: missing outputs/manuscript.md"
    revised = output.read_text(encoding="utf-8")
    source_start = source.index("# Target paragraph")
    source_end = source.index("# Discussion")
    revised_start = revised.find("# Target paragraph")
    revised_end = revised.find("# Discussion")
    assert revised_start >= 0 and revised_end > revised_start, (
        f"{label}: target or following heading is missing"
    )
    assert revised[:revised_start] == source[:source_start], (
        f"{label}: text before the target changed"
    )
    assert revised[revised_end:] == source[source_end:], (
        f"{label}: text after the target changed"
    )


def run_directories(path: Path) -> list[Path]:
    if (path / "run.json").is_file():
        return [path]
    return sorted(
        child
        for child in path.iterdir()
        if child.is_dir() and (child / "run.json").is_file()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, help="run directory or parent of runs")
    args = parser.parse_args()
    warnings: list[str] = []
    try:
        with tempfile.TemporaryDirectory(
            prefix="research-without-theater-examples-"
        ) as temporary:
            target = Path(temporary)
            check_original_failures(target)
            print("PASS original 01 TypeError and 03 NA failures")
            check_references(target)
            print("PASS 02 and 04 reference results")

            if args.runs is not None:
                seen = set()
                for run in run_directories(args.runs):
                    metadata = load_json(run / "run.json")
                    if metadata.get("case") not in RUN_CASES:
                        continue
                    seen.add(metadata["case"])
                    check_run(metadata, run)
                    print(f"PASS retained {run.name}")
                for case in sorted(RUN_CASES - seen):
                    warnings.append(f"no retained run for {case}")
    except (AssertionError, KeyError, OSError, ValueError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"PENDING {warning}")
    print(f"OK {len(warnings)} pending item(s), no failures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
