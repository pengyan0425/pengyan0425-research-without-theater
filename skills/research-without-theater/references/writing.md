# Research prose: present the strongest supported contribution

## Build the paper around its contribution

Treat the paper as a focused presentation of a research contribution, not a
chronological report of the work. Identify the research question, the gap that
matters, the approach that addresses it, the strongest result, and the claim
that the evidence supports. Order the abstract, introduction, Results, and
Conclusion around that argument.

Use this opening sequence when it fits the study:

> problem → gap → approach → strongest result

The conclusion should reinforce the contribution and its meaning. It should
not add a late self-critique that was absent from the evidence-based argument.
Write the strongest supported contribution first, then add a limit only when it
changes how that contribution should be interpreted.

## Give every sentence and experiment a job

Keep a sentence when it establishes the problem, reports a finding, explains a
mechanism supported by evidence, develops the contribution, or states a limit
that changes interpretation. Keep an experiment when it answers a defined
question, tests a stated mechanism, establishes a comparison, or bounds the
claim. Delete process narration, decorative experiments, and sentences whose
only purpose is to reassure the reader that the authors were careful.

Organize Results by the argument they establish rather than by the order in
which analyses were attempted. Methods and Supplementary material can carry
procedural detail when moving it does not hide evidence that changes the main
interpretation.

## State advantages and tradeoffs directly

When the evidence supports an advantage, state the comparison, metric,
magnitude, and applicable conditions. Do not make the reader discover the
contribution by reconstructing a table. When a result is not best on one
metric, explain the actual objective difference or an evidence-supported
tradeoff. For example, a method may improve calibration while giving up some
peak accuracy, or improve transfer across sites while sacrificing performance
on a single in-domain split. Use the measured values and the study's actual
objective to make that explanation.

Do not change a metric, baseline, sample, or comparison rule after seeing the
result merely to create a stronger appearance. Changing the evaluation
dimension can be scientifically justified, but it is a design choice. State
the reason and obtain the user's decision when it changes the study's design,
interpretation, or conclusion.

## Remove defensive self-commentary, preserve real limits

Delete anticipatory defenses, repeated hedges, generic importance claims,
self-undermining judgments, and narration about the writing or analysis
process. Prefer the measured finding and its supported scope. Common warning
signals include:

- “Unfortunately, our model only achieved ...”
- “Our study is by no means exhaustive.”
- “It is important to emphasize that ...” when the following fact is already
  stated plainly.
- “The method is still clearly behind ...” when a direct comparison gives the
  actual difference.
- “The effect was limited” when the relevant estimate and uncertainty are
  available.

Replace the judgment with evidence or a concrete interpretation. For example:

```text
We acknowledge that our study is by no means exhaustive. It is important to
emphasize that these results should be interpreted cautiously. In our
observational sample of 48 catchments, vegetation cover was associated with
lower peak runoff (r = -0.31, 95% CI -0.54 to -0.03). We do not intend to
imply that causation has been conclusively established.
```

becomes:

```text
Across 48 observed catchments, vegetation cover was associated with lower peak
runoff (r = -0.31, 95% CI -0.54 to -0.03).
```

The observational design and association wording preserve the evidence
boundary. If causal identification is central to the argument, state the
actual identification constraint where it affects that argument.

Use the same repair pattern for numerical comparisons:

```text
Unfortunately, our model only achieved an F1 of 0.82.
→ The model achieved an F1 of 0.82.

Our model is still far behind the baseline.
→ F1 was 0.82, compared with 0.87 for the baseline.

The effect was limited to the western sites.
→ The association was observed in the western sites (estimate and interval).
```

The last replacement requires the estimate, interval, and intended scope. If
those facts are unavailable, mark the missing fact instead of inventing it.
Keep a negative or qualified formulation when it is required for accuracy or
directly answers the user's question.

## Keep evidence that changes interpretation

Presentation should be selective, but selection must follow the contribution
and the evidence. Keep a null or adverse result when it changes the central
claim, including an interval spanning zero, an influential exclusion, a failed
replication, a reversed subgroup result, a spatial holdout failure, or an
important sensitivity analysis. Pair it with the claim it qualifies and
explain the resulting scope.

Do not turn an association into an intervention effect, an uncertain estimate
into evidence of no effect, or a proposed analysis into a completed one. Keep
direction, magnitude, units, sample, uncertainty, and inference strength
unchanged when compressing prose. Preserve exploratory labels and distinguish
exploratory from confirmatory analysis.

## Perform a local defensive-writing review

When asked to inspect supplied text, work sentence by sentence and report each
actionable instance in this form:

```text
原文：...
问题：指出自我削弱、过程汇报、重复限定、无论证职责，或说明该限定为何必须保留。
改法：给出保留事实、数字、证据强度和论证功能的替代句。
```

For an English manuscript, keep the replacement in English and explain the
reason in the user's language if requested. Do not silently broaden a local
editing request into a full-paper rewrite. If a sentence is already accurate
and serves an interpretation-relevant limit, report that it should remain.

## Final evidence check

Compare the revised passage with the source. Confirm that every retained
number, unit, direction, sample, uncertainty statement, citation, and causal
verb remains supported. Confirm that the abstract and introduction name the
problem, gap, approach, and strongest result, and that every retained
experiment advances the argument. Mark an unavailable fact precisely, such as
`[sample size needed]`, rather than filling it from assumption.

