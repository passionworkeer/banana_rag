# 知识库(LLM Wiki)

这是基于 Karpathy LLM Wiki 方案的个人知识库 vault,驱动方式是 Obsidian + Claude Code 对话。

## 怎么用

1. 用 Obsidian 打开本目录(`D:\Data\Desktop\rag\knowledge-base\`),首次打开 Obsidian 会自动建 `.obsidian/` 配置目录(本仓库已 `.gitignore`)。
2. 把想读的文章、报告、书摘、网页剪藏扔到 **`raw/`** 下。文件名就是它将派生出的 wiki 页面名。
3. 启动 Claude Code,进入本目录。它会自动读 `CLAUDE.md` 知道工作流。
4. 在 CC 里说"处理 `raw/xxx`"或"处理 `raw/` 下所有未编译文件",CC 会在 **`wiki/`** 下生成对应的总结页面,带 `[[wikilink]]` 交叉引用。
5. 用 Obsidian 的图谱视图看 wiki 节点之间的连接。

## 目录约定

- `raw/` —— 原始资料,只读,CC 不修改。
- `wiki/` —— 编译产物,CC 唯一能写的区域。
- `CLAUDE.md` —— CC 的工作流指令(看不懂可以读,但不需要改)。
- `.obsidian/` —— Obsidian 个人配置,本仓库已忽略。

## 什么时候扩展

- `wiki/` 累计 30+ 页时,让 CC 生成一次 `wiki/_index.md`。
- 50+ 页时再评估是否要分主题子目录(起步不分)。

## 与项目其它部分的关系

`knowledge-base/` 是独立 vault,与项目根的 `docs/`(企业 RAG 调研)、`scrapers/`(爬虫归档)、`logs/`(调试日志)互不相关。Obsidian 打开 `knowledge-base/` 时不会看到那些目录。
