# Agent 与 RAG 面试题库

## 核心论点

本文件是面试 Agent 与 RAG 题目的 Markdown 题库,覆盖 RAG 本质与局限、RAG 评估三层(检索层 Recall@K/MRR/nDCG、生成层 Faithfulness/Answer Relevance/Correctness、端到层用户完成率/延迟/成本)、文档 chunk 策略(按结构切 + 长度修正、Markdown/PDF/网页/代码/表格分别处理)、overlap 经验值 10-20%、Top-K 过大的噪声问题、Rerank 价值(召回解决"找得到"、Rerank 解决"排得准")、Embedding 选型(稠密 vs 稀疏 + 混合)、Milvus 索引选型(HNSW/IVF_FLAT/IVF_PQ)、术语语义漂移的混合检索 + 领域微调 + 术语词典优化、Agent 框架 LangGraph 与记忆组件、Function Call 流程、Workflow vs Agent 选型、多 Agent 路由、Human-in-the-loop、Agent 评估指标(任务完成率/工具调用成功率/延迟/成本/规划能力 vs 幻觉率)等。

核心方法论是"分层拆解再优化":评估 RAG 不能只看 final answer 对错,要拆检索/重排/拼上下文/生成四阶段分别评估;Agent 选型要看任务是固定 Workflow 还是需要自主决策;长上下文和 RAG 不是替代关系,长上下文解决"放得下"、RAG 解决"找得准/可更新/可溯源/可按权限";评估 Agent 不仅看生成质量,还要看工具调用成功率、规划步骤、延迟、成本。Ragas 框架的 Faithfulness(回答是否忠于检索)和 Answer Relevance(回答是否相关)是高频考察指标。

## 关键术语

- RAG
- Rerank
- Embedding
- 向量数据库
- Agent
- LangGraph
- Function Call
- Multi-Agent
- Human-in-the-loop
- Ragas

## 跨资料连接

- [[01-大模型基础]] — Transformer/Attention/MoE 基础题。
- [[00-答题规范与公式速查]] — 通用答题骨架。
- [[00-llm-wiki-demo]] — RAG 本质与 Agentic RAG 转向。
- [[mianshi]] — 原始面试题汇总,本文件是其整理版。
- [[html-README]] — 配套的 HTML 知识页(RAG/Agent/MCP/Memory/Multi-Agent/ReAct)。
- 原始稿位于 `raw/interview/mianshi.md` — 本文件题目的原始面试汇总对应位置。
