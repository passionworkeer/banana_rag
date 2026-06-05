使用CC搭建Karpathy（Obsidian）同款AI知识库，对比Graphify,RAG等知识库管理方案
好文章，好笔记都躺在自己没落的文件夹
想找又找不到，想找半年前读过的某个观点，翻遍笔记也找不到；

同样的概念在五篇笔记里都记过，但彼此没有关联；
每次问 AI 问题，它都要重新读一遍我的资料，之前聊过的理解没有留下来。

有没有一种方案能让自己的知识库有效连接起来，同时进化更新

本文我们复现一下前特斯拉高管卡帕西的知识管理方案，同时对比传统RAG,以及卡帕西应用Graphify知识图谱搭建

一文看懂三大知识库管理方案：RAG - 卡帕西（Obsidian LLM Wiki）- Graphify

图片


卡帕西（Obsidian LLM Wiki）
ClaudeCode + Obsidian + 卡帕西思想 = 无敌个人第二大脑


直接开始搭建卡帕西的 LLM Wiki 知识库，让 AI 帮你持续整理、学习和进化知识。

图片
搭建

1 下载obsidion

一个存在你电脑里的笔记软件;所有笔记都是本地Markdown文件;免费·离线·数据永远属于你
https://obsidian.md/

使用obsidion打开一个文件夹
示例：D:\mywork\self_obisidion

下载obsidion-skills(本文暂时没用)

为 Obsidian 开发代理技能。教会cc使用 Markdown、Base、JSON Canvas 和 CLI。
https://github.com/kepano/obsidian-skills

2 cc使用卡帕西方案构建

https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

进入此文件夹
claude --dangerously-skip-permissions

复制上面的卡帕西的内容，或者下载下来说

“按照这个方法帮我搭建知识库”

录入资料
1 手动将文件直接扔到raw下（任何形式的文件）
2 安装谷歌插件，Obsidian Web Clipper，一键导入知识库

能够一键将网页内容，油管视频，用markdown格式保存到obsidian

如果不行，你可安装cc浏览器插件或其他agent插件，提取网页内容

图片
编译一个wiki
将文件扔到raw，告诉AI“读取raw/中所有文件，编译为一个wiki”

打开obsidian的图谱视图，就是一个专属你的知识库

图片

图片
优势与局限

知识复利 ，是跟传统RAG最大的区别。

传统RAG:问→答→结束
LLM Wik:问→答→答案变成新知识→下次问得更准

适合100-200篇文章，几千篇就不适合了

token消耗

Ingest-一篇5000字的文档：大约消耗500tokens（包括生成摘要、更新相关页面)
Query一次：大约消耗7Oktokens

使用完卡帕西知识库，在来实验下一个卡帕西思想的具体项目
使用Graphify搭建个人知识图谱

知识图谱Graphify
图片
任何输入，一张图表，完全回忆。

将Andrej Karpathy提出的个人知识库工作流进行了产品化与图谱化实现

把分析工作一次性做完，把所有内容压缩成一张可查询的知识图谱，放到磁盘上。后续查询走图谱遍历，不再重新读取原始文件。在混合语料库上每次查询的 token 量降低 71.5 倍。

相关资料

AI编码助手技能（支持Claude Code、Codex、OpenCode、Cursor、Gemini CLI等）。将任何包含代码、SQL模式、R脚本、shell脚本、文档、论文、图像或视频的文件夹转换为可查询的知识图谱。应用代码+数据库模式+基础设施，尽在一个图中

官网：
https://graphifylabs.ai/
github:
github.com/safishamsi/graphify

启动
/graphify .# 可用于任意目录：代码库、笔记、论文都可以

安装与使用

要求： Python 3.10+

pip install graphifyy && graphify install

使用卡帕西博客为例 构建知识图谱
github.com/karpathy/karpathy.github.io

打开CC输入

/graphify ./karpathy.github.io

完成后会在当前目录 出现graphify-out

graphify-out/
├── graph.html   可交互图谱：可点节点、搜索、按社区过滤
├── GRAPH_REPORT.md  God nodes、意外连接、建议提问
├── graph.json   持久化图谱：数周后仍可查询，无需重新读原始文件
└── cache/  SHA256 缓存：重复运行时只处理变更过的文件

目前适合我们使用场景是‘快速熟悉新的项目代码’

在CC里对当前目录做标准分析

/graphify --deep 深度模式：更激进的关系推断
/graphify ./src/auth 处理特定子目录
/graphify --watch Watch 模式：文件变化时重建图谱
查询已有图谱
/graphify query "how does user authentication flow through the system?"
查找两个实体之间的最短路径
/graphify path "UserService" "DatabasePool"
用自然语言解释某个实体
 /graphify explain "PaymentProcessor

最后在简单说下传统的Rag

传统Rag
传统RAG的标准流程

1.数据准备：将企业私有数据(PDF,Word等)进行切片(Chunking)。
2.向量化：通过Embedding模型转化为向量，存入向量数据库（如Chroma,Faiss,,Milvus)。
3.检索：用户提问->向量化->在库中查找相似片段
4。生成：用户问题+检索到的片段>输入大模型->生成答案。

图片
在企业级应用中，传统RAG往往虽然跑通了，但有时候并不理想

致命痛点


1 检索相关性差(Retrieval Noise):
。问题：从向量库检索到的内容可能与用户意图根本不相关，或者虽然关键词匹配但语义不符。
。后果：大模型基于错误的信息生成答案，导致”一本正经地胡说八道”（幻觉）。
2 缺乏意图理解(Query Ambiguity）:
。问题：用户提问往往是不完整的、模糊的（例如：“那个报错怎么修？“），缺失了上下文。
。后果：传统RAG只能傻傻地拿这个模糊问题去检索，导致结果偏差极大。
3 无法处理复杂任务：
 面对需要多步准理(Multi-step reasoning)的问题，传统RAG是一次性流程，无法拆解任务。

解决：Agentic RAG （·问题·经过智能体决策重写后在走传统rag）

三大知识管理方案终极对比
最后我们用一个图表简单对比下

RAG vs 卡帕西 vs Graphify

图片


总之，建立一个个人知识库就用卡帕西
熟悉一个具体项目就用graphify，企业海量数据Rag

适合自己的就是最好的！！




暂无评论