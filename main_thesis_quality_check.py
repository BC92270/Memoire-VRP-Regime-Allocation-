from __future__ import annotations

from pathlib import Path
import re
import sys


THESIS_PATH = Path(
    "thesis/final_thesis_package.md"
)

OUT_PATH = Path(
    "thesis/thesis_quality_check.md"
)

WORD_RE = re.compile(
    r"\b[\w'-]+\b"
)

BAD_GLUED_HEADING_RE = re.compile(
    r"[^\n]# Chapter"
)


def normalize(
    text: str,
) -> str:
    return (
        text
        .replace("−", "-")
        .replace("–", "-")
        .replace("—", "-")
        .replace("\u00a0", " ")
        .lower()
    )


if not THESIS_PATH.exists():
    raise FileNotFoundError(
        THESIS_PATH
    )

text = THESIS_PATH.read_text(
    encoding="utf-8"
)

normalized = normalize(text)
lines = text.splitlines()

errors: list[str] = []
warnings: list[str] = []


required_markers = [
    "# Master Thesis",
    (
        "## Variance Risk Premium "
        "and Regime-Based Allocation"
    ),
    (
        "Informational Allocation versus "
        "Model-Based Direct Variance Carry"
    ),
    "# Abstract and Keywords",
    "# Introduction",
    "# Chapter 1",
    "# Chapter 2",
    "# Chapter 3",
    "# Chapter 4",
    "# Chapter 5",
    (
        "model-based direct "
        "variance-payoff approximation"
    ),
    "13.08%",
    "1.324",
    "927 basis points",
    "899 basis points",
    (
        "depends critically on "
        "the payoff structure"
    ),
]

for marker in required_markers:
    if normalize(marker) not in normalized:
        errors.append(
            f"Missing required marker: {marker}"
        )


forbidden_markers = [
    "collapses in Europe",
    "collapses in the European",
    "-2.8511",
    "-0.3625",
    "-0.9901",
    "0.1281",
    "127 observations",
    "200 monthly observations",
    (
        "more useful as a "
        "regime-state variable"
    ),
    (
        "best understood as a conditional "
        "market-state signal"
    ),
]

for marker in forbidden_markers:
    if normalize(marker) in normalized:
        errors.append(
            f"Stale empirical marker found: "
            f"{marker}"
        )


draft_lines = [
    (line_number, line)
    for line_number, line
    in enumerate(lines, start=1)
    if "draft" in line.lower()
]

for line_number, line in draft_lines:
    errors.append(
        f"Draft wording at line "
        f"{line_number}: {line}"
    )


for line_number, line in enumerate(
    lines,
    start=1,
):
    if line.endswith((" ", "\t")):
        errors.append(
            f"Trailing whitespace at "
            f"line {line_number}"
        )


code_fences = [
    line_number
    for line_number, line
    in enumerate(lines, start=1)
    if line.strip().startswith("```")
]

if len(code_fences) % 2 != 0:
    errors.append(
        "Unclosed Markdown code fence: "
        f"{len(code_fences)} markers found"
    )


bad_glued_headings = list(
    BAD_GLUED_HEADING_RE.finditer(text)
)

if bad_glued_headings:
    errors.append(
        "Glued chapter heading detected"
    )


headings = [
    (
        line_number,
        len(line) - len(line.lstrip("#")),
        line.lstrip("#").strip(),
    )
    for line_number, line
    in enumerate(lines, start=1)
    if line.startswith("#")
]


word_count = len(
    WORD_RE.findall(text)
)

character_count = len(text)
line_count = len(lines)


report: list[str] = [
    "# Final Thesis Quality Check",
    "",
    "## 1. Audited file",
    "",
    f"- File: `{THESIS_PATH}`",
    f"- Lines: {line_count}",
    f"- Words: {word_count}",
    f"- Characters: {character_count}",
    f"- Headings: {len(headings)}",
    f"- Draft mentions: {len(draft_lines)}",
    (
        "- Bad glued chapter headings: "
        f"{len(bad_glued_headings)}"
    ),
    "",
    "## 2. Warnings",
    "",
]

if warnings:
    report.extend(
        f"- {warning}"
        for warning in warnings
    )
else:
    report.append("- None")

report.extend([
    "",
    "## 3. Errors",
    "",
])

if errors:
    report.extend(
        f"- {error}"
        for error in errors
    )
else:
    report.append("- None")

report.extend([
    "",
    "## 4. Result",
    "",
])

if errors:
    report.append(
        "- FINAL THESIS QUALITY CHECK FAILED"
    )
else:
    report.append(
        "- FINAL THESIS QUALITY CHECK PASSED"
    )

OUT_PATH.write_text(
    "\n".join(report) + "\n",
    encoding="utf-8",
)


print("=" * 100)
print("FINAL THESIS QUALITY CHECK")
print("=" * 100)

print(f"File: {THESIS_PATH}")
print(f"Lines: {line_count}")
print(f"Words: {word_count}")
print(f"Headings: {len(headings)}")

print()
print("WARNINGS")
print("-" * 100)

if warnings:
    for warning in warnings:
        print(f"WARNING — {warning}")
else:
    print("None")

print()
print("ERRORS")
print("-" * 100)

if errors:
    for error in errors:
        print(f"ERROR — {error}")
else:
    print("None")

print()
print("=" * 100)

if errors:
    print(
        "FINAL THESIS QUALITY CHECK FAILED"
    )
    print("=" * 100)
    sys.exit(1)

print(
    "FINAL THESIS QUALITY CHECK PASSED"
)
print("=" * 100)
