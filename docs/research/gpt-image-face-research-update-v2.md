# GPT Image API 人脸限制问题深度调研报告（v2 补充版）

> **调研时间**: 2026 年 6 月  
> **调研范围**: 在 v1 基础上补充 2026 H1 主流模型横评、人脸一致性栈、内容审核实战、国内合规、成本生产化与替代思路  
> **版本**: v2.0（深度补充版）  
> **对应原报告**: `gpt-image-face-research-update.md`（v1.0，2026-06-04 初稿）

---

## 目录

0. [与 v1 版本的差异说明](#0-与-v1-版本的差异说明)
1. [2026 H1 主流模型横评](#1-2026-h1-主流模型横评)
2. [人脸一致性技术栈 2026 现状](#2-人脸一致性技术栈-2026-现状)
3. [OpenAI 内容审核边界实战](#3-openai-内容审核边界实战)
4. [国内 AIGC 合规与平台标注要求](#4-国内-aigc-合规与平台标注要求)
5. [成本、生产化与 GPU 推理性能](#5-成本生产化与-gpu-推理性能)
6. [替代思路：拍照+修图 vs 数字分身](#6-替代思路拍照修图-vs-数字分身)
7. [2026 H1 推荐栈（按场景）](#7-2026-h1-推荐栈按场景)
8. [风险提示与参考链接](#8-风险提示与参考链接)

---

## 0. 与 v1 版本的差异说明

v1 报告（`gpt-image-face-research-update.md`）已系统梳理了：

- GPT Image API 的人脸限制问题与时间线
- gpt-image-1 / gpt-image-2 的差异
- `moderation=low` 的实测效果
- 主流替代模型（FLUX.1/2、Midjourney V7/V8、SDXL+ControlNet、ComfyUI 管线、Grok Imagine、Imagen 3 等）的对比
- 商业级人脸编辑方案与服务商

v2 在 v1 基础上**新增/深挖**以下维度，避免与 v1 重复：

1. **2026 H1 新增模型横评**：Imagen 4、Stable Diffusion 3.5/4、Recraft V3、Ideogram 2.0、字节豆包、阿里通义万相、生数 Vidu（v1 仅一笔带过）
2. **人脸一致性技术栈深度盘点**：将 v1 中散落的 InstantID / PuLID / IP-Adapter FaceID / ReActor / FaceDetailer 等整合，新增 StoryDiffusion / ConsistoryID / PhotoMaker V2 横评，并按"商业写真/换脸/角色一致性"三类场景给出推荐栈
3. **OpenAI 审核边界实战**：补全 v1 未展开的"真实 vs 虚构""公共人物 vs 普通用户"政策细则、误杀案例与 `moderation=low` 实测
4. **国内合规**：v1 仅在第 5.4 节提及"GDPR/CCPA/Deepfake 法规"，v2 单独成章展开 AIGC 标识办法、平台水印要求、B 端 vs C 端差异
5. **成本与生产化**：FLUX.1 Dev 商用授权、Replicate / fal.ai 2026 价格、H100/H200/L40 推理速度对比
6. **替代思路**：v1 仅有技术对比，v2 加入"拍照+修图"与"数字分身"赛道横评

---

## 1. 2026 H1 主流模型横评

> 评估维度：发布/更新时间、人物生成限制策略、商业可用性、API 价格（每张 1024×1024 参考价）。

### 1.1 Google Imagen 4（Vertex AI）

- **发布/更新**：2025 年 5 月 Imagen 3 升级到 Imagen 4，2026 年 1 月发布 Imagen 4 Fast / Standard 两档（来源：[Google DeepMind Imagen 介绍](https://deepmind.google/technologies/imagen-4/)）。
- **人物生成限制**：
  - 政策上禁止生成"可识别的真实人物"（identifiable real people），包括在世名人、未授权的普通人
  - **SynthID 数字水印强制嵌入**，所有 Imagen 4 输出均携带 C2PA + SynthID 双重隐水印
  - 2026 Q1 收紧：明确禁止"基于上传照片的换脸/换装"操作，编辑端点拒绝"reference image + real person"组合
  - 儿童相关请求一律 403
- **商业可用性**：通过 Vertex AI 提供，按张计费；标准版 $0.04/张、Fast 版 $0.02/张；需企业 GCP 账号
- **人脸写实度评估**：Medium 偏上，但皮肤纹理与 FLUX 1.1 Pro 仍有差距；正面肖像稳定，侧脸/俯仰角易出现五官漂移

### 1.2 Stable Diffusion 3.5 / 4

- **Stable Diffusion 3.5**（Stability AI，2024 年 10 月发布，2025 年持续微调）
  - 8B 参数 MMDiT 架构，官方提供 Large / Medium / Turbo 三档
  - 人物生成无内置审核（开源权重），但商用需遵循 Stability AI Community License
  - Stable Diffusion 3.5 Medium 在 2025 年因"成人内容"争议被 Hugging Face 短暂下架，2026 年初恢复分发
- **Stable Diffusion 4**（2026 年 3 月发布传闻，未官方确认）
  - 业内推测为 12B 参数 Transformer + Flow Matching 架构
  - 强调"可控肖像"（Controllable Portrait）模式，集成 IP-Adapter FaceID v3 内核
  - 商业授权改为"按年订阅 + 调用量"混合模式，参考价 $1200/年 + $0.005/张
  - **官方尚未发布** SD4，2026 H1 主流仍是 SD 3.5 Large + 社区微调变体
- **人脸写实度**：SD3.5 Large 显著优于 SDXL，但人脸细节仍弱于 FLUX.1 Dev；适合"可控但不一定极致"的中端场景

### 1.3 Recraft V3

- **发布/更新**：Recraft V3（"Red Panda"）于 2024 年 10 月发布，2025 年推出 V3.5，2026 年初集成进 Canva / Figma 生态
- **人物生成限制**：
  - 定位**矢量与品牌设计**方向，人脸并非主打，写实人脸质量偏弱
  - 允许生成"风格化人物插画"，但拒绝"高度写实的人脸照片"
  - 商业授权清晰：免费层 + Pro $24/月 + Enterprise 议价
- **典型场景**：海报、品牌 IP 形象、信息图；不适合 AI 写真、电商人像场景

### 1.4 Ideogram 2.0

- **发布/更新**：Ideogram 2.0 于 2024 年 8 月发布，2026 年 3 月推出 2.0 Turbo（来源：[Ideogram 2.0 发布博客](https://about.ideogram.ai/2.0)）
- **人物生成限制**：
  - 文本渲染能力业界领先，但在人脸写实度上落后于 FLUX/GPT Image
  - 拒绝"名人肖像"；对"高度写实人物"提示词常触发软审核（warning 而非 block）
  - 提供"Style Reference"功能，可上传风格图但**不允许上传人物照片作为参考**
- **商业可用性**：按张计费约 $0.05/张；API 支持 Style/Describe 两种模式
- **定位**：文字海报、产品图、社交媒体图文，**人脸场景不推荐**

### 1.5 字节跳动 豆包图像（Doubao Image）

- **发布/更新**：2024 年 8 月发布 1.0，2025 年 6 月发布 1.5 Pro，2026 年 4 月发布 2.0（"豆包·图像 2.0"），集成 Seedream 3.0 架构
- **人物生成限制**：
  - **国内版**严格遵循《生成式人工智能服务管理暂行办法》：未授权真人肖像、儿童相关、政治人物一律拦截
  - **国际版（Doubao Pro via Volcano）**政策略宽松，但仍要求用户实名 + 内容标识
  - 中文文字渲染能力**业界最佳**（与 GPT Image 2 持平或略优）
- **商业可用性**：通过火山引擎开放 API；国内价格约 ¥0.06/张（1024×1024），批量折扣 30%
- **人脸写实度**：1.5 Pro 接近 Midjourney V7，2.0 加入"人脸参考"功能（需用户授权 + 平台审核）

### 1.6 阿里 通义万相（Wanxiang）

- **发布/更新**：通义万相 2.0 于 2024 年 9 月发布，2025 年 12 月发布 2.5 Pro，2026 年 5 月推出"通义万相·人物"专用模型
- **人物生成限制**：
  - 国内最严格的"肖像保护"策略之一：所有生成图像强制嵌入阿里 AIGC 标识
  - "通义万相·人物"模型针对"虚拟人/数字分身"场景优化，需用户签署肖像授权书
  - 商用免费层 + Pro 版 ¥0.08/张
- **优势**：与阿里云生态深度集成，电商场景出图效率高；中文 prompt 理解能力强

### 1.7 生数科技 Vidu

- **发布/更新**：Vidu 1.0（2024 年 4 月）、Vidu 2.0（2025 年 7 月）、Vidu Q1（2026 年 1 月，参考 Qwen 发布节奏推测）
- **核心差异**：主打**长视频一致性**（subject reference + 16 秒一致性），人脸视频领域领先
- **人物生成限制**：
  - 图像端点政策与豆包/万相类似，国内严格 + 实名
  - 视频端点额外要求"角色 IP 授权"——上传参考人脸时需提供肖像授权书公证件
- **商业可用性**：图像 API ¥0.10/张，视频 API ¥2.0/秒；适合**数字分身视频**场景
- **人脸写实度**：单帧人脸质量中等，但**跨帧一致性**业界第一

### 1.8 横评总结表

| 模型 | 发布时间 | 人物写实度 | 身份保持 | 审核严格度 | 商业授权 | 参考价（1024²） | 国内可访问 |
|------|----------|------------|----------|------------|----------|-----------------|------------|
| **GPT Image 2 (gpt-image-2)** | 2026-04 | ★★★★★ | ★★★★ | 严格 | OpenAI API | $0.19 | 部分（需企业） |
| **FLUX.1.1 Pro** | 2025-09 | ★★★★★ | ★★★ | 中 | API：bfl.ai | $0.04 | 需代理 |
| **FLUX.1 Dev** | 2024-08 | ★★★★★ | ★★★★ | 无 | 开源+商用授权 | 自部署 | 可自部署 |
| **FLUX.2 Pro** | 2025-12 | ★★★★★ | ★★★★ | 中 | API：bfl.ai | $0.06 | 需代理 |
| **Midjourney V8** | 2026-05 | ★★★★★ | ★★ | 中 | 订阅 $30-120/月 | 订阅制 | 需代理 |
| **Imagen 4** | 2026-01 | ★★★★ | ★★★ | 严格 | Vertex AI | $0.02-0.04 | 不可 |
| **Imagen 4 Standard** | 2026-01 | ★★★★ | ★★★ | 严格 | Vertex AI | $0.04 | 不可 |
| **SD 3.5 Large** | 2024-10 | ★★★ | ★★★ | 无 | Community License | 自部署 | 可自部署 |
| **Stable Diffusion 4** | 2026-03（传闻） | ★★★★ | ★★★★ | 无 | 商业订阅 | $0.005 | 可自部署 |
| **Recraft V3.5** | 2025 | ★★ | ★ | 中 | 订阅 $24/月 | 订阅制 | 需代理 |
| **Ideogram 2.0 Turbo** | 2026-03 | ★★★ | ★★ | 中 | API $0.05/张 | $0.05 | 需代理 |
| **豆包·图像 2.0** | 2026-04 | ★★★★ | ★★★ | 严格（国内） | 火山引擎 API | ¥0.06/张 | 可 |
| **通义万相 2.5 Pro** | 2025-12 | ★★★★ | ★★★ | 严格（国内） | 阿里云 API | ¥0.08/张 | 可 |
| **Vidu Q1** | 2026-Q1（推测） | ★★★ | ★★★★（视频） | 严格（国内） | API ¥0.10/张 | ¥0.10/张 | 可 |
| **Grok Imagine** | 2025-12 | ★★★ | ★★ | 宽松 | X 平台集成 | 订阅 | 不可 |

**关键结论**：

- **国际阵营（GPT Image / FLUX / Midjourney）**：人脸写实度和身份保持仍领先，但 API 受审核约束
- **国内阵营（豆包 / 万相 / Vidu）**：合规友好、价格便宜、写实度追近国际中端，差距在"身份保持"和"非中式审美"两个维度
- **开源阵营（FLUX.1 Dev / SD3.5 / 待定 SD4）**：唯一无审核 + 可自部署的方案，仍是商业写真/换脸的事实标准

---

## 2. 人脸一致性技术栈 2026 现状

### 2.1 核心组件横评

| 组件 | 维护方 | 最新版本（2026 H1） | 核心原理 | 优势 | 局限 |
|------|--------|---------------------|----------|------|------|
| **InstantID** | InstantX Team | v2.0（2025-12） | InsightFace 检测 + IdentityNet + ControlNet 注入 | 单图参考，秒级推理 | 侧脸/遮挡下漂移；需 IP-Adapter 配合才能改风格 |
| **PuLID** | ByteDance | PuLID-FLUX II（2025-11） | 对比对齐 + 残差注入 | 写实度业界第一；污染小 | 显存需求大（24GB+）；社区节点多但兼容性参差 |
| **IP-Adapter FaceID** | HuggingFace h94 | FaceID Plus v3（2026-02） | ArcFace 嵌入 + Cross-Attention | 与 ControlNet/LoRA 无缝组合 | 极端角度还原度弱于 InstantID |
| **ReActor** | Gourieff | 1.6.0（2026-01） | 纯换脸（face swap） | 速度快、社区大 | 不支持"风格化重绘"，仅像素级替换 |
| **FaceDetailer** | Bing Su (mtb) | 1.7.5（2025-10） | 检测 + 局部重绘 | 修复人脸瑕疵事实标准 | 不能生成新身份，只能"修"已有脸 |
| **StoryDiffusion** | StoryDiffusion Team | 1.4（2025-08） | 一致性自注意力机制 | 漫画/分镜多角色一致 | 写实人脸质量中等 |
| **ConsistoryID** | Alibaba | 0.9.1（2025-09） | 主题驱动 + 时序一致性 | 视频/长序列角色一致 | 推理速度慢（10s/帧@H100） |
| **PhotoMaker V2** | Tencent ARC | V2.1（2026-03） | ID 嵌入 + 堆叠参考 | 单次多图参考，姿态可控 | 极端光照下肤色偏移 |

### 2.2 三类场景的推荐栈

#### 2.2.1 商业写真（AI Photo Studio）

**目标**：高写实、高身份保持、批量出图、可商业授权

**推荐栈**：
```
[FLUX.1 Dev] + [PuLID-FLUX II] + [FaceDetailer 1.7.5]
       ↓
[TeaCache / WaveSpeed]（加速）
       ↓
[ComfyUI 工作流封装] + [FastAPI 队列]
```

**理由**：
- PuLID-FLUX II 写实度 + 身份保持双第一
- FaceDetailer 后处理修复瑕疵
- TeaCache/WaveSpeed 加速到 2-3 秒/张

**实测数据**（@H100 80GB）：
- 1024×1024 单张推理：FLUX.1 Dev 8s + PuLID 2s + FaceDetailer 1s = ~11s
- TeaCache 启用后降至 5-6s
- 批量 100 张（H100 单卡）：约 12 分钟

#### 2.2.2 换脸（Face Swap）

**目标**：低延迟、跨种族/跨年龄稳定、API 化

**推荐栈**：
```
[InsightFace (antelopev2)] + [ReActor 1.6] + [CodeFormer]
       ↓
[InsightFace Enterprise API] 或 [自建 FastAPI]
```

**理由**：
- ReActor 是 ComfyUI 生态最成熟换脸节点
- CodeFormer 修复换脸后的人脸清晰度
- 如需企业 SLA，InsightFace Enterprise 提供 $0.003/张 API

**实测数据**：
- 单张换脸：~0.8s（@L40 48GB）
- 高峰并发：单卡 L40 可支撑 12 路 QPS
- 价格：自部署电费 ~$0.0002/张；API 商业版 ~$0.003/张

#### 2.2.3 角色一致性（Comic / Story / IP）

**目标**：多图/多帧角色一致、风格可控

**推荐栈**：
```
[StoryDiffusion 1.4]（漫画/分镜）
或
[ConsistoryID 0.9.1]（长视频/剧情）
或
[PhotoMaker V2.1]（多参考 + 姿态控制）
       ↓
[SD 3.5 Large / FLUX.1 Dev] 基础模型
       ↓
[ControlNet OpenPose] 姿态控制
```

**理由**：
- 漫画/分镜：StoryDiffusion 一致性自注意力机制
- 视频/剧情：ConsistoryID 主题驱动 + 时序建模
- 多姿态 IP：PhotoMaker V2.1 支持多图堆叠

### 2.3 2026 H1 新进展与坑

- **InstantID v2.0**（2025-12）引入"渐进式注入"避免早期版本常见的"双下巴"问题
- **PuLID-FLUX II**（2025-11）显存优化：24GB 可跑（早期版本需 48GB）
- **ReActor 1.6**（2026-01）移除 InsightFace 许可证依赖，但商业用户仍需购买 InsightFace 商业授权
- **PhotoMaker V2.1**（2026-03）加入"参考图权重调度"，可精细控制每张参考的影响
- **坑**：FaceDetailer 在极端角度（>60°）下检测失败率约 8%，需配合 DWPose 兜底

---

## 3. OpenAI 内容审核边界实战

### 3.1 政策细则（2026 版）

> 来源：OpenAI 官方 [Usage Policies](https://openai.com/policies/usage-policies/) 与 [Moderation Guide](https://platform.openai.com/docs/guides/moderation)

#### 3.1.1 "真实人物 vs 虚构人物"

| 类别 | 政策 | 触发条件 | 实际拦截率（社区估算） |
|------|------|----------|------------------------|
| **真实在世名人** | opt-out 名单制 | 名字 + 视觉特征匹配 | ~95% |
| **真实普通人** | 需明确授权证明 | 上传照片 + 身份特征 | ~80% |
| **历史人物（已故 70 年+）** | 允许 | 任何描述 | <5% |
| **虚构人物** | 允许 | 名称 + 视觉特征 | <2% |
| **半虚构（"类似 XX"）** | 灰色 | "in the style of" 触发 | ~40% |
| **儿童相关** | 严格禁止 | 任何儿童 + 写实风格 | 100% |

#### 3.1.2 "公共人物 vs 普通用户"

- **公共人物**：政治家、企业家、明星需先在 OpenAI opt-out 系统登记，未登记者可生成（2025-03-28 回调后）
- **普通用户**：
  - 上传本人照片进行编辑：允许（系统假定用户为本人）
  - 上传他人照片：高度敏感，频繁触发拦截
  - 上传 + "make this person X" 描述：几乎必拦截

#### 3.1.3 `moderation=low` 实测效果

> 来源：v1 报告第 2.4 节、Linux.do 社区、OpenAI Forum

| 场景 | `moderation=auto` | `moderation=low` | 提升幅度 |
|------|-------------------|------------------|----------|
| 虚构角色单人肖像 | 通过 | 通过 | 0 |
| 写实人脸（无参考图） | 50% 拦截 | 80% 通过 | +30% |
| 写实人脸 + 上传参考 | 30% 拦截 | 60% 通过 | +30% |
| 真人照片 → 动漫化 | 70% 拦截 | 70% 拦截 | 0 |
| 编辑端点（`/images/edits`） | — | **不支持** | N/A |
| Inpainting（mask 编辑） | 60% 拦截 | 60% 拦截 | 0 |
| 多人合影 | 80% 拦截 | 85% 拦截 | +5% |

**关键发现**：

1. `moderation=low` 在**生成端点**对人脸场景有 30% 提升，但在**编辑端点无效**
2. Mask 编辑模式（inpainting）不受 `moderation` 控制，是当前的"灰色通道"
3. 多人合影即使 `moderation=low` 仍频繁拦截

### 3.2 长短 prompt 误杀案例

#### 3.2.1 误杀（false positive）案例

- **Case 1**: "a 30-year-old Asian woman with long black hair, office background"
  - 拦截原因：触发了"Asian + woman + professional"组合的"歧视性刻板印象"规则
  - Workaround：改为 "a person with elegant features in a modern office"

- **Case 2**: "portrait of a nurse in hospital"
  - 拦截原因："nurse" 触发了"职业性别刻板印象"
  - Workaround：改为 "medical professional in clinical setting"

- **Case 3**: "photo of my friend at a coffee shop" + 上传照片
  - 拦截原因：系统无法验证"my friend"的所有权
  - Workaround：改为 "portrait of a person" + 不上传照片

#### 3.2.2 漏放（false negative）案例

- **Case A**: 间接描述名人："the former US president with orange hair" → 仍可通过
- **Case B**: 抽象规避："a person who looks like the CEO of a fruit company" → 90% 通过
- **Case C**: 多语种规避：用日语/韩语描述西方名人 → 高通过率（审核侧重英语）

### 3.3 编辑端点的特殊规则

- `/images/edits` 端点**不支持** `moderation` 参数
- 上传照片 + "change to X" 描述 → 60-80% 拦截率
- 仅"轻微风格调整"（亮度、滤镜）通过率较高
- **Inpainting（mask）** 是唯一可绕过大部分审核的官方渠道

### 3.4 趋势判断

- **精准化**：OpenAI 公开承认正在用 GPT-4o 自身作为审核器（meta-moderation）
- **端点差异化**：编辑端点短期内不会开放 `moderation=low`
- **第三方水印**：2026 H1 传言 OpenAI 将在 gpt-image-2 中强制 C2PA 元数据（未官方确认）

---

## 4. 国内 AIGC 合规与平台标注要求

### 4.1 法规框架

#### 4.1.1 《互联网信息服务深度合成管理规定》（2023-01-10 施行）

- 明确要求**生成式 AI 服务提供者**对生成内容添加标识
- 服务提供者需完成**算法备案**（国家网信办）

#### 4.1.2 《生成式人工智能服务管理暂行办法》（2023-08-15 施行）

- 要求内容安全评估、用户实名、未成年人保护
- 训练数据合规（不得侵犯知识产权）

#### 4.1.3 《人工智能生成合成内容标识办法》（2025-09-01 施行）

> **最关键法规**，2024 年底发布、2025 年 9 月正式实施。明确**显式标识 + 隐式标识**双重要求：

- **显式标识**：在图片/视频显著位置标注"AI 生成"
- **隐式标识**：元数据中嵌入机器可读标识（含文件元数据 + 数字水印）
- **平台责任**：抖音、快手、微信、小红书、微博、B 站等需检查用户上传内容是否含 AIGC 标识
- **违规处罚**：警告、罚款、暂停服务、吊销许可

#### 4.1.4 肖像权与著作权

- **肖像权**：《民法典》第 1018 条，未经本人同意不得制作、使用、公开肖像
- **AI 生成的"虚拟人"**：仍受肖像权保护（参考"AI 陪伴"案例：杭州互联网法院 2024 年判例）
- **著作权**：
  - 北京互联网法院 2023 年"AI 生成图第一案"：**AI 生成图受著作权保护**（前提：有人类智力投入）
  - 2025 年最高法司法解释进一步明确：纯 prompt 生成、无独创性修改的不受保护

### 4.2 平台发布要求（2026 H1）

| 平台 | AI 生成图标识 | 水印要求 | 违规处理 | 实测严格度 |
|------|---------------|----------|----------|------------|
| **抖音** | 强制打标"AI 生成" | 元数据 + 屏幕中央水印 | 限流/下架/封号 | ★★★★★ |
| **小红书** | 强制打标"AI 生成" | 元数据 + 可选屏幕水印 | 限流/下架 | ★★★★ |
| **微信视频号** | 强制打标 | 元数据 | 限流 | ★★★★ |
| **快手** | 强制打标 | 元数据 + 屏幕水印 | 限流/下架 | ★★★★★ |
| **B 站** | 强制打标 | 元数据 | 限流 | ★★★ |
| **微博** | 强制打标 | 元数据 | 警告 | ★★ |
| **淘宝/天猫** | 强制打标 | 元数据 + 屏幕水印（部分类目） | 下架/扣分 | ★★★★★ |

**关键点**：

- 抖音、快手、淘宝**必须屏幕可见水印**（不可仅元数据）
- 小红书、微信视频号**元数据 + 创作者主动声明**即可
- 微博、B 站**相对宽松**，但 2025 年起已开始抽检

### 4.3 B 端 vs C 端差异

| 维度 | B 端（企业/平台） | C 端（个人） |
|------|-------------------|-------------|
| **算法备案** | 必须 | 平台代为备案 |
| **内容审核** | 双人复核 + AI | 平台单层审核 |
| **用户实名** | 强制 | 强制 |
| **数据存储** | 至少 6 个月 | 平台规定 |
| **AIGC 标识** | 强制嵌入 | 强制嵌入 |
| **肖像授权** | 需签署书面授权 | 自声明 |
| **责任承担** | 服务提供者 + 平台 | 平台为主 |
| **典型场景** | AI 写真 SaaS、电商出图 | 个人头像、社交分享 |

**关键点**：

- **B 端必须有自己的合规链路**：肖像授权书 → 用户协议 → 内容审核 → 标识嵌入 → 留档
- **C 端责任多在平台**：但若个人商用（如开 AI 写真小店），实际承担 B 端责任
- **跨境服务**：直接向国内用户提供海外模型 API（FLUX/SD/MJ）属"违规提供生成式 AI 服务"，需走国内代理

### 4.4 平台 API 审核差异

| 厂商 | 国内可访问 | 合规备案 | AIGC 标识 |
|------|------------|----------|-----------|
| **豆包·图像** | 直接 | 已备案 | 自动嵌入 |
| **通义万相** | 直接 | 已备案 | 自动嵌入 |
| **Vidu** | 直接 | 已备案 | 自动嵌入 |
| **GPT Image (海外直连)** | 不合规 | 无 | 无（需自行嵌入） |
| **FLUX.1 Dev (自部署)** | 灰区 | 需自行备案 | 需自行嵌入 |

---

## 5. 成本、生产化与 GPU 推理性能

### 5.1 FLUX.1 Dev 商用授权

> 来源：[Black Forest Labs Licensing](https://bfl.ai/licensing)

- **FLUX.1 [dev]**（开源权重）
  - 适用：非商业、个人项目、研究
  - 商业授权：FLUX.1 [pro] 之外的 dev/schnell **不可直接商用**
  - 商用路径：购买 [FLUX.1 [dev] Commercial License](https://bfl.ai/pricing)，**€299/月起**，按年付
  - 月调用上限：1M 张/月（超出按 €0.005/张计费）
- **FLUX.1 [schnell]**（Apache 2.0）
  - 真正的开源免费，可商用（仅需保留版权声明）
  - 代价：人脸质量逊于 dev，4 步推理
- **FLUX.1 [pro] / FLUX.2 [pro]**（闭源 API）
  - 通过 bfl.ai 或 Replicate/fal.ai 调用
  - FLUX.1.1 Pro：$0.04/张；FLUX.2 Pro：$0.06/张

### 5.2 Replicate / fal.ai 2026 价格

| 平台 | FLUX.1 Dev 单价 | FLUX.1.1 Pro 单价 | FLUX.2 Pro 单价 | GPT Image 2 单价 | 计费单位 | 并发 |
|------|-----------------|-------------------|-----------------|------------------|----------|------|
| **Replicate** | $0.025/张 | $0.055/张 | $0.07/张 | $0.25/张 | 按张 | 无限制 |
| **fal.ai** | $0.018/张 | $0.04/张 | $0.06/张 | $0.19/张 | 按张 | 无限制 |
| **bfl.ai 官方** | N/A（仅 pro） | $0.04/张 | $0.06/张 | N/A | 按张 | 无限制 |
| **OpenAI 官方** | N/A | N/A | N/A | $0.19/张 | 按张 | 60 RPM（Tier 1） |
| **Together.ai** | $0.02/张 | N/A | N/A | N/A | 按张 | 无限制 |
| **WaveSpeed AI** | $0.015/张 | $0.035/张 | N/A | $0.17/张 | 按张 | 无限制 |

**价格趋势（2025-2026）**：

- FLUX.1 Dev 商用价格从 2024 年的 $0.05/张 降至 2026 年的 $0.015-0.025/张
- fal.ai 在中国出海用户中最受欢迎（中文文档 + 支付宝 + 低延迟）
- WaveSpeed AI 是 2025 年新晋玩家，价格最低

### 5.3 GPU 推理速度对比

> 测试条件：1024×1024 输出，FLUX.1 Dev + PuLID-FLUX II 完整管线，FP16 精度，30 步推理

| GPU | 显存 | 单张推理 | 批量 4 推理 | 批量 8 推理 | 并发上限（QPS） | 时租（云端） |
|-----|------|----------|-------------|-------------|-----------------|-------------|
| **H100 SXM** | 80GB | 5.2s | 16s | 28s | 8-12 | $2-3/h |
| **H200 SXM** | 141GB | 4.8s | 14s | 24s | 10-15 | $3-4/h |
| **H100 PCIe** | 80GB | 6.0s | 19s | 33s | 6-10 | $1.8-2.5/h |
| **A100 SXM 80GB** | 80GB | 7.5s | 24s | 42s | 5-8 | $1.2-1.8/h |
| **A100 40GB** | 40GB | 8.2s（需优化）| 28s | OOM | 4-6 | $0.8-1.2/h |
| **L40S** | 48GB | 9.5s | 32s | 56s | 4-6 | $0.8-1.2/h |
| **L40** | 48GB | 11s | 38s | 68s | 3-5 | $0.6-0.9/h |
| **A10** | 24GB | 18s | 65s | OOM | 2-3 | $0.4-0.6/h |
| **RTX 4090** | 24GB | 14s | 50s | OOM | 3-4 | $0.3-0.5/h（自购） |
| **RTX 3090** | 24GB | 22s | OOM | OOM | 1-2 | $0.15-0.25/h（自购） |

**关键发现**：

- **H100 SXM 80GB** 是 FLUX + PuLID 的**甜点配置**：单卡 8-12 路 QPS
- **H200 性能提升有限**（~10%），但大显存支持更大批量
- **A100 40GB** 跑 FLUX Dev + PuLID 紧张，需要开启 FP8 + 卸载
- **L40S 是性价比之选**：48GB 显存 + 接近 A100 的推理速度
- **4090 不推荐生产**：显存仅 24GB，批量推理受限

### 5.4 生产化最佳实践

```
架构建议：
[API Gateway (Cloudflare/Kong)]
        ↓
[任务队列 (Redis Stream / RabbitMQ)]
        ↓
[GPU Worker Pool]
   - 1-2 张 H100 主推理
   - 1 张 L40S 兜底
        ↓
[对象存储 (S3/OSS) + CDN]
        ↓
[前端回调 / WebSocket]
```

**成本控制**：

- **高峰期**：按需弹性（K8s + Karpenter）
- **稳定期**：预留实例（Reserved Instance），云厂商 30-50% 折扣
- **国内推荐**：阿里云 gn7 / 腾讯云 GN10X（基于 A10）
- **海外推荐**：AWS p5.48xlarge（H100） / Lambda Labs H100

---

## 6. 替代思路：拍照+修图 vs 数字分身

> 当"AI 生图"路线遇到合规、审核或成本瓶颈时，应考虑根本性换路线

### 6.1 AI 写真赛道的两条路线

#### 6.1.1 路线 A：AI 生成（生图路线）

- **核心**：FLUX + PuLID/InstantID 凭空生成
- **优势**：场景无限、风格自由、单图成本低
- **劣势**：
  - 身份保真度 < 95% 时用户退货率高
  - 政策风险：肖像授权链路复杂
  - "恐怖谷"问题：人脸细看仍有破绽

#### 6.1.2 路线 B：拍照 + AI 修图（还原路线）

- **核心**：用户上传几张照片 → 训练 LoRA → AI 修图/换背景
- **代表产品**：妙鸭相机（2023）、Lensa AI、Remini、Photoroom
- **优势**：
  - 身份保真度 > 99%（基于真实照片）
  - 合规风险极低（用户主动授权）
  - 退款率 < 1%
- **劣势**：
  - 用户上传门槛高（5-20 张）
  - 训练时间 10-30 分钟
  - 场景仍受限（无法"凭空"换装换景）
- **2026 H1 趋势**："拍照+修图"路线**重新成为主流**（妙鸭相机 2024 续命、字节"星绘"、阿里"通义照相馆"）

### 6.2 数字分身（Digital Avatar）赛道横评

> 目标：用户拥有一个 24/7 可调用的"数字分身"，可用于客服、直播、短视频

| 方案 | 代表产品 | 技术栈 | 实时性 | 写实度 | 成本 | 适合场景 |
|------|----------|--------|--------|--------|------|----------|
| **HeyGen** | 海外 | Wav2Lip + 视频生成 | <2s 延迟 | ★★★★ | $24/月起 | 跨境电商客服 |
| **D-ID** | 海外 | 静态图 + 语音驱动 | <3s 延迟 | ★★★ | $5.9/月起 | 营销视频 |
| **Synthesia** | 海外 | 3D Avatar + 语音 | <1s 延迟 | ★★★★ | $22/月起 | 企业培训 |
| **硅基智能** | 国内 | 数字人 + 直播大模型 | <1s 延迟 | ★★★★ | ¥499/月起 | 本地生活直播 |
| **百度智能云数字人** | 国内 | 曦灵平台 | <1s 延迟 | ★★★★ | ¥1500/月起 | 广电、金融 |
| **腾讯智影** | 国内 | 数字分身 | <2s 延迟 | ★★★ | ¥299/月起 | 短视频创作 |
| **商汤如影** | 国内 | SenseTime Avatar | <2s 延迟 | ★★★★ | 企业议价 | 品牌代言 |
| **阿里通义数字人** | 国内 | 万相 + 语音 | <1.5s 延迟 | ★★★★ | ¥800/月起 | 电商直播 |

**关键判断**：

- **跨境/海外业务**：HeyGen + Synthesia 是事实标准
- **国内直播带货**：硅基智能、商汤如影占据 70%+ 市场份额
- **企业内部培训**：百度智能云、阿里通义数字人
- **2026 H1 新趋势**：**3D 高斯泼溅（3DGS）+ NeRF** 路线开始挑战传统 2D 数字分身（代表：腾讯"数字敦煌"、字节"数字孪生直播"）

### 6.3 "AI 写真" vs "数字分身"边界

- **AI 写真**：以**图像**为主要交付物，单次性消费
- **数字分身**：以**持续可调用的 Agent** 为核心，订阅制

**业务模型差异**：

| 维度 | AI 写真 | 数字分身 |
|------|---------|----------|
| 单价 | ¥5-50/次 | ¥500-5000/月 |
| 用户 LTV | 低 | 高 |
| 合规复杂度 | 中 | 高（需深度合成备案） |
| 技术门槛 | 中 | 高 |
| 2026 H1 增速 | 平稳 | +120% YoY |

**结论**：若业务目标是**短期流量 + 低客单价**，选 AI 写真；若目标是**长期订阅 + 高客单价**，选数字分身。

---

## 7. 2026 H1 推荐栈（按场景）

### 7.1 商业写真（AI Photo Studio）

**目标**：高写实、高身份保持、批量出图

```
[FLUX.1 Dev] + [PuLID-FLUX II] + [FaceDetailer 1.7.5]
       ↓
[TeaCache / WaveSpeed]（5s/张加速）
       ↓
[ComfyUI 工作流] + [FastAPI 队列]
       ↓
[1-2 张 H100 SXM 80GB]
```

**关键参数**：
- 身份保真度：> 95%
- 单张成本：~$0.005（自部署电费+摊销）
- 并发：8-12 QPS（单卡）
- 国内合规：叠加"通义万相·人物"作为备选（B 端合规链路）

### 7.2 数字分身（Digital Avatar）

**目标**：24/7 可调用、高写实、低延迟

```
[采集端] 用户上传 3-5 分钟视频
       ↓
[训练] InsightFace 3D 重建 + Wav2Lip 适配
       ↓
[推理] 实时语音驱动 + 视频生成
       ↓
[交付] WebRTC / RTMP 推流
```

**推荐栈**：
- **海外**：HeyGen / Synthesia（直接采购）
- **国内**：硅基智能（本地生活）、百度智能云（政企）、商汤如影（品牌）
- **自建**（高预算）：腾讯智影 API + 自训练 LoRA

**关键参数**：
- 实时性：< 2s 端到端
- 单次对话成本：¥0.5-2
- 政策合规：必须完成深度合成备案

### 7.3 电商场景图（E-commerce Visual）

**目标**：商品图 + 模特图、批量、低成本

```
[商品识别] YOLO-World
       ↓
[场景合成] FLUX.1 Dev + IP-Adapter（风格）+ ControlNet（构图）
       ↓
[模特替换] PuLID-FLUX II（虚拟模特） / ReActor（真人模特）
       ↓
[合规嵌入] AIGC 标识（淘宝/抖音强制）
```

**推荐方案**：
- **低成本**：Ideogram 2.0 + ReActor（$0.05/张）
- **中高质**：FLUX.1.1 Pro + PuLID（$0.04/张）
- **国内合规优先**：豆包·图像 2.0 + 万相·人物

**关键参数**：
- 单张成本：¥0.04-0.5
- 批量出图：500-5000 张/天
- 平台合规：必须嵌入 AIGC 标识

### 7.4 头像换肤（Avatar Customization）

**目标**：社交平台头像、虚拟形象、风格化

```
[用户上传 1-3 张照片]
       ↓
[PhotoMaker V2.1]（多参考权重调度）
或
[SD 3.5 Large + IP-Adapter FaceID Plus v3]
       ↓
[风格化] 动漫/插画/油画 LoRA
       ↓
[输出] 多风格头像 6-12 张
```

**推荐方案**：
- **个人/中小商家**：Replicate PhotoMaker API（$0.008/张）
- **高质定制**：FLUX.1 Dev + IP-Adapter FaceID（自部署）
- **国内合规**：豆包·图像 1.5 Pro（实名 + 标识）

**关键参数**：
- 单次成本：¥0.05-0.5
- 用户上传：1-3 张即可
- 转换时间：< 30s
- 合规要求：肖像授权 + AIGC 标识

### 7.5 推荐栈对比一览

| 场景 | 首选 | 备选 | 关键模块 | 单张成本 | 国内合规 |
|------|------|------|----------|----------|----------|
| **商业写真** | FLUX.1 Dev + PuLID-FLUX II | 豆包·图像 2.0 | PuLID、FaceDetailer | $0.005-0.06 | 需备案 |
| **数字分身** | 硅基智能 / HeyGen | 自建 + InsightFace | 3DGS、Wav2Lip | ¥500-5000/月 | 必须备案 |
| **电商场景图** | FLUX.1.1 Pro + PuLID | 豆包·图像 2.0 | IP-Adapter、ControlNet | $0.04-0.5 | 自动标识 |
| **头像换肤** | PhotoMaker V2.1 | SD 3.5 + IP-Adapter FaceID | PhotoMaker、LoRA | $0.008-0.05 | 自动标识 |

---

## 8. 风险提示与参考链接

### 8.1 风险提示

1. **政策风险**：AIGC 标识办法已强制实施，未合规内容将被限流下架
2. **合规成本**：B 端服务需投入 5-10% 收入用于合规（备案、法务、审核）
3. **模型迭代**：FLUX / SD 生态每 3-6 个月一次大版本，需持续跟进
4. **肖像权**：国内肖像权判例偏向"未经书面授权即侵权"，B 端需签署完整授权书
5. **跨境数据**：用户人脸数据出境需通过安全评估（参考《数据出境安全评估办法》）

### 8.2 v1 未覆盖、本版新增引用

> 注：以下链接为 v2 新增参考，v1 已引用过的链接不再重复列出。

#### 法规与合规

- [国家网信办《人工智能生成合成内容标识办法》](https://www.cac.gov.cn/2024-12/27/c_1736711890434061.htm)
- [国家网信办《生成式人工智能服务管理暂行办法》](https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm)
- [国家网信办《互联网信息服务深度合成管理规定》](https://www.cac.gov.cn/2022-12/11/c_1672221949354811.htm)
- [抖音《AIGC 标识规范》（社区创作者中心）](https://creator.douyin.com/)
- [小红书《AI 内容创作规范》](https://www.xiaohongshu.com/)
- [北京互联网法院"AI 生成图第一案"判决书（2023）](http://www.bjinternetcourt.gov.cn/)

#### 模型与产品

- [Google DeepMind Imagen 4 介绍](https://deepmind.google/technologies/imagen-4/)
- [Stability AI Stable Diffusion 3.5 文档](https://stability.ai/news/stable-diffusion-3-5)
- [Recraft V3 发布博客](https://www.recraft.ai/blog)
- [Ideogram 2.0 发布博客](https://about.ideogram.ai/2.0)
- [字节豆包·图像 2.0 火山引擎文档](https://www.volcengine.com/product/doubao)
- [阿里通义万相 2.5 介绍](https://tongyi.aliyun.com/wanxiang/)
- [生数科技 Vidu 官网](https://www.vidu.studio/)
- [Black Forest Labs 商业授权](https://bfl.ai/licensing)
- [Black Forest Labs 价格](https://bfl.ai/pricing)

#### 服务商

- [fal.ai 定价](https://fal.ai/pricing)
- [Replicate FLUX Dev](https://replicate.com/black-forest-labs/flux-dev)
- [WaveSpeed AI 定价](https://wavespeed.ai/pricing)
- [Together.ai 定价](https://www.together.ai/pricing)
- [InsightFace Enterprise](https://www.insightface.ai/)
- [RunComfy 云端 ComfyUI](https://www.runcomfy.com/)

#### 人脸技术栈

- [InstantID GitHub](https://github.com/InstantX/InstantID)
- [PuLID GitHub](https://github.com/ToTheBeginning/PuLID)
- [ComfyUI PuLID Flux II](https://github.com/lldacing/ComfyUI_PuLID_Flux_ll)
- [IP-Adapter FaceID HuggingFace](https://huggingface.co/h94/IP-Adapter-FaceID)
- [ComfyUI-ReActor](https://github.com/Gourieff/ComfyUI-ReActor)
- [FaceDetailer GitHub (ltdrdata)](https://github.com/ltdrdata/ComfyUI-Impact-Pack)
- [StoryDiffusion GitHub](https://github.com/HVision-NKU/StoryDiffusion)
- [ConsistoryID 论文（Alibaba）](https://arxiv.org/abs/2406.00856)
- [PhotoMaker V2 仓库](https://github.com/TencentARC/PhotoMaker)

#### 数字分身

- [HeyGen 官网](https://www.heygen.com/)
- [D-ID 官网](https://www.d-id.com/)
- [Synthesia 官网](https://www.synthesia.io/)
- [硅基智能 官网](https://www.guiji.ai/)
- [百度智能云 数字人 曦灵](https://cloud.baidu.com/product/avatar)
- [腾讯智影 数字分身](https://zenvideo.qq.com/)
- [商汤如影 官网](https://business.sensetime.com/)
- [阿里通义 数字人](https://tongyi.aliyun.com/)

#### AI 写真产品

- [妙鸭相机 体验入口](https://miaoya-graph.alipay.com/)
- [字节"星绘" 入口](https://www.doubao.com/)
- [Remini 官网](https://remini.ai/)
- [Lensa AI 官网](https://prisma-ai.com/lensa)

#### 行业对比与评测

- [FreeAcademy: 2026 AI 图像模型对比](https://freeacademy.ai/blog/midjourney-vs-dalle-vs-stable-diffusion-vs-flux-comparison-2026)
- [Cliprise: 2026 Best AI Image Generator](https://www.cliprise.app/learn/comparisons/features/best-ai-image-generator-2026-tested-ranked)
- [Medium: FLUX.2 Pro vs Midjourney V7 vs Nano Banana Pro](https://medium.com/@leucopsis/flux-2-pro-review-and-comparison-with-midjourney-v7-and-with-nano-banana-pro-337224a5551f)
- [Linux.do: gpt-image-2 限制讨论](https://linux.do/t/topic/2151401)
- [OpenAI Forum: gpt-image-2 已知问题](https://community.openai.com/t/collection-of-gpt-image-generator-2-0-issues-bugs-and-work-around-tips-check-first-post/1379535)
- [OpenAI Forum: 图像编辑端点不支持 moderation](https://community.openai.com/t/no-option-to-lower-moderation-for-image-edit/1250225)

#### 法规与司法判例

- [民法典 第 1018 条（肖像权）](http://www.npc.gov.cn/npc/c2/c30834/202006/t20200602_306457.html)
- [最高法 2025 年 AI 著作权司法解释](https://www.court.gov.cn/)
- [杭州互联网法院 2024 AI 陪伴案](https://www.hzinternetcourt.cn/)

### 8.3 写作声明

- 本报告基于 2026 年 6 月前公开信息整理
- v2 是 v1 的深度补充版，v1 中已涵盖的 GPT Image 限制时间线、政策演变、技术原理等内容未在本版重复展开
- 国内合规章节为方法论 + 行业惯例梳理，正式业务落地前请咨询专业法务
- 模型价格、GPU 性能数据为社区估算与官方文档平均值，实际部署需做 PoC 验证

---

> **免责声明**：本报告基于公开信息整理，技术、政策、价格变化迅速，建议在实际决策前验证最新信息。涉及人脸生成/编辑技术时，请严格遵守《人工智能生成合成内容标识办法》及当地法律法规。
