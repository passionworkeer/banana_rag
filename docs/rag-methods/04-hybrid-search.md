# 04 混合检索 Hybrid Search（BM25 + 向量）

## 定义

同时使用关键词检索（BM25）和向量检索（Dense Vector），最后用融合算法（通常是 RRF）合并两路结果。企业文档场景默认推荐，比纯向量更稳。

## 为什么需要混合

企业文档里大量内容是编号、制度名、客户名、项目代号、SKU、接口名、合同条款号。这些：

- 纯向量检索不稳定：编号、缩写、错别字一多就翻车。
- 纯关键词检索又太死板：同义词、近义词、口语化表达抓不到。

混合检索让两种方式互补：关键词负责"精准命中"，向量负责"语义召回"。

## 标准流程

```
query
  ├─→ BM25 召回              # 关键词命中
  └─→ 向量召回                # 语义命中
        ↓
      RRF / score fusion 合并
        ↓
      重排（可选）
        ↓
      topK
```

## 适用

- 企业文档检索默认推荐。
- 编号、术语、专有名词多的场景。
- 客户希望"既能用关键词搜也能用自然语言搜"。
- 任何对召回质量有要求的生产环境。

## 局限

- 工程复杂度比纯向量高：需要同时维护两个索引。
- 调参更复杂：BM25 的 k1/b 参数、向量召回的 efSearch/topK 都要调。
- 合并策略选择影响结果：RRF 简单稳，但其他加权方案需要评估。

## 最小实现

```python
# 伪代码
bm25_index = BM25Okapi(tokenize(chunks))
vector_index = FaissIndex(embed(chunks))

def hybrid_search(query, top_k=10):
    bm25_hits = bm25_index.search(tokenize(query), top_k=top_k)
    vector_hits = vector_index.search(embed(query), top_k=top_k)
    fused = rrf_fusion([bm25_hits, vector_hits])
    return fused[:top_k]
```

## 工具实现

- OpenSearch hybrid search：https://docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/
- Elasticsearch hybrid search
- Weaviate hybrid search
- Qdrant + BM25 via payload

## 与纯向量的对比

| 维度 | 纯向量 | 混合检索 |
|------|--------|----------|
| 编号/术语 | 不稳定 | 精准 |
| 同义/近义 | 强 | 强 |
| 模糊口语化 | 强 | 强 |
| 索引维护 | 一套 | 两套 |
| 工程成本 | 低 | 中 |

## 来源

- `../enterprise-knowledge-base/03-technology-selection.md` §4、§12
- `../enterprise-knowledge-base/05-enterprise-deep-dive.md` §4.1
- `../enterprise-knowledge-base/plans/03-retrieval-and-rag/plan.md` 检索管线
