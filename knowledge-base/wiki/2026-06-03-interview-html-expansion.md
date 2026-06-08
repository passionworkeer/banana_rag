# 2026-06-03 面试 HTML 知识页扩展实施计划

## 核心论点

本计划基于 [[2026-06-03-interview-html-expansion-design]] 的设计稿,目标是在 [[html-README]] 中新增 13 个知识页(6 面试首期 + 7 学习资源),更新首页和 README,保持与 transformer.html 严格一致的视觉风格。架构上严格复用 :root CSS 变量、组件类、SVG 风格和五区结构(Hero / 原理+图+公式 / 落地 / FAQ),全部为纯静态无外部 JS,每页 400-600 行中深度。

**实施策略** 按"先建样板 → 批量复制 → 填充内容"三步走:Task 0 复制 transformer.html 为 mcp.html 作为基线模板;Task 1-6 完成 6 面试首期(mcp/memory/lora/kv-cache/react-cot/multi-agent);Task 7-13 完成 7 学习资源(rerank/embedding/llm-cache/model-distributed/skill/tool-use/llm-tuning);Task 14 更新 index.html 加"🎯 首期专项"和"📖 学习资源"两个新区;Task 15 更新 README.md;Task 16 追加 29 题原始题到 mianshi.md;Task 17 commit + push。

每页严格遵循的骨架:hero(eyebrow + h1 + lead + pillrow 4-5 个标签)、grid 5 张 card(原理 full + SVG svgbox + 公式 mathbox + 落地 full + FAQ full qa 双栏 5-8 个 Q&A)。视觉规则:不引外部 JS、不写死 hex 色值、必须用 CSS 变量(--accent: #2563eb、--accent-soft: #dbeafe、--radius: 18px、--shadow: 0 10px 30px rgba(15,23,42,.08))。风险:风格漂移(缓解:先小修改 transformer.html 确认风格再批量)、内容不准(缓解:参考现有 Markdown 题库不编造线上数据)、首页过长(缓解:新区用 4-3 卡片网格)、完成时间(13 页 × 500 行 = 6500+ 行手写 HTML)。验收标准:13 个新 HTML 文件存在且标题正确、能从首页跳转、CSS 变量与组件类与 transformer.html 一致、每页有 hero/原理/流程图或公式/落地/FAQ 至少 4 区、commit + push 成功。

## 关键术语

- 模板复用
- 五区结构
- CSS 变量
- SVG 内联
- 首页更新
- 蕉内案例
- FAQ 双栏
- 风格一致
- 不引外部 JS
- commit + push

## 跨资料连接

- [[2026-06-03-interview-html-expansion-design]] — 本实施计划对应的设计稿。
- [[html-README]] — 目标目录入口。
- [[interview-README]] — 面试题库总览。
- [[mianshi]] — 本计划 Task 16 要追加 29 题的位置。
- [[00-答题规范与公式速查]] — 配套的 Markdown 答题骨架。
