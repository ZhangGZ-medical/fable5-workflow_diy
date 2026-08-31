# fable5-workflow_diy v3.0 — Fable 5 智能工作流

> **六阶段全流程：深澄清 → 全量选技 → 拟词 → 确认 → 执行 → 交付。**
> v3.0 两大升级：**澄清加宽加深**（单批次 ≥10 问 × 每题 ≤5 选项）+ **技能分析重构**
> （全量盘点本地 1000+ 技能 → 最佳组合推荐 → 本地缺失则全网/GitHub 搜索安装）。
> **交付优先用技能实现，而非手写。**

---

## 一句话说明

这是子技能的**编排器（Orchestrator）** + **前置决策引擎** + **技能资产管家**。
你不用记住什么时候用哪个技能、按什么顺序加载、提示词怎么写——说出任务，
它自动盘点本地全部技能挑出最优组合，缺什么就去网上找来装上，
先把需求问透（≥10 问）、生成最佳提示词，等你确认后再自动调度、审查、交付。

```
@fable5-workflow_diy 调研一下XXX   ← 一句话就够了
```

## v3.0 vs v2.0 vs v1.0

| 能力 | v1.0 | v2.0 | **v3.0** |
|------|------|------|----------|
| 任务澄清 | ❌ 自动执行 | 一次 ≤3 问，每题 ≤4 选项 | **单批次 ≥10 问（4+3+3 三次调用），每题 ≤5 选项** |
| 技能盘点 | ❌ 无 | ❌ 凭记忆列候选 | **✅ 全量索引脚本：1282 个技能 frontmatter 化，0 空描述** |
| 组合推荐 | ❌ 无 | ❌ 只判"装没装" | **✅ 主技能/辅助/兜底三档推荐，5 级优先级择优** |
| 缺失技能获取 | ❌ 无 | 本地市场 + SkillHub | **✅ + GitHub 搜索（gh/curl/raw 预览）+ 强制安全审查** |
| 仅手动技能识别 | ❌ 无 | ❌ 无 | **✅ 识别 `disable-model-invocation`（本机 96 个）并给降级用法** |
| 提示词生成 | ❌ 无 | ✅ 八要素 | ✅ 八要素 + 技能优先调用链表 |
| 用户确认 | ❌ 不等 | ✅ 必须等"确认执行" | ✅ 保留 |
| 引用格式 | ❌ 无规范 | ✅ A线强制国自然基金引文 | ✅ 保留 |
| 四线流水线 | ✅ | ✅ | ✅ 保留增强 |
| agent-review | ✅ | ✅ | ✅ 保留 |
| MD+DOCX交付 | ✅ | ✅ | ✅ 保留 |

---

## 六阶段全流程

```
你的任务
    │
    ▼
┌───────────────────────────────────┐
│  阶段 0：任务分类                 │  自动判断 A/B/C/D 线
├───────────────────────────────────┤
│  阶段 1：任务澄清  🔺 v3.0        │  单批次 ≥10 问 × ≤5 选项
│                                   │  分 3 次调用：4 + 3 + 3，≤50轮
├───────────────────────────────────┤
│  阶段 2：技能分析  🔺 v3.0        │  全量索引 → 检索匹配 → 最佳组合
│                                   │  → 本地缺 → 全网/GitHub 搜索安装
│                                   │  → 安全审查 → 就绪报告
├───────────────────────────────────┤
│  阶段 3：提示词生成  🔺 v3.0      │  八要素 + 技能优先调用链
├───────────────────────────────────┤
│  阶段 4：用户确认                 │  展示提示词，等「确认执行」
├───────────────────────────────────┤
│  阶段 5：流水线执行               │  A/B/C/D 线 + 子技能调度
├───────────────────────────────────┤
│  阶段 6：审查与交付               │  agent-review → MD+DOCX → 记忆
└───────────────────────────────────┘
```

## 四条流水线

| 你输入的 | 走的线路 | 子技能 | 交付 |
|---------|---------|-------|------|
| 「调研/研究一下 XXX」 | **A线** | Skill分析 → 调研 → 推理 → 写作 → 审查 | DOCX + MD |
| 「为什么/选哪个/帮我决策」 | **B线** | Skill分析 → 推理 → 写作 → 审查 | DOCX + MD |
| 「帮我写/润色/优化」 | **C线** | Skill分析 → 写作 → 审查 | DOCX + MD |
| 「写个代码/修复/重构」 | **D线** | Skill分析 → 推理 → 审查 | 代码 |

### A线：深度调研（最完整）

```
阶段1-4: 澄清 → 技能分析 → 提示词 → 确认
    ↓
multi-agent-research_diy    ← 5个Agent并行搜索
    ↓
cot-reasoning_diy           ← 对调研结果深度推理
    ↓
writing-quality_diy         ← 润色为可交付文本（NSFC引文）
    ↓
agent-review_diy            ← 五维审查 + 修正
    ↓
DOCX + MD 交付
```

### B线：复杂推理

```
阶段1-4: 澄清 → 技能分析 → 提示词 → 确认
    ↓
cot-reasoning_diy           ← 拆解 → 逐项 → 验证 → 综合
    ↓
writing-quality_diy         ← 超过500字则润色
    ↓
agent-review_diy            ← 五维审查 + 修正
```

### C线：写作产出

```
阶段1-4: 澄清 → 技能分析 → 提示词 → 确认
    ↓
writing-quality_diy         ← 风格评估 → 两轮润色
    ↓
agent-review_diy            ← 五维审查 + 修正
```

### D线：代码工程

```
阶段1-4: 澄清 → 技能分析 → 提示词 → 确认
    ↓
cot-reasoning_diy           ← 需求分析 → 设计 → 实现 → 测试
    ↓
agent-review_diy            ← 安全检查 + 边缘情况 + 规范
```

## 阶段 1：任务澄清（🔺 v3.0 加宽加深）

信息不足时，自动追问。**单批次 ≥10 个问题，每题 ≤5 个选项**，动态追问直到信息充分。

**工具限制与绕行**（v3.0 实测）：

| 限制 | 约束 | 处理 |
|------|------|------|
| 单次最多 4 问 | `AskUserQuestion.questions` maxItems=4 | **连发 3 次调用**：4 + 3 + 3 = 10 |
| 每题最多 4 选项 | `options` maxItems=4 | 给满 4 个预设 + **自由文本输入框**兜底第 5 个意图 |

**批次分层**：必答核心组（前 4 问：维度/范围/时间/深度）→ 产出组（3 问：读者/对比/结论形态）
→ 约束组（3 问：是否联网/内部材料/可公开性）。

上限 50 轮，超限自动总结执行。简单任务或用户说「直接执行」则跳过。
**禁止为凑数提问**——每问必须能改变输出内容、结构或技术路线。

## 阶段 2：技能分析（🔺 v3.0 重构）

**先摸清家底，再挑最优组合。** 禁止凭记忆列候选（本地 1000+ 技能，记忆必然过时）。

### 2.0 全量盘点（必做第一步）

```bash
PY="C:/Users/G1381/.workbuddy/binaries/python/versions/3.13.12/python.exe"
SC="C:/Users/G1381/.workbuddy/skills/fable5-workflow_diy/scripts/inventory_skills.py"

"$PY" "$SC" --compact --top-level-only --limit 200   # 建立全局认知
"$PY" "$SC" --query "pdf ocr" --compact              # 按能力检索（空格=AND）
"$PY" "$SC" --query "文献" --json                     # 程序消费
```

扫描用户级（**含嵌套子技能**）、项目级、本地市场三处；**只解析 frontmatter** 不加载正文，
避免 1282 个技能撑爆上下文；描述回退链保证 **0 空描述**。

### 2.2 最佳组合推荐

每项能力按优先级择优：**已装且可调度 > 已装但仅手动（Read SKILL.md 人工执行）>
本地市场可复制 > 全网搜索安装 > 无技能兜底**。输出**主技能 / 辅助技能 / 兜底方案**三档。

### 2.3 缺失技能：全网搜索（GitHub 为重点）

五级优先级：本地市场 → `find-skills` → SkillHub → **GitHub**（`gh search` / GitHub API /
`raw.githubusercontent.com` 预览 SKILL.md / `git clone`）→ WebSearch。
从网络安装前**强制安全审查**（P0 建议不装、P1 需确认、P2 正常装）。

**本机实测基线**：1282 个技能已索引（用户级 962 / 市场 320），其中 **96 个标记「⚠仅手动」**——
这些技能不会被自动调度，但内容仍可用：直接 Read 其 SKILL.md 当操作手册执行。

输出就绪报告（推荐组合表）后再进入下一阶段。

## 阶段 3：提示词生成（v3.0 增强：技能优先调用链）

按八要素生成最佳提示词：角色设定 / 任务背景 / 事实数据 / 输出结构 / 引用格式(NSFC) / 分析框架 / 格式要求 / 技能调用链。

## 阶段 4：用户确认（🆕 v2.0）

展示完整提示词，**必须**等用户说「确认执行」。可在此阶段调整范围、结构等。

## 设计原则

| 原则 | 说明 |
|------|------|
| **先想后做** | 澄清+选技+拟词+确认，四步准备再做 |
| **只问内容** | 澄清聚焦内容，不问格式（格式固定） |
| **问透再动** 🔺 | 单批次 ≥10 问，宁可多问不返工 |
| **全量盘点** 🔺 | 选技前先跑索引脚本，禁止凭记忆列候选 |
| **技能优先** 🔺 | 交付优先用技能实现；缺技能先搜索安装，再考虑手写 |
| **安装先审** 🔺 | 网络来源技能强制安全审查，P0 默认不装 |
| **动态选技** | 不硬编码，按实际需要动态识别和安装 |
| **按需加载** | 不走 A 线就不加载 multi-agent-research，省 Token |
| **顺序串行** | 前一阶段输出是后一阶段的输入，不跳步 |
| **审查强制** | 无论走哪条线，最后一步一定是 agent-review。无审查不交付 |
| **记忆写入** | 交付后自动追加每日日志 |

## 使用示例

### 示例 1：深度调研（A线）

```
@fable5-workflow_diy 调研一下 DeepSeek V4 Pro 在医疗领域的应用前景
```

→ 分类为 A线 → **连发 3 次调用共 10 问**（子领域/时间/竞品/篇幅 · 读者/结论形态/是否联网 ·
内部材料/地理/可公开性）→ **全量索引 1282 个技能**并检索 pubmed·医学文献 →
组合推荐（4 主技能 ✅ + medical-research-toolkit ⬇️ 从 GitHub 安装）→ 生成八要素提示词 →
确认后 5 Agent 并行搜索 → 推理 → 润色(NSFC引文) → 审查 → DOCX+MD

### 示例 2：技术决策（B线）

```
@fable5-workflow_diy 我应该用 PostgreSQL 还是 MongoDB
```

→ 自动分类为 B线 → 追问数据特征/团队背景 → 推理 → 润色 → 审查 → DOCX+MD

### 示例 3：文档润色（C线）

```
@fable5-workflow_diy 润色这篇项目方案，要能直接给投资人看
```

→ 自动分类为 C线 → 需要先读取文件 → 风格评估 → 两轮润色 → 审查 → DOCX+MD

### 示例 4：代码工程（D线）

```
@fable5-workflow_diy 写一个 Python 异步爬虫，支持并发控制和自动重试
```

→ 自动分类为 D线 → 追问并发规模/目标站点 → 设计 → 实现 → 审查（安全/边缘/规范）

## 子技能关系

```
                  fable5-workflow_diy v3.0 (编排层 + 决策引擎 + 技能资产管家)
                                 │
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                        ▼
  阶段1-4 前置决策         阶段5 流水线执行         阶段6 交付
  (深澄清·全量选技·       (A/B/C/D线调度)        (审查·DOCX·记忆)
   拟词·确认)                    │
        │                        │
        │              ┌─────────┼─────────┐
        │              ▼         ▼         ▼
        │    multi-agent  cot-reasoning  writing-quality
        │    research_diy     _diy           _diy
        │              │         │         │
   inventory_skills.py  │         │         │
   (全量盘点·组合推荐)   │         │         │
        │              └─────────┼─────────┘
        │                        ▼
        └──────────────── agent-review_diy ◄──────────────┘
                           (强制收尾)
```

## 完整安装（依赖仓库）

fable5-workflow_diy 依赖以下 DIY 技能。新用户可使用 `github_upload_diy` 或直接 `git clone` 安装全部依赖：

### 核心依赖（每条线都需要的强制依赖）

| 技能 | GitHub 仓库 | 用途 |
|------|-----------|------|
| `agent-review_diy` | https://github.com/ZhangGZ-medical/agent-review_diy | 五维审查（所有线路强制收尾） |
| `md2docx_diy` | https://github.com/ZhangGZ-medical/md2docx_diy | Markdown → DOCX 转换交付 |

### A线（深度调研）额外依赖

| 技能 | GitHub 仓库 | 用途 |
|------|-----------|------|
| `multi-agent-research_diy` | https://github.com/ZhangGZ-medical/multi-agent-research_diy | 5 Agent 并行调研 |
| `cot-reasoning_diy` | https://github.com/ZhangGZ-medical/cot-reasoning_diy | 深度推理分析 |
| `writing-quality_diy` | https://github.com/ZhangGZ-medical/writing-quality_diy | 写作质感增强 |

### B线（复杂推理）额外依赖

| 技能 | GitHub 仓库 | 用途 |
|------|-----------|------|
| `cot-reasoning_diy` | https://github.com/ZhangGZ-medical/cot-reasoning_diy | 深度推理分析 |
| `writing-quality_diy` | https://github.com/ZhangGZ-medical/writing-quality_diy | 写作润色（>500字） |

### C线（写作产出）额外依赖

| 技能 | GitHub 仓库 | 用途 |
|------|-----------|------|
| `writing-quality_diy` | https://github.com/ZhangGZ-medical/writing-quality_diy | 写作质感增强 |

### D线（代码工程）额外依赖

| 技能 | GitHub 仓库 | 用途 |
|------|-----------|------|
| `cot-reasoning_diy` | https://github.com/ZhangGZ-medical/cot-reasoning_diy | 需求分析与方案设计 |

### 吸收的功能来源

| 技能 | GitHub 仓库 | 说明 |
|------|-----------|------|
| `research-reporting_diy` | https://github.com/ZhangGZ-medical/research-reporting_diy | 阶段1-4（澄清/技能分析/提示词/确认）的功能来源：v2.0 引入，v3.0 在其基础上重构（澄清加宽至 ≥10 问、技能分析改为全量盘点 + 组合推荐） |

### 一键安装（推荐）

```bash
# 安装 fable5-workflow_diy 及其全部 6 个依赖
for repo in fable5-workflow_diy agent-review_diy md2docx_diy multi-agent-research_diy cot-reasoning_diy writing-quality_diy research-reporting_diy; do
  git clone "https://github.com/ZhangGZ-medical/$repo" ~/.workbuddy/skills/"$repo"
done
```

> 安装后使用 `Skill` 工具加载 `fable5-workflow_diy` 即可自动识别缺失的技能并提示安装。

## 与 Fable 5 的完整对标

| Fable 5 核心能力 | 流水线中的等价实现 |
|-----------------|-----------------|
| Adaptive Thinking | A/B/D 线的 cot-reasoning（显式推理链） |
| 子 Agent 调度 | A 线的 N Agent 并行调研（动态N，非固定5） |
| 文学性输出 | A/B/C 线的 writing-quality（两轮迭代） |
| 自我验证 | 所有线路末尾的 agent-review（五维审查） |
| 天级自主运行 | 六阶段全自动流程 |
| 持久记忆 | 交付后自动写入每日日志 |
| task 分解与追问 | 阶段1-4 前置决策引擎（v2.0 引入，v3.0：≥10 问/批） |
| 最佳提示词 | 阶段3 八要素提示词生成（v3.0：技能优先调用链） |
| **技能资产管理** | **🆕 v3.0 独有**：全量盘点（1282 技能索引）+ 最佳组合推荐 + 全网/GitHub 获取（`inventory_skills.py`），Fable 5 无对应能力 |

## 注意事项

- 任务类型模糊（同时含调研和写作）→ 默认 **A线**
- 用户说「直接执行」→ 跳过阶段1澄清
- 用户不说「确认执行」→ 永远不动手
- 子技能按需顺序加载，不一次性全加载
- 最终交付：DOCX + MD 双格式，DOCX 在前
- 审查标注的主要改动不超过 3 条
- **选技前必须先跑 `inventory_skills.py`**，不得凭记忆列候选技能
- **「⚠仅手动」技能不等于不可用**——Read 其 SKILL.md 人工执行即可
- **网络来源技能安装前必须安全审查**，P0 一律先警告并征求确认
- 澄清问题宁可多问，但**禁止无信息量的凑数提问**

## 随附工具

| 文件 | 用途 |
|------|------|
| `scripts/inventory_skills.py` | 本地技能全量索引（v3.0 新增）。纯标准库，无依赖。支持 `--query` 检索、`--json`、`--compact`、`--top-level-only`、`--limit`、`--save` |

```bash
# 最快上手：看本地有哪些技能
python scripts/inventory_skills.py --compact --top-level-only --limit 200
```

---

*v3.0 | Orchestrator + Decision Engine + Skill Asset Manager.*
*Absorbed research-reporting_diy. Deep clarification (≥10 Q/batch) + full-skill inventory & best-combo recommendation.*
