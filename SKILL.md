---
name: fable5-workflow_diy
description: >
  Fable 5 智能工作流 v2.0。吸收 research-reporting_diy 全部功能，
  执行前完成：任务分类 → 任务澄清（≤50轮Q&A）→ 动态技能分析 → 最佳提示词生成 → 用户确认，
  然后走 A/B/C/D 四线流水线（子技能按需调度），最后 agent-review 审查 + MD+DOCX 双格式交付。
  触发词：一键工作流、fable5工作流、全流程、fable5 workflow、完整流水线、自动工作流、
  一键调研、全自动执行、智能工作流
version: 2.0.0
base_dir: C:\Users\G1381\.workbuddy\skills\fable5-workflow_diy
agent_created: true
---

# fable5-workflow_diy v2.0 — Fable 5 智能工作流

六阶段全流程：澄清 → 选技 → 拟词 → 确认 → 执行 → 交付。

---

## 核心原则

| 原则 | 规则 |
|------|------|
| 交付格式 | **固定**：MD + DOCX（纵向A4），DOCX在前，不纳入澄清范围 |
| 引用格式 | 调研类（A线）**强制**国自然基金引文格式（正文方括号编号，文末顺序排列） |
| 澄清聚焦 | **只问内容**，不问格式 |
| 澄清上限 | 最多 50 次问答回合，超限则总结理解并执行 |
| 用户确认 | 提示词生成后**必须展示并等待用户确认**，用户说「确认执行」才启动 |
| 审查强制 | agent-review_diy 是每条线的最后一步，没有审查不交付 |
| 子技能按需加载 | 走完前一个再加载下一个，不一次性全加载 |

---

## 总览（v2.0 全流程）

```
你的任务
    │
    ▼
┌─────────────────────────────────┐
│  阶段 0：任务分类                │  自动判断 A/B/C/D 线
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  阶段 1：任务澄清  ⬅️ 新增       │  信息不足 → 彻底询问，≤50轮
│  （信息充分 → 跳过）              │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  阶段 2：技能分析  ⬅️ 新增       │  动态识别所需技能 → 检查安装
│                                  │  → 缺则安装 → 输出就绪报告
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  阶段 3：提示词生成  ⬅️ 新增     │  八要素最佳提示词
│                                  │  （角色/背景/数据/结构/引用/
│                                  │   分析框架/格式/技能调用链）
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  阶段 4：用户确认  ⬅️ 新增       │  展示完整提示词
│                                  │  ⚠️ 必须等「确认执行」
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  阶段 5：流水线执行              │  A/B/C/D 线 + 子技能调度
│                                  │  创建 TaskCreate 跟踪进度
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  阶段 6：审查与交付              │  agent-review → MD+DOCX
│                                  │  → 记忆写入
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

**执行方式**：

- 用 `AskUserQuestion` 工具，一次 ≤3 个问题，每题 ≤4 个选项
- 默认选项标 `(Recommended)`
- 动态追问，直到信息足够
- 如果超 50 轮 → 总结当前理解并执行

**典型首轮问题模板**：

```
Q1: 本次任务聚焦哪些维度？（多选）
   A. 技术/产品分析 (Recommended)
   B. 市场竞争格局
   C. 政策/监管环境
   D. 商业模式/投资价值

Q2: 调研的地理范围？
   A. 全球 (Recommended)
   B. 中国为主
   C. 特定国家/地区

Q3: 时间范围？
   A. 近3年 (Recommended)
   B. 近5年
   C. 不限
```

---

## 阶段 2：技能分析

**目的**：识别所需技能，缺失则安装，确保工具箱就绪。

### 2.1 动态识别

根据任务类型 + 阶段0确定的流水线，对照下表判断需要哪些技能：

| 任务特征 | 可能需要的能力 | 候选技能 |
|---------|-------------|---------|
| 医学/生物医学调研 | 临床试验、文献检索 | `medical-research-toolkit` |
| 金融/市场数据 | 行情、财务分析 | `westock-data`、`neodata-financial-search`、`stock-analyzer` |
| PDF处理 | 读取/合并/转换 | `pdf`、`pdfkit-py` |
| 网页抓取 | 渲染页面、反爬 | `web-scraper`、`playwright-scraper-skill` |
| Excel/数据处理 | 分析、图表 | `xlsx`、`minimax-xlsx` |
| PPT演示 | 演示文稿 | `pptx-generator`、`pptx` |
| DOCX文档 | 读写转换 | `docx`、`md2docx_diy` |
| 医学翻译 | 中英互译 | `cn2en_med_diy`、`en2cn_diy` |
| 大规模并行调研 | 多Agent搜索 | `deep-research:research`系列、`multi-agent-research_diy` |
| 新闻/政策 | 实时资讯 | `multi-search-engine`、`tencent-news` |
| 深度推理 | 多步逻辑 | `cot-reasoning_diy` |
| 写作润色 | 文本质感 | `writing-quality_diy` |
| 质量审查 | 事实/逻辑检查 | `agent-review_diy` |

**A线必检**：`multi-agent-research_diy`、`cot-reasoning_diy`、`writing-quality_diy`、`agent-review_diy`
**B线必检**：`cot-reasoning_diy`、`agent-review_diy`
**C线必检**：`writing-quality_diy`、`agent-review_diy`
**D线必检**：`cot-reasoning_diy`、`agent-review_diy`

### 2.2 检查安装状态

对照 `available_skills` 列表交叉验证已安装状态。同时检查：

```bash
ls ~/.workbuddy/skills/             # 用户级技能
ls .workbuddy/skills/ 2>/dev/null    # 项目级技能
```

### 2.3 安装缺失技能

按优先级查找：

```
# 优先级 1：本地技能市场（最快）
ls ~/.workbuddy/skills-marketplace/skills
cp -r ~/.workbuddy/skills-marketplace/skills/<name> ~/.workbuddy/skills/<name>

# 优先级 2：SkillHub 注册表
curl -s "https://lightmake.site/api/v1/search?q=<query>&limit=10"     # 搜索
curl -L -o /tmp/skill.zip "https://lightmake.site/api/v1/download?slug=<slug>"  # 下载
mkdir -p ~/.workbuddy/skills/<slug>
unzip -o /tmp/skill.zip -d ~/.workbuddy/skills/<slug>

# 优先级 3：find-skills 搜索
Skill(command="find-skills", args="<query>")
```

### 2.4 兜底

三个优先级都未找到 → 记录为「未找到，用替代方案」，不阻塞流程。

### 2.5 输出技能就绪报告

```markdown
## 技能分析结果

**任务类型**：[类型] | **流水线**：[A/B/C/D]
**已安装**：skill-a ✅、skill-b ✅
**需安装**：skill-c ⬇️（已从本地市场复制）| skill-d ⚠️（未找到，用 WebSearch 替代）
**状态**：全部就绪 / N就绪 M缺失
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

### 8. 技能调用链
1. 读取工作空间相关文件（Glob 搜索 .md/.json/.csv/.xlsx/.pdf）
2. 使用 [技能] 查询 [数据]
3. WebSearch: [关键词A]、[关键词B]
4. WebFetch: [页面X]、[页面Y]
5. 启动 Agent 并行调研（3-5个话题，run_in_background: true）
6. md2docx_diy 转换交付
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

> 工作流：fable5-workflow_diy v2.0 | 线路：[A/B/C/D] | 日期：[YYYY-MM-DD]
> 前置阶段：澄清 [N]轮 / 技能 [M]个就绪 / 提示词确认 ✅
> 已执行：[列出实际使用的子技能]

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
| `~/.workbuddy/skills/` | 已安装技能目录 |
| `~/.workbuddy/skills-marketplace/skills/` | 本地技能市场 |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0.0 | 2026-07-02 | 吸收 research-reporting_diy 全部功能：新增阶段1-4（任务澄清/技能分析/提示词生成/用户确认），原流水线重编号为阶段5-6，升级为六阶段智能工作流 |
| v1.0.0 | 初始 | 四线流水线（A/B/C/D）+ agent-review 审查 + MD+DOCX 交付 |

---

## 完整示例

用户输入：
> @fable5-workflow_diy 调研一下DeepSeek V4 Pro在医疗领域的应用前景

执行：
```
阶段 0 — 分类：调研任务 → A线
阶段 1 — 澄清：
  Q1: 聚焦哪个医疗子领域？（多选）
    A. 影像诊断 (Recommended)  B. 临床决策支持  C. 药物研发  D. 患者管理
  Q2: 时间范围？ → 近2年
  Q3: 是否对比竞品？ → 是，GPT-4o / Gemini / 其他国产LLM

阶段 2 — 技能分析：
  - 已安装：multi-agent-research_diy ✅、cot-reasoning_diy ✅、writing-quality_diy ✅、agent-review_diy ✅、md2docx_diy ✅
  - 需安装：medical-research-toolkit ⬇️（从SkillHub下载）
  - 状态：全部就绪

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
