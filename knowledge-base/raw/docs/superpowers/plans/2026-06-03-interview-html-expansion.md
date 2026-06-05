# 面试与学习 HTML 知识页扩展实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `interview/html/` 新增 13 个知识页（6 面试首期 + 7 学习资源），更新首页 index.html 和 README.md，保持与 `transformer.html` 严格一致的视觉风格。

**Architecture:** 严格复用 `transformer.html` 现有的 :root CSS 变量、组件类、SVG 风格和五区结构（Hero / 原理+图+公式 / 落地 / FAQ）。13 个新 HTML 全部为纯静态，无外部 JS。每页 400-600 行（中深度）。首页在 Hero 之后新增「🎯 首期专项」和「📖 学习资源」两个区。

**Tech Stack:** HTML5 + 内联 CSS（CSS 变量）+ 内联 SVG。Google Fonts（Inter / Noto Sans SC，已在 transformer.html 引用）。不引入新依赖。

---

## 文件结构

### 新建文件

```
interview/html/
├── mcp.html                  # 面试首期 - MCP 协议
├── memory.html               # 面试首期 - Agent 记忆
├── lora.html                 # 面试首期 - LoRA 微调
├── kv-cache.html             # 面试首期 - KV Cache
├── react-cot.html            # 面试首期 - ReAct/CoT
├── multi-agent.html          # 面试首期 - Multi-Agent Router
├── rerank.html               # 学习资源 - Rerank
├── embedding.html            # 学习资源 - Embedding
├── llm-cache.html            # 学习资源 - API 缓存
├── model-distributed.html    # 学习资源 - 分布式部署
├── skill.html                # 学习资源 - Skill 机制
├── tool-use.html             # 学习资源 - Tool Use
└── llm-tuning.html           # 学习资源 - 大模型调优
```

### 修改文件

```
interview/html/index.html      # 加两个新区：首期专项 + 学习资源
interview/README.md            # 追加两段表格
mianshi.md                     # 追加 29 题原始题目
```

### 不修改

- 现有 5 个核心 HTML（rag / transformer / agent / sft / dpo）— 不动
- 现有 4 份学习指南（5/26-5/29）和 1 份早报 — 不动
- 8 份 Markdown 题库 — 暂不更新

---

## 模板

**每页严格遵循的骨架**（基于 `transformer.html`）：

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>主题名 知识页</title>
  <style>
    /* 完全复制 transformer.html 的 :root + 所有组件类（crumb / hero / card / svgbox / mathbox / qa / callout 等） */
  </style>
</head>
<body>
<div class="wrap">
  <div class="crumb">
    <a href="./index.html">首页</a>
    <a href="./相关页.html">相关</a>
    ...（5-7 个面包屑）
  </div>
  <div class="hero">
    <span class="eyebrow">分类</span>
    <h1>主题名</h1>
    <p class="lead">一句话定义</p>
    <div class="pillrow">
      <span class="pill">标签1</span>
      ...（4-5 个 pill）
    </div>
  </div>
  <div class="grid">
    <div class="card full">
      <h2>一、原理</h2>
      <p>背景段落</p>
      <ul>...</ul>
    </div>
    <div class="card">
      <h2>二、流程图</h2>
      <div class="svgbox">
        <svg viewBox="..." xmlns="http://www.w3.org/2000/svg">...</svg>
      </div>
    </div>
    <div class="card">
      <h2>三、关键公式</h2>
      <div class="mathbox">...</div>
    </div>
    <div class="card full">
      <h2>四、项目落地</h2>
      <p>蕉内实际案例 + 假设场景</p>
    </div>
    <div class="card full">
      <h2>五、面试 FAQ</h2>
      <div class="qa">
        <div><h3>Q</h3><p>A</p></div>
        ...（5-8 个）
      </div>
    </div>
  </div>
</div>
</body>
</html>
```

**视觉规则**（从 transformer.html 提取的不变量）：

- 主色：`--accent: #2563eb`（蓝）
- 浅色背景：`--accent-soft: #dbeafe`、`--accent-soft-2: #eff6ff`
- 文字：`--text: #0f172a`、`--muted: #475569`
- 圆角：`--radius: 18px`（card）、`28px`（hero）
- 阴影：`--shadow: 0 10px 30px rgba(15,23,42,.08)`
- 卡片网格：`grid-template-columns: repeat(12, ...)`，默认 card 占 6 列，`.full` 占 12 列
- SVG 框：`.svgbox` 用 `linear-gradient(180deg, var(--accent-soft-2), #fff)` 背景
- 公式框：`.mathbox` 用 `linear-gradient(180deg, #fff, #eff6ff)` 背景
- 不引外部 JS
- 字体栈：Inter / Noto Sans SC / system-ui

---

## 实施策略

按"先建样板 → 批量复制 → 填充内容"三步走，避免每页从 0 写：

1. **Task 0**：复制 `transformer.html` 为 `mcp.html`，改名 + 改标题，作为后续 12 页的基线
2. **Task 1-6**：6 面试首期 — 每页基于 `mcp.html` 复制，清空内容，填新主题
3. **Task 7-13**：7 学习资源 — 同上
4. **Task 14**：更新 `index.html` 加两个新区
5. **Task 15**：更新 `README.md`
6. **Task 16**：粘新原始题到 `mianshi.md`
7. **Task 17**：commit + push

每页 400-600 行（与 transformer.html 的 ~210 行相比，新页内容更丰富）。**关键约束**：每页不能引外部 JS，不能写死 hex 色值，必须用 CSS 变量。

---

## 任务清单

### Task 0: 创建基线模板（mcp.html）

**Files:**
- Create: `interview/html/mcp.html`

- [ ] **Step 1: 复制 transformer.html 到 mcp.html**

```bash
cp "D:\Data\Desktop\work\interview\html\transformer.html" "D:\Data\Desktop\work\interview\html\mcp.html"
```

- [ ] **Step 2: 修改 mcp.html 的标题**

将 `<title>Transformer 知识页</title>` 改为 `<title>MCP 知识页</title>`。

将 hero 区的 `<h1>Transformer</h1>` 改为 `<h1>MCP 协议</h1>`，`<span class="eyebrow">主题分类</span>` 改为 `<span class="eyebrow">面试首期 · 工具与协议</span>`。

- [ ] **Step 3: 验证 mcp.html 可打开**

在 IDE 中打开 `interview/html/mcp.html`，确认浏览器能渲染、样式不破。

- [ ] **Step 4: Commit 基线**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/mcp.html
git commit -m "feat: 创建 MCP 知识页基线（复用 transformer.html 模板）"
```

---

### Task 1: 完成 mcp.html（MCP 协议）

**Files:**
- Modify: `interview/html/mcp.html`（清空原 transformer 内容，填 MCP 主题）

- [ ] **Step 1: 重写 hero 区**

- 标题：`MCP 协议`
- 副标题：`Model Context Protocol — Agent 工具调用的标准化协议，让 LLM 通过统一 schema 调用外部工具`
- pill 标签：`MCP` `JSON-RPC` `Tool` `Resource` `Prompt`

- [ ] **Step 2: 写原理区（card full）**

内容大纲：
- MCP 是什么：Anthropic 2024 年提出的开放协议，标准化 LLM 与工具/数据源的通信
- 三大原语：Tool（可调用函数）、Resource（可读取数据）、Prompt（可复用提示模板）
- 通信方式：stdio（本地）/ SSE（服务器推送）/ HTTP（远程）
- 与 Function Call 的关系：MCP 是协议层，Function Call 是模型输出格式，两者互补

- [ ] **Step 3: 画 SVG 流程图**

内容：MCP 客户端-服务器架构图，包含 Host（Cline/Cursor）、MCP Client、MCP Server（多个）、Tool/Resource 三个矩形 + 连接线。

- [ ] **Step 4: 项目落地（card full）**

- 蕉内实际：飞书 Aily 工具集成、Aily MCP 工具调用
- 假设场景：Codex 通过 MCP 接入 RAG 检索 + 业务 API
- 简历表达：协议层理解、跨工具复用、企业级落地

- [ ] **Step 5: 写面试 FAQ（qa 双栏 6 个）**

Q1：MCP 和 Function Call 区别？
Q2：为什么需要 MCP 协议？
Q3：MCP 通信有几种方式？
Q4：MCP server 怎么发现和注册？
Q5：MCP 工具调用的错误怎么处理？
Q6：MCP 和传统 API 调用的本质区别？

- [ ] **Step 6: 更新面包屑和首页**

面包屑加：首页 / RAG / Agent / MCP（指向相关页）

- [ ] **Step 7: 验证**

打开 `mcp.html` 浏览器渲染正常，5 区齐全，400-600 行。

- [ ] **Step 8: Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/mcp.html
git commit -m "feat: 面试首期 - MCP 协议知识页"
```

---

### Task 2: 完成 memory.html（Agent 记忆）

**Files:**
- Create: `interview/html/memory.html`（基于 mcp.html 复制）

- [ ] **Step 1: 复制 mcp.html 为 memory.html**

```bash
cp "D:\Data\Desktop\work\interview\html\mcp.html" "D:\Data\Desktop\work\interview\html\memory.html"
```

- [ ] **Step 2: 替换 hero / 标题 / 副标题 / pill**

- 标题：`Agent 记忆`
- 副标题：`短期/长期记忆机制，让模型在长对话中保留用户偏好和历史上下文`
- pill：`Working Memory` `Episodic` `Semantic` `Compression` `Conflict`

- [ ] **Step 3: 写原理区**

- 四层记忆：Working（当前对话）/ Episodic（事件）/ Semantic（事实）/ Procedural（流程）
- 短期 vs 长期：短期放上下文窗口，长期放向量库
- 压缩策略：摘要、抽取、滑动窗口
- 冲突更新：新记忆 vs 旧记忆如何取舍

- [ ] **Step 4: 画 SVG 分层架构图**

Working → Episodic → Semantic → Procedural 四层 + 双向箭头。

- [ ] **Step 5: 项目落地**

- 蕉内实际：AI 数字员工员工偏好记忆
- 假设场景：客服 Agent 跨会话记住用户购买历史

- [ ] **Step 6: FAQ（6 个）**

Q1：短期和长期记忆怎么划分？
Q2：记忆冲突怎么办？
Q3：上下文窗口有限怎么压缩？
Q4：和 RAG 区别？
Q5：记忆的遗忘机制怎么设计？
Q6：多用户隔离怎么做？

- [ ] **Step 7: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/memory.html
git commit -m "feat: 面试首期 - Agent 记忆知识页"
```

---

### Task 3: 完成 lora.html（LoRA 微调）

**Files:**
- Create: `interview/html/lora.html`（基于 mcp.html 复制）

- [ ] **Step 1: 复制 mcp.html 为 lora.html**

```bash
cp "D:\Data\Desktop\work\interview\html\mcp.html" "D:\Data\Desktop\work\interview\html\lora.html"
```

- [ ] **Step 2: 替换 hero / pill**

- 标题：`LoRA 微调`
- 副标题：`低秩适应 — 用极小参数量（<1%）微调大模型，避免全量训练的高成本`
- pill：`Low-Rank` `Adapter` `Frozen` `Rank r` `A·B`

- [ ] **Step 3: 写原理区**

- 核心思想：冻结原权重 W，引入低秩旁路 ΔW = A·B（A ∈ R^(d×r), B ∈ R^(r×k), r ≪ min(d,k)）
- 为什么低秩：模型微调时权重变化是低秩的
- 训练参数：只训 A 和 B，总参数量约 d×r + r×k
- 推理合并：可将 A·B 合并到 W，零推理成本
- 变体：QLoRA（量化）、AdaLoRA（自适应秩）、LoRA+（不同学习率）

- [ ] **Step 4: 画 SVG 旁路结构图**

W（冻结） + ΔW = A·B（可训） → 输出

- [ ] **Step 5: 写公式区（mathbox）**

`ΔW = A·B`，`A ∈ R^(d×r)`，`B ∈ R^(r×k)`，`r ≪ min(d,k)`

- [ ] **Step 6: 项目落地**

- 蕉内实际：工艺部件库项目 Qwen LoRA 微调（"AI 编程首个纯 AI 项目"）
- 假设场景：蕉内小蕉 AI 行业知识 LoRA 微调

- [ ] **Step 7: FAQ（6 个）**

Q1：秩 r 怎么选？
Q2：LoRA 推理要带 Adapter 吗？
Q3：和全量微调效果差多少？
Q4：QLoRA 和 LoRA 区别？
Q5：冻结哪些层？
Q6：LoRA 显存计算？

- [ ] **Step 8: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/lora.html
git commit -m "feat: 面试首期 - LoRA 微调知识页"
```

---

### Task 4: 完成 kv-cache.html（KV Cache）

**Files:**
- Create: `interview/html/kv-cache.html`

- [ ] **Step 1: 复制 mcp.html 为 kv-cache.html**

```bash
cp "D:\Data\Desktop\work\interview\html\mcp.html" "D:\Data\Desktop\work\interview\html\kv-cache.html"
```

- [ ] **Step 2: 替换 hero / pill**

- 标题：`KV Cache`
- 副标题：`Transformer 推理加速 — 缓存已计算的 K/V，避免每步重新计算全序列 attention`
- pill：`Attention` `Paged` `Memory` `Throughput` `MQA/GQA`

- [ ] **Step 3: 写原理区**

- 为什么需要：自回归生成时每步只新增一个 token，但重新计算全序列 attention 浪费大
- 做法：缓存历史的 K、V 矩阵，新 token 只需算自己的 Q
- 显存代价：每层每步存一个 token 的 K 和 V，总显存 ∝ L × d × n_layers × 2
- 优化方向：
  - Multi-Query Attention (MQA)：所有 head 共享 K/V
  - Grouped Query Attention (GQA)：分组共享
  - PagedAttention (vLLM)：分页管理 KV 块
  - FlashAttention：在线计算 KV，减少显存

- [ ] **Step 4: 画 SVG 时序图**

step 1 / step 2 / step 3 三帧，每帧显示已缓存 K/V 和新计算的 Q。

- [ ] **Step 5: 写公式区**

`Memory(KV) = 2 × L × d × n_layers × n_heads × head_dim`（字节数 × dtype 字节）

- [ ] **Step 6: 项目落地**

- 蕉内实际：生图 Web 端长 prompt 推理
- 假设场景：蕉内 AI 客服长对话 KV 复用

- [ ] **Step 7: FAQ（6 个）**

Q1：KV Cache 显存怎么算？
Q2：PagedAttention 怎么省显存？
Q3：MQA 和 GQA 区别？
Q4：长上下文 KV Cache 满了怎么办？
Q5：KV Cache 和 Prompt Cache 区别？
Q6：Beam Search 时 KV Cache 怎么管理？

- [ ] **Step 8: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/kv-cache.html
git commit -m "feat: 面试首期 - KV Cache 知识页"
```

---

### Task 5: 完成 react-cot.html（ReAct / CoT）

**Files:**
- Create: `interview/html/react-cot.html`

- [ ] **Step 1: 复制 mcp.html 为 react-cot.html**

```bash
cp "D:\Data\Desktop\work\interview\html\mcp.html" "D:\Data\Desktop\work\interview\html\react-cot.html"
```

- [ ] **Step 2: 替换 hero / pill**

- 标题：`ReAct / CoT`
- 副标题：`推理与行动交织的 Agent 思维范式 — 边想边做，而不是想完再做`
- pill：`Thought` `Action` `Observation` `Loop` `Reflection`

- [ ] **Step 3: 写原理区**

- CoT（Chain of Thought）：先想后答，把推理过程显式化
- ReAct：Reason + Act 循环，Thought → Action → Observation → Thought ...
- 与 Plan-and-Execute 区别：ReAct 边想边调整，Plan-and-Execute 先全盘规划
- 何时用 ReAct：环境动态、需多步工具调用、错误需实时纠正
- 何时用 CoT 单次：单步推理、数学题、代码生成
- 反思（Reflection）：执行后自评，决定是否重试
- 失败模式：循环卡住、Observation 不准

- [ ] **Step 4: 画 SVG 循环图**

Thought → Action → Observation → Thought（回到顶部）

- [ ] **Step 5: 项目落地**

- 蕉内实际：Codex 任务规划、飞书 Aily 多步工具调用
- 假设场景：唯品会需求评估的多步推理

- [ ] **Step 6: FAQ（6 个）**

Q1：ReAct 和 Function Call 区别？
Q2：什么时候用 ReAct？
Q3：ReAct 会陷入循环吗？
Q4：CoT 和 ReAct 可以组合吗？
Q5：如何让 Agent 不重复尝试？
Q6：ReAct 和 Plan-and-Execute 选哪个？

- [ ] **Step 7: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/react-cot.html
git commit -m "feat: 面试首期 - ReAct/CoT 知识页"
```

---

### Task 6: 完成 multi-agent.html（多 Agent Router）

**Files:**
- Create: `interview/html/multi-agent.html`

- [ ] **Step 1: 复制 mcp.html 为 multi-agent.html**

```bash
cp "D:\Data\Desktop\work\interview\html\mcp.html" "D:\Data\Desktop\work\interview\html\multi-agent.html"
```

- [ ] **Step 2: 替换 hero / pill**

- 标题：`多 Agent Router`
- 副标题：`Multi-Agent 架构 — 用专门子 Agent 分担复杂任务，Router 统一调度`
- pill：`Router` `Supervisor` `Debate` `Handoff` `Conflict`

- [ ] **Step 3: 写原理区**

- 为什么需要：单 Agent 上下文压力大、专业度不够、错误风险集中
- 核心组件：Router（任务分发）、Sub-Agent（专项执行）、Shared Memory（共享状态）
- 模式：
  - Router 模式：入口分发到子 Agent
  - Supervisor 模式：监控 + 协调
  - Debate 模式：多 Agent 投票
  - Handoff 模式：动态交接
- 通信：消息队列 / 共享状态 / 直接调用
- 决策冲突：优先级、共识、Supervisor 仲裁

- [ ] **Step 4: 画 SVG 架构图**

Router（顶）→ 3 个 Sub-Agent（设计/数据/客服）→ Shared Memory

- [ ] **Step 5: 项目落地**

- 蕉内实际：AI 数字员工多场景分流（设计/数据/客服）
- 假设场景：蕉内数字员工多场景分流

- [ ] **Step 6: FAQ（6 个）**

Q1：单 Agent 什么时候不够用？
Q2：Router 怎么设计？
Q3：Agent 间决策冲突怎么办？
Q4：Sub-Agent 通信用什么协议？
Q5：多 Agent 调试怎么排查？
Q6：Router 和 Supervisor 模式选哪个？

- [ ] **Step 7: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/multi-agent.html
git commit -m "feat: 面试首期 - 多 Agent Router 知识页"
```

---

### Task 7: 完成 rerank.html（Rerank 重排序）

**Files:**
- Create: `interview/html/rerank.html`

- [ ] **Step 1: 复制 mcp.html 为 rerank.html**

```bash
cp "D:\Data\Desktop\work\interview\html\mcp.html" "D:\Data\Desktop\work\interview\html\rerank.html"
```

- [ ] **Step 2: 替换 hero / pill**

- 标题：`Rerank 重排序`
- 副标题：`用 Cross-Encoder / ColBERT / LLM 对初筛结果精排，提升 Top-K 准确率`
- pill：`Cross-Encoder` `ColBERT` `LLM Rerank` `Top-K` `MRR`

- [ ] **Step 3: 写原理区**

- 为什么需要：Embedding 召回速度快但精度有限（双塔结构无交互）
- Cross-Encoder：query 和 doc 拼接后过 BERT，输出相关性分数
- ColBERT：late interaction，每 token 算 query-doc 相似度再聚合
- LLM Rerank：用 LLM 评估相关性（如 GPT-4 / Qwen-Long）
- 评估指标：MRR、NDCG@K、Recall@K
- 工程权衡：Cross-Encoder 准但慢、LLM Rerank 最准但最贵

- [ ] **Step 4: 画 SVG 流程图**

初筛召回（Embedding）→ Top-100 → Rerank → Top-10

- [ ] **Step 5: 写公式区**

`score(q, d) = W·s([CLS]_q;d)`（Cross-Encoder 输出）

- [ ] **Step 6: 项目落地**

- 蕉内实际：蕉内 AI 数字员工知识库检索
- 假设场景：客服系统初筛 + 精排

- [ ] **Step 7: FAQ（6 个）**

Q1：Rerank 为什么不能替代召回？
Q2：Cross-Encoder 慢在哪？
Q3：ColBERT 怎么平衡精度和速度？
Q4：LLM Rerank 怎么降本？
Q5：Rerank 怎么评估？
Q6：Top-K 设多大合适？

- [ ] **Step 8: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/rerank.html
git commit -m "feat: 学习资源 - Rerank 重排序知识页"
```

---

### Task 8: 完成 embedding.html（Embedding 选型）

**Files:**
- Create: `interview/html/embedding.html`

- [ ] **Step 1: 复制 mcp.html 为 embedding.html**

```bash
cp "D:\Data\Desktop\work\interview\html\mcp.html" "D:\Data\Desktop\work\interview\html\embedding.html"
```

- [ ] **Step 2: 替换 hero / pill**

- 标题：`Embedding 选型`
- 副标题：`向量化原理、模型选型、稀疏 vs 稠密检索`
- pill：`BGE` `M3E` `OpenAI` `Dense` `Sparse`

- [ ] **Step 3: 写原理区**

- 原理：文本 → 向量，相似度 = 语义相似度
- 稠密 vs 稀疏：稠密（BGE/M3E）语义理解强，稀疏（BM25/SPLADE）关键词匹配强
- 混合检索：两者加权融合（RRF / 加权求和）
- 选型维度：语言、维度、速度、领域适配、私有化
- 中文常用：BGE-M3 / M3E / Qwen-Embedding / 智源 BGE
- 训练细节：对比学习、难负例采样、in-batch negatives
- 评估：MTEB 榜单、领域内评测

- [ ] **Step 4: 画 SVG 流程图**

文本 → Encoder → 向量 → 相似度计算

- [ ] **Step 5: 写公式区**

`sim(q, d) = cos(E(q), E(d)) = E(q)·E(d) / (||E(q)||·||E(d)||)`

- [ ] **Step 6: 项目落地**

- 蕉内实际：蕉内 AI 数字员工行业知识向量化
- 假设场景：蕉内数字员工场景化知识检索

- [ ] **Step 7: FAQ（6 个）**

Q1：稠密 vs 稀疏怎么选？
Q2：维度越大越好吗？
Q3：怎么评测 Embedding 质量？
Q4：私有化怎么部署 Embedding？
Q5：Embedding 怎么微调？
Q6：多语言场景怎么办？

- [ ] **Step 8: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/embedding.html
git commit -m "feat: 学习资源 - Embedding 选型知识页"
```

---

### Task 9: 完成 llm-cache.html（API 缓存命中）

**Files:**
- Create: `interview/html/llm-cache.html`

- [ ] **Step 1: 复制 mcp.html 为 llm-cache.html**

```bash
cp "D:\Data\Desktop\work\interview\html\mcp.html" "D:\Data\Desktop\work\interview\html\llm-cache.html"
```

- [ ] **Step 2: 替换 hero / pill**

- 标题：`大模型 API 缓存`
- 副标题：`Prompt Cache / KV Cache 复用 / 语义缓存 — 降本和降延迟的关键`
- pill：`Prompt Cache` `KV Cache` `Semantic Cache` `TTL` `Hit Rate`

- [ ] **Step 3: 写原理区**

- Prompt Cache：相同前缀 prompt 复用 KV（如 Anthropic / OpenAI 都有）
- KV Cache 复用：会话内 KV 不重建
- 语义缓存：embedding 相似度判断是否复用历史回答
- 命中率优化：前缀稳定、模板化、相似度阈值
- 失效策略：TTL、版本号、显式 invalidate
- 适用场景：FAQ 客服、代码补全、模板化生成
- 不适用场景：每次 prompt 都不同、个性化对话

- [ ] **Step 4: 画 SVG 流程图**

Request → Cache Key 计算 → 命中/未命中 → 复用/全量推理

- [ ] **Step 5: 写公式区**

`节省成本 = 命中率 × 单次推理成本`

- [ ] **Step 6: 项目落地**

- 蕉内实际：飞书 Aily FAQ 语义缓存
- 假设场景：蕉内数字员工高频问答降本

- [ ] **Step 7: FAQ（6 个）**

Q1：Prompt Cache 和 KV Cache 区别？
Q2：语义缓存怎么判断相似？
Q3：命中率多少算合格？
Q4：缓存失效怎么处理？
Q5：缓存会泄露隐私吗？
Q6：怎么监控缓存效果？

- [ ] **Step 8: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/llm-cache.html
git commit -m "feat: 学习资源 - 大模型 API 缓存知识页"
```

---

### Task 10: 完成 model-distributed.html（分布式部署）

**Files:**
- Create: `interview/html/model-distributed.html`

- [ ] **Step 1: 复制 mcp.html 为 model-distributed.html**

```bash
cp "D:\Data\Desktop\work\interview\html\mcp.html" "D:\Data\Desktop\work\interview\html\model-distributed.html"
```

- [ ] **Step 2: 替换 hero / pill**

- 标题：`模型分布式部署`
- 副标题：`vLLM / SGLang / PagedAttention / TP/PP/DP — 提高 TPS 的核心方法`
- pill：`vLLM` `SGLang` `PagedAttention` `Tensor Parallel` `TPS`

- [ ] **Step 3: 写原理区**

- 推理瓶颈：显存、计算、带宽
- Continuous Batching：动态拼批，提升 GPU 利用率
- PagedAttention（vLLM）：分页管理 KV Cache，类似 OS 虚拟内存
- SGLang RadixAttention：基于前缀树的 KV 复用
- Tensor Parallel（TP）：层内切分到多卡
- Pipeline Parallel（PP）：按层切分到多卡
- Data Parallel（DP）：多副本并行
- 选型：vLLM 通用、SGLang 复杂 prompt、TensorRT-LLM 高性能

- [ ] **Step 4: 画 SVG 架构图**

Prompt → Tokenizer → TP×4 → Scheduler → Batched Decode → Detokenizer

- [ ] **Step 5: 写公式区**

`TPS = batch_size × seq_len / decode_time`（每 GPU）

- [ ] **Step 6: 项目落地**

- 蕉内实际：小蕉 AI 服务 1500+ 用户
- 假设场景：蕉内数字员工高并发场景

- [ ] **Step 7: FAQ（6 个）**

Q1：PagedAttention 为什么能省显存？
Q2：vLLM 和 SGLang 选哪个？
Q3：TP/PP/DP 怎么组合？
Q4：多机推理通信瓶颈？
Q5：怎么测 TPS？
Q6：Continuous Batching 怎么实现的？

- [ ] **Step 8: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/model-distributed.html
git commit -m "feat: 学习资源 - 模型分布式部署知识页"
```

---

### Task 11: 完成 skill.html（Skill 机制）

**Files:**
- Create: `interview/html/skill.html`

- [ ] **Step 1: 复制 mcp.html 为 skill.html**

```bash
cp "D:\Data\Desktop\work\interview\html\mcp.html" "D:\Data\Desktop\work\interview\html\skill.html"
```

- [ ] **Step 2: 替换 hero / pill**

- 标题：`Skill 机制`
- 副标题：`Skill 创建方式（NL / 代码 / hybrid）、与 MCP/Tool 的区别与组合`
- pill：`Skill` `MCP` `Tool` `Hybrid` `Reusable`

- [ ] **Step 3: 写原理区**

- Skill 是什么：可复用的能力单元，封装提示词 + 工具调用 + 工作流
- 创建方式：
  - NL 描述：自然语言定义 Skill 行为
  - 代码实现：用代码定义 Skill（如 Cursor / Codex）
  - Hybrid：NL 描述 + 代码工具组合
- 与 Tool 区别：Tool 是单次函数调用，Skill 是多步工作流
- 与 MCP 区别：MCP 是协议，Skill 是内容
- 组合：Skill 内部可以调用 MCP Tool
- 工程实践：Skill 版本管理、依赖管理、测试

- [ ] **Step 4: 画 SVG 关系图**

User → Skill（NL+Code）→ MCP Tool（多个）→ 业务系统

- [ ] **Step 5: 项目落地**

- 蕉内实际：Codex Skill 使用
- 假设场景：蕉内数字员工 Skill 库

- [ ] **Step 6: FAQ（6 个）**

Q1：Skill 和 Tool 区别？
Q2：Skill 和 MCP 关系？
Q3：怎么创建第一个 Skill？
Q4：Skill 怎么测试？
Q5：Skill 怎么版本管理？
Q6：Skill 和 Prompt 区别？

- [ ] **Step 7: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/skill.html
git commit -m "feat: 学习资源 - Skill 机制知识页"
```

---

### Task 12: 完成 tool-use.html（Tool Use）

**Files:**
- Create: `interview/html/tool-use.html`

- [ ] **Step 1: 复制 mcp.html 为 tool-use.html**

```bash
cp "D:\Data\Desktop\work\interview\html\mcp.html" "D:\Data\Desktop\work\interview\html\tool-use.html"
```

- [ ] **Step 2: 替换 hero / pill**

- 标题：`Tool Use 工具调用`
- 副标题：`Function Calling 原理、JSON Schema、多轮调用状态管理`
- pill：`Function Call` `JSON Schema` `Multi-turn` `Error` `Retry`

- [ ] **Step 3: 写原理区**

- 原理：模型在 prompt 中看到工具 schema，输出结构化调用参数
- 流程：tool 描述注入 → 模型选 tool → 输出参数 → 客户端执行 → 结果回灌 → 继续生成
- JSON Schema：定义 tool 名称、参数、类型、必填、描述
- 多轮调用：一个 prompt 多次 tool call
- 错误处理：参数校验失败、超时、不可重试错误
- 重试策略：指数退避、最大次数、fallback
- 安全：参数注入防护、工具白名单

- [ ] **Step 4: 画 SVG 时序图**

User → LLM → Tool Call → Client → Tool Execute → Result → LLM → Response

- [ ] **Step 5: 写代码示例区（card）**

```json
{
  "name": "search_products",
  "description": "搜索商品",
  "parameters": {
    "type": "object",
    "properties": {
      "keyword": {"type": "string"},
      "limit": {"type": "integer", "default": 10}
    },
    "required": ["keyword"]
  }
}
```

- [ ] **Step 6: 项目落地**

- 蕉内实际：飞书 Aily 工具调用、Codex 工具集成
- 假设场景：蕉内数字员工 RAG 检索工具

- [ ] **Step 7: FAQ（6 个）**

Q1：Function Call 流程是怎样的？
Q2：JSON Schema 怎么写？
Q3：多轮 Tool Call 怎么管理状态？
Q4：Tool Call 错误怎么处理？
Q5：Tool Call 和 Prompt 注入风险？
Q6：怎么调试 Tool Call？

- [ ] **Step 8: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/tool-use.html
git commit -m "feat: 学习资源 - Tool Use 工具调用知识页"
```

---

### Task 13: 完成 llm-tuning.html（大模型调优）

**Files:**
- Create: `interview/html/llm-tuning.html`

- [ ] **Step 1: 复制 mcp.html 为 llm-tuning.html**

```bash
cp "D:\Data\Desktop\work\interview\html\mcp.html" "D:\Data\Desktop\work\interview\html\llm-tuning.html"
```

- [ ] **Step 2: 替换 hero / pill**

- 标题：`大模型调优`
- 副标题：`Prompt 调优、采样参数、结构化输出、推理能力激活 — 不改权重也能大幅提升效果`
- pill：`Prompt` `Temperature` `Top-p` `CoT` `JSON Mode`

- [ ] **Step 3: 写原理区**

- Prompt 调优：少样本（Few-shot）、角色设定、约束条件
- 采样参数：
  - Temperature：高=发散、低=确定
  - Top-p：nucleus sampling，截断低概率
  - Top-k：保留 top k 高概率
  - Frequency / Presence penalty：抑制重复
- 结构化输出：JSON Mode、Function Call、Grammar Constrained Decoding
- 推理激活：CoT、Self-Consistency、ReAct
- 评估：困惑度、人工评估、A/B 测试
- 不改权重的边界：复杂任务仍需微调

- [ ] **Step 4: 画 SVG 决策树**

需求分析 → 选 Prompt 策略 → 选采样参数 → 评估 → 调优

- [ ] **Step 5: 写公式区**

`P'(x) = P(x)^(1/T) / Σ P(x)^(1/T)`（Temperature 缩放）

- [ ] **Step 6: 项目落地**

- 蕉内实际：小蕉 AI 提示词调优
- 假设场景：蕉内数字员工场景化 Prompt 调优

- [ ] **Step 7: FAQ（6 个）**

Q1：Temperature 怎么选？
Q2：Top-p 和 Top-k 区别？
Q3：怎么让输出稳定 JSON？
Q4：CoT 什么时候用？
Q5：Prompt 调优和微调选哪个？
Q6：怎么评估 Prompt 效果？

- [ ] **Step 8: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/llm-tuning.html
git commit -m "feat: 学习资源 - 大模型调优知识页"
```

---

### Task 14: 更新 index.html（首页加两个新区）

**Files:**
- Modify: `interview/html/index.html`

- [ ] **Step 1: 在 Hero 后插入「🎯 首期专项」区**

在 `</div>`（Hero 结束）后、`<!-- MODULE 1: 面试核心知识 -->` 之前，插入：

```html
<!-- MODULE 0: 首期专项 -->
<div class="section">
  <div class="section-head">
    <h2>🎯 首期专项 · 6 面试页</h2>
    <span class="section-sub" style="margin:0">高频追问补齐：从现有 5 个核心页出发，覆盖面试 6 个最常被追问的主题。</span>
  </div>
  <div class="grid">
    <a class="card span-4" href="./mcp.html">
      <h3>MCP <span class="tag accent">新</span></h3>
      <p>Model Context Protocol — Agent 工具调用的标准化协议。</p>
      <div class="tagrow">
        <span class="tag">JSON-RPC</span><span class="tag">Tool</span><span class="tag">Resource</span>
      </div>
    </a>
    <a class="card span-4" href="./memory.html">
      <h3>Memory <span class="tag accent">新</span></h3>
      <p>Agent 短期/长期记忆机制，长对话保留用户偏好。</p>
      <div class="tagrow">
        <span class="tag">Working</span><span class="tag">Episodic</span><span class="tag">Semantic</span>
      </div>
    </a>
    <a class="card span-4" href="./lora.html">
      <h3>LoRA <span class="tag accent">新</span></h3>
      <p>低秩适应 — 用极小参数量微调大模型。</p>
      <div class="tagrow">
        <span class="tag">Low-Rank</span><span class="tag">Adapter</span><span class="tag">A·B</span>
      </div>
    </a>
    <a class="card span-4" href="./kv-cache.html">
      <h3>KV Cache <span class="tag accent">新</span></h3>
      <p>Transformer 推理加速 — 缓存已计算的 K/V。</p>
      <div class="tagrow">
        <span class="tag">Paged</span><span class="tag">MQA</span><span class="tag">Throughput</span>
      </div>
    </a>
    <a class="card span-4" href="./react-cot.html">
      <h3>ReAct / CoT <span class="tag accent">新</span></h3>
      <p>推理与行动交织的 Agent 思维范式。</p>
      <div class="tagrow">
        <span class="tag">Thought</span><span class="tag">Action</span><span class="tag">Loop</span>
      </div>
    </a>
    <a class="card span-4" href="./multi-agent.html">
      <h3>Multi-Agent <span class="tag accent">新</span></h3>
      <p>Multi-Agent 架构 — 用专门子 Agent 分担复杂任务。</p>
      <div class="tagrow">
        <span class="tag">Router</span><span class="tag">Supervisor</span><span class="tag">Handoff</span>
      </div>
    </a>
  </div>
</div>

<!-- MODULE 0.5: 学习资源 -->
<div class="section">
  <div class="section-head">
    <h2>📖 学习资源 · 7 主题</h2>
    <span class="section-sub" style="margin:0">深度学习方向：每个主题 1 页讲解稿，覆盖原理 + 工程 + 项目落地 + FAQ。</span>
  </div>
  <div class="grid">
    <a class="card span-4" href="./rerank.html">
      <h3>Rerank <span class="tag purple">学</span></h3>
      <p>Cross-Encoder / ColBERT / LLM Rerank 原理与选型。</p>
      <div class="tagrow">
        <span class="tag">Cross-Encoder</span><span class="tag">ColBERT</span><span class="tag">MRR</span>
      </div>
    </a>
    <a class="card span-4" href="./embedding.html">
      <h3>Embedding <span class="tag purple">学</span></h3>
      <p>向量化原理、模型选型、稀疏 vs 稠密检索。</p>
      <div class="tagrow">
        <span class="tag">BGE</span><span class="tag">M3E</span><span class="tag">Dense</span>
      </div>
    </a>
    <a class="card span-4" href="./llm-cache.html">
      <h3>API 缓存 <span class="tag purple">学</span></h3>
      <p>Prompt Cache / KV Cache 复用 / 语义缓存。</p>
      <div class="tagrow">
        <span class="tag">Prompt</span><span class="tag">Semantic</span><span class="tag">Hit Rate</span>
      </div>
    </a>
    <a class="card span-4" href="./model-distributed.html">
      <h3>分布式部署 <span class="tag purple">学</span></h3>
      <p>vLLM / SGLang / PagedAttention / TP/PP/DP。</p>
      <div class="tagrow">
        <span class="tag">vLLM</span><span class="tag">SGLang</span><span class="tag">TPS</span>
      </div>
    </a>
    <a class="card span-4" href="./skill.html">
      <h3>Skill 机制 <span class="tag purple">学</span></h3>
      <p>Skill 创建方式（NL / 代码 / hybrid）、与 MCP/Tool 区别。</p>
      <div class="tagrow">
        <span class="tag">Skill</span><span class="tag">MCP</span><span class="tag">Hybrid</span>
      </div>
    </a>
    <a class="card span-4" href="./tool-use.html">
      <h3>Tool Use <span class="tag purple">学</span></h3>
      <p>Function Calling 原理、JSON Schema、多轮调用。</p>
      <div class="tagrow">
        <span class="tag">Function Call</span><span class="tag">JSON</span><span class="tag">Multi-turn</span>
      </div>
    </a>
    <a class="card span-8" href="./llm-tuning.html">
      <h3>大模型调优 <span class="tag purple">学</span></h3>
      <p>Prompt 调优、采样参数、结构化输出、推理激活。</p>
      <div class="tagrow">
        <span class="tag">Prompt</span><span class="tag">Temperature</span><span class="tag">CoT</span><span class="tag">JSON Mode</span>
      </div>
    </a>
  </div>
</div>
```

- [ ] **Step 2: 更新 meta 计数**

将原 `<span><b>3</b> 大模块</span>` 改为 `<span><b>5</b> 大模块</span>`，`<span><b>5</b> 个核心知识页</span>` 改为 `<span><b>18</b> 个知识页</span>`。

- [ ] **Step 3: 更新学习路径，指向新页**

「路径 A · 面试前 3 天速通」追加 MCP、Memory、LoRA、KV Cache。
「路径 B · 日常学习」追加 Rerank、Embedding、Tool Use、Skill。
「路径 C · 训练 / 对齐方向深挖」追加 LoRA（与训练方向结合）。

- [ ] **Step 4: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/html/index.html
git commit -m "feat: 首页加首期专项 + 学习资源两个新区（共 13 张卡片）"
```

---

### Task 15: 更新 README.md

**Files:**
- Modify: `interview/README.md`

- [ ] **Step 1: 在「可视化 HTML 知识页」小节后追加两段**

```markdown
### 面试首期专项（6 个）

| 页面 | 内容 |
|------|------|
| [html/mcp.html](html/mcp.html) | MCP 协议：JSON-RPC、Tool/Resource/Prompt 三大原语、与 Function Call 关系 |
| [html/memory.html](html/memory.html) | Agent 记忆：Working/Episodic/Semantic 四层架构、压缩策略、冲突更新 |
| [html/lora.html](html/lora.html) | LoRA 微调：低秩分解 A·B、秩 r 选择、推理合并、QLoRA 变体 |
| [html/kv-cache.html](html/kv-cache.html) | KV Cache：自回归缓存、PagedAttention、MQA/GQA 优化 |
| [html/react-cot.html](html/react-cot.html) | ReAct/CoT：思维-行动循环、与 Function Call 关系、何时选用 |
| [html/multi-agent.html](html/multi-agent.html) | 多 Agent Router：Router/Supervisor/Debate/Handoff 模式、决策冲突 |

### 学习资源（7 个）

| 页面 | 内容 |
|------|------|
| [html/rerank.html](html/rerank.html) | Rerank：Cross-Encoder、ColBERT、LLM Rerank、与 Embedding 召回的职责划分 |
| [html/embedding.html](html/embedding.html) | Embedding 选型：稠密 vs 稀疏、BGE/M3E/Qwen、训练与微调 |
| [html/llm-cache.html](html/llm-cache.html) | API 缓存：Prompt Cache、KV Cache 复用、语义缓存、命中率优化 |
| [html/model-distributed.html](html/model-distributed.html) | 分布式部署：vLLM/SGLang、PagedAttention、TP/PP/DP 张量并行 |
| [html/skill.html](html/skill.html) | Skill 机制：NL/代码/hybrid 创建、与 MCP/Tool 区别与组合 |
| [html/tool-use.html](html/tool-use.html) | Tool Use：Function Calling 原理、JSON Schema、多轮调用与错误处理 |
| [html/llm-tuning.html](html/llm-tuning.html) | 大模型调优：Prompt 调优、Temperature/Top-p、结构化输出、CoT 激活 |
```

- [ ] **Step 2: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add interview/README.md
git commit -m "docs: README 追加首期专项和学习资源两个表格"
```

---

### Task 16: 追加原始题到 mianshi.md

**Files:**
- Modify: `mianshi.md`（追加，不删除现有内容）

- [ ] **Step 1: 在 mianshi.md 末尾追加新原始题**

把 29 题按 Markdown 列表追加（一行一题），加标题分隔。

- [ ] **Step 2: 验证 + Commit**

```bash
cd "D:\Data\Desktop\work"
git add mianshi.md
git commit -m "docs: 追加 29 题面试原始题到 mianshi.md"
```

---

### Task 17: 最终验证 + 推送

- [ ] **Step 1: 文件计数验证**

```bash
cd "D:\Data\Desktop\work\interview\html"
ls *.html | wc -l
```

预期：24+ 个 HTML（旧 10 + 新 13 + 1 index-legacy）。

- [ ] **Step 2: 逐个打开 13 新页**

IDE 中打开 13 个新 HTML，确认：
- 标题正确
- 5 区齐全（Hero / 原理 / 流程图或公式 / 落地 / FAQ）
- 视觉风格与 transformer.html 一致
- 链接可跳转

- [ ] **Step 3: 最终 commit（如有遗漏）+ push**

```bash
cd "D:\Data\Desktop\work"
git add -A
git status  # 检查无意外文件
git commit -m "feat: 13 个面试与学习 HTML 知识页（首期 6 面试 + 7 学习）" --allow-empty
git push origin main
```

预期：远端 main 推进 N 个 commit。

---

## 自我审查

### Spec 覆盖检查

- ✅ 6 面试首期页（Task 1-6）
- ✅ 7 学习资源页（Task 7-13）
- ✅ 首页 index.html 加两个新区（Task 14）
- ✅ README.md 追加两段（Task 15）
- ✅ mianshi.md 追加原始题（Task 16）
- ✅ 模板结构（每页 5 区：Hero / 原理 / 流程图 / 落地 / FAQ）
- ✅ 视觉风格严格复用 transformer.html
- ✅ commit + push（Task 17）

### 占位符扫描

- ✅ 无 TBD / TODO
- ✅ 无 "implement later"
- ✅ 无 "fill in details"
- ✅ 无 "add appropriate error handling"
- ✅ 每页内容大纲在 Task 1-13 已给具体内容
- ✅ 13 个 Task 步骤可独立执行

### 类型一致性

- 文件命名一致：6 面试页用小写 + 连字符（kv-cache.html、react-cot.html、multi-agent.html）
- 7 学习页命名一致：rerank / embedding / llm-cache / model-distributed / skill / tool-use / llm-tuning
- 命名映射表清晰：每个 Task 都明确「复制 mcp.html 为 X.html」

### 风险点

- 13 页 × 5 步内容填充 = 65 个内容块，每块需要准确技术细节。**缓解**：每页都引用 transformer.html / rag.html 已有类，不引新组件
- 首页一次加 2 个新区可能视觉密度过高。**缓解**：复用现有 .section + .card 样式，不改 token
- 13 页总行数 ≈ 6000+ 行手写 HTML，工作量大。**缓解**：复制基线 + 替换内容，避免从 0 写
