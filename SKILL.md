---
name: fable5-workflow_diy
description: >
  Fable 5 一键工作流。将 cot-reasoning_diy、writing-quality_diy、agent-review_diy、multi-agent-research_diy
  四个技能串联为完整流水线。用户只需 @fable5-workflow_diy + 任务描述，自动完成：任务分类 → 子技能调度 →
  质量审查 → 交付。
  触发词：一键工作流、fable5工作流、全流程、fable5 workflow、完整流水线、自动工作流、
  一键调研、全自动执行
version: 1.0.0
base_dir: C:\Users\G1381\.workbuddy\skills\fable5-workflow_diy
agent_created: true
---

# fable5-workflow_diy — Fable 5 一键工作流

四条流水线，一个入口。输入你的任务，自动走完「调研 → 推理 → 写作 → 审查 → 交付」全流程。

---

## 总览

```
你的任务
    │
    ▼
┌─────────────────────────────┐
│  阶段 0：任务分类            │  ← 自动判断走哪条流水线
└─────────────────────────────┘
    │
    ├── A线：深度调研   ──→ multi-agent-research → cot-reasoning → writing-quality → agent-review
    ├── B线：复杂推理   ──→ cot-reasoning → writing-quality → agent-review
    ├── C线：写作产出   ──→ writing-quality → agent-review
    └── D线：代码工程   ──→ cot-reasoning → agent-review
                                │
                                ▼
                        ┌──────────────┐
                        │  阶段 5：交付  │  ← DOCX + MD + 记忆写入
                        └──────────────┘
```

---

## 执行规则（必须严格遵守）

### 1. 自动分类，不做多余询问

收到任务后，先判断任务类型，然后直接走对应的流水线。**不要问用户「要不要启动XX技能」**——这个工作流本身就是用户的选择。

### 2. 子技能按需加载，不浪费上下文

不要一次性加载所有技能。走完前一个再加载下一个。如果一个技能不需要，就跳过。

### 3. 每个阶段结束后才进入下一阶段

前一阶段的输出是后一阶段的输入，不要并行跳步。

### 4. agent-review 是强制收尾

无论走哪条线，最后一步一定是 agent-review_diy。没有审查不交付。

### 5. 交付格式

Markdown + DOCX 双格式，DOCX 在前。

### 6. 完成后写入记忆

每日日志追加记录（任务名、流水线、核心产出）。

---

## 四条流水线详解

### A线：深度调研（完整四步）

**触发条件**：任务涉及信息收集、多维度分析、需要外部资料

**执行顺序**：

```
Step A1: 加载 multi-agent-research_diy
  → 拆分5个Agent并行搜索
  → 交叉验证、去重、标注置信度
  → 产出：结构化调研原始结果

Step A2: 加载 cot-reasoning_diy
  → 对调研结果做深度推理
  → 拆解核心问题、逐项分析、交叉验证
  → 产出：有推理深度的综合结论

Step A3: 加载 writing-quality_diy
  → 对综合结论做写作质感增强
  → 消除AI味、优化句式、注入中国语境
  → 产出：可交付的成品文本

Step A4: 加载 agent-review_diy
  → 五维审查（事实/完整/逻辑/格式/AI味）
  → 直接给修正版
  → 标出主要改动
```

### B线：复杂推理（三步）

**触发条件**：需要多步逻辑推导、技术选型、架构决策、方案对比

**执行顺序**：

```
Step B1: 加载 cot-reasoning_diy
  → 拆解 → 逐项 → 验证 → 综合

Step B2: 加载 writing-quality_diy
  → 如果输出超过500字，润色

Step B3: 加载 agent-review_diy
  → 五维审查 + 修正
```

### C线：写作产出（两步）

**触发条件**：已经有内容需要润色、或需要从零撰写面向读者的文本

**执行顺序**：

```
Step C1: 加载 writing-quality_diy
  → 风格评估 → 两轮润色

Step C2: 加载 agent-review_diy
  → 五维审查 + 修正
```

### D线：代码工程（两步）

**触发条件**：编程、调试、架构设计、代码审查

**执行顺序**：

```
Step D1: 加载 cot-reasoning_diy
  → 需求分析 → 设计方案 → 代码实现 → 测试验证

Step D2: 加载 agent-review_diy
  → 安全检查 + 边缘情况 + 代码规范
```

---

## 任务分类速查

| 用户说的 | → 走哪条线 |
|---------|-----------|
| 「调研/研究/分析一下 XXX」「XXX 的现状/趋势/对比」 | A线 |
| 「为什么/怎么做/选哪个」「帮我决策 XXX」「对比 A 和 B」 | B线 |
| 「帮我写/润色/改写/优化」「出个报告/方案/文档」 | C线 |
| 「写个代码/修复/重构/实现」「review 这段代码」 | D线 |
| 模糊（同时包含调研和写作） | A线（最完整的保证） |

---

## 子技能加载指令

在对应 Step 执行时，调用 Skill 工具加载子技能：

| Step | 加载指令 |
|------|---------|
| A1 | `Skill(skill="multi-agent-research_diy")` |
| A2/B1/D1 | `Skill(skill="cot-reasoning_diy")` |
| A3/B2/C1 | `Skill(skill="writing-quality_diy")` |
| A4/B3/C2/D2 | `Skill(skill="agent-review_diy")` |

加载后立即按子技能的指令执行，不另做解释。

---

## 交付模板

无论哪条线，最终交付格式：

```
## [任务名]

[成品内容]

---

### 流水线记录

> 工作流：fable5-workflow_diy | 线路：[A/B/C/D] | 日期：[YYYY-MM-DD]
> 已执行：[列出实际使用的子技能]

### 审查备注
[agent-review_diy 的审查结论和主要改动]
```

---

## 示例

用户输入：
> @fable5-workflow_diy 调研一下DeepSeek V4 Pro在医疗领域的应用前景

执行：
```
判断：调研任务 → A线
Step A1: 加载 multi-agent-research_diy
  → 5个Agent并行：医疗AI政策 / 临床案例 / 技术可行性 / 竞品对比 / 开源方案
Step A2: 加载 cot-reasoning_diy
  → 拆解核心问题：监管壁垒/技术瓶颈/商业模式/时间窗口
Step A3: 加载 writing-quality_diy
  → 润色为可交付报告
Step A4: 加载 agent-review_diy
  → 五维审查 + 修正
交付: DOCX + MD
```
