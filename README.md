# Research Without Theater

Research Without Theater is a self-contained Codex skill for scientific coding,
analysis, and manuscript work. It favors direct execution, validation
proportionate to the change, and claims that match the available evidence.

The skill adds no separate runtime, package installation, MCP server, API key,
or network dependency beyond the host that runs it. Normal use happens inside
that host.

## What it changes

The skill adds a compact decision rule to research work: add a mechanism,
check, or sentence when it answers a concrete need in the current task. It
uses that rule across three connected modes:

- **Execution:** read the real inputs and code, repair established technical
  faults, run the changed analysis, and retain provenance for reported values.
- **Writing:** organize prose around the question, finding, evidence, and
  contribution; remove anticipatory defenses while preserving uncertainty,
  limits, and adverse evidence that affect interpretation.
- **Review:** report findings and proposed repairs; run checks that remain
  read-only, while edits or state-changing reruns need authorization.

The skill also distinguishes an implementation repair from a scientific
choice. Changes to an estimand, sample rule, missing-data treatment, formula,
or inferential conclusion require the user's decision when the materials do not
already authorize them. Unexpected or null results remain results; the skill
checks implementation errors and reports the outcome without retuning the
analysis to get a preferred direction.

It supplies model guidance rather than a policy enforcement layer. It does not
replace project rules, statistical judgment, source review, or a user's
decision about the science.

## Install

### Codex Skill Installer

Ask Codex Skill Installer to load the skill folder from GitHub:

```text
$skill-installer install https://github.com/pengyan0425/pengyan0425-research-without-theater/tree/main/skills/research-without-theater
```

The installer reads the folder's `SKILL.md`, including its required `name` and
`description`. Codex normally detects a newly installed skill automatically;
restart Codex if it does not appear.

Alternatively, download the standalone skill ZIP and `SHA256SUMS` from
[Releases](https://github.com/pengyan0425/pengyan0425-research-without-theater/releases).
Extract the complete `research-without-theater` directory and use the local-copy
instructions below.

### Local copy

For a first install, copy the complete skill directory into the Codex user skill
location. The guard stops an existing destination from becoming a nested
`research-without-theater/research-without-theater` directory:

```powershell
$source = (Resolve-Path ".\skills\research-without-theater").Path
$skillsRoot = Join-Path $HOME ".agents\skills"
$destination = Join-Path $skillsRoot "research-without-theater"
if (Test-Path -LiteralPath $destination) {
    throw "Skill directory already exists: $destination"
}
New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null
Copy-Item -LiteralPath $source -Destination $skillsRoot -Recurse
```

On POSIX shells, use the same directory under `$HOME`:

```sh
source_dir="./skills/research-without-theater"
skills_root="$HOME/.agents/skills"
destination="$skills_root/research-without-theater"
if [ -e "$destination" ]; then
  echo "Skill directory already exists: $destination" >&2
  exit 1
fi
mkdir -p "$skills_root"
cp -R "$source_dir" "$skills_root/"
```

The copied directory is self-contained: `SKILL.md`, three optional reference
guides, UI metadata, `LICENSE`, and `NOTICE` travel together. Keep it as a
skill directory; do not flatten its files into `.agents/skills`. For a later
update, review and replace the installed copy deliberately.

For a project-scoped installation, place the same directory under
`.agents/skills/research-without-theater` in the repository where Codex runs.
Codex discovers repository skills and user skills separately. If two installed
skills have the same name, Codex can show both rather than merging them.

## Use

Invoke the skill explicitly:

```text
$research-without-theater
```

Then provide the research task and its existing files. A useful prompt states
the requested deliverable, the fixed scientific choices, and the path or
source of the evidence. The skill can also be selected implicitly when its
description matches a scientific coding or writing request.

It works within the current host's permissions and project rules. Installing
it does not replace global `AGENTS.md`, project instructions, repository
conventions, or another skill's local rules. The skill's bundled boundaries
travel with the skill; no additional runtime configuration is needed.

## Examples

### Code

```text
Use $research-without-theater to repair and run analysis.py.
The paired mean, sample SD, and standard error are the existing method.
Preserve data.csv, write result.json under outputs/, and compare the changed
results with the original implementation. If a missing value requires a new
sample rule, explain its effect and ask before choosing.
```

```text
��ʹ�� $research-without-theater �޸������� analysis.py��
��Ծ�ֵ��������׼��ͱ�׼���Ǽȶ����������� data.csv�������д�� outputs/result.json��
���Ƚ��޸�ǰ��ĺ�����ֵ�����ȱʧֵ��Ҫ�µ�����������˵��Ӱ�첢ѯ���ң���Ҫ����ѡ��
```

### Manuscript

```text
Use $research-without-theater to revise the target Results paragraph.
Keep the design, estimates, uncertainty, and the adverse result that limits
the interpretation. Remove defensive narration, preserve every other section,
and identify missing facts rather than inventing them.
```

```text
��ʹ�� $research-without-theater �޸�Ŀ�� Results ���䡣
�����о���ơ�����ֵ����ȷ���ԣ��Լ����ƽ��͵Ĳ��������ɾ��������������
�����������ֱ�����ȱʧ��ʵҪ��������Ҫ���졣
```

The repository's [examples](examples/README.md) contain eight original
synthetic tasks covering execution, refactoring, method decisions, unexpected
results, writing, association, adverse evidence, and local revision. Their data
and manuscript passages are synthetic and establish no scientific finding.

## Optional evaluation

Normal use needs no separate API key. The optional replay tools require Python
3.10 or newer and an authenticated Codex CLI; model access and the selected
configuration also need to be available in the host.

Run the deterministic example checks:

```sh
python scripts/check_examples.py
python scripts/check_examples.py --runs evals/runs
python scripts/verify_release.py
```

Replay an agent task:

```sh
python scripts/run_eval.py --case 01-runtime-repair --condition skill
python scripts/run_eval.py --case 01-runtime-repair --condition baseline
python scripts/run_eval.py --case 05-defensive-prose --condition skill \
  --model gpt-6.1-sol --effort xhigh
```

`scripts/run_eval.py` accepts `--case`, `--condition`, `--model`, and
`--effort`. It defaults to `gpt-6.1-sol` and `xhigh`. Each run operates on a
disposable fixture copy and exports selected, path-redacted evidence under
`evals/runs/`; raw local logs stay ignored. Review every export for private
content before publishing it.

The [evaluation protocol](evals/README.md) describes the cases, replay, and
review criteria. The current [release review](evals/review.md) records the
initial runs and their limits; the [independent semantic
review](evals/independent-review.md) examines the initial skill artifacts and
the two paired baselines.

## Evidence and limits

The `v0.1.0` evidence set is intentionally narrow. Eleven model executions
completed with return code 0: eight initial skill cases, two baseline
executions for cases 01 and 05, and one targeted rerun of case 03. All nine
skill-condition runs read the entry point. Both paired cases succeeded under
both conditions, so the comparisons show no quality improvement over baseline.
The runs requested `gpt-6.1-sol` at effort `xhigh` and used Codex CLI `0.163.0`,
Python `3.13.12`, and Windows; the CLI exposed no server model fingerprint.
`--ignore-user-config` retained authentication and did not isolate global
instructions or every discoverable skill. This new project has no adoption
data and makes no performance or superiority claim. Read the [evaluation
protocol](evals/README.md), [release review](evals/review.md), and [independent
semantic review](evals/independent-review.md) before reusing these results;
they cover synthetic fixtures in one Windows environment and do not establish a
general quality evaluation.

## Related agents and portability

Codex on Windows is the only host with completed runs in this release.
Other Agent Skills-compatible hosts may read a standard `SKILL.md` directory,
but installation and behavior are untested here. See
[portability](docs/portability.md) for the exact boundary.

## Sources and licensing

The skill is independently authored and licensed under
[Apache License 2.0](LICENSE). The installable directory includes its own
[LICENSE](skills/research-without-theater/LICENSE) and
[NOTICE](skills/research-without-theater/NOTICE).

Nature skills and Stop That Shit informed general ideas in the design.
Their source points, licenses, and conceptual influence are recorded in
[third_party](third_party/README.md) and [sources](docs/sources.md). No copied
skill instructions, Guard components, hooks, or runtime code are distributed.

Contributions follow [CONTRIBUTING.md](CONTRIBUTING.md).

[��������](README.zh-CN.md)
