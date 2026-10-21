# Design decisions

Research Without Theater is a new, self-contained skill. Its organizing rule is: **add a mechanism, check, or sentence when it answers a concrete need in the current task.** The agent applies that rule internally and delivers the work.

## What we learned, and what we changed

| Source | Useful idea | Decision in this project |
| --- | --- | --- |
| Nature skills | Connect claims to evidence; give paragraphs an argument function; respect statistical meaning; divide main text and supporting detail by relevance. | Rebuild these ideas around the user's immediate deliverable. Omit suite routing, automatic comprehensive audits, fixed report lengths, and anticipatory reviewer defenses. |
| Stop That Shit Research | Start directly; let observed needs justify complexity; scale validation to the change. | Apply the same test to research code and prose. Omit Guard, hooks, task contracts, and runtime configuration. |
| Maintainer's research working conventions | Carry authorization forward; repair technical errors; distinguish method choices from implementation; run changed code. | Generalize the decision boundary. Omit personal paths, project history, tool preferences, and document-specific defaults. |

## A common decision rule

First identify the requested result and its existing scientific commitments. Then perform the smallest complete intervention that produces that result. A complete intervention includes the execution or evidence check needed to know whether it worked.

In code, an extra abstraction must solve an observed duplication, failure, scale, or interface problem. In prose, an extra sentence must advance the question, finding, explanation, contribution, or an interpretation-relevant limit. Both decisions depend on the present task.

## Authority and scientific commitments

A repair that restores an explicitly specified computation can proceed. Choosing a different estimand, exclusion rule, formula, or model requires a decision when the user has not authorized it. A surprising outcome alone is never a reason to change settings. A request for read-only review authorizes findings and proposed changes, not edits.

The skill asks for a decision only at that boundary and continues independent authorized work. This makes scope control useful without turning every action into an approval ceremony.

## Evidence and writing

The writing layer uses a contribution-led presentation rule: organize the paper around its strongest evidence-supported advantage, with the abstract and introduction moving from problem to gap to approach to hardest result. Each experiment has an argument function, and each claimed advantage names its comparison, metric, magnitude, and applicable conditions when the evidence permits.

This rule removes process reporting, anticipatory defenses, and self-undermining judgments. It does not permit changing a metric, baseline, sample, or comparison rule after seeing a result merely to improve its appearance. A different evaluation dimension is a scientific design choice and requires a reason and authorization when it changes the study's interpretation. A point estimate with an interval spanning zero remains an uncertain estimate. An observational association remains an association. A sensitivity result that changes the main interpretation belongs with that interpretation; procedural detail can move to Methods or supplementary material.

When the user asks for a defensive-writing review, the skill reports each actionable instance with the original wording, the problem, and a replacement. A limit that changes interpretation stays in the text even when it makes the presentation less favorable.

## Packaging

One entry point plus three optional guides. No calls to upstream skills, no external service requirement, no executable enforcement layer. Versioned synthetic examples and retained behavior runs make the first release reviewable. Structural checks and numerical regression are automated; prose and approval behavior receive human-readable semantic review.

The repository's release checks are for maintainers. Ordinary use of the skill does not require an audit report or a checklist.

## Tradeoffs

This release supplies instructions, not policy enforcement. Model compliance and evidence access still matter. A small set of synthetic cases can reveal specific failures and demonstrate behavior; it cannot establish general productivity gains. Experimental comparisons are reported with their actual environment and contamination limits.

