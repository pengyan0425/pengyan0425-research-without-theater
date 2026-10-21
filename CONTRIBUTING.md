# Contributing to Research Without Theater

Research Without Theater is one original Codex skill for scientific coding,
evidence checks, and manuscript work. Contributions should keep the package
small, source-grounded, and useful during ordinary research work.

Before proposing a change, read [the skill](skills/research-without-theater/SKILL.md),
[the design](docs/design.md), [the examples](examples/README.md), and
[the evaluation protocol](evals/README.md). Read the relevant reference guide
when changing execution, writing, or evidence behavior.

## Contribution rules

- Keep the skill independently authored. Do not vendor upstream instructions,
  Guard components, hooks, runtime code, or another skill.
- Ground edits in an observed task need or a concrete failure. Preserve the
  boundary between technical repair and a scientific choice.
- Use synthetic, public fixtures. Do not add private data, local paths, raw
  session logs, credentials, or unredacted model output.
- A read-only review may run non-mutating checks. File edits and state-changing
  reruns need authorization that is absent from a review-only request.
- Report observed failures and limitations. Do not add adoption, user-count,
  performance, productivity, or superiority claims without published evidence.
- Record any conceptual source and its license. Describe conceptual influence
  separately from copied material.
- When `SKILL.md` changes, update the affected references and examples. Keep
  the English and Chinese READMEs synchronized.

## Validation

Run the deterministic checks affected by the change:

```sh
python scripts/check_examples.py
python scripts/check_examples.py --runs evals/runs
python scripts/verify_release.py
```

Changes to model-facing behavior should add or update a synthetic case and,
when access is available, replay both relevant conditions with
`scripts/run_eval.py`. The optional runner requires Python 3.10 or newer and an
authenticated Codex CLI. Record the requested model, effort, CLI version,
environment, and any contamination limit. Keep raw logs local and review every
export for private content before publication.

Automated checks cover structural and numerical invariants. Read the resulting
artifacts for scientific meaning, evidence strength, scope, and approval
behavior. An exit code of 0 or a matching number does not by itself establish
that the prose or decision is correct.

## Pull requests

Describe the observed problem, the behavior after the change, and the checks
that support it. Link the case or run that demonstrates the behavior. Separate
verified facts from unresolved questions, and do not describe a draft release
as generally validated.

By contributing, you agree that your contribution is licensed under the
repository's [Apache License 2.0](LICENSE).
