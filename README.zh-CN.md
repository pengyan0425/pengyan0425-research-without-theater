# Research Without Theater

Research Without Theater ��һ���԰����� Codex ���ܣ����ڿ��д��롢���ݷ���������д����
������ֱ����ɹ��������Ķ���Ҫ������֤��Χ�����ñ���������֤�������

���ܳ����������������������⣬�����Ӷ�������ʱ������װ��MCP ����API key ������
��������ͨʹ���ڸ���������ɡ�

## ��������

����Χ��һ�����ľ��߹�����֯���й�����ֻ�е����ơ���������ܻش�ǰ����ľ���
��Ҫʱ��������������������ᴩ�����໥������ʹ�ó�����

- **ִ�У�**��ȡ��ʵ����ʹ��룬�޸��Ѿ���ȷ�ļ������������޸ĺ�ķ���������������
  ��ֵ�����롢����������֮�����Դ��¼��
- **д����**Χ���о����⡢���֡�֤�ݺ͹�����֯���֣�ɾ��Ԥ�ȷ��ص�������ͬʱ������
  �ı���͵Ĳ�ȷ���ԡ����ƺͲ���֤�ݡ�
- **���ģ�**�������ֺ��޸Ľ��飻��ִ�б���ֻ���ļ�飬�Ķ��ļ����ı�״̬��������Ҫ
  �����Ȩ��

��������ʵ���޸����ѧѡ�񡣵����ϻ�Ի���δ��Ȩʱ���ı� estimand����������
ȱʧֵ��������ʽ���ƶϽ���ǰ����Ҫ�û�����������������������Ҳ�ǽ�������ܻ�
���ʵ�ִ�����ʵ���棬����Ϊ�˵õ�Ԥ�ڷ�������µ��Ρ�

���ṩģ��ʹ��ָ���������ɲ���ǿ�Ʋ㣬Ҳ���������Ŀ����ͳ���жϡ���Դ������û�
�Կ�ѧ����ľ�����

## ��װ

### Codex Skill Installer

������ Codex Skill Installer �� GitHub ���ؼ���Ŀ¼��

```text
$skill-installer install https://github.com/pengyan0425/pengyan0425-research-without-theater/tree/main/skills/research-without-theater
```

��װ�����ȡĿ¼�е� `SKILL.md`�����б������ `name` �� `description`��Codex ͨ��
���Զ������°�װ�ļ��ܣ�����б�û�и��£����� Codex��

Ҳ���Դ� [Releases](https://github.com/pengyan0425/pengyan0425-research-without-theater/releases)
���ض������� ZIP �� `SHA256SUMS`����ѹ�õ������� `research-without-theater` Ŀ¼��
�ٰ�����ı��ظ���˵����װ��

### ���ظ���

�״ΰ�װʱ������������Ŀ¼���Ƶ� Codex ���û�����λ�á�����ļ�����Ŀ��Ŀ¼�Ѵ���ʱ
ֹͣ�������γ� `research-without-theater/research-without-theater` Ƕ��Ŀ¼��

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

�� POSIX shell �У�ʹ�� `$HOME` �µ�ͬһĿ¼��

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

���ƺ��Ŀ¼���԰����ģ�`SKILL.md`�����������ȡ�Ĳο�ָ�ϡ�����Ԫ���ݡ�`LICENSE`
�� `NOTICE` ��һ���ƶ����뱣������Ŀ¼�ṹ����Ҫ�������ļ�ֱ��ƽ�̵�
`.agents/skills`����������ʱ��Ӧ�����������ʶ���滻�Ѱ�װ������

������Ŀ����װ����ͬһĿ¼���� Codex ���вֿ��
`.agents/skills/research-without-theater` �¡�Codex �ֱ��ֲֿ⼼�ܺ��û����ܣ�
��������Ѱ�װ����ͬ����Codex ����ͬʱ��ʾ���ǣ�������ϲ����ݡ�

## ʹ��

��ʽ���ü��ܣ�

```text
$research-without-theater
```

����ṩ�������������ļ����������ʾ��˵��Ҫ��Ľ�����Ѿ��̶��Ŀ�ѧѡ���Լ�
֤���ļ�����Դλ�á��������뼼������ƥ��ʱ��Ҳ������ Codex ��ʽѡ��ü��ܡ�

�����ڵ�ǰ������Ȩ�޺���Ŀ�����ڹ�������װ�������滻ȫ�� `AGENTS.md`����Ŀ˵����
�ֿ�Լ�����������ܵľֲ����򡣼������Я���ı߽�Ҫ����ڸ��Ƽ���ʱһ����������Ҫ
������������ʱ��

## ʾ��

### ����

```text
��ʹ�� $research-without-theater �޸������� analysis.py��
��Ծ�ֵ��������׼��ͱ�׼���Ǽȶ����������� data.csv�������д�� outputs/result.json��
���Ƚ��޸�ǰ��ĺ�����ֵ�����ȱʧֵ��Ҫ�µ�����������˵��Ӱ�첢ѯ���ң���Ҫ����ѡ��
```

```text
Use $research-without-theater to repair and run analysis.py.
The paired mean, sample SD, and standard error are the existing method.
Preserve data.csv, write result.json under outputs/, and compare the changed
results with the original implementation. If a missing value requires a new
sample rule, explain its effect and ask before choosing.
```

### ����д��

```text
��ʹ�� $research-without-theater �޸�Ŀ�� Results ���䡣
�����о���ơ�����ֵ����ȷ���ԣ��Լ����ƽ��͵Ĳ��������ɾ��������������
�����������ֱ�����ȱʧ��ʵҪ��������Ҫ���졣
```

```text
Use $research-without-theater to revise the target Results paragraph.
Keep the design, estimates, uncertainty, and the adverse result that limits
the interpretation. Remove defensive narration, preserve every other section,
and identify missing facts rather than inventing them.
```

�ֿ��[ʾ��Ŀ¼](examples/README.md)�����˸�ԭ���ϳ����񣬸���ִ�С��ع�������ѡ��
��������д������������������֤�ݺ;ֲ��޸ġ����ݺ����Ķ����Ϊ�ϳ����ݣ���������ʵ
���з��֡�

## ��ѡ����

��ͨʹ�ò���Ҫ���� API key����ѡ�طŹ�����Ҫ Python 3.10 ����߰汾���Լ��Ѿ����
��֤�� Codex CLI����ѡģ�ͺ����û���Ҫ�����������п��á�

����ȷ����ʾ����飺

```sh
python scripts/check_examples.py
python scripts/check_examples.py --runs evals/runs
python scripts/verify_release.py
```

�ط�һ�� agent ����

```sh
python scripts/run_eval.py --case 01-runtime-repair --condition skill
python scripts/run_eval.py --case 01-runtime-repair --condition baseline
python scripts/run_eval.py --case 05-defensive-prose --condition skill \
  --model gpt-6.1-sol --effort xhigh
```

`scripts/run_eval.py` ���� `--case`��`--condition`��`--model` �� `--effort`��
Ĭ��ʹ�� `gpt-6.1-sol` �� `xhigh`��ÿ�����ж�����ʱ���Ƽ��н��У���
`evals/runs/` ��������ѡ�����滻����·����֤�ݣ�ԭʼ������־���ֺ���״̬������ǰ
Ӧ�˹���鵼�������Ƿ������˽���ϡ�

[����Э��](evals/README.md)˵���������طź�����׼����ǰ��[�������](evals/review.md)
��¼��ʼ���м������ƣ�[������������](evals/independent-review.md)����ʼ���ܲ����
���� paired baseline��

## ֤��������

`v0.1.0` ��֤�ݷ�Χ���Ᵽ�ֽ�С��ʮһ��ģ��ִ�е� return code ��Ϊ 0���˸���ʼ
skill case��case 01 �� 05 ������ baseline���Լ�һ�� case 03 targeted rerun���Ŵ�
skill �������ж���ȡ������ļ������� paired case �����������¾��ɹ�����˱Ƚ�û����ʾ
��� baseline ��������������Щ�������� `gpt-6.1-sol` �� `xhigh`��ʹ�� Codex CLI
`0.163.0`��Python `3.13.12` �� Windows��CLI û���ṩ�����ģ��ָ�ơ�
`--ignore-user-config` ��������֤��Ϣ����û�и���ȫ�� instructions ���������пɷ���
���ܡ��������Ŀû�в������ݣ�Ҳ��������ܻ���Խ�����š����ý��ǰ���Ķ�
[����Э��](evals/README.md)��[�������](evals/review.md)��[������������](evals/independent-review.md)��
��Щ֤��ֻ����һ�� Windows �����еĺϳɲ��ԣ�������һ���Ե�����������

## ���� agent �����ֲ��

���汾ֻ�� Windows �ϵ� Codex ��������в��ԡ��������� Agent Skills ����������
�ܹ���ȡ��׼ `SKILL.md` Ŀ¼������װ����Ϊ��δ�ڴ���֤��׼ȷ�߽��
[����ֲ��˵��](docs/portability.md)��

## ��Դ������

����Ϊ����׫д������ [Apache License 2.0](LICENSE)���ɰ�װĿ¼ͬʱ�����Լ���
[LICENSE](skills/research-without-theater/LICENSE)��
[NOTICE](skills/research-without-theater/NOTICE)��

Nature skills �� Stop That Shit Ϊ����ṩ��һ�����Ӱ�졣��Դ�汾�����ɺ͸����ϵ
��¼��[������˵��](third_party/README.md)��[��Դ��¼](docs/sources.md)������Ʒ��
�ַ����ƶ���������ָ�Guard��hooks ������ʱ���롣

���빱�����Ķ� [CONTRIBUTING.md](CONTRIBUTING.md)��

[English](README.md)
