# 企业知识库技术选型

调研日期：2026-05-29

## 1. 总体选型原则

选型优先级：

1. 权限和治理能力优先于炫酷问答效果。
2. 文档解析质量优先于模型大小。
3. 检索可解释性优先于端到端黑盒。
4. 组件可替换优先于绑定单一平台。
5. 先跑通闭环，再扩大 Agent 能力。

## 2. 开源知识库/RAG 平台

| 项目 | 适合用途 | 优点 | 风险/限制 | 链接 |
| --- | --- | --- | --- | --- |
| RAGFlow | 文档理解型 RAG 参考平台 | 强调深度文档理解、可视化知识库、适合研究复杂 PDF 处理链路 | 企业权限、内部系统集成仍需二次开发 | https://github.com/infiniflow/ragflow |
| Dify | LLM 应用平台和知识库原型 | 上手快，应用编排、数据集、工作流生态成熟 | 作为企业知识基础设施时，需要补权限治理和深度定制 | https://github.com/langgenius/dify |
| MaxKB | 轻量知识库问答系统 | 中文社区友好，部署较轻，适合内部 PoC | 复杂多租户、多 Agent 和企业治理能力需扩展 | https://github.com/1Panel-dev/MaxKB |
| AnythingLLM | 团队知识库与聊天入口 | 工作区体验清晰，适合个人/团队文档问答 | 更偏产品应用，不适合作为复杂企业平台内核 | https://github.com/Mintplex-Labs/anything-llm |
| Open WebUI | LLM Web 入口 | 适合作为模型和知识库使用入口 | 不应承担底层知识治理职责 | https://github.com/open-webui/open-webui |

建议：

- PoC 可以用 RAGFlow、Dify 或 MaxKB 快速验证体验。
- 正式企业平台建议自建核心服务，把这些项目作为参考或局部能力来源。

## 3. 文档解析与转换

| 工具 | 适合场景 | 备注 | 链接 |
| --- | --- | --- | --- |
| Docling | PDF、DOCX、PPTX、HTML 等转结构化内容 | 适合保留文档结构和版式信息，适合 RAG 预处理 | https://github.com/docling-project/docling |
| MinerU | 复杂 PDF、论文、扫描件、版式分析、OCR | 适合中文复杂 PDF 和高质量文档理解场景 | https://github.com/opendatalab/MinerU |
| Unstructured | 多格式文档 ETL、分块、企业解析流水线 | 适合做解析服务和数据处理管道 | https://github.com/Unstructured-IO/unstructured |
| Apache Tika | 通用格式识别和文本抽取兜底 | 成熟稳定，适合基础抽取，不负责高级语义结构 | https://tika.apache.org/ |
| MarkItDown | 轻量文档转 Markdown | 适合快速把 Office/PDF/网页转成 Markdown | https://github.com/microsoft/markitdown |

建议组合：

- 默认：Docling + Apache Tika。
- 复杂 PDF/扫描件：MinerU + OCR。
- 企业 ETL/连接器需求强：Unstructured。
- 轻量 Markdown 化：MarkItDown。

## 4. 向量库与搜索库

| 组件 | 适合场景 | 优点 | 注意点 | 链接 |
| --- | --- | --- | --- | --- |
| Qdrant | 自托管向量检索、多租户逻辑隔离 | API 简洁，payload filter 适合权限过滤 | 超大规模需规划 shard/replica | https://qdrant.tech/documentation/ |
| Milvus | 大规模向量检索 | 生态成熟，适合高吞吐大规模向量 | 运维复杂度高于轻量向量库 | https://milvus.io/docs |
| Weaviate | 向量数据库、多租户 collection | 多租户能力明确，GraphQL/REST 生态较完整 | 需要评估团队运维熟悉度 | https://docs.weaviate.io/weaviate |
| pgvector | 中小规模向量检索、与 PostgreSQL 一体化 | 架构简单，元数据和权限模型容易统一 | 超大规模或高并发检索能力有限 | https://github.com/pgvector/pgvector |
| OpenSearch | BM25、混合检索、过滤、日志检索 | 适合关键词和混合搜索，也能承担审计检索 | 向量能力可用但需压测 | https://docs.opensearch.org/latest/vector-search/ |
| Elasticsearch | 企业搜索和混合检索 | 成熟的搜索生态和管理能力 | 授权成本和版本策略需评估 | https://www.elastic.co/enterprise-search/vector-search |

推荐：

- 中小规模试点：PostgreSQL + pgvector + OpenSearch。
- 中大型生产：Qdrant 或 Milvus + OpenSearch。
- 强多租户产品化：Weaviate 或 Qdrant，结合物理隔离策略。

## 5. RAG 编排框架

| 框架 | 适合场景 | 优点 | 注意点 | 链接 |
| --- | --- | --- | --- | --- |
| LlamaIndex | 数据连接、索引、RAG pipeline | 对文档索引和检索抽象友好 | 复杂工作流仍需服务层治理 | https://github.com/run-llama/llama_index |
| LangChain | LLM 应用、工具调用、RAG 组件 | 生态大，组件多 | 需要控制抽象复杂度，避免业务逻辑散落链中 | https://github.com/langchain-ai/langchain |
| LangGraph | 多步骤流程、多 Agent 状态机 | 适合 Agent 编排、状态控制、人工介入 | 需要团队熟悉状态图思维 | https://langchain-ai.github.io/langgraph/ |
| Haystack | 检索 pipeline、搜索问答 | Pipeline 模型清晰，适合检索工程 | 中文生态热度需单独评估 | https://github.com/deepset-ai/haystack |

推荐：

- 单纯文档索引和 RAG：LlamaIndex。
- 需要 Agent 和工具编排：LangChain + LangGraph。
- 检索工程团队偏 pipeline：Haystack。

## 6. Agent 与工具协议

| 技术 | 适合用途 | 说明 | 链接 |
| --- | --- | --- | --- |
| MCP | 让 Agent 通过标准方式访问工具、资源和企业系统 | 适合暴露知识检索、工单、CRM、数据库查询等受控工具 | https://modelcontextprotocol.io/ |
| A2A | Agent 间通信协议 | 适合不同 Agent 或不同厂商 Agent 互相委托任务 | https://a2aproject.github.io/A2A/latest/ |
| LangGraph Multi-Agent | Agent 编排和状态流转 | 适合内部构建 supervisor、handoff、worker agent 模式 | https://langchain-ai.github.io/langgraph/concepts/multi_agent/ |
| AutoGen | 多 Agent 会话和协作 | 适合研究多 Agent 协作模式 | https://github.com/microsoft/autogen |
| CrewAI | 角色型 Agent 协作 | 适合流程化任务实验 | https://github.com/crewAIInc/crewAI |
| Semantic Kernel | 企业应用中的 Agent/插件编排 | .NET/企业微软生态友好 | https://github.com/microsoft/semantic-kernel |

推荐：

- 企业内部工具统一通过 MCP Server 暴露。
- Agent 之间通过 Agent Gateway 调 A2A 或内部协议。
- 多 Agent 状态编排优先考虑 LangGraph。

## 7. 模型与 Embedding

模型选型建议分层：

- Embedding 模型：优先选择中文和中英混合表现稳定的模型，建立公司评测集后再定。
- Reranker：对中文企业文档问答很关键，通常能明显提升命中质量。
- LLM：通过 LLM Gateway 抽象，支持私有模型、云模型和不同供应商切换。
- OCR/版面模型：独立于问答 LLM 评估，不能只看聊天效果。

关键要求：

- Embedding 模型变更需要重建向量索引。
- LLM 输出必须带引用，不能把模型回答当事实源。
- 高敏场景需要私有部署或专有网络调用。

## 8. 推荐生产组合

### 方案 A：稳妥自托管

- API：Java Spring Boot 或 Python FastAPI。
- 元数据：PostgreSQL。
- 对象存储：MinIO/S3。
- 队列：Kafka/RabbitMQ/Redis Stream。
- 文档解析：Docling + MinerU + Apache Tika。
- 搜索：OpenSearch。
- 向量库：Qdrant。
- 编排：LlamaIndex + LangGraph。
- Agent 工具：MCP Server。
- 审计与观测：OpenTelemetry + Prometheus/Grafana + 日志平台。

适合：需要数据可控、私有部署、权限治理强的企业。

### 方案 B：快速 PoC

- 知识库应用：Dify 或 RAGFlow。
- 对象存储：MinIO。
- 向量库：内置或 Qdrant/pgvector。
- 文档解析：产品内置 + Docling/MinerU 补充。
- 权限：先做部门 workspace 隔离。

适合：两到四周内验证业务价值。

### 方案 C：云托管优先

- AWS：Amazon Bedrock Knowledge Bases、OpenSearch、S3、IAM。
- Azure：Azure AI Search、Azure Blob Storage、Microsoft Entra ID。
- Google Cloud：Vertex AI、Vertex AI Search、Cloud Storage。

适合：已有云厂商基础设施，且数据合规允许。

参考：

- AWS Bedrock Knowledge Bases: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- Azure AI Search RAG: https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview
- Google Cloud RAG architecture: https://cloud.google.com/architecture/gen-ai-rag-vertex-ai-vector-search

## 9. 授权与策略引擎

| 组件 | 适合场景 | 说明 | 链接 |
| --- | --- | --- | --- |
| OpenFGA | 复杂关系权限、类 Zanzibar 模型 | 适合表达用户、组、文档、文件夹、项目之间的关系 | https://openfga.dev/docs/fga |
| SpiceDB | 细粒度授权、ReBAC | Authzed 开源实现，适合复杂资源关系权限 | https://github.com/authzed/spicedb |
| Open Policy Agent | 策略即代码、ABAC、服务网关鉴权 | 适合把权限、密级、环境上下文写成统一策略 | https://www.openpolicyagent.org/docs/latest |
| Cerbos | 应用授权策略管理 | 适合 RBAC/ABAC 策略集中管理 | https://docs.cerbos.dev/ |

推荐：

- 部门级 MVP：应用内 RBAC + 数据库权限表即可。
- 生产平台：引入独立授权服务，避免权限逻辑散落在 API、检索服务和 Agent 里。
- 多源 ACL：优先考虑 OpenFGA/SpiceDB，保留原始 ACL 和转换后的关系模型。

## 10. 连接器和数据同步

| 方案 | 适合场景 | 说明 | 链接 |
| --- | --- | --- | --- |
| Unstructured connectors | 企业文档 ETL | 覆盖多种来源，适合配合文档解析流水线 | https://docs.unstructured.io/platform/connectors |
| LlamaIndex connectors | RAG 数据加载 | 适合 PoC 和框架内数据接入 | https://docs.llamaindex.ai/en/stable/module_guides/loading/connector/ |
| Airbyte | 数据同步平台 | 适合已有数据平台团队，连接器生态丰富 | https://airbyte.com/connectors |
| 自研连接器 | 复杂 ACL 和企业内网系统 | 必须支持内容、元数据、ACL、版本、删除同步 | - |

推荐：

- 第一阶段只接人工上传 + 一个核心源系统。
- 正式平台的连接器接口必须统一，不能每个来源各自写一套索引逻辑。
- ACL 变更优先级高于内容变更，撤权链路必须可测试。

## 11. 私有模型服务和国产化倾向

| 组件 | 适合场景 | 说明 | 链接 |
| --- | --- | --- | --- |
| vLLM | 高性能 LLM 推理 | OpenAI-compatible API，适合私有化模型网关 | https://docs.vllm.ai/serving/openai_compatible_server.html |
| Xinference | 统一部署 LLM/embedding/rerank | 适合本地模型实验和统一服务 | https://github.com/xorbitsai/inference |
| Ollama | 本地快速验证 | 易用，适合开发和小规模试验 | https://docs.ollama.com/api/openai-compatibility |
| Text Embeddings Inference | embedding 服务 | 适合独立部署 embedding 模型 | https://huggingface.github.io/text-embeddings-inference/ |
| FastGPT | 中文知识库和工作流应用 | 适合参考国产开源知识库产品体验 | https://github.com/labring/FastGPT |

建议：

- LLM、embedding、reranker 通过 Model Gateway 抽象，不要直接写死某个供应商。
- 私有化时优先保证 embedding/reranker 稳定，因为检索质量高度依赖它们。
- 模型升级必须触发评估集回归；embedding 模型变更通常需要重建向量索引。

## 12. 高级检索和图谱

| 能力 | 适合场景 | 注意 |
| --- | --- | --- |
| Hybrid Search | 企业文档默认推荐 | 关键词适合编号、术语、名称，向量适合语义召回 |
| RRF | 多路召回融合 | 简单稳定，适合 BM25 + vector 合并 |
| Reranker | 提升 topK 精度 | 成本和延迟需控制 |
| Parent-child retrieval | 小块召回、大块生成 | 适合制度、合同、技术文档 |
| GraphRAG | 多跳关系推理 | 不建议第一期全量做 |
| ColPali/视觉检索 | PPT、扫描 PDF、图表 | 适合高价值复杂文档试验 |

参考：

- OpenSearch hybrid search: https://docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/
- OpenSearch RRF: https://opensearch.org/blog/introducing-reciprocal-rank-fusion-hybrid-search/
- Microsoft GraphRAG: https://github.com/microsoft/graphrag
- Neo4j GraphRAG: https://neo4j.com/labs/genai-ecosystem/graphrag/
- ColPali: https://arxiv.org/abs/2407.01449

## 13. 选型建议结论

当前需求描述属于复杂企业知识基础设施，不只是知识库聊天。建议：

1. 先用 Dify/RAGFlow/MaxKB 做体验验证，但不要把正式权限和数据治理绑定在它们内部。
2. 正式平台采用自研 API 和治理层，底层接可替换开源组件。
3. 第一版重点打磨文档解析、权限过滤、引用回答和审计。
4. 第二版再引入多 Agent 通信和跨部门流程。
5. 任何 Agent 能力都必须通过网关访问知识库，不能直接连向量库或搜索库。
