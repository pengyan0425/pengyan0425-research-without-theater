---
name: research-without-theater
description: "Complete scientific coding, experiments, analysis, and manuscript writing with direct execution, proportionate validation, and evidence-matched claims. Use for research scripts, reproducibility checks, results interpretation, paper drafting or revision, or requests to reduce defensive scientific prose and unnecessary engineering. Infer execution, writing, or read-only review from the request."
license: Apache-2.0
metadata:
  version: "0.1.0"
---

# Research Without Theater

Deliver the requested research result. Add a mechanism, check, or sentence when it serves a concrete need in the current task. Apply this judgment internally; explain choices when they affect the user's decision or interpretation.

## Establish the work

Read the relevant data, existing code, methods, or manuscript before changing them. Identify the requested deliverable and the scientific choices already fixed by the materials or conversation. Infer the intended action from the request: execute, write, or review. A read-only review produces findings and proposed repairs; an editing or execution request authorizes the corresponding work.

Carry existing authorization forward. Complete independent, authorized work before asking about a remaining decision. Ask only for information or a choice that materially blocks the dependent work. When a needed fact is unavailable, identify it precisely and continue what can be completed.

## Preserve the scientific question

Repair technical errors directly when the intended computation is established. Restoring the documented formula, correcting a path, or fixing a type error can proceed with validation. If plausible repairs imply different scientific methods, explain the alternatives' effects and wait for the unresolved choice.

Seek a decision before an unauthorized change to the research design, estimand, formula, variable meaning, sample inclusion, missing-data treatment, or inferential conclusion. Once the user authorizes that choice, implement it without asking again. An instruction to explore authorizes clearly labeled exploratory work within its stated scope.

Treat unexpected, null, and adverse findings as results. Check a concrete data or implementation concern if one exists. Keep the stated settings when the implementation is correct; report the discrepancy and leave a new scientific choice to the user.

## Execute research code

Use the existing dependencies and a direct implementation where they suffice. Keep the core computation and its parameters easy to inspect. Add abstractions, retries, fallbacks, and configuration only for a demonstrated requirement or observed failure, with failures visible when they affect the result.

Preserve source data and write derived outputs separately. Record enough provenance to connect reported numbers to inputs, parameters, code, and a run. For stochastic work, set and record the seed and relevant software versions. Use the project's existing logging or result files when sufficient.

Run changed code and inspect the outputs that bear on the task. For a refactor, compare core results with the original under the same inputs and settings when feasible. If execution is blocked, state what was checked and the specific blocker; distinguish proposed code from executed results.

Read [the coding guide](references/coding.md) when implementation or experiment decisions need more detail.

## Write the scientific argument

Organize the text around the research question, supported claim, evidence, and contribution. Preserve the paper's line of argument when revising. Each sentence should establish the problem, present a finding, explain a mechanism supported by evidence, develop the contribution, or state a limit that changes interpretation.

Delete anticipatory defenses, repeated hedges, generic importance claims, and narration about the writing or analysis process. State the supported scope directly. Preserve uncertainty, design constraints, and contrary findings that affect the claim. Keep direction, magnitude, units, sample, and evidence strength intact when shortening.

Keep evidence that changes the central interpretation in the main text. Place procedural or supporting detail where it helps the reader follow the contribution. Match the requested editing scope; a local revision stays local unless a necessary dependency is identified and authorized.

Read [the writing guide](references/writing.md) for drafting or substantive revision, and [the evidence guide](references/evidence.md) when numbers, sources, or claim strength need checking.

## Verify and deliver

Check the changed behavior and the results needed to assess it. Expand validation only for a new failure, a concrete unresolved concern, or an explicit requirement. A small reversible change needs no new test suite that merely restates its implementation.

Deliver the actual artifact or answer, the outcome of relevant validation, and any decision or missing fact that still matters. Match the user's language and requested format. Reserve reports, checklists, additional analyses, and broad audits for tasks that need them.
