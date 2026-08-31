---
name: fable5-workflow_diy
description: >
  Fable 5 智能工作流 v3.0。吸收 research-reporting_diy 全部功能，
  执行前完成：任务分类 → 深度任务澄清（单批次 ≥10 问，每题 ≤5 选项，≤50轮）
  → 全量技能盘点与最佳组合推荐（本地 1000+ 技能索引 + 缺失时全网/GitHub 搜索安装）
  → 最佳提示词生成 → 用户确认，
  然后走 A/B/C/D 四线流水线（子技能按需调度，技能优先于手写），
  最后 agent-review 审查 + MD+DOCX 双格式交付。
  触发词：一键工作流、fable5工作流、全流程、fable5 workflow、完整流水线、自动工作流、
  一键调研、全自动执行、智能工作流
version: 3.0.0
base_dir: C:\Users\G1381\.workbuddy\skills\fable5-workflow_diy
agent_created: true
---

# fable5-workflow_diy v3.0 — Fable 5 智能工作流

六阶段全流程：深澄清 → 全量选技 → 拟词 → 确认 → 执行 → 交付。

> **v3.0 两大升级**
> 1. **澄清加宽加深**：单批次 **≥10 个问题**（分 3 次工具调用：4+3+3），每题 **≤5 个选项**。
> 2. **技能分析增强**：全量盘点本地技能（含嵌套子技能与市场技能）→ 检索匹配 → 输出**最佳推荐组合**；
>    本地无合适技能则**全网搜索（find-skills / SkillHub / GitHub / WebSearch）**并安装后再执行。
>    **交付优先用技能实现，而非手写。**

---

## 核心原则

| 原则 | 规则 |
|------|------|
| 交付格式 | **固定**：MD + DOCX（纵向A4），DOCX在前，不纳入澄清范围 |
| 引用格式 | 调研类（A线）**强制**国自然基金引文格式（正文方括号编号，文末顺序排列） |
| 澄清聚焦 | **只问内容**，不问格式 |
| 澄清密度 | 单批次 **≥10 个问题**，每题 **≤5 个选项**；动态追问至信息充分 |
| 澄清上限 | 最多 50 次问答回合，超限则总结理解并执行 |
| 用户确认 | 提示词生成后**必须展示并等待用户确认**，用户说「确认执行」才启动 |
| 审查强制 | agent-review_diy 是每条线的最后一步，没有审查不交付 |
| 子技能按需加载 | 走完前一个再加载下一个，不一次性全加载 |
| **技能优先** ⬅️ v3.0 | 交付环节**优先用技能实现**；技能缺失先搜索安装，再考虑手写 |
| **全量盘点** ⬅️ v3.0 | 选技前**必须先跑全量技能索引**，不凭记忆列候选 |

---

## 总览（v3.0 全流程）

```
你的任务
    │
    ▼
┌─────────────────────────────────┐
│  阶段 0：任务分类               │  自动判断 A/B/C/D 线
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  阶段 1：任务澄清  🔺 v3.0      │  单批次 ≥10 问 × ≤5 选项
│  （信息充分 → 跳过）            │  分 3 次调用：4 + 3 + 3，≤50轮
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  阶段 2：技能分析  🔺 v3.0      │  全量索引 → 检索匹配 → 最佳组合
│                                 │  → 本地缺 → 全网/GitHub 搜索安装
│                                 │  → 安全审查 → 就绪报告
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  阶段 3：提示词生成  🔺 v3.0    │  八要素 + 技能优先调用链
│                                 │  （角色/背景/数据/结构/引用/
│                                 │   分析框架/格式/技能调用链）
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  阶段 4：用户确认  （v2.0）     │  展示完整提示词
│                                 │  ⚠️ 必须等「确认执行」
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  阶段 5：流水线执行             │  A/B/C/D 线 + 子技能调度
│                                 │  创建 TaskCreate 跟踪进度
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  阶段 6：审查与交付             │  agent-review → MD+DOCX
│                                 │  → 记忆写入
└─────────────────────────────────┘
```

---

## 阶段 0：任务分类

收到任务后，先判断类型，确定走哪条流水线。

| 用户说的 | → 走哪条线 |
|---------|-----------|
| 「调研/研究/分析一下 XXX」「XXX 的现状/趋势/对比」 | **A线**（深度调研） |
| 「为什么/怎么做/选哪个」「帮我决策 XXX」「对比 A 和 B」 | **B线**（复杂推理） |
| 「帮我写/润色/改写/优化」「出个报告/方案/文档」 | **C线**（写作产出） |
| 「写个代码/修复/重构/实现」「review 这段代码」 | **D线**（代码工程） |
| 模糊（同时包含调研和写作） | **A线**（最完整的保证） |

---

## 阶段 1：任务澄清

**目的**：确保任务范围、关键问题、预期产出完全明确再动手。

**触发条件**（以下任一情形即启动澄清，否则跳过直接进入阶段2）：

- 任务含多个子方向，不知聚焦哪个
- 术语/产品名称/技术代号不精确
- 分析维度未定（技术/市场/政策/竞争）
- 未说要回答什么核心问题
- 时间/地理范围模糊
- 不知要概览还是详析（5页 vs 50页）

**跳过条件**：

- 用户说「直接执行」「直接输出无解释、仅交付最终版本」
- 任务极其简单（如「改个拼写错误」）
- 信息已完全充分

**执行方式（v3.0 强化）**：

- 用 `AskUserQuestion` 工具，**一个澄清批次累计 ≥10 个问题**，每题 **≤5 个选项**
- **工具硬限制与绕行**（必读）：

  | 限制 | 实际约束 | v3.0 处理方式 |
  |------|---------|--------------|
  | 单次调用最多 4 问 | `AskUserQuestion.questions` maxItems = 4 | **连发 3 次调用**凑够 ≥10：`4 + 3 + 3 = 10`（或 `4 + 4 + 3 = 11`） |
  | 每题最多 4 选项 | `options` maxItems = 4 | 给满 **4 个预设选项**；第 5 个意图通过工具**自动提供的自由文本输入框**收集，并在题干中用「其他：____」显式提示 |
  | 选项超 4 个 | 不允许 | 拆成两问，或压缩为 4 个最典型选项 + 自由输入兜底 |

- **批次组织**：≥10 问按「必答核心」与「可选细化」分层，必答组先问（前 4 问），可选组后问（第 5-10 问）
- 默认选项标 `(Recommended)`，放在第一个
- 动态追问，直到信息足够
- 如果超 50 轮 → 总结当前理解并执行
- **禁止**为了凑数问无意义问题；每问必须能改变输出内容、结构或技术路线

**标准澄清批次模板（v3.0，≥10 问）**：

调用 1（4 问 · 定位核心）：
```
Q1: 本次任务聚焦哪些维度？（多选）
   A. 技术/产品分析 (Recommended)  B. 市场竞争格局
   C. 政策/监管环境  D. 商业模式/投资价值
   E. 其他（请填写）：____

Q2: 调研的地理范围？
   A. 全球 (Recommended)  B. 中国为主
   C. 特定国家/地区  D. 其他：____

Q3: 时间范围？
   A. 近3年 (Recommended)  B. 近5年
   C. 不限  D. 特定区间（请填写）：____

Q4: 交付深度与篇幅？
   A. 概览（3-5页）  B. 标准（10-20页）(Recommended)
   C. 深度（30页+）  D. 其他：____
```

调用 2（3 问 · 明确产出）：
```
Q5: 最终读者/使用方是谁？
   A. 投资人/决策层 (Recommended)  B. 技术团队  C. 监管机构  D. 学术同行  E. 其他：____

Q6: 是否需要对比分析？
   A. 是，与国内外主要竞品/方案对比 (Recommended)
   B. 否，只做单一对象深描  C. 是，仅与 1-2 个指定对象对比  D. 其他：____

Q7: 结论形态偏好？
   A. 给明确推荐结论 (Recommended)  B. 只列选项与利弊，不下结论
   C. 给出情景化概率判断  D. 其他：____
```

调用 3（3 问 · 锁定约束）：
```
Q8: 是否需要一手数据/联网检索？（决定走 A 线还是 C 线）
   A. 需要，联网检索最新资料 (Recommended)  B. 不需要，基于已有材料  C. 其他：____

Q9: 有无必须引用/必须覆盖的内部材料？
   A. 无  B. 有，我会提供文件 (Recommended)  C. 有，请在工作区自行搜索  D. 其他：____

Q10: 敏感度与可公开性？
   A. 可完全公开  B. 内部使用，避免敏感表述 (Recommended)  C. 涉密，仅框架不涉及细节  D. 其他：____
```

> 上述 10 问为**通用基线**。实际执行时必须按任务领域改写题干与选项
> （医学任务换成适应症/分期/终点指标；工程任务换成技术栈/规模/约束）。

---

## 阶段 2：技能分析（v3.0 重构）

**目的**：**先摸清家底，再挑最优组合**——全量盘点本地技能 → 检索匹配 → 输出最佳推荐组合 →
本地缺失则全网搜索安装 → 尽可能用技能完成交付。

> ⚠️ **v3.0 硬性前置**：禁止凭记忆列候选技能。本地已有 **1000+ 个 SKILL.md**（含嵌套子技能），
> 且随时新增，记忆必然过时。**必须先跑索引脚本**。

### 2.0 全量盘点（⬅️ v3.0 新增，必做第一步）

```bash
PY="C:/Users/G1381/.workbuddy/binaries/python/versions/3.13.12/python.exe"
SC="C:/Users/G1381/.workbuddy/skills/fable5-workflow_diy/scripts/inventory_skills.py"

# 1) 建立全局认知：看总量与分组（紧凑输出，省 token）
"$PY" "$SC" --compact --top-level-only --limit 200

# 2) 按任务能力关键词检索候选（空格=AND）
"$PY" "$SC" --query "pdf ocr"      --compact
"$PY" "$SC" --query "docx"         --compact
"$PY" "$SC" --query "文献 检索"     --compact

# 3) 需要程序消费时
"$PY" "$SC" --query "翻译" --json
```

脚本特性：
- 扫描三处根目录：用户级 `~/.workbuddy/skills/`（含**嵌套**子技能如 `LabClaw:skills:literature:protocol-writing`）、
  项目级 `./.workbuddy/skills/`、本地市场 `~/.workbuddy/skills-marketplace/skills/`
- **只解析 YAML frontmatter**，不加载正文——避免 1282 个技能撑爆上下文
- 描述回退链：`description` → `summary`+`title` → 正文 H1+首段，保证 0 空描述
- 标记 `disable-model-invocation: true` 的技能为 **⚠仅手动**（本机实测 96 个）

**「仅手动触发」技能的降级用法**（v3.0 关键经验）：
这类技能不会被自动调度，但**内容仍然可用**——直接 `Read` 其 SKILL.md，
把其中的工作流/脚本/模板当作**操作手册**人工执行，等价于使用该技能。
就绪报告中需标注此项，避免误判为"不可用"。

### 2.1 能力映射：任务 → 能力 → 候选技能

把任务拆成**必需能力**与**加分能力**，逐项用索引脚本检索：

| 任务特征 | 需要的能力 | 检索关键词（用于 --query） |
|---------|-----------|------------------------|
| 医学/生物医学调研 | 临床试验、文献检索 | `pubmed`、`文献`、`clinical trial` |
| 金融/市场数据 | 行情、财务分析 | `stock`、`finance`、`行情` |
| PDF 处理 | 读取/OCR/转换 | `pdf`、`ocr` |
| 网页抓取 | 渲染、反爬 | `scraper`、`playwright`、`browser` |
| Excel/数据处理 | 分析、图表 | `xlsx`、`excel`、`chart` |
| PPT 演示 | 演示文稿 | `pptx` |
| DOCX 文档 | 读写转换 | `docx`、`md2docx` |
| 医学翻译 | 中英互译 | `翻译`、`cn2en`、`en2cn` |
| 并行调研 | 多 Agent 搜索 | `research`、`agent` |
| 深度推理 | 多步逻辑 | `cot`、`reasoning` |
| 写作润色 | 文本质感 | `writing`、`润色` |
| 质量审查 | 事实/逻辑检查 | `review`、`审查` |

**各线必检基线**（检索命中后仍需人工判断适配度）：
- **A线**：`multi-agent-research_diy`、`cot-reasoning_diy`、`writing-quality_diy`、`agent-review_diy`、`md2docx_diy`
- **B线**：`cot-reasoning_diy`、`agent-review_diy`
- **C线**：`writing-quality_diy`、`agent-review_diy`
- **D线**：`cot-reasoning_diy`、`agent-review_diy`

### 2.2 最佳组合推荐（⬅️ v3.0 新增）

对每项必需能力，**在候选集中按以下优先级挑 1 个**：

1. **已安装且非「仅手动」**（可直接 `Skill` 调度）— 最优
2. **已安装但「仅手动」**（Read 其 SKILL.md 后人工执行）— 次优，标注降级方式
3. **本地市场可复制**（`cp -r` 到 `~/.workbuddy/skills/` 即完成安装）— 需先看 SKILL.md 确认
4. **全网搜索安装**（见 2.3）
5. **无可用技能** → 记录兜底方案（手写/WebSearch 替代），不阻塞流程

组合输出为三档：**主技能**（承担核心交付）/ **辅助技能**（补强环节）/ **兜底方案**。

### 2.3 缺失技能：全网搜索与安装（⬅️ v3.0 增强）

按优先级逐级尝试，**GitHub 为重点来源**：

```bash
# 优先级 1：本地技能市场（最快，零网络）
ls ~/.workbuddy/skills-marketplace/skills
cp -r ~/.workbuddy/skills-marketplace/skills/<name> ~/.workbuddy/skills/<name>

# 优先级 2：平台技能检索
Skill(command="find-skills", args="<query>")

# 优先级 3：SkillHub 注册表
curl -s "https://lightmake.site/api/v1/search?q=<query>&limit=10"
curl -L -o /tmp/skill.zip "https://lightmake.site/api/v1/download?slug=<slug>"
mkdir -p ~/.workbuddy/skills/<slug> && unzip -o /tmp/skill.zip -d ~/.workbuddy/skills/<slug>

# 优先级 4：GitHub 搜索 ⭐ v3.0 重点
#   4a) 已装 gh 时（结构化，最准）
gh search repositories "<capability> skill" --limit 10 \
   --json fullName,description,stargazersCount,pushedAt
#   4b) 未装 gh 时（纯 curl + API）
curl -s "https://api.github.com/search/repositories?q=<capability>+skill&sort=stars&order=desc&per_page=10" \
  | python -c "import sys,json;[print(f\"{i['full_name']}\t★{i['stargazers_count']}\t{i['description']}\") for i in json.load(sys.stdin)['items']]"
#   4c) 已知仓库：先看 SKILL.md 再决定装不装（避免盲装）
curl -sL "https://raw.githubusercontent.com/<owner>/<repo>/HEAD/SKILL.md" | head -40
#   4d) 安装
git clone --depth 1 https://github.com/<owner>/<repo> ~/.workbuddy/skills/<slug>

# 优先级 5：通用网页搜索
WebSearch(query="<capability> claude skill SKILL.md site:github.com")
```

**GitHub 高质量来源参考**：`anthropics/skills`（官方）、各类 `awesome-*-skills` 汇总仓库、
`ZhangGZ-medical/*`（本用户自有 16 个 DIY 技能仓库，优先复用）。

**🔒 安全审查（强制）**：从网络安装任何新技能前，必须先做安全审计：
1. `Skill(skill="skills-security-check")` 加载审查技能
2. 审计目标：`SKILL.md` + `scripts/` + `references/` 全部文件
3. **P0（关键风险）**：强烈警告用户，**明确确认后**才装；默认建议不装
4. **P1（需留意）**：警告用户，取得确认后安装
5. **P2（安全）**：正常安装

> 从**本地市场**或**用户自有仓库**复制的技能，可跳过完整审计，但仍需 `head -40 SKILL.md` 快速过目。

### 2.4 兜底

五个优先级都未找到 → 记录为「未找到，用替代方案」，**不阻塞流程**。
但必须在就绪报告中写明：该环节由什么替代（手写代码 / WebSearch / 通用工具），
以及替代方案相对技能方案的**质量损失预估**。

### 2.5 输出技能就绪报告（v3.0 新格式）

```markdown
## 技能分析结果

**任务类型**：[类型] | **流水线**：[A/B/C/D]
**全量盘点**：本地 1282 个技能已索引（用户级 962 / 市场 320）

### 推荐组合

| 环节 | 能力需求 | 主技能 | 状态 | 辅助/兜底 |
|------|---------|--------|------|----------|
| 调研 | 多源检索 | `multi-agent-research_diy` | ✅ 已安装 | 兜底：5 个 Agent 直接并行 |
| 推理 | 深度分析 | `cot-reasoning_diy` | ✅ 已安装 | — |
| 转换 | MD→DOCX | `md2docx_diy` | ✅ 已安装 | 兜底：pandoc |
| 脱敏 | DICOM 匿名 | `dicom-anonymizer` | ⚠仅手动 | Read SKILL.md 后人工执行 |
| 绘图 | 机制图 | — | ⬇️ 需安装 | 已从 GitHub clone `xxx/yyy` |

**安装动作**：`yyy` ⬇️（GitHub 克隆，已过 P2 安全审查）
**未覆盖**：[能力] ⚠️（改用 WebSearch 替代，预计损失：数据颗粒度下降）

**状态**：N 就绪 / M 需安装 / K 降级 / P 缺失
```

---

## 阶段 3：提示词生成

**目的**：输出一份可直接执行的完整最佳提示词，含八要素。

### 提示词模板

````markdown
## 调研任务提示词

### 1. 角色设定
你是 [根据任务领域动态设定，如：技术尽职调查专家 / 市场研究分析师 / 政策合规顾问]

### 2. 任务背景
[简短说明：为什么做、给谁看、要解决什么问题]

### 3. 事实数据基础
先读取以下文件获取已有数据：

| # | 文件路径 | 内容说明 |
|---|---------|---------|
| 1 | `[绝对路径]/xxx.md` | [说明] |
| 2 | `[绝对路径]/xxx.json` | [说明] |

### 4. 输出结构
```
## 执行摘要
## 1. [一级标题]
### 1.1 [二级标题]
### 1.2 [二级标题]
## 2. [一级标题]
...
## 参考文献
```

### 5. 引用格式（国自然基金）
- 正文：`[1]` 单篇 / `[1,3,5]` 多篇 / `[1-3]` 连续编号
- 文末按正文出现顺序排列
- 期刊论文：`[编号] 作者. 题目. 期刊, 年, 卷(期): 页码.`
- 网址：`[编号] 作者/机构. 标题. 来源, 日期. 访问日期. URL.`
- 内部文件：`[文件: xxx.json]`
- Agent结果：`[来源XX]`

### 6. 分析框架
[定义核心分析维度]

### 7. 格式要求
- 执行摘要前置（≤1页）
- 结论前置，详析后置
- 对比用表格，避免大段文字
- 不确定性标注：`[未公开]` / `[推断]` / `[待确认]`

### 8. 技能调用链（v3.0：技能优先于手写）
严格按阶段 2 输出的「推荐组合」执行。每项交付环节**先问"有没有技能能做"**，
有则用技能，无则记录兜底：

| 环节 | 使用技能 | 兜底（仅当无技能时） |
|------|---------|-------------------|
| 文件读取 | [主技能] | Glob / Read |
| 数据获取 | [主技能] | WebSearch / WebFetch |
| 并行调研 | `multi-agent-research_diy` | N 个 Agent 手动并行 |
| 深度推理 | `cot-reasoning_diy` | 内置推理 |
| 写作润色 | `writing-quality_diy` | 人工润色 |
| 格式转换 | `md2docx_diy` | pandoc |
| 质量审查 | `agent-review_diy` | —（无兜底，强制） |

执行顺序：①读取文件 → ②技能调用/数据获取 → ③Web搜索+Agent并行 → ④深度推理
→ ⑤撰写MD(NSFC引文) → ⑥润色 → ⑦md2docx转换 → ⑧agent-review审查
````

**注意**：非调研类（B/C/D线），提示词模板中引用格式部分可简化。核心八要素必须具备。

---

## 阶段 4：用户确认

生成提示词后 **必须** 展示给用户：

```markdown
---
## 提示词已生成

[嵌入阶段三的完整提示词]

---

**请确认**：
1. 任务范围是否准确？
2. 输出结构是否符合预期？
3. 需要调整的地方？

回复 **"确认执行"** 或 **"开始执行"** 启动任务。
如需修改，告诉我具体调整点。
```

**⚠️ 等待用户明确确认后才进入阶段5，禁止自动执行。**

---

## 阶段 5：流水线执行

### 5.1 创建任务

用 `TaskCreate` 创建对应流水线的执行任务：

| 流水线 | 任务列表 |
|--------|---------|
| A线 | ①读取文件 → ②技能调用/数据获取 → ③Web搜索+Agent并行调研 → ④深度推理 → ⑤撰写MD报告(NSFC引文) → ⑥写作润色 → ⑦md2docx_diy转换 |
| B线 | ①深度推理 → ②写作润色(超500字) → ③md2docx_diy转换 |
| C线 | ①写作润色 → ②md2docx_diy转换 |
| D线 | ①需求分析/方案设计 → ②代码实现 → ③测试验证 |

### 5.2 A线：深度调研

执行子技能串联：

```
Step A1: 加载 multi-agent-research_diy（或 deep-research:research 系列）
  → 拆分5个Agent并行搜索
  → 交叉验证、去重、标注置信度
  → 产出：结构化调研原始结果

Step A2: Agent 并行调研补充（如未使用 multi-agent-research_diy）
  → 每个Agent聚焦一个维度，run_in_background: true
  → 通用配置：

  | Agent | 维度 | 模型 | 搜索来源 |
  |-------|------|------|---------|
  | Agent 1 | 政策/法规 | reasoning | 官方网站、政府公告 |
  | Agent 2 | 技术/标准 | reasoning | 标准组织、技术文档 |
  | Agent 3 | 市场/竞争 | reasoning | 行业报告、新闻、数据库 |
  | Agent 4 | 学术/研究 | reasoning | 学术数据库、会议论文 |
  | Agent 5 | 案例/实践 | reasoning | 行业案例、白皮书 |

Step A3: 加载 cot-reasoning_diy
  → 对调研结果做深度推理
  → 拆解核心问题、逐项分析、交叉验证
  → 产出：有推理深度的综合结论

Step A4: 加载 writing-quality_diy
  → 对综合结论做写作质感增强
  → 消除AI味、优化句式、注入中国语境
  → 产出：可交付的成品文本（含NSFC格式引用）

Step A5: 加载 agent-review_diy
  → 五维审查（事实/完整/逻辑/格式/AI味）
  → 直接给修正版
  → 标出主要改动
```

### 5.3 B线：复杂推理

```
Step B1: 加载 cot-reasoning_diy
  → 拆解 → 逐项 → 验证 → 综合

Step B2: 加载 writing-quality_diy
  → 如果输出超过500字，润色

Step B3: 加载 agent-review_diy
  → 五维审查 + 修正
```

### 5.4 C线：写作产出

```
Step C1: 加载 writing-quality_diy
  → 风格评估 → 两轮润色

Step C2: 加载 agent-review_diy
  → 五维审查 + 修正
```

### 5.5 D线：代码工程

```bash
# 搜索工作空间相关文件
find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.json" 2>/dev/null | head -20
```

```
Step D1: 加载 cot-reasoning_diy
  → 需求分析 → 设计方案 → 代码实现 → 测试验证

Step D2: 加载 agent-review_diy
  → 安全检查 + 边缘情况 + 代码规范
```

### 5.6 子技能加载指令

| Step | 加载指令 |
|------|---------|
| A1 | `Skill(skill="multi-agent-research_diy")` |
| A2 Agent | `Agent(description="...", prompt="...", subagent_type="general-purpose", run_in_background=true)` |
| A3/B1/D1 | `Skill(skill="cot-reasoning_diy")` |
| A4/B2/C1 | `Skill(skill="writing-quality_diy")` |
| A5/B3/C2/D2 | `Skill(skill="agent-review_diy")` |

加载后立即按子技能的指令执行，不另做解释。

---

## 阶段 6：审查与交付

### 6.1 agent-review 强制审查

加载 `agent-review_diy`，执行五维审查：
- 事实性：数据是否准确，引用是否可验证
- 完整性：是否覆盖所有要求维度
- 逻辑一致性：推理链条是否闭环
- 格式合规性：NSFC引用格式（A线）、表格/层级规范
- AI味检测：是否自然流畅

输出修正版本，标注主要改动。

### 6.2 转换 DOCX

```python
from md2docx_diy import md_to_docx
md_to_docx('/path/to/report.md', '/path/to/report.docx', orientation='portrait')
```

### 6.3 交付

`present_files` 展示最终文件（DOCX 在前，MD 在后）。

### 6.4 交付模板

```
## [任务名]

[成品内容]

---

### 流水线记录

> 工作流：fable5-workflow_diy v3.0 | 线路：[A/B/C/D] | 日期：[YYYY-MM-DD]
> 前置阶段：澄清 [N]轮（单批次 ≥10 问）/ 全量盘点 [M]个技能 / 推荐组合 [K]个就绪 / 提示词确认 ✅
> 已执行：[列出实际使用的子技能]
> 新增安装：[技能名 + 来源] | 降级使用：[⚠仅手动技能名 + 降级方式]
> 未覆盖：[能力] → 兜底：[替代方案]

### 审查备注
[agent-review_diy 的审查结论和主要改动]
```

### 6.5 记忆写入

在 `.workbuddy/memory/YYYY-MM-DD.md` 追加记录：
- 任务名称、所用流水线
- 核心发现 3-5 条
- 数据源数量
- 关键结论

---

## 路径约定

| 路径 | 用途 |
|------|------|
| `{WORKSPACE}/` | 根目录：报告输出、文件搜索起点 |
| `{WORKSPACE}/results/` | 调研数据（JSON/MD）存储 |
| `{SKILL}/scripts/inventory_skills.py` | ⬅️ v3.0 全量技能索引脚本（阶段 2.0 必用） |
| `~/.workbuddy/skills/` | 已安装技能目录（含嵌套子技能） |
| `~/.workbuddy/skills-marketplace/skills/` | 本地技能市场 |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **v3.0.0** | 2026-08-31 | **澄清加宽加深**：单批次 ≥10 问（分 3 次调用 4+3+3），每题 ≤5 选项（4 预设 + 自由输入兜底）。**技能分析重构**：新增阶段 2.0 全量盘点（`scripts/inventory_skills.py`，1282 技能 frontmatter 索引）、2.2 最佳组合推荐（主/辅/兜底三档）、2.3 五级联网搜索（新增 GitHub 为重点来源 + 强制安全审查）、识别 `disable-model-invocation` 仅手动技能及降级用法。新增「技能优先」「全量盘点」两项核心原则 |
| v2.0.0 | 2026-07-02 | 吸收 research-reporting_diy 全部功能：新增阶段1-4（任务澄清/技能分析/提示词生成/用户确认），原流水线重编号为阶段5-6，升级为六阶段智能工作流 |
| v1.0.0 | 初始 | 四线流水线（A/B/C/D）+ agent-review 审查 + MD+DOCX 交付 |

---

## 完整示例

用户输入：
> @fable5-workflow_diy 调研一下DeepSeek V4 Pro在医疗领域的应用前景

执行：
```
阶段 0 — 分类：调研任务 → A线

阶段 1 — 澄清（单批次 ≥10 问，分 3 次调用）：
  调用1（4问）：聚焦子领域(影像诊断/临床决策/药物研发/患者管理) / 时间范围 / 是否对比竞品 / 篇幅深度
  调用2（3问）：读者对象(投资人/技术/监管/学术) / 结论形态(明确推荐or利弊罗列) / 是否需一手数据
  调用3（3问）：内部材料覆盖范围 / 地理范围 / 可公开性
  → 每题 4 个预设选项 + 自由输入兜底（第5选项）

阶段 2 — 技能分析（v3.0 新流程）：
  2.0 全量盘点：
    python scripts/inventory_skills.py --compact --top-level-only --limit 200
    python scripts/inventory_skills.py --query "pubmed 文献" --compact
    → 本地 1282 个技能已索引，0 空描述，96 个标记「⚠仅手动」
  2.2 组合推荐：
    主技能 = multi-agent-research_diy(调研) + cot-reasoning_diy(推理)
             + writing-quality_diy(润色) + md2docx_diy(转换)  → 全部 ✅ 已安装
    辅助   = medical-research-toolkit ⬇️（本地市场无 → GitHub 搜索 anthropic/skills 命中 → 安全审查 P2 → clone）
    兜底   = 机制图绘制 ⚠️（无合适技能 → 用 SVG 手写，预估损失：精美度下降）
  2.5 输出就绪报告（新格式：推荐组合表）

阶段 3 — 提示词生成：（展示八要素完整提示词）

阶段 4 — 用户确认：等待「确认执行」

阶段 5 — A线执行：
  Step A1: 加载 multi-agent-research_diy
    → 5个Agent并行：医疗AI政策 / 影像诊断案例 / DeepSeek vs GPT-4o / 技术瓶颈 / 商业模式
  Step A2: Agent并行补充
    → PubMed文献 / NMPA政策 / arXiv技术论文
  Step A3: 加载 cot-reasoning_diy
    → 拆解核心问题：监管壁垒/技术瓶颈/商业模式/时间窗口
  Step A4: 加载 writing-quality_diy
    → 润色为可交付报告（NSFC引用格式）
  Step A5: 加载 agent-review_diy
    → 五维审查 + 修正

阶段 6 — 交付：
  → DOCX + MD + present_files
  → 记忆写入
```
