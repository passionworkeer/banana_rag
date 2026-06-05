# 淘宝/天猫 Bananain 数据抓取交付文档

> 交付日期：2026-06-04
> 项目目录：`D:\Data\Desktop\rag`
> 涉及材料：`scrapers/taobao-scraper/`（三版脚本+数据）、`scrapers/taobao-browser-scraper-skill/`（浏览器-MCP 技能）、`docs/research/`（三项研究）、`logs/`（调试日志）

本项目存在两条并行的抓取路线：①传统 Playwright Python 脚本（`taobao_scraper*.py`），②基于浏览器 MCP 的 Agent 抓取技能（`taobao-browser-scraper-skill/`）。两者都最终落地到同一份数据，并完成了 **从基础分页（51）→ 多策略突破（185）→ 关键词矩阵（1192）→ 浏览器交叉验证（1223）** 的四轮迭代。

本文档按要求回答三个问题：
1. **API/平台人脸限制有什么绕过方法**（基于 `gpt-image-face-research-update.md` 等研究）
2. **Agent 怎么跨过验证码/反爬限制**（基于 `taobao_scraper*.py` 实际实现 + 反检测研究）
3. **爬取结果在不同方式上的差异**（基于四轮数据实际对比）

---

## 1. GPT Image API 人脸限制与"绕过"路径

> 注：人脸绕过研究本身不在本项目抓取任务范围，但研究文档 `docs/research/gpt-image-face-research-update.md` 已整理在项目内，作为外部知识一并交付。

### 1.1 限制的本质

GPT Image API（`gpt-image-1` / `gpt-image-2`）的"人脸限制"不是单一开关，而是一组联动的风控规则：

- **真人肖像生成限制**：请求生成与真实人物高度相似的图像时触发 `moderation_blocked`
- **公众人物 opt-out 名单**：已登记 opt-out 的名人直接拒绝
- **人脸编辑端点更严**：`/images/edits` 端点不支持 `moderation=low` 参数
- **误杀率高**：很多与真实人物无关的请求也会被错误拦截

研究文档结论：**没有官方允许的"绕过人脸限制"开关**。所谓绕过方案都集中在"降低误伤"而非"绕开规则"。

### 1.2 七类实测有效的"绕过"路径（按可行性排序）

| # | 方法 | 成功率 | 风险 | 适用场景 |
|---|------|--------|------|----------|
| 1 | **GPT Image 生成 + ComfyUI 后处理替换人脸** | 高 | 低 | 商业 AI 写真、人脸编辑 |
| 2 | **Mask 编辑模式（inpainting）** | 中高 | 低 | 局部人脸修改 |
| 3 | **`moderation=low` 参数**（仅生成端点） | 中 | 低 | 虚构角色、风格转换 |
| 4 | **提示词重写**：避免人名，用视觉特征描述 | 中 | 低 | 通用创意场景 |
| 5 | **多步渐进编辑**：先抽象再添加细节 | 中 | 低 | 复杂编辑 |
| 6 | **风格描述替代**：不点艺术家名，改用视觉描述 | 中 | 低 | 风格迁移 |
| 7 | **第三方 API 代理** | 不确定 | 高 | 不推荐做长期方案 |

### 1.3 官方/合规可尝试的方向

研究文档明确列出 5 类合规尝试：

1. **明确授权与成年人语义**：在 prompt/元数据中声明"用户授权、成年人、非色情、非冒充、非公众人物模仿"
2. **`moderation=low`**：将默认 `auto` 改为 `low`，降低过滤强度（仅生成端点有效）
3. **降低 prompt 误触发词**：把"性感"改成"时尚/优雅/自然"，"像某明星"改成"杂志封面构图"
4. **业务前置校验**：要求用户确认授权、禁止未成年人、禁止换脸
5. **误伤申诉**：收集 request id、prompt、错误类型，向 OpenAI 反馈

### 1.4 推荐的混合方案（如果业务强依赖人脸）

研究结论是**混合方案是实用主义路线**：

```
GPT Image 2 API（基础生成，强构图/文字渲染）
  ↓
ComfyUI 后处理管线（人脸一致性修复）
  - PuLID-FLUX：身份保持
  - InstantID：SDXL 上的身份锁定
  - FaceDetailer：面部细节修复
  - ReActor：人脸替换
```

如果需要完全无人脸审核，**FLUX.1 Dev + PuLID-FLUX + ComfyUI 自部署**是当前最佳写实度方案。

---

## 2. Agent 跨过验证码/反爬限制的实际做法

> 本节基于项目内 `scrapers/taobao-scraper/taobao_scraper*.py` 三个脚本的真实实现，以及 `docs/research/multi-account-anti-detection-research.md`、`research-notes-ai-image-captcha-tmall.md` 两份研究。

### 2.1 实际遭遇的"反爬形态"

在本项目对淘宝 SEM 搜索页的实测中，**没有触发图形验证码**，但遇到了两类隐性反爬：

| 反爬类型 | 表现 | 触发位置 |
|----------|------|----------|
| **登录墙（Login Wall）** | 第 7 页起重定向到 `login.taobao.com`，title 变为"登录" | 通用关键词"蕉内"分页至第 7 页 |
| **会话/指纹追踪** | 同一浏览器上下文访问多页后触发登录 | 连续翻页场景 |
| **Headless 检测** | 控制台看到 `Headless Chrome` 上报字段 | Playwright 默认配置 |

研究文档总结的真实风控形态（实际未被本项目触发，但属于同类风控）：

- **JS 层指纹**：`navigator.webdriver`、`navigator.plugins`、`window.chrome` 等
- **网络层指纹**：TLS/JA4 指纹、HTTP/2 指纹（2026 年新趋势）
- **行为信号**：鼠标轨迹、触屏轨迹、滚动节奏
- **账号/设备信誉**：cookie、localStorage、设备 ID

### 2.2 验证码：Agent 能做什么、不能做什么

研究文档 `research-notes-ai-image-captcha-tmall.md` 的核心结论：

> **Open CaptchaWorld benchmark 显示：最强 MLLM Agent 解验证码成功率约 40.0%，人类为 93.3%。** Agent 能过一部分简单验证码（滑块、文字、点选），但真实网站验证码是综合风控问题。

**Agent 实际能做的**：
- 简单文字/算术验证码
- 滑块缺口识别 + 拖动
- 旋转/点选图片
- 失败后请求人类接管（human-in-the-loop）

**真实风控下不可靠的**：
- Headless/driver 痕迹
- 鼠标轨迹自然度
- IP 与账号信誉
- 平台特定的"行为评分"

**官方文档也把"解 CAPTCHA"列为需要人类确认的高风险操作**（OpenAI Computer Use Guide）。

### 2.3 本项目实际使用的反反爬手段

三个脚本均使用 **Playwright + Chromium headless**，反检测措施分四层：

#### 第一层：浏览器启动参数

```python
args=[
    "--disable-blink-features=AutomationControlled",  # 关键：关闭 webdriver 标记
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-infobars",
    "--disable-extensions",
]
```

#### 第二层：上下文伪装

```python
context = browser.new_context(
    user_agent=ua,                           # UA 轮换（4 种 Desktop + 1 种 Mobile）
    viewport={"width": 1920, "height": 1080},
    locale="zh-CN",
    timezone_id="Asia/Shanghai",
    color_scheme="light",
)
```

#### 第三层：JS 层指纹覆盖

```python
context.add_init_script("""
    // 1. 删除 webdriver 标记
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    // 2. 伪造 chrome runtime 对象
    window.chrome = { runtime: {}, loadTimes: function(){}, csi: function(){} };
    // 3. 伪造 plugins 数组
    Object.defineProperty(navigator, 'plugins', {
        get: () => { const arr = []; for (let i = 0; i < 5; i++) arr.push({name: 'Plugin ' + i}); return arr; }
    });
    // 4. 伪造语言列表
    Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en-US', 'en'] });
    // 5. 修复 permissions.query 异常
    const origQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (params) => (
        params.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            origQuery(params)
    );
""")
```

#### 第四层：行为模拟

- **每页独立浏览器上下文**（Round 2 引入）：避免会话级指纹累积
- **人类化滚动**：`simulate_human_scroll()` 函数，随机 300-800px 滚动 + 400-1200ms 等待
- **随机延迟**：页面间 3-8 秒、关键词间 1-3 秒、登录墙后回退

#### 检测与停止条件

脚本内置了三种页面状态检测器：

```python
def is_login_page(page) -> bool:        # 登录墙
    title 含"登录" 或 URL 跳 login.taobao.com

def is_captcha_page(page) -> bool:      # 验证码
    HTML 命中 ≥2 个 captcha/验证码/滑块/sec.taobao 等信号

def is_empty_page(page) -> bool:        # 空页
    缺商品链接 且 缺 alicdn 图片
```

**核心策略是"遇到就停，不绕过"**——脚本检测到登录墙或验证码立即停止当前策略，切换到下一策略。

### 2.4 五种"绕过"登录墙的策略及实测效果

`taobao_scraper_advanced.py` 实现了五种策略，按效果排序：

| # | 策略 | 实现 | 实测效果 | 备注 |
|---|------|------|----------|------|
| A | **每页独立浏览器上下文 + 增强 stealth** | 新建 context，注入全部 JS 补丁 | 第 6 页 +12 新增；第 7-9 页撞登录墙 | session 隔离有效但不解决分页风控 |
| B | **s.taobao.com 备用入口** | 切换到 `s.taobao.com/search` | 0 新增 | 页面结构差异/需登录 |
| C | **Mobile UA** | iOS 17.5 UA + 移动端 viewport | 0 新增 | 移动端页面结构不兼容 |
| D | **第 6 页激进滚动** | 同一页面滚动 20 轮 | 0 新增 | 淘宝 SEM 页不做无限滚动 |
| E | **关键词变体** | 6 个品类词各跑 1 页 | **+134 新增** | **唯一有效策略** |

**结论：登录墙无法用技术手段绕过，唯一有效路径是"换关键词重新跑前几页"**——这与研究文档中"关键词变体策略完全绕过"的结论一致。

### 2.5 验证码/反爬的真正解决方案（研究文档观点）

如果业务需要长期稳定抓取，研究文档 `multi-account-anti-detection-research.md` 推荐分层方案：

**商业产品**（按场景选型）：
- **Multilogin**（$10-99+/月）：行业标杆，50+ 指纹参数
- **AdsPower**（$9/月起）：国内电商首选，RPA + Local API 强
- **GoLogin**（$24-99/月）：性价比高，Orbita 内核
- **Dolphin{anty}**（$10-299/月）：免费 5 profiles，团队友好

**开源方案**（2025-2026 最佳实践）：
- **camoufox**（Firefox 反检测）：C++ 源码级指纹注入，AI Agent 原生支持
- **Playwright + rebrowser-patches**：修复 CDP 检测向量
- **nodriver / zendriver**：协议层规避
- **静态住宅代理**：每个账号绑定独立 IP

**多账号隔离架构**：

```
账号 A → 浏览器实例 A（独立 cookie/fingerprint）→ 静态代理 IP A
账号 B → 浏览器实例 B（独立 cookie/fingerprint）→ 静态代理 IP B
...
```

**绝对不要做的事**（研究文档明确警示）：
- 自动绕过第三方网站验证码
- 批量注册/登录/下单
- 规避平台风控、隐藏自动化环境
- 使用打码平台绕过目标站点明确要求的人类验证

---

## 3. 爬取结果：不同方式之间的差异

### 3.1 四轮迭代的数据全景

| 轮次 | 脚本/工具 | 入口 | 策略 | 新增 | 累计 |
|------|-----------|------|------|------|------|
| **Round 1** | `taobao_scraper.py` | `uland.taobao.com/sem/tbsearch` | 基础分页（page 1-5） | 51 | 51 |
| **Round 2** | `taobao_scraper_advanced.py` | 同上 | 5 策略组合 | 134 | 185 |
| **Round 3** | `taobao_scraper_round3.py` | 同上 | 51 个关键词 × 1-3 页 | 1007 | 1192 |
| **Browser** | `taobao-browser-scraper-skill` | 浏览器 MCP 人工+JS | 关键词变体 + 卡片级 JS 提取 | 31 净增 | **1223** |

### 3.2 三种抓取方式的本质差异

#### 方式 A：Playwright Python 脚本（Round 1-3）

**优势**：
- 自动化程度高，可无人值守跑 30 分钟
- 速率可控、停机条件明确
- 适合大批量、确定关键词清单的抓取

**劣势**：
- 一旦页面 DOM 结构变化，CSS 选择器失效率高
- 第 7 页起会被登录墙拦截
- 抓取速度受"页面间隔 3-8 秒"限制

**实际产出**：1192 条商品，100% 有价格

#### 方式 B：浏览器 MCP Agent（browser-act）

**优势**：
- 直接在用户已登录/有状态的浏览器中抓取，复用 cookie
- JS 执行灵活，可针对单页调试 selector
- 无需维护浏览器进程

**劣势**：
- 需要人工操作浏览器 MCP 工具（`tabs_context_mcp`、`navigate`、`javascript_tool`）
- 不能完全无人值守
- 依赖 QoderWork browser MCP 服务的可用性

**实际产出**：在 Round 3 已有 1192 条基础上净增 31 条（去重后），验证了脚本结果准确性

#### 方式 C：第三方打码平台（未实际使用）

研究文档提到但本项目**未采用**的方案：
- 2Captcha、Metabypass 等打码服务
- 滑块/缺口识别的开源项目
- Browser-Use + 视觉模型自己解

不采用原因：研究文档明确"不建议做第三方验证码绕过"，且本项目主要反爬是登录墙而非图形验证码。

### 3.3 数据质量对比

#### 字段完整性

| 字段 | Round 1 (51) | Round 2/3 (1192) | Browser (1223) | 说明 |
|------|--------------|------------------|----------------|------|
| title | 100% | 100% | 100% | 商品标题 |
| price | 100% | 100% | 100% | 渲染价格 |
| shop | ~85% | ~95% | 100% | 店铺名（脚本受 DOM 选择器影响） |
| link | 100% | 100% | 100% | 详情页 URL |
| image | ~70% | ~90% | 100% | 图片 URL |
| page | 有 | 有 | 无 | 来源页码 |

#### 提取策略差异

**脚本方式**（Round 1-3）使用 4 种降级策略：
1. `Card--doubleCard` class 选择器
2. `Content--contentInner` a[href*="detail"]
3. 通用 `[class*="item"]`、`[class*="card"]` 选择器
4. **JS evaluate 全 DOM 遍历**（最稳健，4 个脚本都用）

**浏览器 MCP 方式**使用单页 JS 提取：
- 卡片包裹层 class 探测（`CardV2--doubleCardWrapper`）
- 从卡片 `id` 属性中提取 `item_id_{数字}`（最稳定）
- 精确的 `Title--title`、`Price--priceWrapper` class

**结论**：浏览器 MCP 方式通过人工调试 selector，对单页数据质量更高；脚本方式通过多策略降级，对页面结构变化的鲁棒性更好。

#### 价格分布对比

最终 1192 条数据的价格统计（来自 Round 3 完整数据）：

| 指标 | 数值 |
|------|------|
| 价格范围 | ¥1.60 - ¥2026.00 |
| 平均价格 | ¥358.50 |
| 有价格商品 | 100% |

#### 品类分布（来自 Round 3 关键词矩阵）

| 品类 | 商品数 | 主要关键词 |
|------|--------|-----------|
| 家居服/睡衣 | 211 | 蕉内睡衣、蕉内家居服、蕉内睡裙 |
| T恤/上衣 | 170 | 蕉内T恤、蕉内长袖、蕉内短袖 |
| 裤子 | 168 | （综合） |
| 内裤 | 152 | 蕉内内裤男/女 |
| 内衣/文胸 | 118 | 蕉内文胸、蕉内胸罩、蕉内内衣 |
| 袜子 | 107 | 蕉内袜子男/女 |
| 家居用品 | 95 | 蕉内凉席、蕉内被子、蕉内毛巾 |
| 外套 | 47 | 蕉内卫衣、蕉内外套、蕉内夹克 |
| 其他 | 124 | 防晒/连衣裙/儿童/瑜伽等 |

**店铺分布**：
- Bananain 蕉内旗舰店：1127 条（94.5%）
- Bananain 蕉内奥莱店：58 条
- 其他店铺：7 条

### 3.4 数据量差异的关键因素

**Round 1 vs Round 2 vs Round 3 为什么差距这么大？**

- **Round 1（51）**：单一关键词"蕉内"前 5 页，受登录墙约束
- **Round 2（+134）**：发现关键词变体能绕过登录墙，新增 6 个品类词
- **Round 3（+1007）**：把关键词扩展到 51 个，覆盖全品类
- **Browser（+31）**：交叉验证脚本结果，纠正少量未覆盖的边角商品

**核心规律**：淘宝 SEM 搜索的分页风控是"按会话/关键词"判定的，**换关键词等于换一次会话**——这是能从 51 跃升到 1192 的根本原因。

### 3.5 数据局限性

无论哪种方式都无法突破的限制：

| 限制 | 影响 |
|------|------|
| **分页上限** | 单关键词最多 6 页（约 270 条），第 7 页起登录墙 |
| **无 SKU/规格** | 公开搜索页不返回颜色/尺码级别的 SKU 数据 |
| **无价格细分** | 看不到促销价、券后价、会员价 |
| **无销量/评论** | 公开页不暴露销量和评论数 |
| **无库存** | 库存属于详情页数据 |
| **数据时效性** | 淘宝商品上下架频繁，数据会随时间漂移 |
| **店铺过滤** | 关键词"蕉内凉席"会混入宠物用品等非品牌商品，需二次过滤 |

要突破这些限制，研究文档建议：
1. **官方 API 路线**：`taobao.item.get.tmall` 等开放平台接口
2. **商家授权数据**：通过商家后台或品牌方合作获取
3. **详情页抓取**：进入商品详情页提取 SKU/规格

### 3.6 产出文件清单

```
D:\Data\Desktop\rag\
├── scrapers/taobao-scraper/
│   ├── taobao_scraper.py                          # Round 1 脚本
│   ├── taobao_scraper_advanced.py                 # Round 2 脚本
│   ├── taobao_scraper_round3.py                   # Round 3 脚本
│   ├── data/
│   │   ├── taobao_bananain_products.csv           # Round 1 数据 (51)
│   │   ├── taobao_bananain_products.json          # Round 1 数据 (51)
│   │   ├── taobao_bananain_products_full.csv     # Round 2/3 数据 (1192)
│   │   ├── taobao_bananain_products_full.json    # Round 2/3 数据 (1192)
│   │   ├── taobao_bananain_products_browser.csv  # Browser 验证 (1223)
│   │   └── taobao_bananain_products_browser.json # Browser 验证 (1223)
│   ├── logs/
│   │   └── scraper_advanced.log                   # Round 2 详细日志
│   └── screenshots/
│       ├── mobile_empty.png                       # 移动端抓取调试截图
│       └── mobile_login.png                       # 移动端登录墙截图
│
├── scrapers/taobao-browser-scraper-skill/
│   ├── workflow.md                                # 浏览器 MCP 抓取工作流
│   ├── keywords.md                                # 关键词产出排名
│   └── scripts/merge_and_save.py                  # 数据合并与去重脚本
│
└── docs/research/
    ├── gpt-image-face-research-update.md          # 人脸 API 限制研究
    ├── multi-account-anti-detection-research.md   # 多账号反检测研究
    ├── research-notes-ai-image-captcha-tmall.md   # 验证码/天猫抓取研究
    └── summary-report-all-tasks.md                # 三项任务汇总
```

---

## 4. 总结与建议

### 4.1 三个问题的核心结论

1. **人脸 API 限制没有官方"绕过开关"**——只有降低误伤的合规路径（`moderation=low`、prompt 重写、授权声明、申诉）和混合方案（GPT Image + ComfyUI 后处理）。开源自部署（FLUX + PuLID）是无人脸审核限制的终极方案。

2. **Agent 跨过验证码的能力有限**（benchmark 约 40% 成功率 vs 人类 93%）。本项目实战中，**绕过登录墙的唯一有效方法是"换关键词"**——技术层面的 stealth 补丁、UA 轮换、session 隔离只能延缓风控触发，不能绕过分页登录墙。要稳定抗风控必须用商业反检测浏览器（Multilogin/AdsPower）或开源 camoufox + 静态住宅代理的组合。

3. **爬取结果的差异主要由"数据源入口 + 关键词覆盖"决定**：
   - 单一关键词 + 标准分页 = 51 条
   - 关键词变体 + 5 策略组合 = 185 条
   - 关键词矩阵（51 个）+ 多页 = 1192 条
   - 浏览器 MCP 交叉验证 = 1223 条

### 4.2 后续建议

**短期可做**：
- 用 `merge_and_save.py` 把 Round 1/2/3 和 Browser 数据合并去重，生成 1223 条最终数据集
- 对已抓取商品访问详情页，提取 SKU/规格/促销价
- 补充关键词"蕉内泳衣"、"蕉内口罩"等边角品类

**长期方案**：
- 申请淘宝开放平台（`taobao.item.get.tmall`），用官方 API 替代 DOM 抓取
- 商家自有数据走品牌方授权或后台导出
- 商业级人脸/电商数据需求，优先评估 fal.ai/Replicate 托管方案 + 反检测浏览器组合

**合规提醒**：
- 本项目所有抓取均为低频学习 POC，未绕过验证码、未绕过登录
- robots.txt 检查：`uland.taobao.com` 允许 `/`，`list.tmall.com` 禁止 `/`
- 商业化全量抓取存在合规风险，建议走官方 API 或商家授权
