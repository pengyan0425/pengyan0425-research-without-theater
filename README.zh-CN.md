# Research Without Theater

Research Without Theater 是一个自包含的 Codex 技能，用于科研代码、数据分析和论文写作。
它优先直接完成工作，按改动需要控制验证范围，并让表述与现有证据相符。

技能除运行它的宿主已有能力外，不增加独立运行时、包安装、MCP 服务、API key 或网络
依赖。普通使用在该宿主内完成。

## 技能作用

技能围绕一条简洁的决策规则组织科研工作：只有当机制、检查或句子能回答当前任务的具体
需要时，才增加它。这条规则贯穿三个相互关联的使用场景：

- **执行：**读取真实输入和代码，修复已经明确的技术错误，运行修改后的分析，并保留报告
  数值与输入、参数和运行之间的来源记录。
- **写作：**围绕研究问题、发现、证据和贡献组织文字；删除预先防守的叙述，同时保留会
  改变解释的不确定性、限制和不利证据。
- **审阅：**给出发现和修改建议；可执行保持只读的检查，改动文件或会改变状态的重跑需要
  获得授权。

技能区分实现修复与科学选择。当材料或对话尚未授权时，改变 estimand、样本规则、
缺失值处理、公式或推断结论前，需要用户作出决定。意外结果和零结果也是结果；技能会
检查实现错误并如实报告，不会为了得到预期方向而重新调参。

它提供模型使用指导，不构成策略强制层，也不会代替项目规则、统计判断、来源核验或用户
对科学问题的决定。

## 安装

### Codex Skill Installer

可以请 Codex Skill Installer 从 GitHub 加载技能目录：

```text
$skill-installer install https://github.com/pengyan0425/pengyan0425-research-without-theater/tree/main/skills/research-without-theater
```

安装器会读取目录中的 `SKILL.md`，其中必须包含 `name` 和 `description`。Codex 通常
会自动发现新安装的技能；如果列表没有更新，重启 Codex。

也可以从 [Releases](https://github.com/pengyan0425/pengyan0425-research-without-theater/releases)
下载独立技能 ZIP 和 `SHA256SUMS`，解压得到完整的 `research-without-theater` 目录，
再按下面的本地复制说明安装。

### 本地复制

首次安装时，将完整技能目录复制到 Codex 的用户技能位置。下面的检查会在目标目录已存在时
停止，避免形成 `research-without-theater/research-without-theater` 嵌套目录：

```powershell
$source = (Resolve-Path ".\skills\research-without-theater").Path
$skillsRoot = Join-Path $HOME ".agents\skills"
$destination = Join-Path $skillsRoot "research-without-theater"
if (Test-Path -LiteralPath $destination) {
    throw "Skill directory already exists: $destination"
}
New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null
Copy-Item -LiteralPath $source -Destination $skillsRoot -Recurse
```

在 POSIX shell 中，使用 `$HOME` 下的同一目录：

```sh
source_dir="./skills/research-without-theater"
skills_root="$HOME/.agents/skills"
destination="$skills_root/research-without-theater"
if [ -e "$destination" ]; then
  echo "Skill directory already exists: $destination" >&2
  exit 1
fi
mkdir -p "$skills_root"
cp -R "$source_dir" "$skills_root/"
```

复制后的目录是自包含的：`SKILL.md`、三个按需读取的参考指南、界面元数据、`LICENSE`
和 `NOTICE` 会一起移动。请保留技能目录结构，不要把其中文件直接平铺到
`.agents/skills`。后续更新时，应先审查再有意识地替换已安装副本。

如需项目级安装，将同一目录放在 Codex 运行仓库的
`.agents/skills/research-without-theater` 下。Codex 分别发现仓库技能和用户技能；
如果两个已安装技能同名，Codex 可能同时显示它们，而不会合并内容。

## 使用

显式调用技能：

```text
$research-without-theater
```

随后提供科研任务和相关文件。清楚的提示会说明要求的交付物、已经固定的科学选择，以及
证据文件或来源位置。当任务与技能描述匹配时，也可以由 Codex 隐式选择该技能。

技能在当前宿主的权限和项目规则内工作。安装它不会替换全局 `AGENTS.md`、项目说明、
仓库约定或其他技能的局部规则。技能随包携带的边界要求会在复制技能时一起保留，不需要
额外配置运行时。

## 示例

### 代码

```text
请使用 $research-without-theater 修复并运行 analysis.py。
配对均值、样本标准差和标准误是既定方法。保留 data.csv，将结果写到 outputs/result.json，
并比较修改前后的核心数值。如果缺失值需要新的样本规则，先说明影响并询问我，不要自行选择。
```

```text
Use $research-without-theater to repair and run analysis.py.
The paired mean, sample SD, and standard error are the existing method.
Preserve data.csv, write result.json under outputs/, and compare the changed
results with the original implementation. If a missing value requires a new
sample rule, explain its effect and ask before choosing.
```

### 论文写作

```text
请使用 $research-without-theater 修改目标 Results 段落。
保留研究设计、估计值、不确定性，以及限制解释的不利结果。删除防御性叙述，
其他部分逐字保留；缺失事实要标明，不要补造。
```

```text
Use $research-without-theater to revise the target Results paragraph.
Keep the design, estimates, uncertainty, and the adverse result that limits
the interpretation. Remove defensive narration, preserve every other section,
and identify missing facts rather than inventing them.
```

仓库的[示例目录](examples/README.md)包含八个原创合成任务，覆盖执行、重构、方法选择、
意外结果、写作、关联表述、不利证据和局部修改。数据和论文段落均为合成内容，不构成真实
科研发现。

## 可选评估

普通使用不需要单独 API key。可选回放工具需要 Python 3.10 或更高版本，以及已经完成
认证的 Codex CLI；所选模型和配置还需要在宿主环境中可用。

运行确定性示例检查：

```sh
python scripts/check_examples.py
python scripts/check_examples.py --runs evals/runs
python scripts/verify_release.py
```

回放一次 agent 任务：

```sh
python scripts/run_eval.py --case 01-runtime-repair --condition skill
python scripts/run_eval.py --case 01-runtime-repair --condition baseline
python scripts/run_eval.py --case 05-defensive-prose --condition skill \
  --model gpt-6.1-sol --effort xhigh
```

`scripts/run_eval.py` 接受 `--case`、`--condition`、`--model` 和 `--effort`，
默认使用 `gpt-6.1-sol` 与 `xhigh`。每次运行都在临时复制件中进行，在
`evals/runs/` 导出经过选择且替换本地路径的证据；原始本地日志保持忽略状态。公开前
应人工检查导出内容是否包含隐私材料。

[评估协议](evals/README.md)说明案例、回放和审查标准。当前的[发布审查](evals/review.md)
记录初始运行及其限制；[独立语义审阅](evals/independent-review.md)检查初始技能产物和
两组 paired baseline。

## 证据与限制

`v0.1.0` 的证据范围有意保持较小。十一次模型执行的 return code 均为 0：八个初始
skill case、case 01 与 05 的两条 baseline，以及一次 case 03 targeted rerun。九次
skill 条件运行都读取了入口文件。两组 paired case 在两种条件下均成功，因此比较没有显示
相对 baseline 的质量提升。这些运行请求 `gpt-6.1-sol` 和 `xhigh`，使用 Codex CLI
`0.163.0`、Python `3.13.12` 与 Windows；CLI 没有提供服务端模型指纹。
`--ignore-user-config` 保留了认证信息，但没有隔离全局 instructions 或其他所有可发现
技能。这个新项目没有采用数据，也不提出性能或优越性主张。复用结果前请阅读
[评估协议](evals/README.md)、[发布审查](evals/review.md)和[独立语义审阅](evals/independent-review.md)；
这些证据只覆盖一个 Windows 环境中的合成测试，不构成一般性的质量评估。

## 其他 agent 与可移植性

本版本只在 Windows 上的 Codex 完成了运行测试。其他兼容 Agent Skills 的宿主可能
能够读取标准 `SKILL.md` 目录，但安装和行为均未在此验证。准确边界见
[可移植性说明](docs/portability.md)。

## 来源与许可

技能为独立撰写，采用 [Apache License 2.0](LICENSE)。可安装目录同时带有自己的
[LICENSE](skills/research-without-theater/LICENSE)和
[NOTICE](skills/research-without-theater/NOTICE)。

Nature skills 和 Stop That Shit 为设计提供了一般概念影响。来源版本、许可和概念关系
记录在[第三方说明](third_party/README.md)与[来源记录](docs/sources.md)。本产品不
分发复制而来的上游指令、Guard、hooks 或运行时代码。

参与贡献请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

[English](README.md)
