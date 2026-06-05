# 08 结构化查询（业务系统直查）

## 定义

当问题涉及 SKU、款号、批次、供应商、订单、库存、检测报告等结构化数据时，不走 embedding 检索，直接用 SQL/API/GraphQL 查业务系统，再把结果当作"带引用的检索片段"喂给 LLM。

## 触发场景

- "某款号最近一次检测报告有哪些？"
- "去年 Q3 不合格批次数量趋势"
- "这单的发货状态"
- "供应商 X 的合格率"
- "员工 Y 负责的项目列表"

这些问题**不能用陈旧的文档 embedding 回答**，因为：

- 业务数据实时变化，文档向量是 T-1 甚至 T-7 的快照。
- 聚合、排序、Top N、对比需要数据库能力，向量检索做不到。
- 答案需要精确数字，不能是"看起来像"。

## 与传统 RAG 的关系

| 维度 | 传统 RAG | 结构化查询 |
|------|----------|------------|
| 数据源 | 文档/制度 | 业务系统 |
| 检索方式 | 相似度匹配 | SQL/API/GraphQL |
| 实时性 | 离线 T+1 | 实时 |
| 答案形态 | 文本片段 | 结构化记录 |
| 引用方式 | 文档 + 页码 | 记录 ID + 字段值 |

## 适用

- 任何涉及"具体某条记录"或"统计聚合"的问题。
- 业务系统本身有 API 或数据库可查。
- 答案需要可解释、可追溯到具体记录。
- 数据需要实时性。

## 局限

- 需要业务系统配合（开放 API 或允许 SQL）。
- 表结构和字段命名要稳定，否则查询链路脆弱。
- 需要查询意图识别：哪类问题走结构化，哪类走 embedding。
- 不同业务系统查询语法不同，需要适配层。

## 最小实现

```python
def structured_or_vector(query, query_type, filters):
    if query_type == "structured_data_query":
        sql = build_sql(query, filters)        # LLM 翻译成 SQL
        result = db.execute(sql)                # 业务库执行
        return format_as_citation(result)
    else:
        return vector_search(query, filters)
```

## 来源

- `../enterprise-knowledge-base/plans/03-retrieval-and-rag/plan.md` Task 5
- `../enterprise-knowledge-base/05-enterprise-deep-dive.md` §4.1
