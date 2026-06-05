# Karpathy LLM Wiki 落地 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `D:\Data\Desktop\rag\knowledge-base\` 下落地 Karpathy LLM Wiki 方案的目录骨架、工作流指令和一份验证用示例文章,确保 Obsidian 打开可见、CC 启动后能按约定编译。

**Architecture:** 纯文件落地。`knowledge-base/` 作为独立 Obsidian vault,内部只有 `raw/`(只读输入)、`wiki/`(CC 写)、`CLAUDE.md`(工作流指令)、`README.md`(使用说明)。编译由 CC 对话驱动,不写编排脚本。

**Tech Stack:** 无运行时技术栈。文件层只有 Markdown + Git。

**Spec:** `D:\Data\Desktop\rag\docs\superpowers\specs\2026-06-05-llm-wiki-design.md`

**Working Directory:** `D:\Data\Desktop\rag` (本项目根,git 仓库)

---

## 任务清单概览

| 任务 | 产物 |
|---|---|
| Task 1 | `knowledge-base/raw/.gitkeep` + `wiki/.gitkeep` |
| Task 2 | `knowledge-base/.gitignore`(忽略 `.obsidian/`) |
| Task 3 | `knowledge-base/CLAUDE.md`(CC 工作流指令) |
| Task 4 | `knowledge-base/README.md`(用户使用说明) |
| Task 5 | `knowledge-base/raw/00-llm-wiki-demo.md`(示例文章) |
| Task 6 | 根 `README.md` 加 `knowledge-base/` 定位说明 |
| Task 7 | 端到端冒烟验证(目录结构 + 示例) |

每个任务独立 commit。

---

### Task 1: 创建 raw/ 和 wiki/ 目录占位

**Files:**
- Create: `knowledge-base/raw/.gitkeep`
- Create: `knowledge-base/wiki/.gitkeep`

- [ ] **Step 1: 创建两个目录及其 .gitkeep**

PowerShell:
```powershell
New-Item -ItemType Directory -Force -Path "D:\Data\Desktop\rag\knowledge-base\raw"
New-Item -ItemType Directory -Force -Path "D:\Data\Desktop\rag\knowledge-base\wiki"
New-Item -ItemType File -Force -Path "D:\Data\Desktop\rag\knowledge-base\raw\.gitkeep"
New-Item -ItemType File -Force -Path "D:\Data\Desktop\rag\knowledge-base\wiki\.gitkeep"
```

Bash(若用 bash,目录用斜杠):
```bash
mkdir -p "D:/Data/Desktop/rag/knowledge-base/raw" "D:/Data/Desktop/rag/knowledge-base/wiki"
touch "D:/Data/Desktop/rag/knowledge-base/raw/.gitkeep" "D:/Data/Desktop/rag/knowledge-base/wiki/.gitkeep"
```

- [ ] **Step 2: 验证目录和文件存在**

```bash
ls -la "D:/Data/Desktop/rag/knowledge-base/raw" "D:/Data/Desktop/rag/knowledge-base/wiki"
```

预期:两个目录都列出,各含一个 `.gitkeep` 文件。

- [ ] **Step 3: 提交**

```bash
cd "D:/Data/Desktop/rag" && git add knowledge-base/raw/.gitkeep knowledge-base/wiki/.gitkeep && git commit -m "feat(llm-wiki): scaffold raw/ and wiki/ directories"
```

---

### Task 2: 添加 .gitignore 忽略 .obsidian/

**Files:**
- Create: `knowledge-base/.gitignore`

- [ ] **Step 1: 写 .gitignore**

```gitignore
# Obsidian 个人配置,不进 git
.obsidian/
```

- [ ] **Step 2: 提交**

```bash
cd "D:/Data/Desktop/rag" && git add knowledge-base/.gitignore && git commit -m "feat(llm-wiki): ignore .obsidian/ personal config"
```

---

### Task 3: 写 CLAUDE.md(CC 工作流指令)

**Files:**
- Create: `knowledge-base/CLAUDE.md`

- [ ] **Step 1: 写入 CLAUDE.md**

完整内容:

````markdown
# CLAUDE.md

你正在 `knowledge-base/` 目录下工作,这是用户的个人 LLM Wiki vault,基于 Karpathy 的 LLM Wiki 方案。

## 区域职责

- **`raw/`** 是**只读输入区**。你不得修改、重命名、删除其中的文件。
- **`wiki/`** 是你**唯一能写**的输出区。所有衍生内容(摘要、交叉引用)都放这里。

## 单文件编译流程

用户让你处理一个 `raw/` 文件时,执行:

1. 读文件,提取核心观点,生成 500-1000 字摘要。
2. 在 `wiki/` 下创建 `<slug>.md`,slug 默认采用原文件主名(去掉扩展名);同名冲突时追加 `-2`、`-3`。
3. 页面结构:
   - **核心论点**:200-400 字,说清这篇文章/资料讲什么、立场是什么。
   - **关键术语**:5-10 个,加 `[[wikilink]]` 指向 `wiki/` 中已有的对应页面;无对应页面时纯文本。
   - **跨资料连接**:列出与已有 `wiki/*.md` 的关联点,用 `[[wikilink]]` 引用。
4. **不写"读后感"或主观评论**。只整理,不发挥。

## 触发方式

- 单文件:用户说"处理 `raw/xxx.md`"或"处理这个" → 处理该文件。
- 批量:用户说"处理 `raw/` 下所有未编译文件" → 扫描 `raw/` 中尚无对应 `wiki/<slug>.md` 的文件,逐个处理。
- 重编译:用户说"重新编译 `raw/yyy.md`" → 覆盖对应 `wiki/yyy.md`。

## 禁做项

- 不做整库全量重编译(单文件粒度,token 太贵)。
- 不维护全局索引页;Obsidian 图谱视图即索引。仅在 `wiki/` 累计 30+ 页时,才写一次 `wiki/_index.md`。
- 不做向量化、不做问答接口(本 vault 不是 RAG)。
- 不为单篇文章之外的资源(图片、附件)做特殊处理,随所属文章引用即可。

## 链接格式

- Obsidian 内部链接:`[[页面名]]` 或 `[[页面名|显示文本]]`。
- 不用 Markdown 普通链接做内部引用。

## Frontmatter

不强制。如果觉得必要(记录源 URL、作者、阅读日期),可加 YAML frontmatter;不强制所有页面都加。
````

- [ ] **Step 2: 验证文件写入**

```bash
ls -la "D:/Data/Desktop/rag/knowledge-base/CLAUDE.md"
```

预期:文件存在,大小约 1.5-2KB。

- [ ] **Step 3: 提交**

```bash
cd "D:/Data/Desktop/rag" && git add knowledge-base/CLAUDE.md && git commit -m "feat(llm-wiki): add CLAUDE.md workflow spec for CC"
```

---

### Task 4: 写 README.md(用户使用说明)

**Files:**
- Create: `knowledge-base/README.md`

- [ ] **Step 1: 写入 README.md**

完整内容:

````markdown
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
````

- [ ] **Step 2: 验证文件写入**

```bash
ls -la "D:/Data/Desktop/rag/knowledge-base/README.md"
```

预期:文件存在。

- [ ] **Step 3: 提交**

```bash
cd "D:/Data/Desktop/rag" && git add knowledge-base/README.md && git commit -m "docs(llm-wiki): add README.md user guide"
```

---

### Task 5: 放一份示例文章到 raw/

**Files:**
- Create: `knowledge-base/raw/00-llm-wiki-demo.md`

- [ ] **Step 1: 写入示例文章**

内容:一篇简短、技术性、便于 CC 提取术语和论点的样例文章,选用本项目自身作为话题(自指)以验证跨资料连接的最小路径。

````markdown
---
title: RAG 检索增强生成的本质
source: 自撰笔记
date: 2026-06-05
---

# RAG 检索增强生成的本质

RAG(Retrieval-Augmented Generation)是一种把外部知识库接入大语言模型推理流程的模式:用户提问 → 把问题向量化 → 在向量库中找最相似的若干片段 → 把这些片段作为上下文一起喂给 LLM → LLM 生成答案。

## 为什么需要 RAG

LLM 本身知识截止在训练数据上,且无法直接引用企业私有资料。RAG 解决了两个问题:
1. **时效性**:外部知识库可以持续更新,LLM 推理时拿到的是最新切片。
2. **私有性**:企业数据不出库,LLM 只在生成阶段被"喂"摘要,数据主权不丢。

## RAG 的致命痛点

工业落地中,传统 RAG 经常跑通但效果不理想,主要是三个原因:
- **检索噪声**:向量相似 ≠ 语义相关,检索到的片段可能和用户意图无关,LLM 基于错误上下文"一本正经胡说八道"。
- **意图理解缺失**:用户提问往往模糊("那个报错怎么修?"),缺失上下文;RAG 把模糊问题直接去检索,结果跑偏。
- **无法多步推理**:复杂问题需要拆解,而 RAG 是一次性流程。

## Agentic RAG 的转向

新一代方向是让 LLM 智能体在检索前先重写问题、规划检索路径,再走传统 RAG。这就是 Agentic RAG 的核心思想。
````

- [ ] **Step 2: 验证文件存在**

```bash
ls -la "D:/Data/Desktop/rag/knowledge-base/raw/00-llm-wiki-demo.md"
```

预期:文件存在,大小约 1-1.5KB。

- [ ] **Step 3: 提交**

```bash
cd "D:/Data/Desktop/rag" && git add knowledge-base/raw/00-llm-wiki-demo.md && git commit -m "feat(llm-wiki): add demo article for compile validation"
```

---

### Task 6: 在项目根 README.md 加 knowledge-base/ 定位说明

**Files:**
- Modify: `README.md`(项目根,非 knowledge-base/)

- [ ] **Step 1: 读当前 README.md**

```bash
cat "D:/Data/Desktop/rag/README.md"
```

预期:已有 30 行左右表格型 README(用户已看过内容)。

- [ ] **Step 2: 在表格前/后加一行说明**

在 `## 目录结构` 表格后追加一节(保持现有表格不动):

```markdown

## 知识库 vault

`knowledge-base/` 是基于 Karpathy LLM Wiki 方案的**独立 Obsidian vault**,与上表中的 `docs/`(企业 RAG 调研)、`scrapers/`(爬虫归档)、`logs/`(调试日志)互不相关。用 Obsidian 打开 `knowledge-base/` 时,只看到 `raw/` 和 `wiki/`,不会被其它目录污染。详见 [knowledge-base/README.md](knowledge-base/README.md)。
```

- [ ] **Step 3: 验证修改**

```bash
grep -n "knowledge-base" "D:/Data/Desktop/rag/README.md"
```

预期:至少匹配到新增段落中的 "knowledge-base"。

- [ ] **Step 4: 提交**

```bash
cd "D:/Data/Desktop/rag" && git add README.md && git commit -m "docs: document knowledge-base/ vault in project README"
```

---

### Task 7: 端到端冒烟验证

**目的:** 验证整库结构、CC 启动指令、示例文章齐全,所有承诺的"成功标准 1-2 项"可观察。

- [ ] **Step 1: 验证目录结构**

```bash
ls -la "D:/Data/Desktop/rag/knowledge-base"
ls -la "D:/Data/Desktop/rag/knowledge-base/raw"
ls -la "D:/Data/Desktop/rag/knowledge-base/wiki"
```

预期:
- `knowledge-base/` 下有:`raw/`、`wiki/`、`CLAUDE.md`、`README.md`、`.gitignore`
- `raw/` 下有:`.gitkeep`、`00-llm-wiki-demo.md`
- `wiki/` 下仅有:`.gitkeep`(空目录,符合 spec)

- [ ] **Step 2: 验证 .gitignore 正确**

```bash
cat "D:/Data/Desktop/rag/knowledge-base/.gitignore"
```

预期:内容为 `.obsidian/`。

- [ ] **Step 3: 验证 git 状态干净**

```bash
cd "D:/Data/Desktop/rag" && git status
```

预期:`working tree clean`(所有文件已提交,包括 6 个新 commit)。

- [ ] **Step 4: 验证 git log 显示所有 commit**

```bash
cd "D:/Data/Desktop/rag" && git log --oneline -10
```

预期:看到至少 7 个 commit —— 1 个初始 + 1 个 spec + 6 个 plan 任务。

- [ ] **Step 5: 验证项目根 README 已含 knowledge-base/ 说明**

```bash
grep -A 2 "知识库 vault" "D:/Data/Desktop/rag/README.md"
```

预期:看到新加的段落。

- [ ] **Step 6: 验证(可选,需用户手动)Obsidian 可打开 vault**

用户自行验证:在 Obsidian 中"Open folder as vault" → 选 `D:\Data\Desktop\rag\knowledge-base\` → 应看到 `raw/` 和 `wiki/` 文件夹,以及 `00-llm-wiki-demo.md`。**这一步不阻塞 plan 完成**,但建议用户在第一次使用前确认。

- [ ] **Step 7: 验证(可选,需用户手动)CC 启动指令可被读取**

用户自行验证:在 `knowledge-base/` 下启动 `claude --dangerously-skip-permissions`,CC 应自动读取 `CLAUDE.md` 并据此工作。**这一步不阻塞 plan 完成**。

---

## Self-Review

**1. Spec 覆盖核对:**

| Spec 章节 | 任务 |
|---|---|
| §2 目录布局 (knowledge-base/, raw/, wiki/) | Task 1 |
| §2 .obsidian/ 忽略 | Task 2 |
| §2 CLAUDE.md | Task 3 |
| §2 README.md | Task 4 |
| §6 成功标准 1 (Obsidian 看到 raw/、wiki/) | Task 7 Step 1 |
| §6 成功标准 5 (项目 README 含 knowledge-base/) | Task 6 |
| §3.2 单文件编译流程的可读样例 (raw/ 有内容) | Task 5 |
| §6 成功标准 2-4 (CC 实际编译出 wiki 页 + 交叉引用) | **非本 plan 范围**,spec 6.2-6.4 验证需用户手动跑 CC |

**结论:** Task 1-7 覆盖了"骨架落地 + 可观察"的所有 spec 条款。spec §6.2-6.4(CC 实际编译出 wiki 页、生成交叉引用)需用户手动跑 CC,不在文件落地 plan 内,这是 plan scope 边界。

**2. 占位符扫描:** 无"TBD"/"TODO"/"fill in details"。所有代码块完整。Task 7 Step 1 的 PowerShell + Bash 双写法是显式给 Windows/macOS 工程师看的,不是占位。

**3. 类型/命名一致性:** 文件名/路径在所有任务间一致 (`knowledge-base/`、`raw/`、`wiki/`、`CLAUDE.md`、`README.md`、`.gitignore`、`.gitkeep`、`.obsidian/`、`00-llm-wiki-demo.md`、项目根 `README.md`)。
