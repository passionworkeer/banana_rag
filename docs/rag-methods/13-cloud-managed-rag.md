# 13 云托管 RAG（Bedrock / Azure AI Search / Vertex AI）

## 定义

直接使用云厂商提供的企业级 RAG 服务。不自建向量库、不自建解析服务、不自建权限层，而是把云厂商的"知识库/搜索"产品当作底座。

## 主流服务

| 厂商 | 服务 | 特点 |
|------|------|------|
| AWS | Amazon Bedrock Knowledge Bases | 整合 Bedrock 模型 + OpenSearch + S3 + IAM |
| Azure | Azure AI Search（带 RAG 能力） | 与 Entra ID、Blob Storage、OpenAI 深度集成 |
| Google Cloud | Vertex AI Search / Vector Search | Vertex AI 生态、Document AI 解析 |
| Snowflake | Snowflake Cortex Search | 数据仓库内做搜索，无需数据迁移 |
| Databricks | Mosaic AI Vector Search | Lakehouse 内一体化，与 Delta Lake 集成 |

## 适用

- 已有云厂商基础设施的组织。
- 数据合规允许使用云服务的场景。
- 追求快速上线，不打算自建底座。
- 团队规模小，没有专门的平台工程组。

## 不适用

- 强合规要求（金融、政企、法务）必须全私有化。
- 数据不能出内网。
- 已有自建技术栈，迁移成本高。
- 需要深度定制（云厂商能力受限于其产品边界）。

## 优势

- 上线最快：几小时到几天即可验证业务价值。
- 内置权限：IAM / Entra ID 身份体系。
- 内置审计：调用日志、检索 trace。
- 内置安全裁剪：Azure AI Search / Amazon Q Business 都有文档级 ACL。
- 运维负担低：扩缩容、备份、监控都交给云厂商。

## 局限

- 供应商绑定：模型、向量库、搜索都被绑定。
- 成本透明度差：embedding、rerank、LLM、存储分开计费，需要持续优化。
- 定制空间小：解析、检索、权限细节不能改底层。
- 数据出云：即使有合规承诺，仍需法务和安全评审。
- 多云迁移成本：一旦绑定，迁移到另一家要重建索引。

## 内置 ACL 能力参考

- Azure AI Search 文档级访问控制：https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview
- Amazon Q Business 连接器：https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/connector-concepts.html
- Vertex AI Search 数据源访问控制：https://cloud.google.com/generative-ai-app-builder/docs/data-source-access-control

## 与自建方案的对比

| 维度 | 云托管 | 自建 |
|------|--------|------|
| 上线速度 | 天级 | 月级 |
| 定制空间 | 小 | 大 |
| 供应商锁定 | 强 | 无 |
| 单次成本 | 中 | 低（规模大时） |
| 运维负担 | 低 | 高 |
| 合规可控 | 取决于厂商 | 完全可控 |

## 推荐策略

- 短期 PoC：可以先用云托管验证业务价值。
- 中期生产：评估合规后决定是否继续用云托管或迁移到自建。
- 长期：如果有强定制需求，建议抽象一层 RAG 接口，底层可插拔。

## 来源

- `../enterprise-knowledge-base/03-technology-selection.md` §8 方案 C
- `../enterprise-knowledge-base/05-enterprise-deep-dive.md` §9
- `../enterprise-knowledge-base/01-research-summary.md` 阶段 1
