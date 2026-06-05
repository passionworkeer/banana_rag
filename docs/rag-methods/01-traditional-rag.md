# 01 传统 RAG（Baseline RAG）

## 定义

把企业私有数据切片、向量化、存入向量库，用户提问时检索相似片段，喂给 LLM 生成答案。RAG = Retrieval-Augmented Generation。

## 标准流程

1. 数据准备：PDF/Word/Markdown 等文档切片（Chunking）。
2. 向量化：通过 Embedding 模型转成向量，存入向量数据库（Chroma、Faiss、Milvus）。
3. 检索：用户提问 → 向量化 → 在库中找相似片段（topK）。
4. 生成：用户问题 + 检索到的片段 → LLM → 生成答案。

## 适用

- 文档量中等（几千到几万条切片）。
- 单次问答场景，不需要长期记忆。
- PoC 阶段快速验证价值。
- 没有复杂权限要求。

## 局限

- 检索相关性差：向量相似不等于语义相关，容易召回到无关片段。
- 缺乏意图理解：模糊问题（如"那个报错怎么修？"）直接拿去检索会偏得很远。
- 无法处理复杂任务：多步推理、跨文档归纳等场景一次性流程搞不定。
- 无知识复利：每次问答独立，答案不会变成新知识沉淀。

## 最小实现

```python
# 伪代码示意
chunks = split(document, chunk_size=500, overlap=50)
embeddings = embed(chunks)              # OpenAI / bge / m3e
vector_store.add(chunks, embeddings)    # Chroma / Faiss / Milvus

query_emb = embed(user_query)
hits = vector_store.search(query_emb, top_k=5)
context = "\n".join([h.text for h in hits])
answer = llm(f"基于以下内容回答：\n{context}\n\n问题：{user_query}")
```

## 何时升级

出现以下任意一条时，传统 RAG 不够用，应考虑其他方法：

- 编号、术语、缩写必须精准命中 → 04 混合检索。
- topK 召回质量差，关键词和语义都不准 → 05 RRF+Reranker。
- 文档有章节结构，召回的片段缺少上下文 → 06 Parent-child。
- 用户提问经常模糊 → 07 查询理解。
- 问题需要"某款号某批次"等结构化查询 → 08 结构化查询。
- 需要回答"X 部门和 Y 系统的关系"等多跳问题 → 09 GraphRAG。
- 文档大量是扫描 PDF/PPT/图表 → 10 ColPali。
- 任务需要拆解、多次检索 → 11 Agentic RAG。

## 来源

- `../rag_idea.md` 141-150 行
- `../enterprise-knowledge-base/01-research-summary.md`
- `../enterprise-knowledge-base/03-technology-selection.md` §2
