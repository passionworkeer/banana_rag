# 05 RRF + Reranker

## 定义

RRF（Reciprocal Rank Fusion）把多路召回的结果按排名倒数加权合并，Reranker（重排模型）再对合并后的候选集精细打分排序。两者通常配合使用，是企业级 RAG 提升 topK 精度的标准组合。

## RRF

公式：`score(d) = Σ 1 / (k + rank_i(d))`

- `k` 通常取 60，避免排名靠后文档分母过小。
- 不需要各路分数归一化，每路只提供排名即可。
- 简单稳定，适合 BM25 + vector 合并。

## Reranker

- Cross-Encoder 模型（如 bge-reranker、Qwen rerank、Cohere Rerank）。
- 把 query 和候选 chunk 一起编码，得到精确相关性分数。
- 比 bi-encoder 向量检索准，但慢且贵，所以只对 topK 候选做。

## 适用

- 任何对 topK 精度有要求的场景。
- 多路召回（BM25 + vector + sparse）合并。
- 答案质量比延迟更重要的场景。

## 局限

- Reranker 增加延迟和成本。
- Reranker 模型本身需要评估，中文领域要选好模型。
- RRF 对极端偏置不敏感，但当一路结果普遍很差时仍会拉低整体质量。

## 最小实现

```python
def rrf_fusion(rankings, k=60):
    """rankings: list of lists, each sublist is doc_ids ordered by score desc"""
    scores = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return sorted(scores.items(), key=lambda x: -x[1])

def hybrid_rerank(query, chunks, top_k=20, rerank_top_n=5):
    bm25_hits = bm25_search(query, top_k=top_k)
    vector_hits = vector_search(query, top_k=top_k)
    fused = rrf_fusion([bm25_hits, vector_hits])[:top_k]
    candidates = [chunks[doc_id] for doc_id, _ in fused]
    rerank_scores = reranker.score(query, candidates)
    ranked = sorted(zip(candidates, rerank_scores), key=lambda x: -x[1])
    return ranked[:rerank_top_n]
```

## 工具实现

- OpenSearch RRF：https://opensearch.org/blog/introducing-reciprocal-rank-fusion-hybrid-search/
- Qwen reranking：https://docs.qwencloud.com/developer-guides/embeddings/reranking
- bge-reranker、cohere rerank、jina reranker

## 何时只做 RRF 不做 Rerank

- 答案延迟要求 < 500ms。
- 召回质量已经够用，重排带来的提升 < 5%。
- 文档类型简单、问题模式单一。

## 来源

- `../enterprise-knowledge-base/03-technology-selection.md` §12
- `../enterprise-knowledge-base/05-enterprise-deep-dive.md` §4.1
