# 2026-06-03 面试 HTML 扩展设计

## 核心论点

`interview/html/` 已有 5 个核心知识页(Transformer/RAG/Agent/SFT/DPO)+ 4 份 Agent 学习指南(5/26-5/29)+ 1 份 AI 行业早报,Markdown 题库 01-08 已积累 3992 行内容。但核心页只有 5 个,覆盖度与 Markdown 题库不匹配。本次扩展目标是把高频追问和学习方向补齐到 13 个新页面,保持与 `transformer.html`/`rag.html` 严格一致的视觉风格,让首页能"一站式导航"。

去重原则:RAG、MCP、Agent Memory 已有覆盖,RAG 走 `rag.html`,MCP 和 Memory 走 6 面试页路线(不重复做),实际新做 13 页(去重后)。6 面试首期页(高频追问):mcp.html(MCP 协议)、memory.html(Agent 记忆)、lora.html(LoRA 微调)、kv-cache.html(KV Cache)、react-cot.html(ReAct/CoT)、multi-agent.html(多 Agent Router)。7 学习资源页(深度方向):rerank.html、embedding.html、llm-cache.html、model-distributed.html、skill.html、tool-use.html、llm-tuning.html。每页严格复用 `transformer.html` 的设计 token 和组件类,五区结构(hero/原理/SVG 公式/落地/FAQ),400-600 行中深度。首页变更:在 Hero 之后、模块一之前新增"🎯 首期专项 · 6 面试页"和"📖 学习资源 · 7 主题"两个区,现有 4 大模块保持原位。风险:风格漂移(缓解:先小修改 transformer.html 确认风格再批量)、内容不准(缓解:参考现有 Markdown 题库,不编造线上数据)、首页过长(缓解:新区用 4-3 卡片网格)、完成时间(13 页 × 500 行 = 6500+ 行手写 HTML)。

## 关键术语

- MCP 协议
- Agent 记忆
- LoRA
- KV Cache
- ReAct
- CoT
- Multi-Agent
- Rerank
- Embedding
- Skill 机制

## 跨资料连接

- [[html-README]] — 本扩展的目标目录与配套浏览指南。
- [[2026-06-03-interview-html-expansion]] — 本设计的实施计划。
- [[00-答题规范与公式速查]] — 配套的 Markdown 答题骨架。
- [[01-大模型基础]] — LoRA、KV Cache 等技术细节的 Markdown 来源。
- [[02-Agent与RAG]] — MCP、ReAct 等 Agent 内容的 Markdown 来源。
- [[03-模型训练与对齐]] — LoRA/PPO/DPO/GRPO 的详细展开。
