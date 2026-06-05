# 06 Parent-child 检索

## 定义

小块用于召回，大块用于生成。检索时命中"子块"，生成时把它的"父块"一起塞进 LLM 上下文。解决"小块召回准但上下文不足"、"大块上下文全但召回不准"的矛盾。

## 结构

```
父块（章节级，500-2000 tokens）
├── 子块 1（段落级，100-300 tokens）  ← 索引这层
├── 子块 2
└── 子块 3
```

检索时拿子块 ID 召回，生成时取对应父块。

## 适用

- 制度文档：章节结构清晰，命中具体条款但需要看上下文。
- 合同/法务：跨条款引用是常态。
- 技术文档：API 文档、代码块需要保留完整上下文。
- 长篇报告：报告章节之间有逻辑关系。

## 不适用

- 文档本身短且独立（如 FAQ）。
- 没有明显层级结构的语料。
- 子块本身已包含足够信息。

## 分块策略建议

| 文档类型 | 推荐分块 | 注意 |
|----------|----------|------|
| 制度/流程 | 按标题层级 + parent-child | 保留章节号和生效时间 |
| 合同/法务 | 条款级 + 定义区关联 | 跨条款引用 |
| PPT | 每页为基本单元 | 保留图文关系 |
| Excel | sheet/table 为单元 | 表头补全 |
| 技术文档 | heading/code block/API endpoint | 代码块不要切碎 |
| 扫描件 | 页级 OCR + 段落 | 保留页码和坐标 |

## 关键原则

- 小块用于召回，大块用于生成。
- chunk 不能跨越不同密级内容。
- chunk 必须保留源文档、页码、标题路径、坐标或段落 ID。
- 表格要同时保存 Markdown、HTML/JSON 结构和原图引用。

## 最小实现

```python
def split_parent_child(doc, parent_size=1500, child_size=300):
    parents = []
    children = []
    for parent in split_by_heading(doc, size=parent_size):
        parent_id = hash(parent)
        parents.append({"id": parent_id, "text": parent})
        for child in split_by_paragraph(parent, size=child_size):
            children.append({
                "id": hash(child),
                "parent_id": parent_id,
                "text": child
            })
    return parents, children

def retrieve(query, children_index, parents_map, top_k=5):
    child_hits = children_index.search(query, top_k=top_k)
    parent_ids = {c["parent_id"] for c in child_hits}
    return [parents_map[pid] for pid in parent_ids]
```

## 来源

- `../enterprise-knowledge-base/03-technology-selection.md` §12
- `../enterprise-knowledge-base/05-enterprise-deep-dive.md` §4.2
