# fable5-workflow_diy v2.0 — Fable 5 智能工作流

> **六阶段全流程：澄清 → 选技 → 拟词 → 确认 → 执行 → 交付。** 吸收 research-reporting_diy 全部功能，执行前先搞清楚要做什么、需要什么技能、最佳提示词是什么，确认后再走四线流水线。

---

## 一句话说明

这是子技能的**编排器（Orchestrator）** + **前置决策引擎**。你不用记住什么时候用哪个技能、按什么顺序加载、提示词怎么写——说出任务，它先帮你厘清需求、选好技能、生成最佳提示词，等你确认后再自动调度、审查、交付。

```
@fable5-workflow_diy 调研一下XXX   ← 一句话就够了
```

## v2.0 vs v1.0

| 能力 | v1.0 | v2.0 |
|------|------|------|
| 任务澄清 | ❌ 自动执行 | ✅ 信息不足时彻底询问，上限50轮 |
| 技能分析 | ❌ 硬编码4个子技能 | ✅ 动态识别→检查→安装→兜底 |
| 提示词生成 | ❌ 无 | ✅ 八要素最佳提示词 |
| 用户确认 | ❌ 不等 | ✅ 必须等"确认执行" |
| 引用格式 | ❌ 无规范 | ✅ A线强制国自然基金引文 |
| 四线流水线 | ✅ | ✅ 保留增强 |
| agent-review | ✅ | ✅ 保留 |
| MD+DOCX交付 | ✅ | ✅ 保留 |

---

## 六阶段全流程

```
你的任务
    │
    ▼
┌───────────────────────────────────┐
│  阶段 0：任务分类                  │  自动判断 A/B/C/D 线
├───────────────────────────────────┤
│  阶段 1：任务澄清  🆕              │  信息不足 → 彻底询问，≤50轮
├───────────────────────────────────┤
│  阶段 2：技能分析  🆕              │  识别→检查→安装→就绪报告
├───────────────────────────────────┤
│  阶段 3：提示词生成  🆕            │  八要素最佳提示词
├───────────────────────────────────┤
│  阶段 4：用户确认  🆕              │  展示提示词，等「确认执行」
├───────────────────────────────────┤
│  阶段 5：流水线执行                │  A/B/C/D 线 + 子技能调度
├───────────────────────────────────┤
│  阶段 6：审查与交付                │  agent-review → MD+DOCX → 记忆
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

## 阶段 1：任务澄清（🆕 v2.0）

信息不足时，自动追问。一次 ≤3 个问题，每题 ≤4 个选项，动态追问直到信息充分。

**典型追问**：
- 聚焦哪个维度？（技术/市场/政策/竞争）
- 地理范围？（全球/中国/特定区域）
- 时间范围？（近3年/近5年/不限）
- 概览还是详析？（5页/50页）

上限 50 轮，超限自动总结执行。简单任务或用户说「直接执行」则跳过。

## 阶段 2：技能分析（🆕 v2.0）

动态识别当前任务需要哪些技能。已安装 ✅、缺则从本地市场/SkillHub安装 ⬇️、三个源都找不到则记录替代方案 ⚠️。输出就绪报告后再进入下一阶段。

## 阶段 3：提示词生成（🆕 v2.0）

按八要素生成最佳提示词：角色设定 / 任务背景 / 事实数据 / 输出结构 / 引用格式(NSFC) / 分析框架 / 格式要求 / 技能调用链。

## 阶段 4：用户确认（🆕 v2.0）

展示完整提示词，**必须**等用户说「确认执行」。可在此阶段调整范围、结构等。

## 设计原则

| 原则 | 说明 |
|------|------|
| **先想后做** | 澄清+选技+拟词+确认，四步准备再做 |
| **只问内容** | 澄清聚焦内容，不问格式（格式固定） |
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

→ 自动分类为 A线 → 追问聚焦哪个子领域/是否对比竞品 → 动态安装 medical-research-toolkit → 生成八要素提示词 → 确认后 5 Agent 并行搜索 → 推理 → 润色(NSFC引文) → 审查 → DOCX+MD

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
                  fable5-workflow_diy v2.0 (编排层 + 决策引擎)
                                 │
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                        ▼
  阶段1-4 前置决策         阶段5 流水线执行         阶段6 交付
  (澄清·选技·拟词·确认)    (A/B/C/D线调度)        (审查·DOCX·记忆)
        │                        │                        │
        │              ┌─────────┼─────────┐              │
        │              ▼         ▼         ▼              │
        │    multi-agent  cot-reasoning  writing-quality  │
        │    research_diy     _diy           _diy         │
        │              │         │         │              │
        │              └─────────┼─────────┘              │
        │                        ▼                        │
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
| `research-reporting_diy` | https://github.com/ZhangGZ-medical/research-reporting_diy | v2.0 的阶段1-4（澄清/技能分析/提示词/确认）来源于此 |

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
| task 分解与追问 | 🆕 阶段1-4 前置决策引擎 |
| 最佳提示词 | 🆕 阶段3 八要素提示词生成 |

## 注意事项

- 任务类型模糊（同时含调研和写作）→ 默认 **A线**
- 用户说「直接执行」→ 跳过阶段1澄清
- 用户不说「确认执行」→ 永远不动手
- 子技能按需顺序加载，不一次性全加载
- 最终交付：DOCX + MD 双格式，DOCX 在前
- 审查标注的主要改动不超过 3 条

---

*v2.0 | Orchestrator + Decision Engine. Absorbed research-reporting_diy full workflow.*
