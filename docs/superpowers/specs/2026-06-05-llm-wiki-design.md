# Karpathy LLM Wiki 落地方案

**日期:** 2026-06-05
**目标:** 在 `D:\Data\Desktop\rag` 项目下复现 Karpathy LLM Wiki 方案,作为个人阅读 & 知识库使用,驱动方式为 Obsidian + Claude Code 对话,纯对话驱动、不写编排脚本。

## 1. 背景与定位

`rag_idea.md` 描述了 Karpathy 方案的形态:把原始资料扔到 `raw/`,让 LLM 编译为有交叉引用的 `wiki/`,通过 Obsidian 图谱视图浏览。与传统 RAG(检索-回答-结束)和 Graphify(代码图谱)的根本差异在于"知识复利"——每次编译都是一次整理,wiki 越用越密。

**本文档不是 RAG 方案:** 不接向量化、不接问答接口。问问题时,直接由 CC 读取 `wiki/` + `raw/` 在上下文窗口内推理,token 量与原始文章总量线性相关,这与 `rag_idea.md` 中提到的 70k tokens/query 量级一致。

**不实现 Graphify 路径:** `rag_idea.md` 也提到 Graphify,但定位是"熟悉一个具体项目代码",与个人阅读库场景不重叠,本文档不涉及。

## 2. 目录布局

新增目录 `D:\Data\Desktop\rag\knowledge-base\`,与现有 `docs/`、`scrapers/`、`logs/` 平级。该目录是**独立 Obsidian vault**,Obsidian 打开此目录时只看到 `raw/` 和 `wiki/`,不被旧 `docs/` 污染。

```
D:\Data\Desktop\rag\knowledge-base\
├── .obsidian\              # Obsidian 自动生成,首次打开时建立;不进 git
├── CLAUDE.md               # CC 启动后看到的工作流指令
├── README.md               # 给"未来的你"的使用说明
├── raw\                    # 原始资料(只读区,CC 不修改)
│   └── .gitkeep
└── wiki\                   # 编译产物(CC 唯一能写的区域)
    └── .gitkeep
```

**与项目根的关系:** `D:\Data\Desktop\rag\README.md` 加一行,说明 `knowledge-base/` 是个人 LLM Wiki vault,与 `docs/`(企业 RAG 调研)、`scrapers/`(爬虫归档)互不相关。

**与现有 `docs/` 的关系:** 互不引用、互不依赖。`docs/` 内的 `rag-methods/` 调研保留原样,`knowledge-base/` 是独立工作空间。

## 3. 工作流

CC 启动并进入 `knowledge-base/` 后,从 `CLAUDE.md` 读取以下约定:

### 3.1 区域职责
- **`raw/`** 是只读输入区。CC 不修改、不重命名、不删除其中的文件。
- **`wiki/`** 是 CC 唯一能写的输出区。所有衍生内容、摘要、交叉引用都放在这里。

### 3.2 单文件编译流程
CC 处理一个新 `raw/` 文件时,执行以下步骤:
1. 读取文件,提取核心观点,生成 500-1000 字摘要。
2. 在 `wiki/` 下创建 `<slug>.md`,slug 默认采用原文件主名(MD/文本)或源信息标题(网页/文章/书摘)。
3. 页面包含三段:核心论点、关键术语、跨资料连接。**不写"读后感"或个人评论**。
4. 扫描已有 `wiki/*.md`,根据关键术语和论点挂 `[[wikilink]]` 到已存在的页面。
5. 同名 slug 冲突时,文件名后追加 `-2`、`-3` 等后缀。

### 3.3 触发方式
- **单文件:** 用户在 CC 中说"处理 `raw/xxx.md`"或"处理这个",CC 处理该文件。
- **批量:** 用户说"处理 `raw/` 下所有未编译文件",CC 扫描 `raw/` 中尚未在 `wiki/` 有对应 slug 的文件,逐个处理。
- **不主动全量重编译:** 单文件粒度,避免 token 爆炸。如果用户明确说"重新编译 `raw/yyy.md`",CC 才覆盖对应 `wiki/yyy.md`。

### 3.4 不做的事
- 不维护全局索引页;Obsidian 图谱视图即索引。仅在 `wiki/` 积累到 30+ 页时,才让 CC 生成一次 `wiki/_index.md`。
- 不做向量化、不做问答接口。
- 不写"读后感"或主观评论。
- 不为单篇文章之外的资源(如图片、附件)做特殊处理——它们随所属文章一起被引用即可。

## 4. 关键约定

- **入库时间排序:** `raw/` 内文件按时间排,不分主题。主题由 wiki 侧的 `[[wikilink]]` 自然涌现。
- **slugs:** 文件名同名(去掉扩展名)优先;同名冲突追加 `-2`、`-3`。
- **链接格式:** Obsidian 内部链接 `[[页面名]]` 或 `[[页面名|显示文本]]`;不用 Markdown 普通链接。
- **Frontmatter:** 不强制。如果 CC 觉得需要(如记录源 URL、作者、阅读日期),可加 YAML frontmatter;不强制所有页面都加。
- **目录:** `wiki/` 起步就一个文件夹,不分主题子目录;50+ 页时再评估。

## 5. 版本控制

- `raw/` 和 `wiki/` 都进 git,原始资料和 wiki 资产都要可追溯。
- `.obsidian/` 不进 git(个人配置,跨机器无意义)。
- `.gitignore` 在 `knowledge-base/` 下单独维护。

## 6. 成功标准(可验证)

每条都要能在 Obsidian + CC 环境中跑通:

1. Obsidian 打开 `D:\Data\Desktop\rag\knowledge-base\`,文件树显示 `raw/` 和 `wiki/`。
2. 在 `raw/` 放一个测试文章,启动 CC 说"处理这个",`wiki/` 下生成对应 `<slug>.md`,页面含核心论点 + `[[...]]` 链接(允许 0 个,如果有第二篇文章再连)。
3. 在 `raw/` 放第二篇相关文章,处理后,第二篇 wiki 页里出现指向第一篇的 `[[wikilink]]`。
4. Obsidian 图谱视图能看到两个节点的连线。
5. `D:\Data\Desktop\rag\README.md` 包含 `knowledge-base/` 的定位说明。

## 7. 不在范围内

- 任何 Python 脚本、CLI 工具、CI 流水线(本方案纯对话驱动)。
- Graphify 路径。
- 与 `docs/`、`scrapers/`、`logs/` 内容的交叉引用。
- 自动化定时任务或文件监听(用 Obsidian 自身的 file watcher 即可)。
- 多用户 / 多设备同步(用 Obsidian 自己的同步方案,与本项目无关)。
