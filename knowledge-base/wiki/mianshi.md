# 面试原始题汇总

## 核心论点

本文件是面试题目的原始收集入口,保留为非整理版本,后续整理时根据已有分类判断是否重复,重复题合并到已有问题的"相似问法/常见追问",新题按分类补进对应文档(如 [[01-大模型基础]] ~ [[08-前端AI应用与产品设计]]),并写详细回答。所有新题目继续粘到本文件末尾。

当前汇总的题目涵盖七大方向:**项目深度拷问** (图文模态对齐、Milvus 索引选型、专业术语语义偏移、Embedding 微调/Adapter 适配、Agent 对话/画像项目数据格式映射、长期画像与实时状态冲突、检索依赖问题、QA 业务型 vs deepsearch agent、MCP schema 与协议、Agent evaluation 流程、rag 文档 chunk、embedding 选型、检索/生成问题判断、手撕 multiattention);**AI Agent 核心技术原理** (CoT vs ReAct、Function Call 完整流程、Workflow vs Agent 选型);**Agent 记忆与检索优化** (长短期记忆设计、动态压缩与选择性遗忘、RAG 知识精准输入、Rerank 提升决策准确性);**多 Agent 与人机协作** (单 Agent 局限、Router 路由规则、Human-in-the-loop 机制);**系统评估与性能优化** (Agent 评估指标、生成质量外的维度、延迟优化、RAG 是否被长上下文替代);**AI 业务/项目/原理** (Transformer/Attention/Self-Attention/MoE/SFT/LoRA/KV Cache/DPO/PPO/GRPO/KL/RAG/Rerank/LangGraph/MinerU 等核心八股)。

**2026-06-03 新增 29 题** 主要覆盖:AI 写代码能力预期、三数之和、Java 锁(synchronized vs ReentrantLock)、ThreadLocal、Java 异常分类、线程池异常处理、HTTPS 加密、Java 线程状态、反射与动态代理、类加载触发场景;实习项目深挖(AI 出码流程、系统设计、token 消耗、SDD/TDD、Skill 创建方式、Function Call 与 MCP 关系、MCP 通信方式、Function Call 工具描述方式、MCP 调用查询天气流程、笔试交互、AI 代码验证、单 agent vs 多 agent、英文口语);MySQL 深度分页优化、B+ 树 vs 红黑树 vs 平衡二叉树 vs 哈希、HashMap 1.7 vs 1.8 优化、线程池核心参数、Redis 场景与分布式锁原理、分布式锁过期时间与看门狗机制等。

## 关键术语

- 原始题
- 项目拷打
- Agent 原理
- 记忆与检索
- 多 Agent
- 评估与性能
- 2026-06-03 新增
- AI 出码
- Java 并发
- MySQL 索引

## 跨资料连接

- [[interview-README]] — 面试题库总览与整理规则。
- [[01-大模型基础]] ~ [[08-前端AI应用与产品设计]] — 八大整理版题库。
- [[00-答题规范与公式速查]] — 通用答题骨架。
- [[2026-06-03-interview-html-expansion]] — 本文件 2026-06-03 新增 29 题对应 HTML 扩展计划。
- [[html-README]] — 配套 HTML 知识页。
