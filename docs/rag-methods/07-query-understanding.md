# 07 查询理解（分类 + 重写 + 元数据过滤）

## 定义

用户提问先经过一层查询理解：判断问题类型、补全上下文、补充元数据过滤条件，然后才进检索。这层是"先想清楚要搜什么，再去搜"。

## 三个子能力

### Query Classification（查询分类）

把问题分到预设类型，决定后续走哪条检索链路。

| Query Type | 示例 | 检索策略 |
|------------|------|----------|
| factual_lookup | 标准是什么、制度在哪里 | BM25 + vector |
| standard_interpretation | 这个条款如何适用 | BM25 + vector + SOP |
| case_similarity | 有没有类似历史案例 | vector + metadata + rerank |
| report_generation | 生成报告初稿 | template + retrieval + citation |
| structured_data_query | 某款号检测报告有哪些 | structured query + record citation |
| cross_space_task | QA Agent 询问法务 Agent | Agent Gateway + scoped retrieval |

### Query Rewrite（查询重写）

- 补同义词：把缩写展开成全称。
- 补上下文：把"那个报错"补成"登录页面的 401 报错"。
- 改写句式：让检索系统更易理解。
- 拆子问题：把复杂问题拆成多个简单问题。

### Metadata Filter（元数据过滤）

在向量检索/BM25 之外，先用元数据缩小候选范围：

- `department_id`：部门。
- `space_id`：知识空间。
- `project_id`：项目。
- `classification`：密级。
- `effective_date / expire_date`：生效时间。
- `status`：active / archived / draft。

## 适用

- 用户提问经常模糊、口语化、不完整。
- 检索结果受元数据约束（部门、项目、密级）。
- 需要把不同类型问题路由到不同检索链路。
- 任何对召回精度有要求的生产环境。

## 局限

- 分类器本身需要训练集和评估。
- Query rewrite 增加一次 LLM 调用，延迟和成本上升。
- 错误分类会把问题引向错误链路，需要监控。
- 元数据 schema 必须先设计好，否则过滤无的放矢。

## 最小实现

```python
def understand_query(query, user_context, llm):
    # 1. 分类
    qtype = classify(query, llm, taxonomy=QUERY_TYPES)

    # 2. 重写
    rewritten = llm(f"把以下问题改写成更利于检索的完整表述：\n{query}")

    # 3. 元数据过滤
    filters = {
        "department_id": user_context.department,
        "classification_ceiling": user_context.classification,
        "status": "active",
        "effective_date_lte": today(),
    }

    return {
        "query": rewritten,
        "query_type": qtype,
        "filters": filters,
    }
```

## 与权限的关系

元数据过滤同时承担两个职责：

- 业务过滤：部门、项目、生效状态。
- 权限过滤：密级上限、用户可见空间。

这两个不能混在一起设计，权限过滤必须独立审计。

## 来源

- `../enterprise-knowledge-base/05-enterprise-deep-dive.md` §4.1
- `../enterprise-knowledge-base/plans/03-retrieval-and-rag/plan.md` Task 1
