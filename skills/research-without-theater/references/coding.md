# Research code: deliver a result that can be checked

## Start from the actual computation

Inspect the entry point, relevant input schema, method specification, and affected outputs. Establish units, experimental units, inclusion rules, missing-value handling, and the intended statistic where relevant. Use existing project conventions for environment and execution.

Implement the straightforward solution first. Keep scientific formulas visible rather than scattering them across generic wrappers. A new dependency or generalized framework should answer a present requirement such as scale, an existing interface, or repeated code that is actually changing.

## Technical repair or scientific choice?

| Situation | Action |
| --- | --- |
| CSV contains numeric strings; the documented statistic is already fixed | Parse the values, preserve the specified sample, run the calculation. |
| Implementation disagrees with an unambiguous documented equation | Restore that equation and explain any changed output. |
| Requested refactor preserves the estimator | Compare the original and refactored core results on identical inputs. |
| A failing step could be fixed either by excluding records or imputing them, with no specified rule | Describe the effect on the sample and estimator; request the choice before applying either. |
| User has already approved an exclusion rule | Implement it, record the resulting sample, and validate. |
| Correct code yields the opposite direction or an interval spanning the null | Report the observed estimate and uncertainty under the stated method. |

Correcting an established implementation may change a number. Explain the correction and its consequence. The need for a decision comes from an unresolved scientific choice, not from the mere fact that output changes.

## Make reported results traceable

Use a small result file, notebook record, or existing run log sufficient to recover input identity, code version, relevant package versions, parameters, and seed where used. Do not overwrite original data. Keep exploratory results distinguishable from planned tests.

For a short deterministic script, its named input, changed source, execution command, and saved result can already provide this traceability. Reuse that record before introducing run metadata or a status subsystem. An unmet prerequisite often needs only an actionable error; add a separate reporting mechanism when the workflow needs it.

For a deterministic calculation, avoid adding random seeds or unrelated environment inventories. For a stochastic experiment, expose the seed and record the versions that can affect its output. If exact reproducibility depends on hardware or nondeterministic kernels, document the observed limitation in the run record.

## Close the loop

Execute the affected path. Inspect values, sample counts, units, and generated artifacts relevant to the change. Compare pre/post values for a refactor with a tolerance justified by the computation. Restore intended failures if a fallback would conceal missing data or an invalid estimator.

A failing check justifies investigating that failure. It does not authorize changing the scientific target to obtain the expected result. Report a real blocker with the command or input needed to reproduce it; finish any independent deliverables.
