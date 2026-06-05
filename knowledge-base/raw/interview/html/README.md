# 面试与学习中心 · 浏览指南

起点：`index.html`（浏览器打开即可，全本地、不联网）。

## 第一次浏览（30 分钟扫一遍）

按 index 顺序从上到下，每张抽 30 秒看 hero + 架构图 + FAQ 头 2 条：

1. `index.html` 首页——整体结构
2. `agent.html` / `rag.html` / `transformer.html`——核心基础
3. `rlhf.html` 或 `grpo.html`——对齐训练
4. `a2a.html` 或 `multi-agent.html`——Agent 架构
5. `flash-attention.html` 或 `paged-attention.html`——推理部署
6. `ai-pm.html`——AI PM 视角
7. `reasoning-models.html` 或 `browser-agent.html`——2025 新范式

## 每张页怎么看（5 分钟/张）

- **hero**：标题 + lead + pillrow（30 秒，明白主题）
- **架构 SVG 图**：核心机制（1-2 分钟）
- **公式 / 表格**：核心数据（30 秒）
- **FAQ 8-10 条**：挑 3 条面试最可能问的背（2 分钟）
- **回答模板 + 概念速查表**：面试前一晚过

## 面试定向精读路径

### Agent 岗
`agent` → `a2a` → `multi-agent` → `mcp` → `tool-use` → `agent-observability` → `browser-agent` → `context-engineering` → `prompt-injection`

### 推理部署岗
`transformer` → `kv-cache` → `flash-attention` → `paged-attention` → `speculative-decoding` → `quantization` → `inference-engines` → `long-context`

### 训练 / 推理研究员
`sft` → `lora` → `rlhf` → `ppo` → `grpo` → `dpo-advanced` → `reward-model` → `constitutional-ai` → `reasoning-models`

### AI PM / 技术 PM
`ai-pm` → `context-engineering` → `prompt-engineering` → `prompt-injection` → `agent-observability` → `router` → `planner`

## 三大方向（2025 新增）

- **Reasoning 范式**：`reasoning-models`（o1 / R1 / Test-Time Compute / PRM）
- **多模态**：`vlm`（LLaVA / Qwen-VL / InternVL）+ `document-parsing`（MinerU / PaddleOCR）
- **Agent 落地**：`browser-agent`（Computer Use / CUA）+ `agent-observability`（LLM Trace）

## 门面 3 张（"不知道看哪个就看这 3 张"）

- `reasoning-models.html`——2025 新范式代表
- `a2a.html`——Agent 新协议
- `flash-attention.html`——推理部署新优化

3 张过完，整个仓库调性就清楚了。

## 文件组织

```
interview/html/
├── index.html               # 入口
├── README.md                # 本文件
├── agent / rag / ...         # 25+ 张知识页（统一格式）
├── daily/ 配套题库/         # 见 index 跳转
└── 2026-05-2X.html          # Agent 学习指南
```

每张页**统一格式**：hero + 架构图 SVG + 公式/表格 + 8-10 条 FAQ + 回答模板 + 概念速查表。
配色按方向：紫 #7c3aed（对齐训练 / Agent）/ 蓝 #2563eb（推理部署）/ 天蓝 #0ea5e9（AI PM）。

## 注意事项

- 全是本地 HTML，**不联网**也能看
- 链接都是相对路径 `./xxx.html`，**别把单文件拷到别处打开**（链接会断）
- SVG 箭头渲染是核心视觉，最值得看
