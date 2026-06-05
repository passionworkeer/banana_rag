# GPT Image 人脸限制、Agent 验证码能力、天猫商品数据调研

调研日期：2026-06-03  
工作目录：`D:\Data\Desktop\rag`

## 0. 结论摘要

这三个问题的性质不同：

1. `gpt-image-2` 传入人脸后报限制，主要是内容安全和肖像/人脸相关风控。官方没有提供“关闭人脸限制”的开关；能做的是降低误伤、整理授权和 prompt、避免高风险内容，必要时走支持渠道申诉。`moderation=low` 可能降低部分误判，但不是绕过策略。
2. Agent 通过验证码在实验环境里有一定能力，尤其是简单滑块、旋转、文字/图片识别题，但真实网站验证码不只是视觉题，还包含设备指纹、IP、账号信誉、行为轨迹和风控联动。Codex/Computer Use 可以操作浏览器，但不应被设计成绕过第三方验证码的工具；可用于自有系统测试、可访问性测试、验证码鲁棒性评估，或人类接管流程。
3. 天猫/淘宝“蕉内”商品数据：普通 `list.tmall.com` 入口不适合无登录稳定抓取；但用户提供的 `uland.taobao.com/sem/tbsearch` SEM 搜索页在本次实测中，无扫码、无登录、用浏览器渲染后可以看到商品卡片。更完整的测试里，第 1-6 页都还能抽到 45 条左右商品，到了第 7 页开始重定向到登录页。这个入口可以做学习性质的低频 POC，但不是稳定官方接口，长期全量抓取仍应优先使用淘宝开放平台或商家授权数据源。

## 1. GPT Image API 传入人脸后的限制报错

### 1.1 官方能力与限制

OpenAI 官方图像生成文档说明，OpenAI API 支持用 GPT Image 模型生成和编辑图片，并包含最新的 `gpt-image-2`。官方文档还说明，GPT Image 系列支持 `moderation` 参数，取值为：

- `auto`：默认标准过滤。
- `low`：较低限制的过滤。

官方文档还说明，`input_fidelity` 控制模型在编辑和参考图工作流中保留输入图细节的强度；但对 `gpt-image-2`，应省略这个参数，因为 API 不允许修改，模型会处理每个图像输入。

参考：

- [OpenAI Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
- [OpenAI Usage Policies](https://openai.com/policies/usage-policies/)
- [OpenAI image/video policy guide](https://openai.com/policies/creating-images-and-videos-in-line-with-our-policies/)

### 1.2 人脸输入为什么更容易报错

从产品机制看，人脸图像比普通商品图、风景图、插画图更敏感，原因包括：

- 可能涉及真实个人身份、肖像权和同意问题。
- 可能涉及名人、公众人物、未成年人或第三方肖像。
- 用户可能要求“换脸”“冒充某人”“保留某人脸部特征但换场景”，这会接近身份混淆或深度伪造风险。
- 真人身体、人脸、年龄、穿着场景和 prompt 中的暧昧词，会被组合评估，容易触发成人、未成年人或非自愿性内容相关过滤。
- 参考图越清晰，模型越能保留身份特征，也越可能触发保守策略。

因此，人脸输入被限制不一定代表 prompt 本身违规，也可能是策略误伤或上下文组合触发。

### 1.3 可尝试的官方/合规解决方案

可尝试方案分为三类：减少误判、减少身份风险、提高申诉可解释性。

#### A. 明确授权和成年人语义

在 prompt 或业务侧元数据中明确：

- 图片由用户本人上传或获得被拍摄者授权。
- 图中人物是成年人。
- 生成目标不是身份冒充、不是换脸、不是色情或性化内容。
- 输出用途是头像、服装试穿、证件照风格、广告素材、艺术化写真等合规场景。

示例语义：

```text
Use the provided user-authorized adult portrait as a visual reference.
Create a non-sexual, realistic editorial portrait.
Do not alter identity into another person.
Do not imitate a public figure.
```

中文业务提示可以写成：

```text
参考用户授权上传的成年人照片，生成一张非色情、非冒充、非公众人物模仿的商务头像。
保持自然人像风格，不生成裸露、性暗示、未成年人形象或误导性身份内容。
```

#### B. 尝试 `moderation=low`

如果确定业务场景合规，但经常被误判，可以尝试把 `moderation` 从默认 `auto` 调为 `low`。这只能降低部分过滤强度，不保证通过，也不能允许违反政策的内容。

适用场景：

- 成人用户本人头像。
- 服装、发型、妆容、背景替换。
- 正常商业、证件、社媒头像、写真风格。

不适用场景：

- 未成年人。
- 性感化或裸露内容。
- 换脸、冒充、公众人物相似生成。
- 未授权第三方照片。

#### C. 降低 prompt 的误触发词

某些词在中文场景里容易误触发成人或身份风险。建议改写：

- “性感”改成“时尚、优雅、自然、杂志风”。
- “少女”改成“年轻成年人风格”，但不要用于真实未成年人。
- “像某明星”改成“自然棚拍、电影感、杂志封面构图”，不要点名公众人物。
- “真实复刻脸”改成“保留人物基本外观，不改变身份，不模仿他人”。

#### D. 做业务前置校验

在调用 API 前对输入做规则校验：

- 要求用户确认授权。
- 明确禁止上传未成年人照片。
- 禁止要求生成成人、性化、裸露或身份冒充内容。
- 禁止把 A 的脸换到 B 的身体上。
- 对失败请求记录 request id、prompt、输入类型、业务场景，方便排查。

#### E. 误伤申诉

如果合规样例稳定失败，建议收集：

- OpenAI 返回的错误类型和 request id。
- 最小复现 prompt。
- 输入图片类型说明，不直接在不安全渠道传播人脸原图。
- 业务合规说明：授权、成年人、非色情、非冒充。

然后向 OpenAI support 或客户经理反馈。

### 1.4 社区结论

在社区讨论里，图像模型对人脸、成人、身体、参考图的过滤经常被认为有误伤。能看到的主流建议基本是：

- 改 prompt，去掉容易触发的词。
- 明确授权和成年人。
- 尝试 `moderation=low`。
- 对误伤请求申诉。
- 如果业务强依赖真人肖像高保真编辑，准备备用模型或私有化方案。

没有发现可靠、官方允许的“绕过人脸限制”方案。所谓绕过通常要么不稳定，要么会违反平台策略，不建议作为产品方案。

社区参考：

- [Linux.do 相关讨论：GPT image 2 无法编辑图片，只能生成](https://linux.do/t/topic/2075535?tl=en)

### 1.5 如果要复杂人脸流程，ComfyUI 是更像样的替代路线

如果你的目标不是“绕过 OpenAI”，而是“做一个可控、可编排、可局部修图的人脸生成流水线”，ComfyUI 这条路更合适。它的优势是：

- 可以把身份保持、姿态、风格、细节修复拆成多个节点。
- 可以把人脸检测、身份特征、局部修复、放大器、后处理分开。
- 可以本地跑，减少把敏感人脸发给第三方 API 的压力。

我查到的主流节点/仓库大致可以这样分工：

| 组件 | 作用 | 适合场景 | 备注 |
| --- | --- | --- | --- |
| `cubiq/ComfyUI_IPAdapter_plus` | 参考图条件控制，偏风格和主体迁移 | 风格参考、构图参考、人物参考 | 更像通用 reference adapter，不是专门的人脸身份锁定 |
| `cubiq/ComfyUI_InstantID` | SDXL 上的身份保持 | 头像、写真、商务照、明确授权肖像 | 需要 `insightface`、`antelopev2`、ControlNet；只支持 SDXL |
| `cubiq/PuLID_ComfyUI` | 身份定制，偏稳定的人脸保真 | 需要更强身份一致性的人像 | 需要 `facexlib`、`InsightFace antelopev2` |
| `balazik/ComfyUI-PuLID-Flux` | FLUX 版身份定制 | 想用 FLUX 做脸部一致性 | 属于 prototype/alpha 路线，模型和显存要求更高 |
| `ltdrdata/ComfyUI-Impact-Pack` | Detailer / Upscaler / Pipe | 最终修脸、放大、补细节 | 常用于最后一轮脸部和皮肤细节收尾 |
| `ComfyUI-ReActor` 系列节点 | Face swap | 明确授权的换脸或替换场景 | 只适合有明确同意和合法用途的情况 |

已确认的仓库参考：

- [cubiq/ComfyUI_IPAdapter_plus](https://github.com/cubiq/ComfyUI_IPAdapter_plus)
- [cubiq/ComfyUI_InstantID](https://github.com/cubiq/ComfyUI_InstantID)
- [cubiq/PuLID_ComfyUI](https://github.com/cubiq/PuLID_ComfyUI)
- [balazik/ComfyUI-PuLID-Flux](https://github.com/balazik/ComfyUI-PuLID-Flux)
- [ltdrdata/ComfyUI-Impact-Pack](https://github.com/ltdrdata/ComfyUI-Impact-Pack)
- [GraftingRayman/Comfyui-reactor-node](https://github.com/GraftingRayman/Comfyui-reactor-node)

一个比较实用的自托管流程会是：

```text
用户授权上传人脸
 -> 人脸检测 / 对齐
 -> 选择身份保持节点
    - SDXL: InstantID 或 PuLID_ComfyUI
    - FLUX: PuLID-Flux
 -> 叠加风格或构图条件
    - IPAdapter Plus / ControlNet
 -> 出图
 -> FaceDetailer / Impact Pack 做局部修复
 -> 人工复核
```

如果你只是想要“有点像本人”的头像、写真、广告图，这条路通常比单次 API 更能控细节；如果你要的是“真实身份高度保真且复杂流程”，ComfyUI 也比单次 `gpt-image-2` 更容易做成多步骤管线。

但它仍然不是“安全策略绕过器”。如果原始输入或输出本身不合规，换成 ComfyUI 也不该做。

## 2. Agent 通过验证码能力调研

### 2.1 验证码类型拆分

常见验证码可以粗分为：

- 文本识别：输入扭曲字符、算术题。
- 滑块：拖动缺口到正确位置。
- 旋转：旋转图片到正确方向。
- 点选：按文字提示点击目标区域。
- 图像选择：选出包含汽车、红绿灯、斑马线、公交车等图片。
- 行为验证码：核心不是题目本身，而是鼠标轨迹、触屏轨迹、设备指纹、IP、cookie、账号信誉。
- 混合验证码：图片识别 + 行为轨迹 + 风控评分 + 二次挑战。

Agent 能力通常只覆盖“看图、规划、移动鼠标、点击、拖动”这一层，真实风控还会看很多不可见信号。

### 2.2 研究 benchmark 结论

Open CaptchaWorld 是一个用于测试多模态 LLM Agent 解验证码能力的 benchmark。论文摘要显示，最强 MLLM agent 的成功率最高约 40.0%，远低于人类 93.3%。

BrowserArena 研究真实 Web 导航任务中的 Agent 表现，明确把 CAPTCHA resolution 列为持续失败模式之一。

参考：

- [Open CaptchaWorld: A Comprehensive Web-based Platform for Testing and Benchmarking Multimodal LLM Agents](https://arxiv.org/abs/2505.24878)
- [BrowserArena: Evaluating LLM Agents on Real-World Web Navigation Tasks](https://arxiv.org/abs/2510.02418)

### 2.3 现成项目类型

GitHub 上能找到几类项目：

1. 打码平台封装  
   例如 2Captcha、Metabypass 这类服务的 Python 包装器。它们本质上是把验证码交给外部服务或人工/模型服务处理。

   示例：

   - [tngeene/2-captcha-solver-python](https://github.com/tngeene/2-captcha-solver-python)
   - [metabypass/captcha-solver-python](https://github.com/metabypass/captcha-solver-python)

2. 滑块/缺口识别  
   常见做法是 OpenCV 或深度学习识别滑块缺口位置，再用 Selenium、Puppeteer、Playwright 拖动。

   示例：

   - [Python3WebSpider/CrackWeiboSlide](https://github.com/Python3WebSpider/CrackWeiboSlide)
   - [Python3WebSpider/DeepLearningSlideCaptcha](https://github.com/Python3WebSpider/DeepLearningSlideCaptcha)
   - [peduajo/geetest-slice-captcha-solver](https://github.com/peduajo/geetest-slice-captcha-solver)
   - [fvitas/geetest-slider-captcha-solver](https://github.com/fvitas/geetest-slider-captcha-solver)

3. Browser agent 尝试  
   使用 browser-use、Playwright、视觉模型让 Agent 自己看图并操作。

   示例：

   - [ShreyashPatil530/browser-use-captcha-solver](https://github.com/ShreyashPatil530/browser-use-captcha-solver)
   - [Yaxin9Luo/Open_CaptchaWorld](https://github.com/Yaxin9Luo/Open_CaptchaWorld)

这些项目说明“技术上有人在做”，但不代表真实网站可稳定通过，也不代表合规。

### 2.4 Codex / Computer Use 是否能做

从能力上看，Codex 或 Computer Use 类 Agent 理论上具备：

- 浏览器截图。
- 视觉理解。
- 点击、拖动、键盘输入。
- 多步循环观察。
- 失败后重试。

因此，在自有测试环境中，它可以尝试：

- 识别简单文字验证码。
- 找滑块缺口并拖动。
- 点击图像中的指定目标。
- 对旋转图片做方向判断。
- 在失败时请求人类接管。

但真实网站验证码不是一个孤立 UI 题，核心风险在于：

- 浏览器自动化指纹。
- Headless/driver 痕迹。
- 鼠标轨迹是否自然。
- IP 和账号信誉。
- cookie、localStorage、设备 ID。
- 是否触发高风险操作。
- 平台是否允许自动化。

OpenAI Computer Use 官方文档也把 “Solving CAPTCHA challenges” 列为需要确认/高风险的人机操作类别之一。参考：[Computer Use guide](https://developers.openai.com/api/docs/guides/tools-computer-use)。

### 2.5 建议边界

建议可以做：

- 自有网站验证码可用性测试。
- 内部风控评估。
- 无障碍评估：验证码是否阻碍合法用户。
- benchmark 研究。
- human-in-the-loop：Agent 遇到验证码暂停，让用户手动完成。

不建议做：

- 自动绕过第三方网站验证码。
- 批量注册、批量登录、批量下单。
- 规避平台风控、隐藏自动化环境。
- 使用打码平台绕过目标站点明确要求的人类验证。

## 3. 天猫/淘宝“蕉内”商品数据调研

### 3.1 问题重新界定

原问题是：如果不扫码，打开天猫/淘宝网站，能否把关于“蕉内”的全部商品价格、名字、图片拿下来。

第一次我直接测了 `list.tmall.com/search_product.htm?q=蕉内`，HTTP 层返回 200，但源码里几乎没有可直接抽取的商品结构，只有很少的关键词和安全/登录痕迹。这个入口不适合作为稳定抓取入口。

你后来给的链接是：

```text
https://uland.taobao.com/sem/tbsearch?bc_fl_src=tbsite_NOX36458&bd_vid=7457002409230251015&channelSrp=baiduSomama&clk1=776c8f806b9d2caaecced746a71b3839&commend=all&ie=utf8&initiative_id=tbindexz_20170306&keyword=%E8%95%89%E5%86%85&localImgKey=&page=1&preLoadOrigin=https%3A%2F%2Fwww.taobao.com&q=%E8%95%89%E5%86%85&refpid=mm_26632258_3504122_32538762&search_type=item&sourceId=tb.index&spm=tbpc.pc_sem_alimama%2Fa.search_manual.0&ssid=s5-e&tab=all
```

这个入口实测结果不同：浏览器渲染后可以看到商品卡片。

### 3.2 无登录 HTTP 访问结果

对用户给出的 `uland.taobao.com/sem/tbsearch` 链接做普通 HTTP 请求：

- HTTP 状态：200。
- 标题：`淘宝搜索sem`。
- HTML 长度：约 10,562。
- `蕉内` 出现：1 次。
- 价格字段相关出现：0 次。
- 图片/`alicdn` 相关出现：18 次。
- 安全/登录相关词出现：6 次。

结论：源码层不是完整商品列表，不能直接当作结构化数据源。必须浏览器执行 JS 后才会出现商品卡片。

### 3.3 浏览器渲染实测

使用 Playwright CLI 打开用户提供链接，未扫码、未登录：

- 页面标题：`蕉内_淘宝搜索`。
- 页面顶部显示 `亲，请登录`，但商品列表仍可见。
- 第 1 页 DOM 中，带 `蕉内` 和 `¥` 的商品链接：45 个。
- 第 1 页可见价格数量：45 个。
- 第 1 页 `alicdn` 图片节点：54 个。
- 第 2 页改 `page=2` 后，也能看到 45 个带 `蕉内` 和价格的商品链接。
- 本次没有出现扫码或验证码拦截。

我也用 Codex 内置 Browser 做了同页验证：内置浏览器 DOM 快照里同样出现了 45 个带 `蕉内` 和 `¥` 的商品链接，第一批可见商品包括防晒衣、内裤、家居服等。也就是说，这不是单纯 HTTP 源码抓取，而是浏览器渲染后可见内容。

我还额外做了一个更长的分页测试：

- 第 1-6 页都能稳定渲染出 45 条左右商品卡片。
- 统计上，第 1-6 页里大部分卡片都可见价格，且能分出广告跳转链接和部分直接详情链接。
- 第 7 页开始重定向到登录页。
- 第 8 页继续停留在登录页。

这说明：

- 公开搜索页可做低频抽取。
- 但它不是一个无限分页、无限稳定的数据源。
- 如果跑得更久，风控和登录墙会出现。

更完整的分页统计如下：

| 页码 | 页面标题 | 商品卡片数 | 唯一标题数 | 直接详情链接 | 广告跳转链接 | 可解析 `item_id` | 代表图片数 | 结果 |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 蕉内_淘宝搜索 | 45 | 44 | 34 | 9 | 36 | 13 | 成功 |
| 2 | 蕉内_淘宝搜索 | 45 | 43 | 34 | 9 | 36 | 13 | 成功 |
| 3 | 蕉内_淘宝搜索 | 45 | 45 | 35 | 8 | 37 | 13 | 成功 |
| 4 | 蕉内_淘宝搜索 | 45 | 43 | 34 | 9 | 36 | 13 | 成功 |
| 5 | 蕉内_淘宝搜索 | 45 | 43 | 34 | 9 | 36 | 13 | 成功 |
| 6 | 蕉内_淘宝搜索 | 45 | 44 | 34 | 9 | 36 | 13 | 成功 |
| 7 | 登录 | 0 | 0 | 0 | 0 | 0 | 0 | 被重定向到登录页 |
| 8 | 登录 | 0 | 0 | 0 | 0 | 0 | 0 | 继续停留在登录页 |

页面网络请求里可以看到淘宝 mtop 接口和广告/日志接口，例如：

- `h5api.m.taobao.com/h5/mtop.tmall.kangaroo.core.service.route.aldlampservicefixedresv2/1.0/`
- `h5api.m.taobao.com/h5/mtop.user.getusersimple/1.0/`
- 多个 `mmstat` 日志请求失败。

控制台里能看到页面识别到 Headless Chrome 相关上报字段，说明长期自动化访问可能触发风控或数据变化。

### 3.4 样例抽取结果

第一页样例：

| 商品名 | 价格 | 店铺/来源 | 图片 URL 示例 |
| --- | ---: | --- | --- |
| 刘浩存同款蕉内氮气504Dry运动内衣女美背性感背心薄文胸瑜伽胸罩 | 169.00 | Bananain蕉内旗舰店 | `https://img.alicdn.com/imgextra/i1/3035493001/O1CN01BUsmET1Y2VjYJ1NQA_!!3035493001-0-alimamacc.jpg` |
| 10A抗菌 蕉内银皮301S袜子女中筒袜防臭运动透气短袜春夏船袜棉袜 | 59.00 | Bananain蕉内旗舰店 | `https://img.alicdn.com/imgextra/i1/3035493001/O1CN01M9XoWQ1Y2VjQaMAlC_!!3035493001-0-alimamacc.jpg` |
| 蕉内银皮301C可爱印花三角内裤透气学生少女纯棉内裤女生抗菌内裤 | 89.00 | Bananain蕉内奥莱店 | `https://img.alicdn.com/img/O1CN01t6jWQl1o2XcA5NFM6_!!1054195167.jpg` |
| 蕉内银皮300S男士内裤纯棉透气裆抗菌亲肤平角四角短裤衩大码男生 | 79.00 | Bananain蕉内奥莱店 | `https://img.alicdn.com/img/O1CN01LeBmxV1o2XZHMkamu_!!1054195167.jpg` |
| 3件 蕉内凉皮311CA男士冰丝内裤莫代尔纯棉透气裆四角短裤男生 | 198.00 | Bananain蕉内旗舰店 | `https://gw.alicdn.com/imgextra/O1CN01XoaIk51Y2VjoWTOkl_!!3035493001.jpg` |

第二页样例：

| 商品名 | 价格 | 店铺/来源 | 图片 URL 示例 |
| --- | ---: | --- | --- |
| 蕉内舒服蕾303A美背性感内衣女薄款蕾丝文胸法式三角杯细肩带胸罩 | 99.00 | Bananain蕉内旗舰店 | `https://img.alicdn.com/img/O1CN01rJI3hA1Y2VjoWbce3_!!3035493001.jpg` |
| 3件 蕉内银皮301P男士平角内裤莫代尔纯棉透气裆冰丝四角短裤男生 | 89.00 | Bananain蕉内旗舰店 | `https://img.alicdn.com/imgextra/i3/3035493001/O1CN01TK9gzx1Y2VjBHdARt_!!3035493001-0-alimamacc.jpg` |
| 蕉内银皮301C可爱印花三角内裤透气学生少女纯棉内裤女生抗菌内裤 | 89.00 | Bananain蕉内奥莱店 | `https://img.alicdn.com/img/O1CN01t6jWQl1o2XcA5NFM6_!!1054195167.jpg` |

### 3.5 可行性判断

分场景判断：

| 目标 | 可行性 | 判断 |
| --- | --- | --- |
| 不扫码，打开用户给的 SEM 链接，看第一页商品 | 可行 | 本次实测成功 |
| 不扫码，抽第一页商品名、价格、图片 | 可行 | DOM 里可见，45 条左右 |
| 不扫码，翻到第 2-6 页继续抽 | 可行但需低频 | 本次每页都成功 |
| 不扫码，继续翻到第 7 页以后 | 不可稳定 | 本次第 7 页开始登录墙 |
| 长期稳定抓完“全部蕉内商品” | 不稳定 | 搜索结果会变化，广告位重复，风控和分页策略会变 |
| 抽真实 SKU、促销价、库存、销量、优惠券、规格价 | 不建议靠公开页 | 需要登录态、详情页、官方 API 或商家授权 |
| 商业化稳定数据管道 | 建议用官方 API/授权 | 公开页面容易变且有合规风险 |

因此，应把结论从“不能做”修正为：

> 对你给的 `uland.taobao.com/sem/tbsearch` 链接，无扫码无登录可以抽取公开渲染出来的搜索页商品卡片；但它不是稳定、完整、官方的数据接口。学习 POC 可做，生产级全量抓取不建议依赖它。

### 3.6 官方 API 路线

淘宝开放平台有 `taobao.item.get.tmall`，说明为“获取天猫单个商品的详细信息”。页面字段里能看到 `pic_url`、`price`、`title` 等字段。

参考：

- [淘宝开放平台 taobao.item.get.tmall](https://developer.alibaba.com/docs/api.htm?apiId=41669)
- [淘宝开放平台 API 文档中心](https://developer.alibaba.com/docs/api.htm?apiId=65016)

官方 API 的优点：

- 字段结构清晰。
- 适合长期维护。
- 更容易合规。
- 可结合商家授权拿更完整数据。

局限：

- 需要 AppKey、签名、权限。
- 某些字段需要授权。
- 搜索/全量商品列表能力可能不等于单商品详情 API，需要组合其他接口或商家后台数据。

### 3.7 Robots 与入口差异

本次读取的 robots：

- `https://uland.taobao.com/robots.txt`：`Allow: /`
- `https://list.tmall.com/robots.txt`：`Disallow: /`
- `https://www.tmall.com/robots.txt`：`Disallow: /*?*`
- `https://www.taobao.com/robots.txt`：允许 `/list/*`，但也有 `Disallow: /*?*`

这说明不同域名和入口差异很大。用户给的 `uland.taobao.com` 在 robots 层面比 `list.tmall.com` 宽松，但 robots 不是完整授权协议，仍需要结合平台服务条款、访问频率、数据用途和账号授权判断。

### 3.8 POC 方案建议

如果只是学习和内部验证，可以做一个低频 POC：

1. 使用浏览器渲染，而不是只抓 HTML。
2. 从 DOM 中抽取商品卡片：标题、价格、店铺名、详情链接、图片 URL。
3. 翻页时使用 `page=N`，每页抽取后去重。
4. 遇到登录、验证码、安全页立即停止，转人工确认。
5. 不做指纹隐藏、验证码绕过、登录绕过。
6. 限速，例如每页间隔数秒以上，避免并发。
7. 保存原始页面快照和抽取结果，便于复核。
8. 只把公开页面中可见的数据用于学习，不做商业转售或大规模再分发。

如果想做一个更稳一点的实验脚本，建议加这几个停止条件：

- 页面标题包含 `登录`，立刻停。
- URL 跳到 `login.taobao.com` 或页面标题变成 `登录`，立刻停。
- 顶部单独出现 `亲，请登录` 不一定要停，因为公开商品列表仍可能可见；应结合商品卡片数判断。
- 页面出现明显验证码或安全校验，立刻停。
- 连续页面卡片数骤降或图片节点明显异常，立刻停。
- 请求频率控制在低速，页面之间留出足够等待时间。

可参考的抽取方向是“只抽公开可见的搜索页”，不要尝试反向绕登录、绕验证码或隐藏自动化环境。

生产级方案：

1. 申请淘宝开放平台能力。
2. 如果是商家自有数据，走商家授权或后台导出。
3. 用官方接口获取商品详情、图片、价格。
4. 对搜索结果页仅做补充观察，不作为主数据源。

## 4. 推荐落地路线

### 4.1 人脸生图业务

短期：

- 先把 prompt 改成授权、成年人、非色情、非冒充。
- 对稳定误伤场景尝试 `moderation=low`。
- 加请求日志和错误分类。

中期：

- 做输入内容校验和用户授权确认。
- 建立“失败样例库”，区分政策拒绝和误伤。
- 对误伤向 OpenAI support 反馈。

长期：

- 如果核心业务是高保真人脸编辑，准备多模型备选。
- 如果需要复杂人脸流程，优先考虑 ComfyUI 的 InstantID / PuLID / IPAdapter / FaceDetailer 管线，而不是只依赖单次 API 调用。
- 对肖像权、未成年人、公众人物制定明确产品规则。

### 4.2 验证码 Agent

短期：

- 只在自有测试环境做 benchmark。
- 做 human-in-the-loop：遇到验证码暂停，用户完成。

中期：

- 如果要测试自家验证码强度，可以搭一个滑块/点选/旋转测试站。
- 用 Agent 评估通过率、失败类型、耗时和用户体验。

长期：

- 不把“绕过第三方验证码”作为产品能力。
- 把验证码视为需要人类授权的交互点。

### 4.3 天猫商品数据

短期学习 POC：

- 以用户给的 `uland.taobao.com/sem/tbsearch` 为入口。
- 抽前几页公开可见结果；本次第 1-6 页可见，第 7 页开始登录墙。
- 输出 CSV/JSON：`title, price, shop, item_url, image_url, page, fetched_at`。

中期：

- 加去重、字段清洗、详情页链接解析。
- 对价格、图片缺失做质量标记。
- 明确停止条件：验证码、登录墙、安全页、异常跳转。

长期：

- 使用淘宝开放平台或商家授权。
- 不依赖页面 DOM 结构做生产级数据源。

## 5. 最终判断

1. `gpt-image-2` 人脸限制没有官方绕过方案。可做的是合规 prompt、`moderation=low`、授权声明、误伤申诉和备用模型；如果业务需要复杂授权人脸流程，可以接 ComfyUI 的 InstantID / PuLID / IPAdapter / FaceDetailer 管线。
2. Agent 能过一部分简单验证码，但真实网站验证码是综合风控问题。Codex/Computer Use 能做自有测试和人工接管，不应被设计为第三方验证码绕过器。
3. 天猫/淘宝“蕉内”数据：用户给的 SEM 链接无扫码可渲染并抽取公开搜索商品卡片，本次第 1-6 页都各抽到 45 条左右，第 7 页开始跳登录。它适合学习 POC，不适合承诺“稳定全量”。商业或长期使用应走官方 API/授权数据。
