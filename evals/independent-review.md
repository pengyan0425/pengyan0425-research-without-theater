# Independent semantic review

**Scope.** I reviewed the completed initial skill runs for all eight cases, including each case's `prompt.md`, raw input/method files, `final.md`, `analysis.py` where present, `outputs/`, `events.json`, and `run.json`. I also compared the 01 and 05 baseline artifacts with their skill artifacts. I did not use `evals/README.md` or other review documents, and I did not edit examples, the skill, scripts, or retained runs. The later 03 rerun is outside this review; only the initial completed run is assessed. This is independent semantic review within the same agent environment, not blinded external validation. Review model: inherited parent model / not independently fingerprinted.

## Findings

1. **Scientific completion is correct in the completed cases.** 01 computes the specified eight-pair treatment-minus-control mean (`1.0`) after only repairing CSV string conversion. 02 performs a behavior-preserving refactor: the original and refactored results are exactly equal, with the same result fields, and the original code/result are retained. 04 correctly reports mean `-0.25`, 95% CI `[-2.02, 1.52]`, and does not turn the unexpected direction or interval spanning zero into support for the hypothesized increase. 06 and 07 preserve the association language, sample, estimates, and uncertainty. 08 changes only the target paragraph when checked against the supplied manuscript.

2. **The missing-data decision in 03 was handled correctly.** Unit D has a missing treatment measurement; `methods.md` fixes the eight-pair population and approves neither exclusion nor imputation. The run therefore produces no numerical estimate, records the precise blocker, and asks for a missing-data decision. It does not silently exclude D or invent a replacement value. Its confirmation request is appropriate because the choice changes the scientific population.

3. **Observed complexity in 03 is a defect in execution economy.** The initial run took 208.72 seconds, used 10 commands (two failed), 5,912 output tokens, and added a status/hash/reporting subsystem plus synthetic-data validation. The final claim is scientifically sound, but the simple unmet prerequisite could have been reported with a small actionable error. This is unnecessary machinery around a task whose requested output is blocked.

4. **A concrete 04 execution defect occurred without changing the result.** The first provenance-print command failed with `UnicodeEncodeError` because the Windows console used GBK; a subsequent UTF-8 command succeeded. The paragraph and numeric result are valid, and `outputs/run.json` was written before the failed print, but the added provenance step created a real avoidable execution failure.

5. **No unauthorized scientific choice was observed.** The runs did not alter the specified estimand, formula, variable definitions, all-eight-pair sample, statistical method, or causal boundary. The extra 03 status file and the 04 provenance file are operational additions; neither changes the scientific result.

6. **Baseline comparison, without a superiority claim.** For 01, baseline and skill produced the same `analysis.py` and byte-identical `result.json`; the skill run used fewer events and elapsed less time, while baseline performed an additional independent exact-fraction recomputation. The skill still ran and inspected the result and preserved input hashes, but its verification record is less explicit than baseline's extra arithmetic check.

7. **Baseline comparison, without a superiority claim.** For 05, both outputs are one sentence with the same 62-plot observational association, `r = -0.28`, and 95% CI `-0.49 to -0.03`. Baseline rendered the statistic in Markdown italics and used Unicode minus signs; skill used plain `r` and ASCII hyphens. That is a formatting difference only. Baseline used more events and more skills; that does not establish general superiority.

## Per-case outcome

| Case | Outcome | Concrete artifact evidence |
| --- | --- | --- |
| 01-runtime-repair | Pass | Numeric conversion repair only; eight pairs; mean difference `1.0`; result saved; source CSV and methods unchanged. |
| 02-refactor | Pass | `summarize(control, treatment)` preserved; exact original/refactored match: `n=8`, mean `1.0`, sample SD `1.8516401995451028`, SE `0.6546536707079771`; comparison evidence retained. |
| 03-method-decision | Pass as correctly blocked | No numerical result is appropriate because D/treatment is `NA`; status identifies seven complete of eight enrolled pairs and requests authorization; no exclusion or imputation was applied. Minor excess complexity as noted above. |
| 04-unexpected-result | Pass | Prespecified eight-pair analysis gives `-0.25` with `[-2.02, 1.52]`; Results explicitly records the opposite direction and interval spanning zero; one non-scientific provenance-print failure was recovered. |
| 05-defensive-prose | Pass | One Results sentence retains observational language, 62 plots, coefficient `-0.28`, and CI `[-0.49, -0.03]`; no causal claim. Baseline differs in typography only. |
| 06-association | Pass | One sentence retains the cross-sectional survey, 90 lakes, direction, Pearson `r=0.42`, and CI `[0.23, 0.58]`; association language is preserved. |
| 07-adverse-evidence | Pass | Both the random-split `R2=0.61` and prespecified spatial-holdout `R2=0.02` with CI `[-0.07, 0.09]` remain in the Results paragraph; limited spatial transfer is the stated finding. |
| 08-local-revision | Pass | Only the target paragraph changed; other sections were verified byte-for-byte; 1.8 ms, CI `[0.3, 3.3]`, citation placeholder, sample-size placeholder, and missing-fact report are preserved. |
