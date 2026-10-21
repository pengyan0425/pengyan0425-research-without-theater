# Source record

This record distinguishes conceptual influence from copied material and gives
the source points used for `v0.1.0`. All entries were checked on 2026-10-21.

## Upstream influence

| Source | Source point | License | Relationship |
| --- | --- | --- | --- |
| [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) | Verified commit [`473e8d7b1b918fe37208d3a5e143a3ac9af4c91b`](https://github.com/Yuan1z0825/nature-skills/tree/473e8d7b1b918fe37208d3a5e143a3ac9af4c91b) | Apache-2.0 | Conceptual influence |
| [lennney/stop-that-shit](https://github.com/lennney/stop-that-shit) | Public label `0.2.5`; release-page commit [`8bc1ac558167121e7f28d9fb0bec05c039952206`](https://github.com/lennney/stop-that-shit/commit/8bc1ac558167121e7f28d9fb0bec05c039952206) | MIT | Conceptual influence |

Nature skills informed the attention to evidence-matched claims, paragraph
function, statistical meaning, and the placement of supporting detail. A
locally installed copy may contain edits; the commit above identifies the
remote source examined for this record, not byte identity with every installed
copy.

Stop That Shit informed direct delivery, complexity justified by an observed
need, and validation proportional to the change. The public repository uses
the label `0.2.5`; no `v0.2.5` tag was verified. The release-page commit
identifies the published revision examined.

The `SKILL.md`, references, examples, scripts, and documentation were authored
for Research Without Theater. No upstream skill instructions, code, Guard,
hooks, task contracts, or runtime configuration are vendored or loaded at run
time. The applicable license texts and source-specific notices are retained in
[`third_party/`](../third_party/README.md), and the installable directory has a
self-contained [NOTICE](../skills/research-without-theater/NOTICE).

## OpenAI documentation

- [Build skills](https://developers.openai.com/codex/build-skills.md) documents
  the `SKILL.md` `name` and `description` fields, the Codex Skill Installer's
  GitHub-repository route, and the user skill location under `$HOME/.agents`.
- [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills)
  was also checked as the product documentation entry point.

## License text verification

The packaged Apache and MIT texts were checked with SHA-256:

| Path | SHA-256 |
| --- | --- |
| `LICENSE` | `CFC7749B96F63BD31C3C42B5C471BF756814053E847C10F3EB003417BC523D30` |
| `skills/research-without-theater/LICENSE` | `CFC7749B96F63BD31C3C42B5C471BF756814053E847C10F3EB003417BC523D30` |
| `third_party/nature-skills/LICENSE` | `C71D239DF91726FC519C6EB72D318EC65820627232B2F796219E87DCF35D0AB4` |
| `third_party/stop-that-shit/LICENSE` | `FD3DEDC4895151462FE37E0140082568534D6A39169065D68A5D521FDEFF8FA4` |
