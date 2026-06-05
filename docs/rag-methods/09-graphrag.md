# 09 GraphRAG（多跳推理）

## 定义

传统 RAG 基于"文档相似度"检索，适合回答"这个标准是什么"。GraphRAG 基于"实体关系图谱"检索，适合回答"X 部门和 Y 系统的关系"、"为什么这个制度适用于这个项目"等需要多跳推理的问题。

## 核心思想

- 抽取实体（人、部门、系统、项目、客户、产品、制度）。
- 抽取关系（属于、负责、依赖、适用、引用）。
- 建图谱（Neo4j、NebulaGraph、LightRAG、Microsoft GraphRAG）。
- 查询时图遍历 + 子图召回，再喂给 LLM。

## 适合的场景

- 企业组织、人员、系统、项目、客户、产品之间关系复杂。
- 问题经常需要多跳推理（A → B → C → D）。
- 需要解释"为什么这个制度适用于这个项目"。
- 有结构化数据和半结构化数据可结合。

## 不适合

- 第一阶段只是文档搜索问答。
- 文档质量差、实体标准不统一。
- 缺少图谱治理人员。
- 文档更新频率极高，关系频繁变化。

## 主流实现

| 项目 | 特点 |
|------|------|
| Microsoft GraphRAG | 微软开源，社区热度高，文档详尽 |
| Neo4j GraphRAG | 图数据库原生支持，企业级稳定 |
| LightRAG | HKUDS 开源，轻量，适合 PoC |
| NebulaGraph + 自研 | 国内大规模图数据库 |

## 推荐路线

1. 第一版：只保留元数据关系表（部门、空间、文档、项目、负责人），不建正式图谱。
2. 第二版：做轻量实体抽取（系统名、项目名、产品名、客户名、制度名）。
3. 第三版：再引入 Neo4j/NebulaGraph/GraphRAG。

## 与 Graphify 的区别

Graphify 是**个人/项目**层面的一次性分析（看 `03-graphify.md`），GraphRAG 是**企业**层面的长期知识基础设施。

| 维度 | Graphify | GraphRAG |
|------|----------|----------|
| 范围 | 单个文件夹 | 全企业 |
| 维护 | 一次性 + watch | 持续治理 |
| 权限 | 无 | 严格部门隔离 |
| 工具 | graph.html / graph.json | Neo4j / NebulaGraph |
| 适合 | 快速熟悉陌生项目 | 跨部门关系推理 |

## 何时上

满足以下至少两条时，再考虑引入 GraphRAG：

- 业务问题经常需要 2 跳以上推理。
- 有专门的图谱治理角色。
- 实体抽取质量能达到 80% 以上准确率。
- 文档更新频率允许图谱定期重建。

## 来源

- `../enterprise-knowledge-base/03-technology-selection.md` §12
- `../enterprise-knowledge-base/05-enterprise-deep-dive.md` §4.3
- Microsoft GraphRAG：https://github.com/microsoft/graphrag
- Neo4j GraphRAG：https://neo4j.com/labs/genai-ecosystem/graphrag/
- LightRAG：https://github.com/HKUDS/LightRAG
