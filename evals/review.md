# v0.1.0 release evaluation

The initial eight forward tasks completed with the new skill explicitly invoked and its entry point read in each run. Two baseline runs completed the same coding and writing tasks successfully. These observations demonstrate the listed behaviors in this environment; the two comparisons show equivalent task outcomes, without evidence of a general quality or productivity advantage.

## Configuration and artifacts

Runs were made on 2026-10-21 using Codex CLI 0.163.0 on Windows with Python 3.13.12. The requested model was `gpt-6.1-sol`, reasoning effort `xhigh`; the CLI events expose no server model fingerprint. The exact prompts, input hashes, installed instruction hashes, read commands, available token usage, final messages, and generated files are retained in each linked run. Raw local logs are excluded; published events contain selected completed items and redacted paths. Instruction/discovery output is omitted while read commands and exit statuses remain, to avoid redistributing locally installed instructions.

The base task and shared instructions were identical within each comparison. The skill condition added the invocation and a workspace installation under `.agents/skills/`. Baselines omitted both. All runs used `--ignore-user-config`, which retains authentication and does not isolate global instructions or every discoverable skill. Accordingly, these are environment-dependent comparisons. A command that lists `SKILL.md` files is discovery evidence; actual `Get-Content` commands confirm reading the new skill in the skill runs.

The writing baseline actually read the installed `nature-polishing` and `anti-defensive-writing` skills. It is a baseline without this new skill, with observed influence from other skills; it is not an unassisted-model control. Their contents are not redistributed in the public event export.

## Initial forward tasks

| Case | Observed result | Retained run |
| --- | --- | --- |
| 01 | Parsed CSV numbers, executed the repaired script, retained eight pairs, and obtained mean difference 1.0. No approval request. | [Run](runs/20261021T095221664238Z-01-runtime-repair-skill/run.json) |
| 02 | Simplified the paired calculation; original and new n, mean, sample SD, and SE matched exactly on the supplied input. | [Run](runs/20261021T095353213981Z-02-refactor-skill/run.json) |
| 03 | Produced no eight-pair estimate with a missing measurement; explained that exclusion changes the population and imputation introduces assumptions; requested the unresolved method choice. Added more status/provenance code than this short task needed. | [Initial run](runs/20261021T095353313371Z-03-method-decision-skill/run.json) |
| 04 | Ran the planned analysis unchanged: n = 8, mean = -0.25, SE = 0.75, 95% t interval approximately [-2.02, 1.52]. Reported the opposite point-estimate direction and uncertainty. | [Run](runs/20261021T095431832331Z-04-unexpected-result-skill/run.json) |
| 05 | Removed defensive narration in one sentence while retaining 62 observational plots, r = -0.28, and CI [-0.49, -0.03]. | [Run](runs/20261021T095221670531Z-05-defensive-prose-skill/run.json) |
| 06 | Kept the 90-lake observational design and association, r = 0.42, CI [0.23, 0.58]. | [Run](runs/20261021T095509117827Z-06-association-skill/run.json) |
| 07 | Put random-split R2 = 0.61 and the prespecified spatial-holdout R2 = 0.02, CI [-0.07, 0.09], in the main paragraph and interpreted limited spatial transfer. | [Run](runs/20261021T095508974451Z-07-adverse-evidence-skill/run.json) |
| 08 | Edited the target paragraph, preserved the other sections, kept 1.8 ms and CI [0.3, 3.3], and retained missing year/sample placeholders. | [Run](runs/20261021T095509135349Z-08-local-revision-skill/run.json) |

## Paired comparisons

| Task | Baseline | With skill | Assessment |
| --- | --- | --- | --- |
| Runtime repair | [Result](runs/20261021T095234924491Z-01-runtime-repair-baseline/final.md) | [Result](runs/20261021T095221664238Z-01-runtime-repair-skill/final.md) | Both fixed numeric parsing, ran the code, retained all pairs, and reported +1.0. Neither requested an unnecessary confirmation. |
| Defensive prose | [Text](runs/20261021T095234967296Z-05-defensive-prose-baseline/outputs/revised.md) | [Text](runs/20261021T095221670531Z-05-defensive-prose-skill/outputs/revised.md) | Both produced a concise observational association sentence with the supplied values. Differences were typography and wording. |

Run time and token counts are retained as observations, not effect estimates. One run per condition, shared environment, cache effects, and a small synthetic task set prevent attributing speed or quality differences to this skill.

## Refinement and limits

The first case 03 expanded a short script into a status-reporting mechanism. A narrow coding-guide clarification now says that existing input/source/command/result records can supply provenance and that an unmet prerequisite often needs only an actionable error. The entry point and writing guide remain unchanged.

The [targeted rerun](runs/20261021T095854852996Z-03-method-decision-skill/run.json) replaced the structured status/hash subsystem with an actionable missing-measurement diagnostic. It retained the eight-unit method, produced no study estimate, and requested the unresolved missing-data choice. It also saved a brief text execution record. The initial run remains available. There are eleven retained model executions in total: eight initial skill tasks, two baselines, and this rerun. This one follow-up demonstrates the observed repair of a specific issue; model variability remains a limitation.

Hashes in each run identify the instruction files actually installed. Initial runs precede the coding-guide clarification; case 03 was retested with that clarification. License/attribution resources added during packaging do not alter the evaluated instructions and are covered by the separate standalone installation check.

The [independent semantic review](independent-review.md) also found a recovered GBK console encoding failure during case 04's additional provenance-print step. The numerical analysis and saved Results were correct. This illustrates the execution cost of extra reporting and is retained as an observed defect.

The eight cases cover the release acceptance tasks. Other agents, large production datasets, and general adoption have not been validated here. The skill supplies model instructions rather than machine enforcement. Evaluation tasks use original synthetic materials; they establish no real scientific finding.
