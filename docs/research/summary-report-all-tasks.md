# 三项调研任务执行报告

> 执行日期：2026-06-04
> 基于原始调研文档：research-notes-ai-image-captcha-tmall.md（2026-06-03）

---

## 任务一：GPT Image API 人脸限制 — 深度补充调研

### 执行状态：已完成

### 核心发现

**gpt-image-2（2026年4月21日发布）的改进与局限**：gpt-image-2 在图像质量上有重大升级（原生 4K 分辨率、多图角色一致性），审核框架继承了 gpt-image-1，误杀率有所降低，但真人肖像生成的核心限制仍未根本解决。

**社区 Workaround 效果排名**：GPT + ComfyUI 后处理（FaceDetailer/InstantID）成功率最高；Mask 编辑模式绕过全图审核次之；提示词重写（避免人名，用视觉特征描述）和 `moderation=low` 参数设置效果中等。

**替代方案对比结论**：
- 人脸生成写实度：FLUX.1 Dev/FLUX.2 > GPT Image 2 > Midjourney V8
- 身份保持能力：ComfyUI 管线（PuLID+InstantID+FaceDetailer）> FLUX.1+PuLID-FLUX > SD XL+IP-Adapter FaceID
- 商业级推荐技术栈：FLUX.1 Dev + PuLID-FLUX + ComfyUI（AI 写真服务）；InsightFace + ReActor + FaceDetailer（人脸替换服务）；fal.ai/Replicate 托管方案（低成本快速上线）

**OpenAI 政策趋势**：总体"精准化"而非简单的放松或加严——虚构人物和创意场景逐步放松，真实人物和潜在有害场景持续严格。

### 产出文件

- 详细报告：`gpt-image-face-research-update.md`（27KB）

---

## 任务二：多账号反检测浏览器方案 + browser-act Skills 安装

### 执行状态：已完成

### A. browser-act Skills 安装结果

| 步骤 | 状态 | 说明 |
|------|------|------|
| CLI 安装 | 成功 | `browser-act-cli v0.1.25`，通过清华 PyPI 镜像安装 |
| browser-act Skill | 已安装 | 复制到 `~/.qoderwork/skills/browser-act/SKILL.md` |
| browser-act-skill-forge Skill | 已安装 | 复制到 `~/.qoderwork/skills/browser-act-skill-forge/SKILL.md` |
| 预构建 Solutions | 已备份 | 52 个预构建 Skills 复制到 `~/.qoderwork/skills/browser-act-solutions/` |
| 核心指南加载 | 成功 | `get-skills core` 和 `get-skills advanced` 均可正常加载 |
| Chrome Profile 检测 | 成功 | 发现 1 个可导入的本地 Chrome Profile |
| stealth-extract 测试 | 失败 | 需要下载浏览器包，SSL 连接被阻断（网络环境限制） |
| API Key 配置 | 未配置 | stealth 模式需要注册获取 API Key |

**browser-act 三种浏览器模式总结**：

| 模式 | 特点 | 适用场景 | 需要 API Key |
|------|------|----------|-------------|
| chrome | 导入本地 Chrome 登录态，独立运行 | 复用已登录状态、并行操作同账号多页面 | 否 |
| chrome-direct | 直接控制运行中的 Chrome | 需要扩展/证书/SSO 等不可导出配置 | 否 |
| stealth | 反检测浏览器，指纹伪装+代理轮换 | 多账号隔离、突破反爬、批量采集 | 是 |

**多账号架构关键设计**：每个账号一个独立浏览器实例，具备独立的 Cookie/Session、浏览器指纹、代理 IP。browser-act 的 stealth 固定身份模式（每浏览器绑定专属静态代理）是实现多账号长期管理的最佳方案。

### B. 多账号反检测浏览器调研结果

**商业产品对比**：

| 产品 | 价格区间 | 核心优势 | 适用场景 |
|------|----------|----------|----------|
| Multilogin | $10-99+/月 | 行业标杆，50+指纹参数，内置住宅代理 | 高端需求 |
| AdsPower | $9/月起 | 中国市场领先，RPA+Local API 自动化最强 | 国内电商运营 |
| GoLogin | $24-99/月 | Enterprise 计划性价比最高 | 大规模账号管理 |
| Dolphin{anty} | $10-299/月 | 免费5个profiles，团队协作友好 | 入门评估 |

**开源方案推荐**：camoufox（Firefox 反检测，C++ 源码级指纹注入）+ Playwright + 静态住宅代理。这是 2025-2026 年最具价值的开源方案：JS 无法检测指纹伪装、AI Agent 原生支持、<200MB 轻量级。

**2026 年指纹检测新趋势**：TLS/JA4 指纹和 HTTP/2 指纹已超越 JS 层信号成为最持久的检测手段；User-Agent 字符串已被 Client Hints 取代；WebGL 渲染器仍是 JS 层最强信号。

### 产出文件

- 详细报告：`multi-account-anti-detection-research.md`（42KB）

---

## 任务三：天猫/淘宝蕉内商品数据实操抓取

### 执行状态：已完成（含 3 轮扩展抓取）

### 最终抓取统计

经过 3 轮迭代抓取，从最初的 51 个商品扩展到 **1192 个唯一商品**。

| 轮次 | 策略 | 新增商品 | 累计总数 | 说明 |
|------|------|----------|----------|------|
| 第一轮 | 基础分页（第1-5页） | 51 | 51 | Playwright + Chromium headless |
| 第二轮 | 多策略突破 | 134 | 185 | 每页独立上下文、s.taobao.com、mobile UA、滚动加载、6个关键词变体 |
| 第三轮 | 关键词矩阵（51个品类词） | 1007 | **1192** | 每个品类词独立搜索1-3页，覆盖蕉内全品类 |

### 最终数据概览

| 指标 | 数值 |
|------|------|
| **唯一商品总数** | **1192** |
| 唯一 item_id 数 | 1189 |
| 有价格数据商品 | 1192（100%） |
| 价格范围 | ¥1.60 - ¥2026.00 |
| 平均价格 | ¥358.50 |
| 总耗时 | 约 30 分钟（3 轮累计） |

### 品类分布

| 品类 | 商品数 |
|------|--------|
| 家居服/睡衣 | 211 |
| T恤/上衣 | 170 |
| 裤子 | 168 |
| 内裤 | 152 |
| 内衣/文胸 | 118 |
| 袜子 | 107 |
| 家居用品（被子/凉席/毛巾） | 95 |
| 外套（夹克/防晒衣） | 47 |
| 连衣裙/裙装 | 35 |
| 保暖 | 34 |
| 运动/瑜伽 | 15 |
| 儿童 | 9 |
| 其他 | 31 |

### 店铺分布

| 店铺 | 商品数 |
|------|--------|
| Bananain蕉内旗舰店 | 1127（94.5%） |
| Bananain蕉内奥莱店 | 58 |
| 其他店铺 | 7 |

### 各策略效果分析

**第一轮（基础分页）**：对 `uland.taobao.com/sem/tbsearch` 做标准分页抓取，第1-5页每页约45条商品，去重后51个。

**第二轮（多策略突破）**：
- 策略A（每页独立浏览器上下文）：第6页新增12个，第7-9页撞到登录墙
- 策略B（s.taobao.com）：0新增（需要登录或页面结构不同）
- 策略C（Mobile UA）：0新增（移动端页面不返回可提取数据）
- 策略D（页面滚动加载）：0新增（该页面不做无限滚动）
- 策略E（关键词变体）：**+134 新增**（蕉内防晒+34, 蕉内袜子+30, 蕉内家居服+29, 蕉内内裤+18, 蕉内旗舰店+7, Bananain蕉内+4）

**第三轮（关键词矩阵）**：使用 51 个品类关键词（涵盖内裤、袜子、家居服、内衣、T恤、裤子、外套、被子、凉席、毛巾、儿童、运动等全品类），每个词搜索1-3页。50/51 个关键词成功产出新数据，**+1007 新增**。最高产关键词：蕉内卫衣(+41)、蕉内凉席(+41)、蕉内被子(+40)、蕉内拖鞋(+39)、蕉内儿童(+37)。

### 遇到的限制及应对

| 限制 | 表现 | 应对结果 |
|------|------|----------|
| 分页登录墙 | 第7页起重定向到登录页 | 关键词变体策略完全绕过 |
| s.taobao.com 不可用 | 返回0数据 | 切换到 SEM 入口成功 |
| 移动端不可用 | 页面结构不兼容 | 放弃移动端，专注 PC 端 |
| 跨页商品重复 | 同一商品不同URL参数 | item_id 去重解决 |
| 无验证码/风控 | 关键词搜索未触发风控 | 幸运/低频访问策略有效 |

### 技术实现

三轮抓取均使用 Playwright sync API + Chromium headless 模式，反检测措施包括：移除 `navigator.webdriver` 标记、模拟 Chrome 指纹、UA 轮换、每请求独立浏览器上下文、随机等待 3-8 秒。提取层采用 JS DOM 遍历 + 多选择器降级策略。

### 产出文件

| 文件 | 格式 | 大小 | 说明 |
|------|------|------|------|
| `taobao_scraper.py` | Python | 23KB | 第一轮基础抓取脚本 |
| `taobao_scraper_advanced.py` | Python | 20KB | 第二轮多策略突破脚本 |
| `taobao_scraper_round3.py` | Python | 8KB | 第三轮关键词矩阵脚本 |
| `taobao_bananain_products.csv` | CSV | 25KB | 第一轮数据（51条，已保留） |
| `taobao_bananain_products.json` | JSON | 31KB | 第一轮数据（51条，已保留） |
| `taobao_bananain_products_full.csv` | CSV | 708KB | **最终完整数据（1192条）** |
| `taobao_bananain_products_full.json` | JSON | 832KB | **最终完整数据（1192条）** |

---

## 所有产出文件清单

```
D:\Data\Desktop\rag\
├── research-notes-ai-image-captcha-tmall.md    # 原始调研文档（2026-06-03）
├── gpt-image-face-research-update.md           # 任务一：GPT Image 人脸限制深度调研（27KB）
├── multi-account-anti-detection-research.md    # 任务二：多账号反检测浏览器调研（42KB）
├── summary-report-all-tasks.md                 # 本报告：三项任务汇总
├── taobao_scraper.py                           # 任务三：第一轮基础抓取脚本
├── taobao_scraper_advanced.py                  # 任务三：第二轮多策略突破脚本
├── taobao_scraper_round3.py                    # 任务三：第三轮关键词矩阵脚本
├── taobao_bananain_products.csv                # 任务三：第一轮数据（51条）
├── taobao_bananain_products.json               # 任务三：第一轮数据（51条）
├── taobao_bananain_products_full.csv           # 任务三：最终完整数据（1192条）
├── taobao_bananain_products_full.json          # 任务三：最终完整数据（1192条）
└── scraper_advanced.log                        # 第二轮抓取日志
```

## 后续建议

**任务一后续**：如果核心业务依赖高保真人脸编辑，建议优先评估 FLUX.1 + ComfyUI 管线；短期内对 GPT Image 使用 `moderation=low` + 优化 prompt 降低误杀率。

**任务二后续**：browser-act CLI 已成功安装，Skills 已就位。要启用 stealth 模式（反检测浏览器），需要先完成 API Key 注册（`browser-act auth login`）。建议先在 chrome 模式下验证基本流程，再升级到 stealth 模式做多账号隔离。

**任务三后续**：当前 1192 个商品数据已覆盖蕉内品牌的主要品类。如需进一步扩展，可以考虑：增加更多品类关键词（如"蕉内泳衣"、"蕉内口罩"等）；对已抓取商品访问详情页提取 SKU/规格/评论等深度数据；申请淘宝开放平台 API 获取更完整的结构化数据。三个抓取脚本均可直接修改参数复用。
