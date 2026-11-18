"""速查 · RAG 检索打分分段实验（右键 Run 本文件，从上往下读输出）。

配合 `速查/RAG与笔记检索速查.md` 看。本文件只演示"概念"，
不提供阶段 5 的完整实现——骨架要你自己搭。
"""

import re
from pathlib import Path

NOTES_DIR = Path(__file__).resolve().parent.parent / "阶段5" / "notes"


def show(title: str) -> None:
    print(f"\n===== {title} =====", flush=True)


# ---------------------------------------------------------------------------
# 实验 1：按空行切段 + 标题拼到段落前
# ---------------------------------------------------------------------------
show("实验 1：切段落 + 标题拼接")

SAMPLE = """# 示例笔记

## 指针

指针是保存内存地址的变量。

数组名会退化为指向首元素的指针。

## 结构体

结构体把不同类型的数据组合在一起。
"""

heading = ""
chunks = []
for para in re.split(r"\n\s*\n", SAMPLE):
    para = para.strip()
    if not para:
        continue
    if para.startswith("#") and "\n" not in para:
        heading = para.lstrip("#").strip()
        continue
    chunks.append(f"{heading}：{para}" if heading else para)

print("段落数 =", len(chunks))
for chunk in chunks:
    print("  ", chunk[:50])
print("要点：标题行不单独成段，而是拼到后面每段开头 —— 这样搜'指针'才能命中正文。")


# ---------------------------------------------------------------------------
# 实验 2：bigram（相邻两字）
# ---------------------------------------------------------------------------
show("实验 2：bigram 是怎么切的")


def bigrams(text: str) -> set[str]:
    text = re.sub(r"\s+", "", text.lower())
    if len(text) == 1:
        return {text}
    return {text[i:i + 2] for i in range(len(text) - 1)}


for s in ["数组指针", "数组和指针", "指针", "针", ""]:
    print(f"{s!r:10} -> {sorted(bigrams(s))}")
print("字数 - 1 = bigram 个数（中文 4 字 → 3 个）。")


# ---------------------------------------------------------------------------
# 实验 3：打分 = 重合数 ÷ |Q|
# ---------------------------------------------------------------------------
show("实验 3：给段落打分")

query = "数组和指针的关系"
q = bigrams(query)
paragraphs = [
    "指针：数组名在大多数表达式中会退化为指向首元素的指针。",
    "结构体：结构体把不同类型的数据组合成一个整体。",
    "极限：数列极限的定义。",
]
print("query bigram =", sorted(q), f"（|Q| = {len(q)}）")
for p in paragraphs:
    overlap = len(q & bigrams(p))
    score = overlap / len(q)
    print(f"  {score:.2f}  重合{overlap}个  ← {p[:24]}")


# ---------------------------------------------------------------------------
# 实验 4：排序 + top_k
# ---------------------------------------------------------------------------
show("实验 4：降序排序，取前 k 个")

scored = []
for p in paragraphs:
    score = len(q & bigrams(p)) / len(q)
    if score:
        scored.append((score, p))
scored.sort(key=lambda item: item[0], reverse=True)
for score, p in scored[:2]:
    print(f"  {score:.2f}  {p[:24]}")
print("要点：先过滤掉 0 分（没重合的段不返回），再排序取前 k。")


# ---------------------------------------------------------------------------
# 实验 5：空 query 的坑（除以 0）
# ---------------------------------------------------------------------------
show("实验 5：空 query 会除以 0")
empty = bigrams("")
print("bigrams('') =", empty, "→ |Q| =", len(empty))
try:
    print(len(empty & bigrams("任意段落")) / len(empty))
except ZeroDivisionError as e:
    print("果然崩了：", type(e).__name__, "—— 所以必须先判断空集合直接返回 []。")


# ---------------------------------------------------------------------------
# 实验 6：真实样例笔记 + 路径安全
# ---------------------------------------------------------------------------
show("实验 6：真实的 notes/ 目录")
print("笔记目录存在：", NOTES_DIR.exists())
if NOTES_DIR.exists():
    files = sorted(p for p in NOTES_DIR.rglob("*") if p.is_file())
    print("文件：", [p.name for p in files])
    total = 0
    for p in files:
        text = p.read_text(encoding="utf-8", errors="ignore")
        total += len([x for x in re.split(r"\n\s*\n", text) if x.strip()])
    print("粗算段落总数（含标题行，未拼接）：", total)

show("实验 7：路径逃逸（read_file 为什么要 resolve + parents）")
if NOTES_DIR.exists():
    base = NOTES_DIR.resolve()
    for name in ["C语言-指针与内存.md", "../ref_check.py", "notes/../C语言-指针与内存.md"]:
        target = (base / name).resolve()
        inside = base in target.parents
        print(f"  {name!r:32} → 在目录内？{inside}")
    print("要点：'..' 会被 resolve() 解析掉，判断时看解析后的路径，不看原始字符串。")
