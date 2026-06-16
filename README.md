# fable5-workflow_diy — Fable 5 一键工作流

> **四条流水线，一个入口。**输入你的任务，自动走完「调研 → 推理 → 写作 → 审查 → 交付」全流程。对标 Claude Fable 5 的端到端体验。

---

## 一句话说明

这是 4 个子技能的**编排器（Orchestrator）**。你不用记住什么时候用哪个技能、按什么顺序加载——说出任务，它自动分类、自动调度、自动审查、自动交付。

```
@fable5-workflow_diy 调研一下XXX   ← 一句话就够了
```

## 它能做什么

| 你输入的 | 自动走的线路 | 涉及子技能 | 交付格式 |
|---------|------------|-----------|---------|
| 「调研/研究一下 XXX」 | **A线**（完整） | 调研 → 推理 → 写作 → 审查 | DOCX + MD |
| 「为什么/选哪个/帮我决策」 | **B线**（推理） | 推理 → 写作 → 审查 | DOCX + MD |
| 「帮我写/润色/优化」 | **C线**（写作） | 写作 → 审查 | DOCX + MD |
| 「写个代码/修复/重构」 | **D线**（工程） | 推理 → 审查 | 代码 |

## 四条流水线详解

### A线：深度调研（4步全流程）

```
multi-agent-research_diy    ← 5个Agent并行搜索
    ↓
cot-reasoning_diy           ← 对调研结果深度推理
    ↓
writing-quality_diy         ← 润色为可交付文本
    ↓
agent-review_diy            ← 五维审查 + 修正
    ↓
DOCX + MD 交付
```

### B线：复杂推理（3步）

```
cot-reasoning_diy           ← 拆解 → 逐项 → 验证 → 综合
    ↓
writing-quality_diy         ← 超过500字则润色
    ↓
agent-review_diy            ← 五维审查 + 修正
```

### C线：写作产出（2步）

```
writing-quality_diy         ← 风格评估 → 两轮润色
    ↓
agent-review_diy            ← 五维审查 + 修正
```

### D线：代码工程（2步）

```
cot-reasoning_diy           ← 需求分析 → 设计 → 实现 → 测试
    ↓
agent-review_diy            ← 安全检查 + 边缘情况 + 规范
```

## 设计原则

| 原则 | 说明 |
|------|------|
| **自动分类** | 不问你「要不要启动XX技能」——这就是你选择这个技能的原因 |
| **按需加载** | 不走 A 线就不加载 multi-agent-research，省 Token |
| **顺序串行** | 前一阶段输出是后一阶段的输入，不跳步 |
| **审查强制** | 无论走哪条线，最后一步一定是 agent-review。无审查不交付 |
| **记忆写入** | 交付后自动追加每日日志 |

## 使用示例

### 示例 1：深度调研

```
@fable5-workflow_diy 调研一下 DeepSeek V4 Pro 在医疗领域的应用前景
```

→ 自动识别为「调研」→ 走 A 线 → 5 个 Agent 并行搜索 → 推理 → 润色 → 审查 → 输出 DOCX

### 示例 2：技术决策

```
@fable5-workflow_diy 我应该用 PostgreSQL 还是 MongoDB 做新项目的数据库
```

→ 自动识别为「推理」→ 走 B 线 → 拆解性能/团队/生态/成本 → 润色 → 审查

### 示例 3：文档润色

```
@fable5-workflow_diy 润色这篇项目方案，要能直接给投资人看
```

→ 自动识别为「写作」→ 走 C 线 → 风格评估 → 两轮润色 → 审查

### 示例 4：代码工程

```
@fable5-workflow_diy 写一个 Python 异步爬虫，支持并发控制和自动重试
```

→ 自动识别为「代码」→ 走 D 线 → 设计 → 实现 → 审查（安全/边缘/规范）

## 子技能关系

```
                    fable5-workflow_diy (编排层)
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   multi-agent       cot-reasoning    writing-quality
   research_diy          _diy             _diy
   (调研层)            (推理层)          (写作层)
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    agent-review_diy
                      (审查层 — 强制收尾)
```

## 与 Fable 5 的完整对标

| Fable 5 核心能力 | 流水线中的等价实现 |
|-----------------|-----------------|
| Adaptive Thinking | A/B/D 线的 cot-reasoning（显式推理链） |
| 子 Agent 调度 | A 线的 5 Agent 并行调研 |
| 文学性输出 | A/B/C 线的 writing-quality（两轮迭代） |
| 自我验证 | 所有线路末尾的 agent-review（五维审查） |
| 天级自主运行 | A 线的全自动四步流程 |
| 持久记忆 | 交付后自动写入每日日志 |

## 注意事项

- 如果任务类型模糊（同时含调研和写作），默认走 **A线**（最完整）
- 子技能按需顺序加载，不要一次性全部加载（浪费上下文）
- 最终交付始终是 DOCX + MD 双格式，DOCX 在前
- 审查标注的主要改动不超过 3 条

---

*Orchestrator of the [Fable 5 Workflow System](https://github.com/ZhangGZ-medical)*
