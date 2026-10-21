"""Replay a synthetic task in a disposable workspace with an authenticated Codex CLI.

Raw logs remain in ignored .eval-work/. Only selected, path-redacted events and
artifacts are exported. Review exported material before publishing it.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "research-without-theater"
CASES = sorted(p.name for p in (ROOT / "examples").iterdir() if p.is_dir())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=CASES, required=True)
    parser.add_argument("--condition", choices=("skill", "baseline"), required=True)
    parser.add_argument("--model", default="gpt-6.1-sol")
    parser.add_argument("--effort", default="xhigh")
    parser.add_argument("--timeout", type=int, default=900, help="Maximum CLI seconds")
    args = parser.parse_args()
    cli = shutil.which("codex.cmd" if os.name == "nt" else "codex")
    if not cli:
        parser.error("Codex CLI was not found; install and authenticate it first.")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-" + args.case + "-" + args.condition
    workspace = ROOT / ".eval-work" / run_id
    export = ROOT / "evals" / "runs" / run_id
    fixture = ROOT / "examples" / args.case
    shutil.copytree(fixture, workspace)
    installed = workspace / ".agents" / "skills" / SKILL.name
    if args.condition == "skill":
        shutil.copytree(SKILL, installed)
    installed_hashes = {p.relative_to(installed).as_posix(): digest(p) for p in installed.rglob("*") if p.is_file()} if args.condition == "skill" else {}
    source_hashes = {p.name: digest(p) for p in fixture.iterdir() if p.is_file()}
    shared = (
        "Complete the research task below in English. Work only in the current disposable "
        "workspace; installed skill instructions may be read. Do not use the network, user "
        "configuration, memory files, or parent project files. Preserve supplied data, methods, "
        "and manuscript source files; write deliverables under outputs/. Python scripts can "
        "be edited when the task calls for it. Finish with a concise account of the result "
        "and any remaining decision.\n\nTASK\n" + (fixture / "prompt.md").read_text(encoding="utf-8")
    )
    prefix = (
        "Use $research-without-theater at .agents/skills/research-without-theater/SKILL.md "
        "for this task.\n\n" if args.condition == "skill" else ""
    )
    prompt = prefix + shared
    (workspace / "submitted-prompt.txt").write_text(prompt, encoding="utf-8")
    command = [cli, "exec", "--ephemeral", "--ignore-user-config", "--skip-git-repo-check",
               "--model", args.model, "-c", f'model_reasoning_effort="{args.effort}"',
               "-c", 'approval_policy="never"', "--sandbox", "danger-full-access",
               "--color", "never", "--json", "--cd", str(workspace),
               "--output-last-message", str(workspace / "final.md"), "-"]
    started = datetime.now(timezone.utc)
    try:
        completed = subprocess.run(command, input=prompt, text=True, encoding="utf-8",
                                   errors="replace", capture_output=True, timeout=args.timeout)
        raw_stdout, raw_stderr, returncode = completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as exc:
        raw_stdout = exc.stdout or ""
        raw_stderr = exc.stderr or ""
        if isinstance(raw_stdout, bytes):
            raw_stdout = raw_stdout.decode("utf-8", "replace")
        if isinstance(raw_stderr, bytes):
            raw_stderr = raw_stderr.decode("utf-8", "replace")
        returncode = 124
    (workspace / "raw-events.jsonl").write_text(raw_stdout, encoding="utf-8")
    (workspace / "raw-stderr.txt").write_text(raw_stderr, encoding="utf-8")
    export.mkdir(parents=True)

    substitutions = [(str(workspace), "<WORKSPACE>"), (str(ROOT), "<REPOSITORY>"),
                     (str(ROOT.parent), "<PROJECTS_ROOT>")]
    user_profile = os.environ.get("USERPROFILE") or os.environ.get("HOME")
    if user_profile:
        substitutions.append((user_profile, "<USER_HOME>"))
    for variable, label in (("ProgramFiles(x86)", "<PROGRAM_FILES_X86>"),
                            ("ProgramFiles", "<PROGRAM_FILES>"), ("SystemRoot", "<SYSTEM_ROOT>")):
        if os.environ.get(variable):
            substitutions.append((os.environ[variable], label))

    def redact(text: str) -> str:
        for original, replacement in substitutions:
            for variant in {original, original.replace("\\", "/"), original.replace("\\", "\\\\"), original.replace("\\", "\\\\\\\\")}:
                text = re.sub(re.escape(variant), lambda match: replacement, text, flags=re.IGNORECASE)
        return text

    events = []
    usage = None
    for line in raw_stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "item.completed":
            item = event.get("item", {})
            if item.get("type") in {"agent_message", "command_execution", "file_change"}:
                command_text = item.get("command", "").replace("\\", "/")
                if item.get("type") == "command_execution" and any(
                    marker in command_text for marker in ("SKILL.md", ".codex/skills/", ".agents/skills/", "AGENTS.md")
                ):
                    item["aggregated_output"] = "[Instruction/discovery output omitted from public export; command and exit status retained.]"
                    item["output_omitted_reason"] = "Avoid redistributing installed instructions or user-specific context"
                events.append(json.loads(redact(json.dumps(item, ensure_ascii=False))))
        if event.get("type") == "turn.completed":
            usage = event.get("usage")
    reads = [item.get("command", "") for item in events
             if item.get("type") == "command_execution" and item.get("exit_code") == 0
             and "SKILL.md" in item.get("command", "")
             and re.search(r"\b(?:Get-Content|cat|head|tail|more|read_text|readFileSync)\b",
                           item.get("command", ""), flags=re.IGNORECASE)]
    confirmed = any("research-without-theater" in command for command in reads)
    outputs = workspace / "outputs"
    exported_files = []
    if outputs.is_dir():
        for source in sorted(outputs.rglob("*")):
            if source.is_file():
                relative = source.relative_to(workspace)
                target = export / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                try:
                    target.write_text(redact(source.read_text(encoding="utf-8")), encoding="utf-8")
                except UnicodeDecodeError as exc:
                    raise ValueError(f"Review binary artifact manually before export: {relative}") from exc
                exported_files.append(relative.as_posix())
    if (workspace / "analysis.py").exists():
        (export / "analysis.py").write_text(redact((workspace / "analysis.py").read_text(encoding="utf-8")), encoding="utf-8")
    final = workspace / "final.md"
    if final.is_file():
        (export / "final.md").write_text(redact(final.read_text(encoding="utf-8")), encoding="utf-8")
    (export / "prompt.txt").write_text(prompt, encoding="utf-8")
    (export / "events.json").write_text(json.dumps(events, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    immutable = {name: digest(workspace / name) == before for name, before in source_hashes.items()
                 if not name.endswith(".py")}
    version = subprocess.run([cli, "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()
    record = {
        "run_id": run_id, "case": args.case, "condition": args.condition,
        "started_utc": started.isoformat(), "elapsed_seconds": round((datetime.now(timezone.utc) - started).total_seconds(), 2),
        "model_requested": args.model, "reasoning_effort_requested": args.effort,
        "model_confirmation": "CLI request; server model fingerprint not exposed by these events",
        "codex_version": version, "python_version": platform.python_version(),
        "platform": platform.system(), "returncode": returncode,
        "user_config": "--ignore-user-config; authentication retained; global instructions and other discoverable skills may still apply",
        "new_skill_installed_in_workspace": args.condition == "skill",
        "new_skill_read_observed": confirmed, "observed_skill_read_commands": reads,
        "entrypoint_sha256": installed_hashes.get("SKILL.md"),
        "skill_files_sha256": installed_hashes,
        "input_sha256": source_hashes, "immutable_inputs_unchanged": immutable,
        "output_files": exported_files, "token_usage": usage,
        "export_note": "Selected completed events and text artifacts; paths redacted and instruction/discovery output omitted. Raw local logs excluded. Review before publication.",
    }
    (export / "run.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if returncode:
        (export / "error.txt").write_text(redact(raw_stderr), encoding="utf-8")
    print(json.dumps({"run": run_id, "returncode": returncode, "skill_read_observed": confirmed, "export": str(export.relative_to(ROOT))}))
    return returncode


if __name__ == "__main__":
    sys.exit(main())
