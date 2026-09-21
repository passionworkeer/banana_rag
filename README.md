# RAG 探索项目

> **归档日期：2026-09-21。** 本项目停止主动维护，作为阶段性的 RAG 方法研究、知识库探索与抓取脚本记录公开保留。资料、依赖和目标网站行为可能已变化；欢迎 fork 后自行更新。第三方材料继续遵循其原有许可与使用条件。

汇集三类独立但相关的探索工作。

## 目录结构

| 主题 | 位置 | 说明 |
|------|------|------|
| 企业 RAG / 知识库研究 | `docs/enterprise-knowledge-base/` | 6 篇通用研究，覆盖架构、选型、权限治理与需求澄清。 |
| 通用研究笔记 | `docs/research/` | gpt-image 人脸限制、多账号防检测、天猫验证码等调研与汇总。 |
| 淘宝/Bananain 抓取脚本 | `scrapers/taobao-scraper/` | 三轮迭代的爬虫与公开商品抓取结果。最新:`taobao_scraper_round3.py`。 |
| 浏览器-MCP 抓取技能 | `scrapers/taobao-browser-scraper-skill/` | 自包含技能定义(`workflow.md` / `keywords.md` / `scripts/`),保留。 |
| RAG 方法论与推荐方案 | `docs/rag-methods/` | 13 个范式级方法 + 总览 + 推荐组合,见 [docs/rag-methods/00-rag-methods-overview.md](docs/rag-methods/00-rag-methods-overview.md)。 |

## 知识库 vault

`knowledge-base/` 是基于 Karpathy LLM Wiki 方案的**独立 Obsidian vault**，包含通用学习材料与对应摘要。用 Obsidian 打开该目录即可浏览 `raw/` 和 `wiki/`。详见 [knowledge-base/README.md](knowledge-base/README.md)。

## 抓取工作流

1. `scrapers/taobao-scraper/taobao_scraper.py`(Round 1)→ `data/taobao_bananain_products.{csv,json}`(51 条)
2. `scrapers/taobao-scraper/taobao_scraper_advanced.py`(Round 2)→ `data/taobao_bananain_products_full.{csv,json}`
3. `scrapers/taobao-scraper/taobao_scraper_round3.py`(Round 3)→ 关键词扩展再写回 `data/taobao_bananain_products_full.*`
4. `scrapers/taobao-browser-scraper-skill/scripts/merge_and_save.py`→ `data/taobao_bananain_products_browser.*`(1223 条,`source=browser`)

## 备注

- 当前归档中，Round 1 CSV/JSON 各 51 条，`full.csv` 为 1192 条，`full.json` 与 browser CSV/JSON 各 1223 条；这些文件保留各自采集阶段的记录。
- 商品链接保留 `id` 与适用的 `skuId`。`full.csv` 中 8 条记录只有广告跟踪跳转地址，`link` 留空，其他字段保留。
- Python 脚本按各自依赖运行，仓库未统一配置包管理。
- 重复数据集保留(Round 1 51 条 ⊂ Round 3 1223 条),用文件名区分
- 脚本内硬编码路径已改为基于 `__file__` 的相对路径,可从 `scrapers/taobao-scraper/` 直接运行
