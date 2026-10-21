# Reproducible examples / 可复现案例

All data and manuscript passages here are synthetic and original. The Lee citation is a deliberately incomplete fictional placeholder. No scientific inference about a real study is intended.

本目录全部数据和文稿均为合成或原创案例。Lee 引用是故意不完整的虚构占位符，不代表真实研究。

| Case | Task / 任务 | Input prompt |
| --- | --- | --- |
| 01 | Repair a runtime error and execute / 修复运行错误并实际执行 | [Prompt](01-runtime-repair/prompt.md) |
| 02 | Preserve core numbers in a refactor / 重构保持核心数值一致 | [Prompt](02-refactor/prompt.md) |
| 03 | Explain a missing-data method choice and await a decision / 说明缺失值处理的方法影响并等待选择 | [Prompt](03-method-decision/prompt.md) |
| 04 | Report an unexpected and uncertain estimate / 如实报告反方向且不确定的估计 | [Prompt](04-unexpected-result/prompt.md) |
| 05 | Remove defensive prose, preserve evidence / 压缩防御性文字并保留证据强度 | [Prompt](05-defensive-prose/prompt.md) |
| 06 | Describe observational association / 准确表述观察性关联 | [Prompt](06-association/prompt.md) |
| 07 | Retain adverse main-result evidence / 正文保留影响结论的不利证据 | [Prompt](07-adverse-evidence/prompt.md) |
| 08 | Keep local revision local and identify missing facts / 控制局部返修范围并标明缺失事实 | [Prompt](08-local-revision/prompt.md) |

Run the numerical regression with `python scripts/check_examples.py`. Replay an agent task with `python scripts/run_eval.py --case 01-runtime-repair --condition skill`. The runner works on a disposable copy and retains sanitized artifacts under `evals/runs/`. It needs an authenticated Codex CLI; ordinary skill use has no additional API requirement. See [the evaluation protocol](../evals/README.md).

数值回归：`python scripts/check_examples.py`。行为复现：`python scripts/run_eval.py --case 01-runtime-repair --condition skill`。运行器在独立副本中执行，在 `evals/runs/` 保留脱敏产物；需要已登录的 Codex CLI，日常使用技能无需额外 API。评估方法见[协议](../evals/README.md)。

Chinese task equivalents / 中文任务示例：

1. 修复 `analysis.py` 的错误，按现有配对均值方法实际运行，将结果写入 `outputs/result.json`。
2. 简化 `summarize`，保持接口和估计方法，运行并比较重构前后的核心数值。
3. 按现有方法准备配对分析；缺失测量没有已批准的处理规则，请说明影响并推进能独立完成的工作。
4. 运行既定分析，按真实结果写 Results；原假设预期处理会提高结果变量。
5. 将防御性段落压缩为一句 Results，保留数值、方向及证据强度。
6. 根据观察性调查材料写一句准确的关联性结果。
7. 将随机划分和预先指定的空间留出结果写入主结果段落。
8. 只改目标段落，其他段落原样保留；保留缺失年份和样本量占位符，不补造事实。
