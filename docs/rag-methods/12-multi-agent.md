# 12 多 Agent 协作（MCP / A2A / LangGraph）

## 定义

把企业知识库从"问答"升级为"工作流协作"。不同部门、不同职能的智能体通过受控协议互相委托任务、共享上下文、调用工具。Agent Gateway 负责鉴权、路由、限流、审计。

## 角色划分

- **部门 Agent**：HR Agent、法务 Agent、研发 Agent、销售 Agent、QA Agent。
- **工具 Agent**：文档整理 Agent、审批 Agent、工单 Agent、数据分析 Agent。
- **平台 Agent**：审计 Agent、知识维护 Agent。

## 三类协议

| 协议 | 用途 | 适合场景 |
|------|------|----------|
| MCP（Model Context Protocol） | Agent 访问工具、资源和企业系统 | 把知识检索、工单、CRM、数据库查询封装成工具 |
| A2A（Agent2Agent） | Agent 间任务委托和通信 | 不同部门 Agent 互相协作 |
| LangGraph Multi-Agent | 内部多 Agent 状态机 | supervisor / handoff / worker 模式 |

## Agent 调用上下文

```json
{
  "request_id": "req-xxx",
  "user_id": "u123",
  "caller_agent": "qa-agent",
  "target_agent": "legal-agent",
  "delegation_reason": "license_review",
  "allowed_scopes": ["rd-platform", "legal-public-guidance"],
  "classification_ceiling": "internal",
  "expires_at": "2026-06-05T18:00:00+08:00"
}
```

## Agent Gateway 必须负责

- Agent 注册和能力声明。
- 用户身份透传。
- 权限收敛，而不是权限扩大。
- 工具调用审批。
- 跨部门调用审计。
- 输出引用检查。
- 限流和成本控制。
- 敏感操作人工确认。

## 适用

- 跨部门、跨系统的复杂工作流。
- 需要身份、权限、审计闭环的场景。
- 多业务线共享一套知识底座。
- 任务需要多专业领域知识协作。

## 不适用

- 简单问答（直接 RAG + Agentic RAG 即可）。
- 权限模型还没设计好的早期阶段。
- 团队没有 Agent 工程经验。
- 业务方没有明确"跨部门流程"诉求。

## 主流框架

| 框架 | 特点 |
|------|------|
| LangGraph | 状态机思维，supervisor/handoff 模式清晰 |
| AutoGen | 微软开源，多 Agent 会话研究价值高 |
| CrewAI | 角色型协作，流程化任务实验 |
| Semantic Kernel | .NET 生态友好，企业微软栈首选 |
| MCP | 工具/资源暴露协议，跨框架通用 |

## 治理注意

- 部门隔离不能只靠 prompt。Agent 之间通信必须经过 Agent Gateway。
- 不能让 Agent 直接绕过权限访问其他部门知识库。
- 每个 Agent 必须有明确的"能力声明"和"调用上下文"。
- 高风险操作必须人工确认，不能让 Agent 自主决定。
- 所有跨部门调用必须有审计日志。

## 与 Agentic RAG 的边界

- Agentic RAG：一个智能体包装 RAG 链路。
- Multi-agent：多个智能体协作完成工作流，RAG 只是其中一个 Agent 的能力。

通常演进路径：传统 RAG → Agentic RAG → 多 Agent 协作。

## 来源

- `../enterprise-knowledge-base/03-technology-selection.md` §6
- `../enterprise-knowledge-base/04-agent-and-entrypoints/plan.md`
- `../enterprise-knowledge-base/05-enterprise-deep-dive.md` §6
- MCP：https://modelcontextprotocol.io/
- A2A：https://a2aproject.github.io/A2A/latest/
- LangGraph：https://langchain-ai.github.io/langgraph/concepts/multi_agent/
