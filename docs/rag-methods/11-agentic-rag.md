# 11 Agentic RAG（智能体重写 + RAG）

## 定义

在传统 RAG 前面套一个智能体层：用户问题先经过智能体决策（重写、拆解、规划），再走 RAG 检索。智能体不只决定"怎么搜"，还决定"要不要搜"、"搜几次"、"搜完之后还要不要做别的事"。

## 解决的传统 RAG 痛点

| 痛点 | 传统 RAG 表现 | Agentic RAG 做法 |
|------|----------------|------------------|
| 检索相关性差 | 直接拿模糊问题搜 | 智能体改写、补上下文 |
| 缺乏意图理解 | 模糊问题硬搜 | 智能体先判断意图再路由 |
| 无法处理复杂任务 | 一次性流程 | 智能体拆任务、多次检索、工具组合 |

## 典型模式

- **Query Rewrite Agent**：识别问题不完整或模糊，主动问用户或根据上下文补全。
- **Multi-step Retrieval Agent**：把"分析供应商 X 的合规风险"拆成"列出供应商 X 资料 → 查询相关法规 → 对照历史案例"。
- **Tool-using Agent**：除向量检索外，还调用 SQL、API、计算器等工具。
- **Reflection Agent**：检查检索结果是否够用，不够就换关键词或换工具重试。

## 适用

- 复杂多步任务（多文档、多工具、需推理）。
- 用户提问模糊或上下文不完整。
- 需要"对答案本身做检查"的场景。
- 接入多种数据源和工具。

## 不适用

- 单次、简单问答（直接 RAG 更便宜更快）。
- 智能体能力边界不清的领域（容易跑偏）。
- 延迟要求 < 2s 的场景。
- 没有明确工具协议（MCP 之类）的环境。

## 最小实现

```python
def agentic_rag(query, agent):
    # 1. 理解问题，决定是否需要检索、检索什么
    plan = agent.plan(query)

    # 2. 拆任务，依次执行
    context = []
    for step in plan.steps:
        if step.type == "retrieve":
            chunks = retriever.search(step.query)
            context.extend(chunks)
        elif step.type == "structured_query":
            data = db.query(step.sql)
            context.append(format(data))
        elif step.type == "tool":
            result = tool_registry[step.tool].run(**step.args)
            context.append(result)

    # 3. 反思：上下文够不够
    if not agent.is_sufficient(context):
        return agentic_rag(agent.refine(query, context), agent)

    # 4. 生成
    return agent.generate(query, context)
```

## 与多 Agent 协作的关系

Agentic RAG 是"单个智能体 + RAG"；多 Agent 协作（看 `12-multi-agent.md`）是"多个智能体分工协作"。

- Agentic RAG：一个智能体做完整链路决策。
- Multi-agent：HR Agent、法务 Agent、QA Agent 各管一摊，跨部门通过 Agent Gateway 协作。

## 治理注意

- 智能体本身会跑偏、会产生幻觉，需要评估集。
- 工具调用必须经过白名单和参数校验。
- 高风险操作必须人工确认。
- Prompt 注入：检索内容是数据，不是指令。

## 来源

- `../rag_idea.md` 164 行（Agentic RAG 概念）
- `../enterprise-knowledge-base/04-agent-and-entrypoints/plan.md`
- `../enterprise-knowledge-base/05-enterprise-deep-dive.md` §6
