# Feedback (DSH)

评价对象：`hedge-fund-mini` 全部 15 课、根目录 `run.py` 与 `readme.md`。

评价方式：通读 15 份 lesson README 与第 13–15 课的完整代码；实际运行
lesson 9 / 14 / 15；对 15 份 README 的文件树标注做自动核对；对配置优先级
做离线实测。本文件按提问顺序整理该次对话的全部结论。

---

## 一、总体评价（新建的 13–15 课 + 全课程）

### 1.1 实际验证过的事实

不只读代码，能跑的路径都跑了一遍（使用根目录 `.env` 中已有的配置）：

| 验证项 | 结果 |
| --- | --- |
| `run.py --lesson 15 --ticker AAPL` | 通过，输出形状与 README 一致（BUY 76/100） |
| `run.py --lesson 14 --ticker AAPL --temperature 0` | 通过，CLI 覆盖生效 |
| `run.py --lesson 9 --ticker AAPL`（老课回归） | 通过 → `run.py` 的两段式解析未破坏旧课 |
| `run.py --lesson 9 --ticker AAPL --temperature 0` | 正确报 `unrecognized arguments` |
| 配置优先级离线实测 | 与 README 表格一致；`LLM_TEMPERATURE=0.2` 被 `config.toml` 压回 `0.0` |
| 15 份 README 文件树标注自动核对 | **141 条标注全部准确**，无一条 "unchanged" 实际已改动 |
| 15 份 README 的 run 命令 vs 目录号 | 全部对应，根 `readme.md` 清单同步 |

141 条标注零错误，说明工作纪律很好，值得先记一笔。

### 1.2 做得好的地方

1. **增量结构是真的增量。** 13→14 只动 `config.py`、`lesson.py` 与新增的
   `config.toml`；14→15 只新增 `output.py` 并改一行打印。"复制前课、不改无关
   文件"这一条守住了，相邻课 diff 干净。
2. **`run.py` 的 `add_arguments` 钩子设计正确。** 先 `parse_known_args()` 取
   `--lesson`，再让选中课注册自己的参数，最后 `parse_args()`——是该需求的
   标准解法，且旧课完全无感。
3. **表现层分离得干净。** `output.py` 是纯函数、无副作用、不发模型调用；
   API key 既不进分析 JSON 也不进报告。
4. **顺序有教学理由。** "先让模型跑通 → 再讲配置分层 → 最后讲展示"，比先讲
   配置合理得多，README 也写出了理由。

### 1.3 主要问题（按优先级）

**1. `confidence` 公式让 lesson 9 的核心对比变成摆设。**
`utils/confidence.py` 的返回值恒在 50–100 之间（completeness=100 时），权重比
最多约 2:1。实测本次运行 equal average 与 confidence-weighted average
**都是 76/100**。学生看完 lesson 9 会得出"加权平均根本没用"的结论。
建议放大动态范围（允许低到 10 左右），或在 README 中承认两者常常相同并给出
一个能看出差异的构造例子。

**2. 配置优先级顺序反直觉，且随课发布的 TOML 架空了 env 层。**
`config.py` 的顺序是 `defaults < env < TOML < CLI`，与 12-factor、
pydantic-settings 等主流（env > 文件）相反。更麻烦的是 `config.toml` 写死了
`temperature` 和 `reasoning_effort`，所以 README 表格里 `LLM_TEMPERATURE=0.2`
那个例子**在默认配置下永远不生效**——实测：带这两行时 env 的 0.2 被压成 0.0，
注释掉才生效。学生照文档做实验会得到"文档与现实不符"的结果。
建议注释掉这两行，或另附一份 toml 作对照，并在 README 里说明"为什么文件压过
环境"。

**3. LLM 层在文档化的那条运行路径上没有决策价值。**
实测：Buffett 规则分 77 → 模型返回 **77**；Lynch 规则分 74 → 模型返回 **74**。
两次都精确复读规则分，只换了措辞。同时 `business_summary` 与
`recent_headlines` 从 lesson 1 起就声明、始终为空且从未被使用——这正好是让 LLM
产生"规则看不到的增量"的天然入口。建议二选一：把这类信息接进 prompt，或在
README 中明说"这一版模型只负责复述"。

**4. `StockSnapshot` 有 5 个死字段。**
`business_summary`、`target_mean_price`、`forward_pe`、`current_ratio`、
`recent_headlines` 从 lesson 1 声明至今既未填充也未使用（`market_cap` 填了但下游
也没用）。而 `01-start/README.md` 写的是 "The model includes fields later lessons
will use"——14 课之后仍未兑现。建议删除，或在某一课真正用起来。

**5. 信号阈值重复三处。**
70/45 两个魔法数硬编码在 `agents/warren_buffett.py`、`agents/peter_lynch.py`
与 `orchestrator.py::_signal_from_score`。课程一直强调"agent 接口一致、逻辑可
对比"，这里恰好是收成 `utils/signals.py` 里一个 `signal_from_score()` 的最佳
教学点。

**6. `--config` 指到不存在的文件会抛裸 traceback。**
README 只说"文件必须存在"，没说会看到什么。打错路径是学生很容易触发的路径，
加三行友好报错更符合 `AGENTS.md` 中 "likely to occur during the documented run"
的标准。

### 1.4 小问题清单

- `01-start/README.md` 的 What's here 树**没有任何 new/changed 标注**；
  lesson 2 用 "changed from lesson 1"，lesson 3 起改用 "changed:"——三种写法并存。
- `llm/__init__.py` 是空文件，而 `agents/`、`utils/` 的 `__init__.py` 有 docstring。
- 根 `readme.md` 表格 13–15 行的 padding 未对齐（渲染无问题，只是源文件看着乱）。
- `.env.example` 中 `LLM_MODEL=gpt-6-luna` 是占位模型名，README 只说"填
  `LLM_API_KEY`"；照做的学习者第一次调用就会撞模型不存在的错误，建议加注释说明
  这两行要替换成自己的服务商。
- `pyproject.toml` 声明了 `typer>=0.16.0`，课程代码中一次都没用过（CLI 全是
  `argparse`）。建议要么用它演示 CLI 层，要么从依赖中删除。

### 1.5 如果只做最小改动

1. 注释掉 `15-complete-report/config.toml` 的两行（或改优先级顺序），让 README
   的 env 例子真的成立。
2. 在 lesson 9 README（以及 confidence 公式）中诚实交代"两种平均常常相同"，
   或调宽 confidence 范围。
3. 让 LLM 产生可观察的差异，或在 lesson 10 README 中点破"模型此刻只是复述"。

---

## 二、从 `.env` 获取信息的方式一共出现过几种

**一共 4 种**，都在 lesson 10 之后，正好对应"读 env 这件事该由谁负责"的四次
搬迁。Lesson 1–9 完全不碰 `.env`。

| # | 课 | 谁读 env | 写法 | 缺变量时 |
| --- | --- | --- | --- | --- |
| 1 | 10 | agent 自己 | 3 个显式 `os.getenv` | 报错 |
| 2 | 11–12 | 共享客户端 | 3 个显式 `os.getenv` | 报错 |
| 3 | 13 | `load_config()` | 3 个显式 `os.getenv` → `RuntimeConfig` | 报错 |
| 4 | 14–15 | `load_config()` 分层合并 | 循环拼变量名 | 只有 `LLM_API_KEY` 必需 |

**1. lesson 10 —— 在 agent 内部读**
`10-first-llm-call/agents/warren_buffett.py:14-18` 在
`WarrenBuffettAgent.__init__` 中 `os.getenv("LLM_MODEL")` / `LLM_BASE_URL` /
`LLM_API_KEY`，三个都取不到就 `RuntimeError`。`ChatOpenAI` 也在 agent 里直接构造。

**2. lesson 11 —— 搬进共享客户端**
`11-shared-llm-interface/llm/openai_client.py:11-15` 接管这三行，逻辑一字未改，
只是换位置。lesson 12 保持不变，于是同一个客户端开始服务两个 agent。

**3. lesson 13 —— 搬进 config 对象**
`13-runtime-settings/config.py:18-25` 把三行收进 `load_config()`，返回
`RuntimeConfig`。这是关键转折：客户端从此完全看不到 env，只接收一个配置对象，
"设置从哪来"与"怎么用设置"分家了。

**4. lesson 14–15 —— 变成分层合并**
`15-complete-report/config.py:32-35` 不再逐个硬编码，而是在 settings 字典上循环
`os.getenv(f"LLM_{name.upper()}")`，于是 `LLM_TEMPERATURE`、
`LLM_REASONING_EFFORT` 也进入 env 层；同时 `model` / `base_url` 从"必需"降级为
"有默认值"，只有 `api_key` 仍然必需。

**两个维度的变化，以及一件从未改变的事：**

- **读取位置**变了 3 次：agent → 共享客户端 → config 对象。
- **读取写法**出现 2 种：逐变量硬编码 `os.getenv("LLM_X")`（10–13），与在字典上
  循环生成变量名 `os.getenv(f"LLM_{name.upper()}")`（14–15）。
- **`.env` 的加载方式从头到尾只有一种**：始终是 `lesson.py` 里的
  `load_dotenv(".env")`（10/11/12 的第 9 行、13 的第 11 行、14 的第 32 行、
  15 的第 34 行），显式路径、不带 `override=`，位置和写法一次都没动。

参考项目用的是无参 `load_dotenv()`（如
`simple-hedge-fund/src/simple_hedge_fund/config.py:26`，靠自动向上查找 `.env`），
本课程统一改成显式 `".env"`——这是有意的差异，因为课程强调从仓库根目录运行。

---

## 三、目前最主流的方式

分场景看，"最主流"有两个答案；但更要紧的是：**课程现在的顺序恰好是反主流的
那个方向。**

### 3.1 按场景分

**写脚本、教学、单文件工具 —— `load_dotenv()` + `os.getenv()`**
即课程中第 2 种（lesson 11–12）的形态。它至今仍是使用量最大的做法，原因很朴素：
零抽象、零类型、任何地方都能读。绝大多数教程和示例都停在这里。

**正经应用 / 服务 —— `pydantic-settings` 的 `BaseSettings`**
当前现代 Python 项目（尤其 pydantic / FastAPI 生态）最主流的升级路径，形态上正是
课程的第 3 种——"先解析成一个配置对象，再注入下游"。区别只在解析器是库而非手写
函数：`SettingsConfigDict(env_file=".env")` 一行搞定 .env、类型转换、校验与报错。

值得注意：**本课程本来就依赖 `pydantic>=2.7.0`**，所以对它来说
`pydantic-settings` 不是引入新范式，而是把已有的东西用到底。

### 3.2 优先级顺序主流是反的

所有主流工具（12-factor、pydantic-settings、dynaconf、click/typer 的 `envvar=`）
一律是：

```
CLI  >  环境变量  >  .env / 配置文件  >  代码里的默认值
```

课程 lesson 14 是 `默认值 < env < TOML < CLI`，**把文件放到了环境变量之上**。
这不是风格分歧，是会咬人的：容器和 CI 中覆盖配置的**唯一**手段就是环境变量。如果
镜像里打包的 `config.toml` 能压过 env，部署时就再也改不动这个值，必须先改文件、
重新构建。env 高于文件的根本原因就在这。

实测 lesson 14：`LLM_TEMPERATURE=0.2` 被 `config.toml` 里的 `temperature = 0.0`
压回 0，正是这个问题的具体表现。

`pydantic-settings` 的默认顺序是
`init 参数 > 环境变量 > .env 文件 > secrets > 默认值`，而 CLI 只要把值当作 init
参数传进去就天然站在最高位——所以"CLI > env > 文件 > 默认值"在库方案里是免费
得到的。

### 3.3 建议

1. **最小改动、收益最大**：保持手写，把 `config.py` 中四段 update 的次序换成
   `默认值 → TOML → env → CLI`，同步 lesson 14 README 的表格。改动约 5 行，而
   lesson 14 的教学目标（讲清优先级）反而更立得住——因为讲的是真实世界的顺序。
2. **在 README 里点一句**："真实项目里这一层通常交给 `pydantic-settings`，它的
   顺序就是这个表"。一句话把课程与主流生态接上，不用动代码。
3. **真要重写**：用 `pydantic-settings` 替代手写 `load_config()`。更主流、与课程
   已有的 pydantic 模型呼应更好，但抽象变多，对"看清每一步"的教学目标是减分的，
   不推荐在 lesson 14 这个位置做。

---

## 四、对"想学 AI agent 的人"，这份教程思路清晰吗

**会——工程思路清晰，而且是这份教程最强的部分；但 "AI agent" 这条主题线偏细，
学习者会带着一个越来越大的疑问看完全程。**

### 4.1 清晰的地方

1. **接口从第 3 课到第 15 课一次没变**：`analyze(snapshot) -> AnalystDecision`。
   中间内部实现换了四次——单指标规则 → 多指标规则 → LLM 单次调用 → 共享客户端
   注入。这正是 agent 系统的核心命题"接口稳定、实现可替换"，而且课程用看得见的
   diff 在演示它。
2. **"一课一概念 + 文件树标注"让学习者能精确知道这一课动了什么**。141 条标注
   全部准确，这种可信度直接决定学习者敢不敢信 README 的描述。
3. **"What to watch" 段落很成熟**。lesson 10 主动拆解了"哪些值来自模型、哪些由
   代码拼出来"；lesson 11 直接给出 diff 命令并说明"这次重构不改决策路径，JSON
   应当逐字节可比"。这些正是学习者会卡住的地方，被提前接住了。
4. 每课都有明确预期输出，并注明"值会变"，减少了很多"跑出来和文档不一样"的
   挫败感。

### 4.2 会让"想学 AI agent 的人"困惑的地方

**1. "agent" 这个词第 3 课就出现了，但直到第 10 课才有 AI。**
lesson 3 自己写着 "no LLM or investor persona"，是诚实的；但课程从头到尾**没有
给 "agent" 下过一句定义**。学习者带着 ReAct / LangGraph / function calling 的预期
进来，看到的是 `_score_roe` 里的 if/elif，会疑惑"这也叫 agent？那什么不叫？"
建议在 lesson 3 明确一句：本课把 agent 定义为"吃结构化输入、吐结构化决策、可被
编排和替换的单元"，并预告第 10 课起内部实现会换成模型。

**2. LLM 上场的动机没有被兑现——最大的叙事缺口。**
实测：Buffett 77 → 77，Lynch 74 → 74，模型精确复读规则分。lesson 10 的
"What to watch" 甚至举了 score 77 这个例子，却没有点破"模型其实没改分"。
学习者到第 12 课结束一定会问：**那 LLM 到底解决了什么问题？** 课程没有回答。

**3. 现代 agent 的核心拼图基本都没覆盖。**
没有工具调用（数据先取好再喂进去，agent 从不决定"该取什么"）、没有循环或多步
推理、没有记忆、没有 agent 之间的通信（两个 agent 互不知道对方，orchestrator 按
固定顺序调用）。这不是讲得不好，是**覆盖面与学习者的预期不是一回事**。学完会搭
"确定性的多视角决策流水线"，而不是 "agent"。

**4. 最后三课离开了 agent 主题。**
配置对象、TOML 优先级、报告排版——这些是通用 Python 工程技能，不服务于 agent
本身。一门 15 课的 agent 教程，最后 20% 在讲配置分层，主线感觉是断的。放到附录
或独立小节更合适。

**5. 第 7/9 课的 confidence 概念讲了，但现象没出现。**
`confidence` 恒落在 50–100，实测 equal 与 confidence-weighted **都是 76**。
学习者会得出"加权平均没用"的结论——概念被教了，效果却看不见。

**6. Junior / Senior 在第 8 课被丢弃。**
前四课花力气建立的两个 agent，第 8 课说"他们不再参与决策"。README 给了理由，但
学习者会有"前面白学了"的感觉。这本是绝佳的演示机会：**让 Junior 和 Senior 也留在
agents 列表里**，就能当场证明"同接口的 agent 可以任意增减"。

### 4.3 结论

- **"一个 agent 系统是怎么搭起来的"** → 9 分，思路非常清晰，值得推荐。
- **"AI agent 是什么、LLM 在里面的价值是什么"** → 4 分，这两点基本没有回答。

---

## 五、建议的改动清单（汇总，按性价比）

| 优先级 | 改动 | 位置 | 成本 |
| --- | --- | --- | --- |
| 1 | 修正配置优先级为 `默认值 < TOML < env < CLI`，并同步 README 表格 | `15-complete-report/config.py`、lesson 14 README | ~5 行 |
| 2 | 注释掉 `config.toml` 里写死的 `temperature` / `reasoning_effort`，让 env 例子成立 | `15-complete-report/config.toml` | 2 行 |
| 3 | 在 lesson 3 给出 "agent" 的定义，并预告第 10 课起内部实现换成模型 | lesson 3 README | 一段话 |
| 4 | 让 LLM 产生可观察的差异：把 `business_summary` / `recent_headlines` 这类死字段接进 prompt；或至少点破"当前模型只是复述" | `agents/*.py`、lesson 10 README | 小到中 |
| 5 | 调宽 confidence 范围（或诚实说明两种平均常常相同） | `utils/confidence.py`、lesson 9 README | 小 |
| 6 | 把 70/45 信号阈值收成一个共用函数 | `utils/signals.py` | 小 |
| 7 | 结尾补一节"从这里到真正的 agent"：工具调用 / 循环 / 记忆 / 多 agent 的对照与最小例子 | 新增 lesson | 中 |
| 8 | 删除或启用 `StockSnapshot` 的 5 个死字段 | `models.py`、`yfinance_service.py` | 小 |
| 9 | 让 Junior / Senior 留在 orchestrator 中，演示同接口可插拔 | `orchestrator.py`、lesson 8 README | 小 |
| 10 | `--config` 指向不存在文件时给出友好报错 | `config.py` | 3 行 |
| 11 | 统一 README 标注写法；lesson 1 补标注；清理未使用的 `typer` 依赖 | 各 README、`pyproject.toml` | 小 |
