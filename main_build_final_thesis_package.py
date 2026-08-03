from pathlib import Path
import re

ABSTRACT = Path("thesis/abstract_keywords.md")
CLEAN_THESIS = Path("thesis/full_thesis_clean.md")
OUT = Path("thesis/final_thesis_package.md")

for path in [ABSTRACT, CLEAN_THESIS]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

title_page = """# Master Thesis

## Variance Risk Premium and Regime-Based Allocation

### Informational Allocation versus Model-Based Direct Variance Carry

This document contains the complete thesis, including the abstract, keywords, literature review, methodology, empirical results, robustness analysis, limitations and conclusion.

---
"""

abstract_text = ABSTRACT.read_text(encoding="utf-8").strip()
thesis_text = CLEAN_THESIS.read_text(encoding="utf-8").strip()

final_text = "\n\n".join([
    title_page.strip(),
    abstract_text,
    "---",
    thesis_text,
]).strip() + "\n"

OUT.write_text(final_text, encoding="utf-8")

word_count = len(re.findall(r"\b[\w'-]+\b", final_text))
line_count = len(final_text.splitlines())
draft_mentions = final_text.lower().count("draft")
bad_glued_headings = len(re.findall(r"[^\n]# Chapter", final_text))

print("=" * 80)
print("Final thesis package build complete")
print("=" * 80)
print(f"Saved to: {OUT}")
print(f"Lines: {line_count}")
print(f"Words: {word_count}")
print(f"Draft mentions: {draft_mentions}")
print(f"Bad glued headings '# Chapter': {bad_glued_headings}")