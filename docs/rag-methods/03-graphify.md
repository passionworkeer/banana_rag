# 03 Graphify（实体知识图谱）

## 定义

把任何文件夹（代码、SQL 模式、R 脚本、shell 脚本、文档、论文、图像或视频）一次性分析完毕，压缩成可查询的知识图谱。后续查询走图谱遍历，不再重新读取原始文件。

## 关键特征

- 一次构建、长期可查：分析工作一次性做完，结果物化到磁盘。
- Token 极省：卡帕西博客案例中，每次查询 token 量降低 71.5 倍。
- 持久化：数周后仍可查询，无需重新读原始文件。
- 增量缓存：SHA256 缓存，重复运行只处理变更过的文件。
- 多种查询方式：自然语言、路径查询、实体解释。

## 适用

- 快速熟悉陌生项目代码库。
- 论文集、文档集、参考资料集的关系梳理。
- 需要"全图鸟瞰"的场景。
- 混合语料（代码 + 文档 + 模式）。

## 不适用

- 实时更新要求高的企业知识库。
- 需要严格权限隔离的部门数据。
- 文档量小、关系稀疏的资料集。

## 输出物

运行 `/graphify <dir>` 后生成 `graphify-out/`：

```
graphify-out/
├── graph.html           可交互图谱，可点节点、搜索、按社区过滤
├── GRAPH_REPORT.md      God nodes、意外连接、建议提问
├── graph.json           持久化图谱
└── cache/               SHA256 缓存
```

## 查询命令

- `/graphify query "how does user authentication flow through the system?"` — 自然语言查询。
- `/graphify path "UserService" "DatabasePool"` — 找两个实体的最短路径。
- `/graphify explain "PaymentProcessor"` — 用自然语言解释某个实体。

## 运行模式

- `/graphify <dir>` — 标准分析。
- `/graphify --deep` — 深度模式，更激进的关系推断。
- `/graphify <subdir>` — 处理特定子目录。
- `/graphify --watch` — Watch 模式，文件变化时重建图谱。

## 与 LLM Wiki 的区别

| 维度 | LLM Wiki | Graphify |
|------|----------|----------|
| 形态 | 笔记 + 整理 | 实体关系图谱 |
| 优化对象 | 知识复利 | 一次性深度分析 |
| 查询方式 | Markdown 链接 + 语义 | 图遍历 + 路径查找 |
| 适合规模 | 100-200 篇文章 | 单个代码库或大型文档集 |
| 工具载体 | Obsidian | 任意目录 + graph.html |

## 来源

- `../rag_idea.md` 82-137 行
- 官网：https://graphifylabs.ai/
- GitHub：https://github.com/safishamsi/graphify
