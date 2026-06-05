# 面试题库

这个目录用于长期整理面试题。根目录的 `mianshi.md` 保留为原始收集入口，你后续可以继续把新题目直接粘进去；整理时再把题目去重、归类、补成可直接用于面试的回答。

## 目录

| 文件 | 内容 |
|------|------|
| [00-答题规范与公式速查.md](00-答题规范与公式速查.md) | 统一答题框架、公式速查、HTML 折叠卡、知识点展示方式 |
| [01-大模型基础.md](01-大模型基础.md) | Transformer、Attention、KV Cache、MoE、长上下文、重复生成等基础八股 |
| [02-Agent与RAG.md](02-Agent与RAG.md) | RAG、Agent、工具调用、记忆、多 Agent、LangGraph、MCP、评估和延迟优化 |
| [03-模型训练与对齐.md](03-模型训练与对齐.md) | SFT、LoRA、PPO、DPO、GRPO、KL、偏好数据、Reward、LLM-as-Judge |
| [04-多模态与文档解析.md](04-多模态与文档解析.md) | OCR、MinerU、图文对齐、多模态检索、图纸/工业文档解析 |
| [05-工程基础.md](05-工程基础.md) | Go、MySQL、Redis、MQ、WebSocket、文件上传、vLLM、服务治理 |
| [06-手撕算法.md](06-手撕算法.md) | Multi-Head Attention、SFT Loss、快排、第 K 大、最大正方形、接雨水、LIS、并发队列 |
| [07-项目深挖与行为题.md](07-项目深挖与行为题.md) | 项目拷打、业务理解、实习经历、Agent 项目讲述、长期实习、反问 |
| [08-前端AI应用与产品设计.md](08-前端AI应用与产品设计.md) | AI 工作流编辑器、前端质量监控、多模态交互、WebLLM、幻觉反馈设计 |

## 可视化 HTML 知识页

入口：[html/index.html](html/index.html)（按模块分类：首期专项 / 学习资源 / 面试核心 / 学习指南 / AI 早报 / 配套题库 / 学习路径）

### 面试核心知识（5 个）

| 页面 | 内容 |
|------|------|
| [html/rag.html](html/rag.html) | RAG 流程图、BM25 / RRF / 相似度公式、评估指标和面试答法 |
| [html/transformer.html](html/transformer.html) | Transformer Block 图、Attention 公式、Multi-Head、KV Cache 和长上下文 |
| [html/agent.html](html/agent.html) | Agent 闭环图、Workflow 对比、工具调用、记忆和人工断点 |
| [html/sft.html](html/sft.html) | SFT 训练流程、shift right、loss mask、样本质量和面试追问 |
| [html/dpo.html](html/dpo.html) | DPO 偏好训练流、loss 公式、Reference Model、beta 和 PPO 对比 |

### 面试首期专项（6 个高频追问补齐）

| 页面 | 内容 |
|------|------|
| [html/mcp.html](html/mcp.html) | MCP 协议：JSON-RPC、Tool/Resource/Prompt 三大原语、与 Function Call 关系 |
| [html/memory.html](html/memory.html) | Agent 记忆：Working/Episodic/Semantic 四层架构、压缩策略、冲突更新 |
| [html/lora.html](html/lora.html) | LoRA 微调：低秩分解 A·B、秩 r 选择、推理合并、QLoRA 变体 |
| [html/kv-cache.html](html/kv-cache.html) | KV Cache：自回归缓存、PagedAttention、MQA/GQA 优化 |
| [html/react-cot.html](html/react-cot.html) | ReAct/CoT：思维-行动循环、与 Function Call 关系、何时选用 |
| [html/multi-agent.html](html/multi-agent.html) | 多 Agent Router：Router/Supervisor/Debate/Handoff 模式、决策冲突 |

### 学习资源（7 个深度学习方向）

| 页面 | 内容 |
|------|------|
| [html/rerank.html](html/rerank.html) | Rerank：Cross-Encoder、ColBERT、LLM Rerank、与 Embedding 召回的职责划分 |
| [html/embedding.html](html/embedding.html) | Embedding 选型：稠密 vs 稀疏、BGE/M3E/Qwen、训练与微调 |
| [html/llm-cache.html](html/llm-cache.html) | API 缓存：Prompt Cache、KV Cache 复用、语义缓存、命中率优化 |
| [html/model-distributed.html](html/model-distributed.html) | 分布式部署：vLLM/SGLang、PagedAttention、TP/PP/DP 张量并行 |
| [html/skill.html](html/skill.html) | Skill 机制：NL/代码/hybrid 创建、与 MCP/Tool 区别与组合 |
| [html/tool-use.html](html/tool-use.html) | Tool Use：Function Calling 原理、JSON Schema、多轮调用与错误处理 |
| [html/llm-tuning.html](html/llm-tuning.html) | 大模型调优：Prompt 调优、Temperature/Top-p、结构化输出、CoT 激活 |

### Agent 学习指南（4 个，按日组织）

| 页面 | 内容 |
|------|------|
| [html/2026-05-26.html](html/2026-05-26.html) | 模型微调与长序列优化：SFT 全流程、Loss Masking、稀疏注意力 |
| [html/2026-05-27.html](html/2026-05-27.html) | Agent 决策冲突解决：设计 / 代码 / 协作三类冲突与解决路径 |
| [html/2026-05-28.html](html/2026-05-28.html) | 知识库治理：RAG vs 规则系统 vs 混合架构 |
| [html/2026-05-29.html](html/2026-05-29.html) | RLHF 与 DPO 对齐：KL 散度、PPO 目标函数、Reference Model |

### AI 行业早报

| 页面 | 内容 |
|------|------|
| [html/ai-daily-2026-05-29.html](html/ai-daily-2026-05-29.html) | 5/29 行业早报：Anthropic 融资、月之暗面商业化、微软 Build、苹果 WWDC |

## 整理规则

1. **相同题不重复写**：例如”Attention 的本质””Self-Attention 公式””为什么要 Scaling”合并到同一题下，用”相似问法”标注。
2. **每题给可面试回答**：不只写定义，还写面试中可以直接说出的结构化答案。
3. **技术题按层次回答**：先给一句话结论，再讲原理、工程落地、常见追问。
4. **项目题按四段回答**：业务问题、我的拆解、我的动作、验证结果。
5. **不确定事实不伪造**：没有真实指标时，用”阶段性验证指标 / 可以这样设计指标”表达，不编线上数据。

## 后续更新流程

1. 你把新题目继续粘到根目录 [mianshi.md](../mianshi.md)。
2. 我根据已有分类判断是否是重复题。
3. 重复题合并到已有问题的”相似问法 / 常见追问”。
4. 新题按分类补进对应文档，并写详细回答。
5. 如果出现新方向，比如前端 AI、推荐系统、操作系统，可以再加新分类文件。
6. **新 HTML 知识页**直接放到 `html/`，命名按主题（如 `2026-05-XX.html` 或 `主题名.html`），首页 [html/index.html](html/index.html) 会自动收录。

## 推荐使用方式

面试前先看：

1. [html/index.html](html/index.html)：从首页按模块进入
2. [07-项目深挖与行为题.md](07-项目深挖与行为题.md)：确定今天主讲哪 2-3 个项目
3. [html/agent.html](html/agent.html) + [html/rag.html](html/rag.html)：核心图速览
4. [02-Agent与RAG.md](02-Agent与RAG.md)：准备 Agent / RAG 高频追问
5. [06-手撕算法.md](06-手撕算法.md)：面试前快速过代码模板

日常学习：

1. 每天看 1 份「Agent 学习指南」（按日期选）
2. 配套看对应方向的 Markdown 题库
3. 扫「AI 行业早报」保持行业敏感度

回答时优先使用这个结构：

```text
结论：这题核心是……
原理：它本质上解决……
落地：在项目里我会……
风险：需要注意……
```
