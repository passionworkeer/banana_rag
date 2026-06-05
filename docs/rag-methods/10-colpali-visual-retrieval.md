# 10 ColPali / 视觉检索

## 定义

不再走 OCR + 文本 embedding 的传统路线，直接把文档页面渲染成图像，用视觉-语言模型（如 ColPali、Qwen3-VL-Embedding）编码成向量。检索时把查询和页面图一起编码，返回最相关的页面/区域。

## 解决的问题

- PPT 图表信息全在图里，OCR 抽不出来。
- 扫描 PDF 没有文本层。
- 复杂排版（多栏、表格嵌套、图注混排）OCR 后结构破坏。
- 流程图、架构图、盖章扫描件等"非纯文本"内容。

## 工作原理

```
文档页面 → 渲染为图像 → ColPali/VL-Embedding 编码 → 页面级向量
查询文本 → 同样模型编码 → 向量
      ↓
   相似度匹配 → 返回最相关页面
```

## 适用

- 高价值复杂文档（合同正本扫描、设计稿、PPT、财报）。
- PPT 图表为主的报告。
- 扫描 PDF、影印件。
- 流程图、架构图。

## 不适用

- 纯文本 PDF（OCR + 文本检索更便宜）。
- 大批量低价值文档（成本不划算）。
- 实时性要求极高的场景（编码慢）。

## 局限

- 模型大、算力贵：单页编码 GPU 成本远高于纯文本。
- 索引存储大：每页一张高维向量。
- 不支持精确"段落级"召回，粒度是页或区域。
- 跨页关系需要后处理。

## 主流实现

| 项目 | 特点 |
|------|------|
| ColPali | 论文级实现，arXiv:2407.01449 |
| Qwen3-VL-Embedding | 阿里通义视觉 embedding |
| PaddleOCR PP-Structure | 版面分析 + 文本抽取的折中方案 |

## 推荐做法

- 第一版以文本和表格为主，ColPali 作为高价值文档的实验性补充。
- 视觉检索不适合全量建索引，应按"文档类型 + 价值"筛选。
- 索引必须保留页码和坐标，方便引用回原图。

## 与多模态的关系

ColPali 是"视觉为主"的多模态检索。企业 RAG 的多模态通常是分层组合：

| 内容 | 索引方式 |
|------|----------|
| 文本 | BM25 + embedding（主索引） |
| 表格 | 表格 JSON + 行列文本 + 表头增强 |
| 图片/流程图 | OCR + caption + 原图引用 |
| PPT 页面 | 页级视觉索引 + 文本索引 |
| 扫描 PDF | OCR 文本 + 页图 |
| 音视频 | ASR 转写 + 章节摘要 |

## 来源

- `../enterprise-knowledge-base/03-technology-selection.md` §12
- `../enterprise-knowledge-base/05-enterprise-deep-dive.md` §1.2、§5
- ColPali 论文：https://arxiv.org/abs/2407.01449
- Qwen3-VL-Embedding：https://github.com/QwenLM/Qwen3-VL-Embedding
