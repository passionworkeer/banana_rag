# 企业知识库 RAG 调研文档

调研日期：2026-05-29

本目录沉淀企业级知识库落地方案调研，覆盖员工上传文档、自动解析与沉淀、部门隔离、统一检索问答、多 Agent 协作与治理。

建议按以下顺序阅读：

1. [01-research-summary.md](01-research-summary.md)：结论摘要、推荐路线、阶段规划。
2. [02-reference-architecture.md](02-reference-architecture.md)：目标架构、数据流、租户隔离、Agent 协作、安全治理。
3. [03-technology-selection.md](03-technology-selection.md)：开源项目、解析工具、向量库、检索框架、Agent 框架的技术选型。
4. [04-source-links.md](04-source-links.md)：GitHub 仓库和官方技术文档链接索引。
5. [05-enterprise-deep-dive.md](05-enterprise-deep-dive.md)：企业落地深水区，包括 ACL 同步、连接器、治理、评估、部署和成本。
6. [06-decision-questionnaire.md](06-decision-questionnaire.md)：后续方案设计需要确认的问题清单。
7. [07-company-context-bananain.md](07-company-context-bananain.md)：结合蕉内当前组织、项目和会议记录提炼出来的公司定制上下文。
8. [08-supply-chain-qa-ai-employee-mvp.md](08-supply-chain-qa-ai-employee-mvp.md)：供应链 QA AI 员工第一版 MVP 假设方案。
9. [09-supply-chain-qa-ai-employee-prd.md](09-supply-chain-qa-ai-employee-prd.md)：供应链 QA AI 员工 PRD 草案。
10. [10-supply-chain-qa-knowledge-structure.md](10-supply-chain-qa-knowledge-structure.md)：供应链 QA 知识结构、资料整理规则和模板。
11. [11-supply-chain-qa-meeting-brief.md](11-supply-chain-qa-meeting-brief.md)：后续业务沟通提纲和问题清单。
12. [plans/README.md](plans/README.md)：整体平台拆解后的多份 `plan.md` 执行计划。

核心建议：

- 不建议把“企业知识库”做成单一聊天应用。应该拆成文档接入层、解析治理层、索引检索层、权限隔离层、Agent 编排层、观测评估层。
- 文档入口统一为异步上传接口，上传后进入队列，由解析、OCR、分类、脱敏、分块、向量化、索引、审核等任务流水线处理。
- 部门隔离不能只依赖前端或提示词。必须在身份认证、元数据、检索过滤、向量库/搜索库、对象存储、审计日志多层同时执行。
- Agent 之间可以通信，但应通过受控协议和工具网关通信，不能直接绕过权限访问其他部门知识库。
- 推荐先做“核心 RAG 平台 + 少量部门试点”，再逐步引入多 Agent、知识图谱、自动分类和复杂工作流。
- 企业 RAG 最容易在安全评审卡住的点通常是源系统权限同步、撤权时效、检索时权限裁剪、审计可还原，而不是向量检索本身。
