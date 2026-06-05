# RAG 与知识库方法总览

汇总当前项目涉及到的 RAG、知识图谱、知识库管理方法。每种方法都有一份独立文档，本文件负责索引、对比和阅读引导。

## 1. 文档来源

本文档综合两处来源：

- `rag_idea.md`：对比 RAG、卡帕西 LLM Wiki、Graphify 的科普型文章。
- `docs/enterprise-knowledge-base/`：Bananain 企业知识库 RAG 调研（11 篇编号研究 + 7 份子计划）。

两处来源里的方法去重后一共 13 个，按范式维度列出。

## 2. 方法索引

| 编号 | 方法 | 来源 | 文档 |
|------|------|------|------|
| 01 | 传统 RAG（Baseline RAG） | rag_idea.md + 企业调研 | [01-traditional-rag.md](01-traditional-rag.md) |
| 02 | LLM Wiki（卡帕西 / Obsidian） | rag_idea.md | [02-llm-wiki-karpathy.md](02-llm-wiki-karpathy.md) |
| 03 | Graphify（实体知识图谱） | rag_idea.md | [03-graphify.md](03-graphify.md) |
| 04 | 混合检索 Hybrid Search（BM25 + 向量） | 企业调研 03/05 | [04-hybrid-search.md](04-hybrid-search.md) |
| 05 | RRF + Reranker | 企业调研 03/05 | [05-rrf-reranker.md](05-rrf-reranker.md) |
| 06 | Parent-child 检索 | 企业调研 03/05 | [06-parent-child-retrieval.md](06-parent-child-retrieval.md) |
| 07 | 查询理解（分类 + 重写 + 元数据过滤） | 企业调研 05 | [07-query-understanding.md](07-query-understanding.md) |
| 08 | 结构化查询（业务系统直查） | 企业调研 03/05 | [08-structured-query.md](08-structured-query.md) |
| 09 | GraphRAG（多跳推理） | 企业调研 03/05 | [09-graphrag.md](09-graphrag.md) |
| 10 | ColPali / 视觉检索 | 企业调研 03/05 | [10-colpali-visual-retrieval.md](10-colpali-visual-retrieval.md) |
| 11 | Agentic RAG（智能体重写 + RAG） | rag_idea.md | [11-agentic-rag.md](11-agentic-rag.md) |
| 12 | 多 Agent 协作（MCP / A2A / LangGraph） | 企业调研 03/05 | [12-multi-agent.md](12-multi-agent.md) |
| 13 | 云托管 RAG（Bedrock / Azure AI Search / Vertex AI） | 企业调研 03/05 | [13-cloud-managed-rag.md](13-cloud-managed-rag.md) |

## 3. 阅读建议

按"先建立基线，再做增强，最后做协作"分三组：

基线组（必须懂）：
- 01 传统 RAG
- 02 LLM Wiki
- 03 Graphify

增强组（提升召回和精度）：
- 04 混合检索
- 05 RRF + Reranker
- 06 Parent-child 检索
- 07 查询理解
- 08 结构化查询
- 09 GraphRAG
- 10 ColPali / 视觉检索

协作与平台组（变聊天为工作流）：
- 11 Agentic RAG
- 12 多 Agent 协作
- 13 云托管 RAG

## 4. 横向对比

| 方法 | 适合规模 | 适合场景 | 主要优势 | 主要风险 |
|------|----------|----------|----------|----------|
| 01 传统 RAG | 中小 | 单次问答、PoC | 简单、上手快 | 检索噪声、意图不清、无法多步 |
| 02 LLM Wiki | 100-200 篇 | 个人/小团队知识复利 | 知识越用越准 | token 高、不适合海量 |
| 03 Graphify | 单个代码库或文档集 | 快速熟悉陌生项目 | 一次构建、长期可查 | 适合代码胜过适合制度 |
| 04 混合检索 | 中大 | 默认推荐 | 兼顾关键词和语义 | 工程复杂度比纯向量高 |
| 05 RRF+Rerank | 中大 | 提升 topK 精度 | 命中质量明显提升 | 成本和延迟增加 |
| 06 Parent-child | 中大 | 制度、合同、技术文档 | 小块召回、大块生成 | 索引和生成双层维护 |
| 07 查询理解 | 全部 | 模糊、口语化提问 | 提升首轮召回 | 分类器本身需要评估 |
| 08 结构化查询 | 中大 | 编号/SKU/聚合问题 | 数据新鲜、可解释 | 需要业务系统配合 |
| 09 GraphRAG | 中大 | 多跳关系推理 | 解释能力强 | 建模和治理成本高 |
| 10 ColPali | 特定 | 扫描 PDF/PPT/图表 | 视觉信息直接召回 | 模型大、算力贵 |
| 11 Agentic RAG | 全部 | 复杂多步任务 | 任务可拆解 | 智能体本身会跑偏 |
| 12 多 Agent 协作 | 大 | 跨部门工作流 | 流程化能力 | 权限和审计治理复杂 |
| 13 云托管 RAG | 全部 | 已有云基础设施 | 上线最快 | 供应商绑定、合规审查 |

## 5. 关联文档

- `../rag_idea.md`：科普型文章原文。
- `../enterprise-knowledge-base/README.md`：企业知识库 RAG 调研索引。
- `../enterprise-knowledge-base/plans/03-retrieval-and-rag/plan.md`：本项目落地计划。
- `./99-recommended-stack.md`：根据本文档给出的推荐组合。
