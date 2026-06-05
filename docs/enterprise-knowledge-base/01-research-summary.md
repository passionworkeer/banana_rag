# 企业知识库 RAG 调研总览

调研日期：2026-05-29

## 1. 背景需求

企业内部存在大量异构文档，包括 PDF、DOCX、PPTX、Excel、图片扫描件、网页、邮件、制度文档、项目资料、会议纪要、技术方案等。目标不是简单“上传后聊天”，而是形成一套企业知识基础设施：

- 员工通过统一接口上传文档。
- 系统自动解析、清洗、分类、打标签、分块、向量化和索引。
- 不同部门、项目、密级之间隔离。
- 员工或业务系统通过问答、搜索、Agent 调用知识。
- 不同 Agent 可以协作，但必须遵守权限、审计和数据边界。
- 系统可持续运营：可观测、可回滚、可评估、可治理。

## 2. 调研结论

### 推荐路线

建议采用“自研平台骨架 + 成熟开源组件”的路线，而不是完全依赖一个开源知识库应用。

推荐底座：

- 上传与任务编排：自研 API + 队列 + 工作流。
- 文档解析：Docling、MinerU、Unstructured、Apache Tika、MarkItDown 组合使用。
- 索引检索：OpenSearch/Elasticsearch 做关键词与混合检索，Qdrant、Milvus、Weaviate 或 pgvector 做向量检索。
- RAG 编排：LlamaIndex 或 LangChain/LangGraph。
- 知识库产品参考：RAGFlow、Dify、MaxKB、AnythingLLM。
- Agent 通信：MCP 用于工具/资源暴露，A2A 或内部 Agent Gateway 用于 Agent 间任务通信。
- 安全治理：SSO/IAM、ABAC/RBAC、部门租户隔离、DLP、审计日志、检索前权限过滤、答案后处理。

### 为什么不直接套一个开源产品

RAGFlow、Dify、MaxKB、AnythingLLM 等项目适合快速验证知识库体验，但企业级需求通常会遇到以下问题：

- 复杂权限模型：部门、项目、岗位、文档密级、临时授权、离职回收。
- 多格式文档质量：扫描 PDF、复杂表格、图片、PPT 图文关系、版式保留。
- 数据治理：审计、保留策略、删除、版本回滚、血缘追踪。
- Agent 间通信：不是单一聊天机器人，而是多个部门 Agent、流程 Agent、审计 Agent、知识维护 Agent 协作。
- 与企业系统集成：OA、飞书/钉钉/企业微信、AD/LDAP、ERP、CRM、工单系统、对象存储。

因此，建议把开源产品当作参考或局部能力，而不是把它们作为不可控的总平台。

## 3. 目标架构一句话

员工把文档上传到统一接口；文档原件进入对象存储，元数据进入数据库，任务进入队列；解析流水线把文档转成结构化 Markdown/JSON，抽取元数据和权限标签，生成分块、向量、关键词索引和可选知识图谱；查询时由权限网关确定用户可见范围，再通过混合检索、重排、上下文压缩和 LLM 生成答案；部门 Agent 通过受控 Agent Gateway 调用其他 Agent，而不是直接访问其他部门数据。

## 4. 推荐分阶段落地

### 阶段 1：企业知识库 PoC

目标：证明文档接入、解析、索引、问答可用。

范围：

- 支持 PDF、DOCX、PPTX、TXT/Markdown、Excel。
- 建立上传 API、任务状态 API、查询 API。
- 用 1-2 个部门数据做试点。
- 使用基础 RBAC：用户只查自己部门或授权空间。
- 建立检索评估集：20-50 个真实问题。

建议组件：

- FastAPI/Spring Boot/Node.js 任一企业熟悉栈实现 API。
- MinIO/S3 存原文件。
- PostgreSQL 存元数据、任务、权限。
- OpenSearch 做 BM25 与混合搜索。
- Qdrant 或 pgvector 做向量检索。
- Docling/MinerU/Unstructured 做解析。
- LlamaIndex 或 LangChain 做 RAG 编排。

### 阶段 2：部门隔离与知识治理

目标：进入企业真实使用前的安全与治理。

范围：

- 接入企业 SSO、AD/LDAP/OIDC。
- 引入 department_id、space_id、project_id、classification、acl_policy 等元数据。
- 检索层强制权限过滤。
- DLP/敏感词/PII 检测。
- 文档版本、删除同步、重建索引、失败重试。
- 审计日志：谁上传、谁查了什么、命中了哪些文档、答案引用了哪些片段。

### 阶段 3：多 Agent 与跨部门协作

目标：让知识库从“问答”变成“企业工作流协作”。

范围：

- 部门 Agent：HR Agent、法务 Agent、研发 Agent、销售 Agent。
- 工具 Agent：文档整理 Agent、审批 Agent、工单 Agent、数据分析 Agent。
- Agent Gateway：鉴权、路由、限流、审计、协议适配。
- MCP Server 暴露企业工具和受控知识查询能力。
- A2A 或内部协议承载 Agent 间任务协作。
- 引入任务状态、回执、可追踪引用和人工确认。

## 5. 核心风险

- 权限泄露：只在 prompt 中写“不要回答未授权内容”是不够的，必须在检索前过滤。
- 解析质量差：复杂 PDF、扫描件、表格、PPT 图文关系会显著影响 RAG 质量。
- 文档版本混乱：旧制度和新制度同时被命中会导致错误答案。
- 低质量分块：分块过小丢上下文，过大降低召回，表格与代码块需要特殊处理。
- Agent 越权：Agent 之间通信如果没有能力边界，会绕过部门隔离。
- 缺少评估：没有固定测试集和引用检查时，系统上线后很难判断变好还是变差。
- 源系统权限同步：SharePoint、Confluence、网盘、OA 等系统的 ACL 如果不能同步和回放，安全评审很难通过。
- 撤权滞后：员工离职、项目成员移除、文档改密级后，索引和缓存必须及时失效。
- 知识运营缺位：没有部门知识管理员时，系统会持续积累重复、过期、低质量文档。

## 6. 补充调研结论

企业落地时，建议把下面能力提前纳入一期架构，即使第一版不全部实现：

- ACL 同步接口：连接器不只同步内容，还要同步源系统权限、版本、删除和移动事件。
- 授权服务：从 RBAC 起步，但预留 ABAC/ReBAC，可接 OpenFGA、OPA、SpiceDB 或 Cerbos。
- 评估集：每个试点部门建立真实问题集、权限负例、过期文档干扰集。
- 审计回放：能够回答“某用户在某时刻为什么看到这些引用”。
- 多模态兜底：PPT、表格、扫描件、流程图至少保留原图、页码和坐标引用。
- Agent Gateway：所有 Agent 工具调用和跨部门委托都经过统一鉴权、限流、审计。
- 成本归因：按部门统计 embedding、rerank、LLM token、OCR、存储和 GPU 成本。

## 7. 重点参考链接

- RAGFlow: https://github.com/infiniflow/ragflow
- Dify: https://github.com/langgenius/dify
- MaxKB: https://github.com/1Panel-dev/MaxKB
- AnythingLLM: https://github.com/Mintplex-Labs/anything-llm
- LlamaIndex: https://github.com/run-llama/llama_index
- LangChain: https://github.com/langchain-ai/langchain
- LangGraph multi-agent: https://langchain-ai.github.io/langgraph/concepts/multi_agent/
- Docling: https://github.com/docling-project/docling
- MinerU: https://github.com/opendatalab/MinerU
- Unstructured: https://github.com/Unstructured-IO/unstructured
- MarkItDown: https://github.com/microsoft/markitdown
- Apache Tika: https://tika.apache.org/
- Qdrant multi-tenancy: https://qdrant.tech/documentation/guides/multiple-partitions/
- Weaviate multi-tenancy: https://docs.weaviate.io/weaviate/manage-collections/multi-tenancy
- Milvus: https://milvus.io/docs
- OpenSearch hybrid search: https://docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/
- Model Context Protocol: https://modelcontextprotocol.io/
- Agent2Agent Protocol: https://a2aproject.github.io/A2A/latest/
- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OpenFGA: https://openfga.dev/docs/fga
- Open Policy Agent: https://www.openpolicyagent.org/docs/latest
- Azure AI Search document-level access control: https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview
- Amazon Q Business connector concepts: https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/connector-concepts.html
- Google Vertex AI Search data source access control: https://docs.cloud.google.com/generative-ai-app-builder/docs/data-source-access-control
