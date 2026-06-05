# Taobao Browser Scraper

通过浏览器 MCP 工具抓取淘宝 SEM 搜索结果的商品数据。可提取商品标题、价格、店铺名、itemId 和链接。无需登录即可抓取前 6 页，通过关键词变体策略绕过第 7 页的登录墙。

## 前置条件

- 浏览器连接器已连接（QoderWork browser MCP）
- 已确定目标搜索关键词
- Python 3 可用（用于数据合并脚本）

## 核心流程

```
任务进度:
- [ ] Step 1: 设置浏览器标签页
- [ ] Step 2: 发现页面 DOM 结构
- [ ] Step 3: 逐页提取商品数据
- [ ] Step 4: 通过关键词变体扩大覆盖面
- [ ] Step 5: 合并、去重、保存文件
```

### Step 1: 设置浏览器标签页

1. 获取浏览器工具：`qw_mcp_list`，keyword 填 "browser"
2. 获取工具 schema：`qw_mcp_get`，分别获取 `tabs_context_mcp`、`tabs_create_mcp`、`navigate`、`javascript_tool`
3. 通过 `tabs_context_mcp` 创建或复用标签页
4. 导航到第一个搜索页：

```
URL 模式:
https://uland.taobao.com/sem/tbsearch?keyword={KEYWORD}&q={KEYWORD}&search_type=item&sourceId=tb.index&tab=all&page={PAGE}
```

关键词需要 URL 编码。页码从 1 开始。

### Step 2: 发现 DOM 结构（首次使用）

在提取之前，先检查页面以确认卡片结构：

```javascript
(() => {
  const links = document.querySelectorAll(
    'a[href*="detail.tmall"], a[href*="item.taobao"], a[href*="click.simba"]'
  );
  const sample = links[0];
  if (!sample) return 'no product links found';
  let card = sample;
  for (let i = 0; i < 8; i++) {
    if (card.parentElement) card = card.parentElement;
    else break;
  }
  return JSON.stringify({
    tag: card.tagName,
    cls: card.className.substring(0, 200),
    id: card.getAttribute('id')
  });
})()
```

需要关注的关键信息：
- 卡片包裹层 class（如 `CardV2--doubleCardWrapper--*`）
- 商品 ID 在卡片元素的 `id` 属性中（格式：`item_id_{数字}`）
- 标题 class（如 `Title--title--*`）
- 价格包裹层（如 `Price--priceWrapper--*`）
- 店铺信息 class（如 `[class*="shop"]`、`[class*="Shop"]`）

### Step 3: 提取商品数据

在每个页面上使用以下提取 JS。根据 Step 2 的发现调整 class 选择器。

```javascript
(() => {
  const cards = document.querySelectorAll('[class*="CardV2--doubleCardWrapper"]');
  const r = [];
  for (const c of cards) {
    const id = (c.getAttribute('id') || '').match(/item_id_(\d+)/);
    if (!id) continue;
    const itemId = id[1];

    const t = c.querySelector('[class*="Title--title"]');
    const title = t ? t.textContent.trim().substring(0, 150) : '';

    const p = c.querySelector('[class*="Price--priceWrapper"]');
    let price = '';
    if (p) {
      const m = p.textContent.match(/[¥￥]\s*(\d+\.?\d*)/);
      if (m) price = m[1];
    }

    let shop = '';
    c.querySelectorAll('[class*="shop"],[class*="Shop"],[class*="Seller"]')
      .forEach(e => {
        const x = (e.textContent || '').trim()
          .replace(/^\d+年老店/, '').trim();
        if (x.length > 1 && x.length < 40 && !shop) shop = x;
      });

    r.push({ i: itemId, t: title, p: price, s: shop });
  }
  return JSON.stringify({ n: r.length, d: r });
})()
```

**工具调用格式：**

```json
{
  "action": "javascript_exec",
  "tabId": "<标签页ID>",
  "text": "<上面的JS代码>"
}
```

### Step 4: 通过关键词变体扩大覆盖面

**关键突破点**：淘宝 SEM 搜索在通用关键词的第 7 页后会遇到登录墙。每个新关键词可以获得全新的前 1-3 页（有时可达 6 页），不受登录墙限制。

**策略**：生成覆盖目标品牌所有商品类别的关键词变体。

以蕉内为例：

```
与品牌名组合的品类关键词:
内裤, 袜子, 家居服, 内衣, T恤, 裤子, 外套, 卫衣,
被子, 凉席, 毛巾, 拖鞋, 儿童, 运动, 防晒帽, 防晒衣,
半身裙, 长袖, 衬衫, 保暖, 四件套, 睡裙, 背心, POLO,
围巾, 连衣裙, 瑜伽
```

每个关键词的操作：
1. 导航到关键词搜索的第 1 页
2. 提取商品数据
3. 可选：继续翻到第 2-3 页获取更多数据
4. 切换到下一个关键词

**预期产量**：每页约 48 个商品。通用关键词在第 3-5 页后收益递减。特定品类关键词有时仅第 1 页就能产出 48 个独立商品。

### Step 5: 合并、去重、保存

收集完所有关键词的数据后：

1. **汇总所有原始数据**到同一个数据集中
2. **按 itemId 去重**（同一商品会在不同关键词/页面中出现）
3. **清洗数据**：
   - 移除非品牌商品（通过店铺名或标题中的品牌名过滤）
   - 清洗店铺名：`re.sub(r'^\d+年老店', '', shop_name).strip()`
   - 标准化链接：`https://item.taobao.com/item.htm?id={itemId}`
4. **保存为 JSON 和 CSV**

使用合并脚本：`python scripts/merge_and_save.py`

详见 [scripts/merge_and_save.py](scripts/merge_and_save.py)。

## 问题排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 提取到 0 个商品 | 遇到登录墙或页面未加载 | 检查页面标题；换一个关键词 |
| 所有价格显示相同值 | 价格元素正则不对 | 检查价格包裹层 class，调整正则 |
| 标题中包含价格/店铺文字 | 标题选择器范围太大 | 使用精确的 `Title--title` class |
| 第 7 页后跳转登录 | 淘宝需要认证 | 切换到关键词变体策略 |
| Simba 广告链接太长 | 广告追踪链接在 href 中 | 改用卡片元素 `id` 属性中的 `item_id` |
| 大量非品牌商品 | 关键词太宽泛 | 使用更具体的品类关键词 |

## 浏览器 MCP 工具参考

| 工具 | 用途 |
|------|------|
| `tabs_context_mcp` | 列出/创建浏览器标签页 |
| `tabs_create_mcp` | 创建新标签页 |
| `navigate` | 导航到 URL（参数：`url` + `tabId`） |
| `javascript_tool` | 执行 JS（参数：`action: "javascript_exec"` + `text` + `tabId`） |
| `read_page` | 以无障碍树形式读取页面内容 |
| `get_page_text` | 获取页面完整文本 |

## 性能提示

- 每次 navigate + extract 循环大约需要 4-5 秒
- 优先使用具体品类关键词而非通用关键词
- 通用品牌关键词（如"蕉内"）覆盖面广但在第 5 页后趋于饱和
- 品类关键词（如"蕉内防晒帽"）每页产出的独立商品更多
- 抓取大量关键词时应增量保存数据（防止上下文丢失）
- 非品牌商品在收集后过滤，而非在提取时过滤
