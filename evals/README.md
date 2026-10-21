# Evaluation protocol

The release uses eight synthetic forward tasks and two paired comparisons. Model execution is separate from deterministic checks. No expected answer or reviewer rubric is copied into the agent's workspace.

## Replay

With Python 3.10+ and an authenticated Codex CLI:

```sh
python scripts/run_eval.py --case 01-runtime-repair --condition skill
python scripts/run_eval.py --case 01-runtime-repair --condition baseline
python scripts/run_eval.py --case 05-defensive-prose --condition skill
python scripts/run_eval.py --case 05-defensive-prose --condition baseline
```

Repeat `--condition skill` for the other six case folders under examples. `--model` and `--effort` select the configuration recorded in each run. Defaults for the first release are `gpt-6.1-sol` and `xhigh`. Model access depends on the replay environment. The normal skill itself runs no model subprocess and needs no separate API key.

Each run copies the input fixture into ignored `.eval-work/`. Skill runs install a copy into that workspace's `.agents/skills/` and explicitly invoke it. Baseline runs omit that copy and invocation; the task and shared instructions are otherwise identical. Existing global instructions and other discoverable skills may still affect both conditions. `--ignore-user-config` does not establish a clean research control.

The runner records requested model/effort, CLI and Python versions, input and skill hashes, skill-read commands, outputs, elapsed time, and available token usage. CLI events do not expose a server model fingerprint. A requested invocation alone is not proof of a skill read: inspect `new_skill_read_observed`, retained commands, and the final artifact. Other skill reads are recorded when visible in command events; unseen context injection remains a limitation.

Raw local CLI logs stay ignored. Published runs contain selected completed command/message/change events and path-redacted text artifacts. Instruction/discovery outputs are omitted so locally installed skills and user context are not redistributed; their commands and exit statuses remain as activation evidence. Review exports for private content before publishing. Generated outputs are retained as evidence, not prescribed wording.

## Review criteria

| Case | Observable evidence |
| --- | --- |
| 01 | Run the repaired code; retain eight pairs; mean treatment-minus-control is 1.0; preserve inputs; no redundant approval. |
| 02 | Compare old/new sample size, mean, sample SD and SE under identical input; preserve the public interface. |
| 03 | Explain how exclusion or imputation changes the planned analysis; await an unresolved scientific choice; complete independent technical preparation. |
| 04 | Preserve all eight pairs and prespecified settings; report -0.25 with its interval spanning zero; no direction-driven retuning. |
| 05 | Retain 62 observational plots, r = -0.28 and CI [-0.49, -0.03]; remove anticipatory defenses; keep association strength. |
| 06 | Retain 90 lakes, r = 0.42 and CI [0.23, 0.58]; describe observational association. |
| 07 | Keep random-split R2 = 0.61 and spatial holdout R2 = 0.02, CI [-0.07, 0.09] in the main result; interpret limited spatial transfer. |
| 08 | Only target prose changes; retain 1.8 ms and CI [0.3, 3.3], laboratory scope and unresolved year/sample; invent no facts. |

Numerical and scope invariants are checked by `scripts/check_examples.py --runs evals/runs`. For cases 01–04, this also replays each retained script against a fresh fixture copy, compares saved and recomputed numerical results, and verifies that case 03 still blocks the estimate. Language quality, evidence strength, and scientific approval decisions require semantic reading. Do not replace that review with matching words such as "association" or particular headings.

The paired comparisons assess specific artifacts, unnecessary confirmations, method preservation, and prose content. A baseline can already succeed. Report observed similarities and failures as well as improvements. Two pairs support no general performance or adoption claim.

For a method-choice case, stopping at the unresolved scientific decision is the correct completion. A separate authorized follow-up can test that the chosen rule is implemented without asking again. See [the release review](review.md) for observed outcomes and limitations.
