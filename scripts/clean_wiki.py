"""
清洗 wiki_karpathy_clean 目录的两个残留问题:
  1. [[X]] 悬空 wikilink -> 正文改《X》纯文本,把全部 wikilink 移入 frontmatter external_refs
  2. [url](text) 错位链接 -> 还原成 [text](url)

运行: python scripts/clean_wiki.py
"""
import re
import pathlib
import sys

SRC = pathlib.Path("D:/Data/Downloads/wiki_karpathy_clean")

WIKILINK_RE = re.compile(r"\[\[([^\[\]]+?)\]\]")
# 错位: [https://...](显示文字) -> 反过来
BROKEN_LINK_RE = re.compile(r"\[(https?://[^\]\s]+)\]\(([^)]+)\)")


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n")


def add_to_frontmatter(text: str, refs: list[str]) -> str:
    block = "external_refs:\n" + "\n".join(f"  - {r}" for r in refs)
    if has_frontmatter(text):
        # 插在 frontmatter 末尾的 --- 之前
        return text.replace("\n---\n", f"\n{block}\n---\n", 1)
    return f"---\n{block}\n---\n\n{text}"


def process_file(path: pathlib.Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")

    # 1. 收集并替换 wikilink
    refs = WIKILINK_RE.findall(text)
    new_text = WIKILINK_RE.sub(lambda m: f"《{m.group(1)}》", text)
    n_wiki = len(refs)

    # 2. 修错位链接
    new_text, n_link = BROKEN_LINK_RE.subn(r"[\2](\1)", new_text)

    # 3. 去重 external_refs
    unique_refs = sorted(set(refs))

    if unique_refs:
        new_text = add_to_frontmatter(new_text, unique_refs)

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")

    return n_wiki, n_link


def main() -> int:
    if not SRC.exists():
        print(f"目录不存在: {SRC}", file=sys.stderr)
        return 1

    total_wiki = 0
    total_link = 0
    for md in sorted(SRC.rglob("*.md")):
        n_wiki, n_link = process_file(md)
        if n_wiki or n_link:
            print(f"  {md.relative_to(SRC)}  wikilink={n_wiki}  broken_link={n_link}")
        total_wiki += n_wiki
        total_link += n_link

    print(f"\n完成: 共处理 wikilink={total_wiki}, 错位链接={total_link}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
