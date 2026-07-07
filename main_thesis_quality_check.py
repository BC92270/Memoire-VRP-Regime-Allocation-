from pathlib import Path
import re
from collections import Counter

THESIS_PATH = Path("thesis/full_thesis_draft.md")
OUT_PATH = Path("thesis/thesis_quality_check.md")

text = THESIS_PATH.read_text(encoding="utf-8")
lines = text.splitlines()

word_count = len(re.findall(r"\b[\w'-]+\b", text))
char_count = len(text)
line_count = len(lines)

headings = []
for i, line in enumerate(lines, start=1):
    if line.startswith("#"):
        level = len(line) - len(line.lstrip("#"))
        title = line.lstrip("#").strip()
        headings.append((i, level, title))

heading_titles = [h[2] for h in headings]
duplicates = {k: v for k, v in Counter(heading_titles).items() if v > 1}

flags = {
    "Draft mentions": [],
    "TODO/FIXME mentions": [],
    "Possible placeholder text": [],
    "Code-fence issues": [],
}

for i, line in enumerate(lines, start=1):
    low = line.lower()
    if "draft" in low:
        flags["Draft mentions"].append((i, line))
    if "todo" in low or "fixme" in low:
        flags["TODO/FIXME mentions"].append((i, line))
    if "lorem ipsum" in low or "placeholder" in low:
        flags["Possible placeholder text"].append((i, line))

code_fences = [i for i, line in enumerate(lines, start=1) if line.strip().startswith("```")]
if len(code_fences) % 2 != 0:
    flags["Code-fence issues"].append(("Unclosed code fence", f"{len(code_fences)} fence markers found"))

chapter_markers = [
    "Introduction Draft",
    "Chapter 1",
    "Chapter 2",
    "Chapter 3",
    "Chapter 4",
    "Chapter 5",
]

missing_markers = [m for m in chapter_markers if m not in text]

report = []
report.append("# Thesis Quality Check")
report.append("")
report.append("## 1. File statistics")
report.append("")
report.append(f"- File: `{THESIS_PATH}`")
report.append(f"- Lines: {line_count}")
report.append(f"- Words: {word_count}")
report.append(f"- Characters: {char_count}")
report.append("")
report.append("## 2. Chapter marker check")
report.append("")
if missing_markers:
    for m in missing_markers:
        report.append(f"- Missing marker: `{m}`")
else:
    report.append("- All expected chapter markers found.")
report.append("")
report.append("## 3. Heading structure")
report.append("")
for line_no, level, title in headings:
    indent = "  " * (level - 1)
    report.append(f"{indent}- L{line_no}: {'#' * level} {title}")
report.append("")
report.append("## 4. Duplicate headings")
report.append("")
if duplicates:
    for title, count in duplicates.items():
        report.append(f"- `{title}` appears {count} times")
else:
    report.append("- No duplicate heading titles detected.")
report.append("")
report.append("## 5. Flags")
report.append("")
for category, items in flags.items():
    report.append(f"### {category}")
    report.append("")
    if not items:
        report.append("- None detected.")
    else:
        for item in items[:50]:
            if isinstance(item[0], int):
                report.append(f"- L{item[0]}: {item[1]}")
            else:
                report.append(f"- {item[0]}: {item[1]}")
        if len(items) > 50:
            report.append(f"- Additional items omitted: {len(items) - 50}")
    report.append("")

OUT_PATH.write_text("\n".join(report), encoding="utf-8")

print("=" * 80)
print("Thesis quality check complete")
print("=" * 80)
print(f"Lines: {line_count}")
print(f"Words: {word_count}")
print(f"Headings: {len(headings)}")
print(f"Duplicate heading titles: {len(duplicates)}")
print(f"Report saved to: {OUT_PATH}")