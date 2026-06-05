# RAG 探索项目

汇集三类独立但相关的探索工作。

## 目录结构

| 主题 | 位置 | 说明 |
|------|------|------|
| 企业 RAG / 知识库研究 | `docs/enterprise-knowledge-base/` | Bananain 公司相关,11 篇编号研究 + 7 个子方案。结构完整,不动。 |
| 通用研究笔记 | `docs/research/` | gpt-image 人脸限制、多账号防检测、天猫验证码等调研与汇总。 |
| 淘宝/Bananain 抓取脚本 | `scrapers/taobao-scraper/` | 三轮迭代的爬虫、数据、日志、截图。最新:`taobao_scraper_round3.py`。 |
| 浏览器-MCP 抓取技能 | `scrapers/taobao-browser-scraper-skill/` | 自包含技能定义(`workflow.md` / `keywords.md` / `scripts/`),保留。 |
| 抓取调试日志 | `logs/playwright-cli-2026-06-03/` | 2026-06-03 Playwright 控制台与页面快照归档。 |
| RAG 方法论与推荐方案 | `docs/rag-methods/` | 13 个范式级方法 + 总览 + 推荐组合,见 [docs/rag-methods/00-rag-methods-overview.md](docs/rag-methods/00-rag-methods-overview.md)。 |

## 抓取工作流

1. `scrapers/taobao-scraper/taobao_scraper.py`(Round 1)→ `data/taobao_bananain_products.{csv,json}`(51 条)
2. `scrapers/taobao-scraper/taobao_scraper_advanced.py`(Round 2)→ `data/taobao_bananain_products_full.{csv,json}`(1223 条,`source=script`)
3. `scrapers/taobao-scraper/taobao_scraper_round3.py`(Round 3)→ 关键词扩展再写回 `data/taobao_bananain_products_full.*`
4. `scrapers/taobao-browser-scraper-skill/scripts/merge_and_save.py`→ `data/taobao_bananain_products_browser.*`(1223 条,`source=browser`)

## 备注

- 无 git / 无包管理
- 重复数据集保留(Round 1 51 条 ⊂ Round 3 1223 条),用文件名区分
- 脚本内硬编码路径已改为基于 `__file__` 的相对路径,可从 `scrapers/taobao-scraper/` 直接运行
