# 2026-06-03 面试与学习 HTML 知识页扩展设计

## 背景

`interview/html/` 已有 5 个核心知识页（Transformer / RAG / Agent / SFT / DPO）+ 4 份 Agent 学习指南（5/26-5/29）+ 1 份 AI 行业早报。Markdown 题库 01-08 已积累 3992 行内容。

本仓库的整理规则是：每场面试高频追问 1 页 HTML 可视化讲解稿，每个学习方向 1 页深度讲解。**但当前只有 5 个核心页**，覆盖度与 Markdown 题库不匹配。

本次扩展目标：把高频追问和学习方向补齐到 13 个新页面，**保持与现有 transformer.html / rag.html 严格一致的视觉风格**，让首页能"一站式导航"。

## 范围

**去重原则**：你最初提到的 10 个学习主题里，RAG、MCP、Agent Memory 已有覆盖，去重后实际新做 7 个学习页。RAG 走 `rag.html`、MCP 和 Memory 走 6 面试页路线（不重复做）。

### 6 个面试首期页（高频追问补齐）

| 文件 | 主题 | 一句话定义 |
|------|------|------------|
| `mcp.html` | MCP 协议 | Model Context Protocol — Agent 工具调用的标准化协议 |
| `memory.html` | Agent 记忆 | 短期/长期记忆机制，让模型在长对话中保留用户偏好 |
| `lora.html` | LoRA 微调 | 低秩适应 — 用极小参数量微调大模型 |
| `kv-cache.html` | KV Cache | Transformer 推理加速 — 缓存已计算的 K/V |
| `react-cot.html` | ReAct / CoT | 推理与行动交织的 Agent 思维范式 |
| `multi-agent.html` | 多 Agent Router | Multi-Agent 架构与任务路由 |

### 7 个学习资源页（深度学习方向）

| 文件 | 主题 | 一句话定义 |
|------|------|------------|
| `rerank.html` | Rerank 重排序 | Cross-Encoder / ColBERT / LLM Rerank 原理 |
| `embedding.html` | Embedding 选型 | 向量化原理、模型选型、稀疏 vs 稠密 |
| `llm-cache.html` | API 缓存命中 | Prompt Cache / KV Cache 复用 / 语义缓存 |
| `model-distributed.html` | 分布式部署 | vLLM / SGLang / PagedAttention / TP/PP/DP |
| `skill.html` | Skill 机制 | Skill 创建方式（NL / 代码 / hybrid）、与 MCP/Tool 区别 |
| `tool-use.html` | Tool Use | Function Calling 原理、JSON Schema、多轮调用 |
| `llm-tuning.html` | 大模型调优 | Prompt 调优、采样参数、结构化输出、推理激活 |

### 首页变更

- 在 `Hero` 之后、模块一之前，**新增两个区**：
  - **🎯 首期专项 · 6 面试页**：6 张卡片，每张含标签 + 跳转
  - **📖 学习资源 · 7 主题**：7 张卡片，主题色不同（紫色边）
- 现有 4 大模块（核心知识 / 学习指南 / AI 早报 / 配套题库）保持原位
- 学习路径区更新指向新页

## 模板结构

每页严格复用 `transformer.html` 设计 token 和组件类。五区结构：

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <!-- 完全复用 transformer.html 的 :root CSS 变量和组件类 -->
  <!-- 不引入新组件，避免风格漂移 -->
</head>
<body>
<div class="wrap">
  <div class="crumb">...首页 + 其它 N 页导航...</div>
  <div class="hero">
    <span class="eyebrow">主题分类</span>
    <h1>主题名</h1>
    <p class="lead">一句话定义</p>
    <div class="pillrow">4-5 个 pill 标签</div>
  </div>
  <div class="grid">
    <div class="card full">原理 · 文字拆解（ul/ol）</div>
    <div class="card">SVG 流程图（.svgbox）</div>
    <div class="card">关键公式（.mathbox）</div>
    <div class="card full">项目落地（蕉内案例 + 假设场景）</div>
    <div class="card full">面试 FAQ（.qa 双栏，5-8 个 Q&A）</div>
  </div>
</div>
</body>
</html>
```

**深度**：每页 400-600 行（中深度）。

**视觉规则**：
- 不引外部字体（与现有页一致，已用 Google Fonts）
- 不引外部 JS
- SVG 内联手绘
- 公式用 `.mathbox` + `.frac` 等现有类
- 颜色全部走 `:root` 变量，不写死 hex

## 文件结构

```
interview/
├── html/
│   ├── index.html                # 首页（重构：加两个新区）
│   ├── index-legacy.html         # 旧版备份
│   ├── rag.html / transformer.html / agent.html / sft.html / dpo.html  # 已有 5 页
│   ├── 2026-05-26.html ~ 2026-05-29.html  # 已有 4 学习指南
│   ├── ai-daily-2026-05-29.html  # 已有 1 早报
│   ├── mcp.html                  # 新
│   ├── memory.html               # 新
│   ├── lora.html                 # 新
│   ├── kv-cache.html             # 新
│   ├── react-cot.html            # 新
│   ├── multi-agent.html          # 新
│   ├── rerank.html               # 新
│   ├── embedding.html            # 新
│   ├── llm-cache.html            # 新
│   ├── model-distributed.html    # 新
│   ├── skill.html                # 新
│   ├── tool-use.html             # 新
│   └── llm-tuning.html           # 新
├── 01-大模型基础.md ~ 08-前端AI应用与产品设计.md  # 现有题库
└── README.md                     # 更新
```

## 写作约定

- **原理区**：先 1 段背景，再 ul/ol 拆解，引用现有 transformer.html 风格
- **SVG**：简单流程图用纯 SVG 内联（不引外部库）
- **公式**：用 `.mathbox` + `.frac` 类；如无公式可省
- **项目落地**：
  - 蕉内实际案例优先（如 LoRA → 工艺部件库项目、Memory → AI 数字员工）
  - 无实际案例时用「假设落地场景」
  - 避免暴露内部敏感实现细节
- **FAQ**：5-8 个 Q&A，按"基础 → 原理 → 工程 → 边界"顺序排列
- **不确定事实**：用"可以这样设计 / 阶段性指标"表达，不编线上数据

## 实施步骤

1. 写首页变更草稿（只改 index.html 头部加两个区）
2. 逐个产出 13 个 HTML（按"面试 6 页 → 学习 7 页"顺序）
3. 更新 README.md（追加两段：首期专项、学习资源）
4. 提交 commit、push
5. 验证：13 个新页 + 首页 + 旧 5 页全部本地可打开

## 不做的事

- ❌ 不重做已有 RAG / Transformer / Agent / SFT / DPO 5 页
- ❌ 不重做 RAG 学习页（已有 rag.html 覆盖）
- ❌ 不做新的 subdir（保持扁平结构）
- ❌ 不写代码生成器 / 转换脚本（13 页规模不划算）
- ❌ 不做交互（搜索、折叠、动画）— 保持纯静态

## 风险

- **风格漂移**：13 页手写时容易偏离 transformer.html 风格。**缓解**：先在 transformer.html 上做"小修改"确认风格，再批量
- **内容不准**：LoRA / KV Cache 等技术细节需准确。**缓解**：参考 03-模型训练与对齐.md、01-大模型基础.md 现有内容，不编造线上数据
- **首页过长**：加 2 个新区后首页可能太长。**缓解**：新区用 4-3 卡片网格 + 折叠描述，与现有 4 模块并列
- **完成时间**：13 页 × ~500 行 = 6500+ 行手写 HTML，单次产出耗时较长。**缓解**：接受这个规模（用户已确认一次性产出），不偷工减料

## 验收标准

- [ ] 13 个新 HTML 文件存在，标题正确
- [ ] 每个新页能从首页跳转到
- [ ] 每个新页的 CSS 变量、组件类、视觉密度与 transformer.html 一致
- [ ] 每个新页有：hero / 原理 / 流程图或公式 / 落地 / FAQ 至少 4 区
- [ ] README.md 更新反映新结构
- [ ] commit + push 成功

## 不在本次范围

- ❌ 把 8 份 Markdown 题库也升级为 HTML（成本太高）
- ❌ 给 HTML 加搜索/筛选/折叠（保持纯静态）
- ❌ 第二批 / 第三批页面规划（按用户后续需求启动新 spec）
