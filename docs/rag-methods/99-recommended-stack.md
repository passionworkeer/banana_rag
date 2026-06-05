# 推荐方案：怎么选、用什么、什么顺序

本文档根据 `rag_idea.md` 三大场景（个人知识库 / 熟悉项目 / 企业海量）以及本项目 `docs/enterprise-knowledge-base/` 调研结论，给出具体推荐。

## 1. 三场景 → 首选方案

| 场景 | 首选 | 备选 | 关键原因 |
|------|------|------|----------|
| 个人/小团队知识库（100-200 篇） | **02 LLM Wiki（卡帕西/Obsidian）** | 01 传统 RAG + Dify | 知识复利，越用越准；本地优先，零成本 |
| 快速熟悉陌生项目代码 | **03 Graphify** | 01 传统 RAG（按文件检索） | 一次构建、长期可查；71.5× token 节省 |
| 企业海量数据 + 部门隔离 | **04 混合检索 + 05 RRF+Rerank + 11 Agentic RAG** | 13 云托管 RAG（PoC 阶段） | 工程成熟、可治理、符合企业合规要求 |

`rag_idea.md` 原文结论："建立一个个人知识库就用卡帕西，熟悉一个具体项目就用 Graphify，企业海量数据 RAG"——本项目的方法论和该结论一致。

## 2. 推荐组合（按阶段）

### 阶段 0：本地尝鲜（0-1 天）

仅用于验证"AI 整理笔记是不是真有用"。

- 方法：**02 LLM Wiki**。
- 工具：Obsidian + Claude Code + Karpathy gist 工作流。
- 投入：1-2 小时搭环境 + 5-10 篇笔记试跑。
- 验收：扔一篇新资料进 `raw/`，让 AI 整理后，Obsidian 图谱视图出现新的关联。

### 阶段 1：项目代码熟悉（0.5-1 天）

- 方法：**03 Graphify**。
- 工具：`/graphify <dir>` + 浏览器打开 `graph.html`。
- 投入：跑一次标准分析 + 用 `query`/`path`/`explain` 验证。
- 验收：用 `/graphify explain` 解释 3 个核心实体，答案和代码对得上。

### 阶段 2：企业 PoC（2-4 周）

- 方法：01 传统 RAG + 04 混合检索 + 05 RRF+Rerank + 07 查询理解 + 08 结构化查询。
- 工具栈：参考 `enterprise-knowledge-base/03-technology-selection.md` 方案 A 或 B。
  - 方案 A（稳妥自托管）：FastAPI + PostgreSQL + MinIO + OpenSearch + Qdrant + LlamaIndex + LangGraph。
  - 方案 B（快速 PoC）：Dify 或 RAGFlow + MinIO + 内置向量库。
- 投入：1-2 名工程师 + 1 个试点部门。
- 验收：20-50 个真实问题评估集 + 引用准确率 > 90% + 权限负例泄露率 = 0。

### 阶段 3：知识治理与权限（4-8 周）

- 方法：阶段 2 的全部 + ACL 同步 + 撤权链路 + 审计回放。
- 工具栈：增加 SSO（飞书/OIDC）、OpenFGA 或 SpiceDB、DLP 工具。
- 投入：增加 1 名安全/治理方向工程师。
- 验收：源系统 ACL 同步可测试 + 撤权 < N 分钟生效 + 审计可按用户/文档/问题回放。

### 阶段 4：智能体协作（8 周以后）

- 方法：阶段 3 的全部 + 11 Agentic RAG + 12 多 Agent 协作。
- 工具栈：增加 Agent Gateway、MCP Server、A2A 协议、LangGraph Multi-Agent。
- 投入：增加 1-2 名 Agent 工程师。
- 验收：2-3 个部门 Agent 上线 + 跨部门任务可委托 + 所有调用有审计。

### 阶段 5：高级能力（按需）

- 09 GraphRAG：当出现"为什么 X 适用于 Y"等多跳问题且评估确认能提升时才上。
- 10 ColPali：当扫描 PDF/PPT 占比 > 20% 且有高价值文档时上。
- 13 云托管 RAG：当 PoC 持续投入大、自建底座成本不划算时迁移评估。

## 3. 哪些方法不建议优先尝试

| 方法 | 建议 | 原因 |
|------|------|------|
| 09 GraphRAG | 不要在第一版上 | 建模和治理成本高，效果提升不确定 |
| 10 ColPali | 不要在第一版全量上 | 算力贵，适合作为高价值文档的实验性补充 |
| 12 多 Agent 协作 | 阶段 4 之前不要上 | 权限和审计治理复杂，没有 Agent Gateway 会乱套 |
| 13 云托管 RAG | 短期 PoC 可用，长期慎用 | 供应商锁定、数据出云风险 |

## 4. 给本项目（企业 RAG 调研项目）的具体建议

本项目目前已有完整的 Bananain 企业知识库调研（`docs/enterprise-knowledge-base/`），缺的是"个人/小团队"和"熟悉项目"两个轻量场景的实践。建议补充：

1. **加跑一次 LLM Wiki 实验**（半天）：用 Karpathy 工作流对 `docs/enterprise-knowledge-base/` 这 11 篇文档做整理，对比"扔进 Obsidian 让 AI 持续整理"和"扔进向量库做 RAG"的检索体验差异。
2. **加跑一次 Graphify 实验**（半天）：用 `/graphify ./scrapers` 分析项目里 3 轮爬虫的代码关系，验证 Graphify 在熟悉陌生代码上的效率提升。
3. **把方法清单作为决策辅助**：未来 Bananain 的阶段 2-4 推进时，按本文档的阶段路线决定何时引入 GraphRAG / ColPali / 多 Agent。

## 5. 决策 checklist

开始任何一个新 RAG 项目前，先回答 4 个问题：

- [ ] 文档量级是多少？（< 200 篇 → LLM Wiki / 数万篇 → 混合检索 + 企业 RAG）
- [ ] 提问模式是模糊还是精准？（模糊 → 查询理解 + Agentic）
- [ ] 是否需要权限隔离？（要 → 走企业 RAG 路线 / 不要 → 个人 Wiki 即可）
- [ ] 是否有结构化数据查询诉求？（要 → 准备 SQL/API 适配层 / 不要 → 纯 embedding）

## 6. 一句话总结

- **个人/小团队** → 02 LLM Wiki 复利。
- **熟悉项目** → 03 Graphify 一次构建。
- **企业海量** → 04+05+07+08 起步，11+12 演进，09/10 按需。
- **快速上线** → 13 云托管 PoC，但留好抽象层防锁定。

## 关联文档

- [00-rag-methods-overview.md](00-rag-methods-overview.md)：13 个方法总览与对比。
- `../rag_idea.md`：科普原文。
- `../enterprise-knowledge-base/README.md`：企业调研索引。
- `../enterprise-knowledge-base/plans/00-platform-roadmap/plan.md`：企业级落地路线。
