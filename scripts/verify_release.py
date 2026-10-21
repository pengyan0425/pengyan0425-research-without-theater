"""Check release structure, local links, and standalone skill installation."""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "research-without-theater"
IGNORED = {".git", ".eval-work", "__pycache__", "dist", "node_modules"}
TEXT = {".md", ".txt", ".json", ".yaml", ".yml"}
PRIVACY = (
    re.compile(
        r"(?i)(?<![A-Za-z0-9_])[A-Z]:[\\/]"
        r"(?:Users|AIwork)(?:[\\/][^\s\"'<>`]+)+"
    ),
    re.compile(r"(?<![\w.])/(?:home|Users)/[^/\s\"'`]+(?:/\S*)?"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
)


def files(base: Path, suffixes: set[str] | None = None) -> list[Path]:
    return sorted(
        path
        for path in base.rglob("*")
        if path.is_file()
        and not IGNORED.intersection(path.relative_to(base).parts)
        and (suffixes is None or path.suffix.lower() in suffixes)
    )


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = next(
        (index for index in range(1, len(lines)) if lines[index].strip() == "---"),
        None,
    )
    if end is None:
        return {}
    result: dict[str, str] = {}
    nested = False
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if match:
            key, value = match.groups()
            result[key] = scalar(value)
            nested = key == "metadata"
        elif nested:
            match = re.match(r"^\s+([A-Za-z][\w-]*):\s*(.*)$", line)
            if match:
                result[f"metadata.{match.group(1)}"] = scalar(match.group(2))
    return result


def interface(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    section = ""
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if match:
            section = match.group(1)
            continue
        match = re.match(r"^\s+([A-Za-z][\w-]*):\s*(.*)$", line)
        if match and section in {"interface", "policy"}:
            result[f"{section}.{match.group(1)}"] = scalar(match.group(2))
    return result


def prose_lines(text: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    fence = ""
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^\s*(```+|~~~+)", line)
        if match:
            marker = match.group(1)[0]
            if not fence:
                fence = marker
            elif fence == marker:
                fence = ""
            continue
        if not fence:
            result.append((number, re.sub(r"`[^`]*`", "", line)))
    return result


def slug(heading: str) -> str:
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    heading = re.sub(r"[*_~`]", "", heading)
    heading = unicodedata.normalize("NFKC", heading).strip().lower()
    return re.sub(r"[^\w -]", "", heading).replace(" ", "-")


def anchors(text: str) -> set[str]:
    result: set[str] = set()
    for _, line in prose_lines(text):
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        base = slug(match.group(1))
        candidate = base
        number = 1
        while candidate in result:
            candidate = f"{base}-{number}"
            number += 1
        result.add(candidate)
    return result


def links(text: str) -> list[tuple[int, str]]:
    result = []
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
    for number, line in prose_lines(text):
        for match in pattern.finditer(line):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            elif re.search(r"\s+[\"'(]", target):
                target = re.split(r"\s+[\"'(]", target, maxsplit=1)[0]
            result.append((number, target))
    return result


def check_links(
    failures: list[str],
    warnings: list[str],
    base: Path,
    label: str,
    require_local_paths: bool = False,
) -> None:
    root = base.resolve()
    for source in files(base, {".md"}):
        relative = source.relative_to(base)
        if relative.parts[:2] == ("evals", "runs"):
            continue
        try:
            text = source.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            failures.append(
                f"{label}: cannot read {relative.as_posix()}: {exc}"
            )
            continue
        for number, raw in links(text):
            parsed = urlsplit(raw)
            if parsed.scheme or parsed.netloc or raw.startswith("//"):
                continue
            path_text = unquote(parsed.path)
            if require_local_paths and not path_text:
                failures.append(
                    f"{label}:{relative.as_posix()}:{number}: "
                    f"standalone skill has a relative link without a target: {raw}"
                )
                continue
            target = source if not path_text else (source.parent / path_text).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                failures.append(
                    f"{label}:{relative.as_posix()}:{number}: "
                    f"local link escapes checked tree: {raw}"
                )
                continue
            if not target.exists():
                failures.append(
                    f"{relative.as_posix()}:{number}: "
                    f"local target does not exist: {raw}"
                )
                continue
            fragment = unquote(parsed.fragment)
            if (
                fragment
                and target.is_file()
                and target.suffix.lower() == ".md"
                and fragment not in anchors(target.read_text(encoding="utf-8"))
            ):
                failures.append(
                    f"{label}:{relative.as_posix()}:{number}: "
                    f"markdown anchor not found: {raw}"
                )


def check_text(failures: list[str], base: Path) -> None:
    for path in files(base, TEXT):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            failures.append(
                f"cannot read {path.relative_to(base).as_posix()}: {exc}"
            )
            continue
        for pattern in PRIVACY:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                failures.append(
                    f"{path.relative_to(base).as_posix()}:{line}: "
                    "personal path or credential found"
                )
                break


def check_structure(failures: list[str]) -> None:
    for path in (
        ROOT / "VERSION",
        ROOT / "LICENSE",
        ROOT / "NOTICE",
        SKILL / "LICENSE",
        SKILL / "NOTICE",
    ):
        if not path.is_file() or not path.read_bytes().strip():
            failures.append(f"missing or empty release file: {path.relative_to(ROOT)}")

    entrypoints = [path for path in files(ROOT) if path.name == "SKILL.md"]
    if len(entrypoints) != 1:
        failures.append(f"expected one SKILL.md, found {len(entrypoints)}")
    if sum(path.name == "SKILL.md" for path in files(SKILL)) != 1:
        failures.append("installable skill must contain exactly one SKILL.md")

    version = (
        (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        if (ROOT / "VERSION").is_file()
        else ""
    )
    skill_text = (
        (SKILL / "SKILL.md").read_text(encoding="utf-8")
        if (SKILL / "SKILL.md").is_file()
        else ""
    )
    meta = frontmatter(skill_text)
    for name in ("name", "description", "license"):
        if not meta.get(name, "").strip():
            failures.append(f"SKILL.md frontmatter missing {name}")
    if "metadata" not in meta:
        failures.append("SKILL.md frontmatter missing metadata")
    if meta.get("name") != SKILL.name:
        failures.append("SKILL.md name does not match its directory")
    if len(meta.get("description", "")) < 40:
        failures.append("SKILL.md description is absent or too short")
    if meta.get("license") != "Apache-2.0":
        failures.append("SKILL.md license must be Apache-2.0")
    if not version or meta.get("metadata.version") != version:
        failures.append("SKILL.md metadata.version does not match VERSION")

    ui_path = SKILL / "agents" / "openai.yaml"
    ui = interface(ui_path.read_text(encoding="utf-8")) if ui_path.is_file() else {}
    for name in ("display_name", "short_description", "default_prompt"):
        if not ui.get(f"interface.{name}"):
            failures.append(f"agents/openai.yaml missing interface.{name}")
    if ui.get("policy.allow_implicit_invocation") not in {"true", "false"}:
        failures.append(
            "agents/openai.yaml policy.allow_implicit_invocation "
            "must be true or false"
        )
    if "$research-without-theater" not in ui.get("interface.default_prompt", ""):
        failures.append("agents/openai.yaml default_prompt must invoke the skill")


def check_install(failures: list[str], warnings: list[str]) -> None:
    with tempfile.TemporaryDirectory(
        prefix="research-without-theater-install-"
    ) as temporary:
        installed = Path(temporary) / ".agents" / "skills" / SKILL.name
        installed.parent.mkdir(parents=True)
        shutil.copytree(SKILL, installed)
        for name in ("SKILL.md", "LICENSE", "NOTICE", "agents/openai.yaml"):
            if not (installed / name).is_file():
                failures.append(f"standalone install missing {name}")
        check_links(
            failures,
            warnings,
            installed,
            "standalone",
            require_local_paths=True,
        )


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    try:
        check_structure(failures)
        check_links(failures, warnings, ROOT, "repository")
        check_text(failures, ROOT)
        check_install(failures, warnings)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        failures.append(f"release validation could not complete: {exc}")

    for warning in warnings:
        print(f"PENDING {warning}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print(f"OK {len(warnings)} pending item(s), no failures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
