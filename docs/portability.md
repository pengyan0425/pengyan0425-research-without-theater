# Portability

Research Without Theater targets Codex. Its installable directory follows the
standard `SKILL.md` layout, but the current release evidence comes from one
Windows Codex environment. Compatibility with another Agent Skills host is
possible in principle and untested here.

| Surface | Status in `v0.1.0` |
| --- | --- |
| Codex CLI on Windows | Used for the recorded model evaluations |
| Codex local skill discovery | Covered by the documented user and project locations |
| GitHub Skill Installer route | Documented for the public repository; separate from the recorded model evaluations |
| POSIX local-copy route | Documented; not run in the recorded Windows evaluation |
| Other Agent Skills-compatible hosts | Untested installation and behavior |

## Host requirements

The skill itself adds no separate runtime, package installation, MCP server,
API key, or network dependency beyond capabilities already present in the host.
It executes the requested research work through that host's tools and
permissions. A task that requires source verification can use the evidence or
search capability the host already provides.

Ordinary use requires no Codex CLI subprocess. The optional evaluation tools
require Python 3.10 or newer and an authenticated Codex CLI. The recorded runs
used Python `3.13.12`, Codex CLI `0.163.0`, requested model `gpt-6.1-sol`, and
reasoning effort `xhigh` on Windows. These versions describe the observed
environment and do not define a support guarantee for other versions.

## Instruction precedence

The skill works alongside the host's current instructions. Installing or
copying it does not replace a global `AGENTS.md`, project instructions,
repository conventions, or another skill's local rules. A read-only review may
run checks that do not change state; edits and state-changing reruns require
authorization from the request or conversation.

## Evaluation boundary

The replay runner uses `--ignore-user-config`, but this retains authentication
and does not isolate global instructions or every discoverable skill. The CLI
does not expose a server model fingerprint. Results from one model invocation
therefore cannot be treated as a clean cross-agent benchmark or as evidence
that another host will follow the same instructions.

The semantic review is independent within the same agent environment, not a
blinded external evaluation. See [the evaluation protocol](../evals/README.md),
[the release review](../evals/review.md), and [the independent semantic
review](../evals/independent-review.md) for the recorded scope.
