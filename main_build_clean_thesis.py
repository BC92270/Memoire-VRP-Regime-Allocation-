from pathlib import Path
import re

CHAPTERS = [
    Path("thesis/introduction_draft.md"),
    Path("thesis/chapter_1_literature_review_draft.md"),
    Path("thesis/chapter_2_data_methodology_draft.md"),
    Path("thesis/chapter_3_empirical_results_draft.md"),
    Path("thesis/chapter_4_robustness_implementation_draft.md"),
    Path("thesis/chapter_5_limitations_conclusion_draft.md"),
]

OUT = Path("thesis/full_thesis_clean.md")

WORD_RE = re.compile(r"\b[\w'-]+\b")
BAD_GLUED_HEADING_RE = re.compile(r"[^\n]# Chapter")

parts = []

for path in CHAPTERS:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    text = path.read_text(encoding="utf-8").strip()

    cleaned_lines = []
    for line in text.splitlines():
        line = line.rstrip()

        # Remove "Draft" only from markdown headings.
        if line.startswith("#"):
            line = re.sub(r"\s+Draft\s*$", "", line)

        cleaned_lines.append(line)

    parts.append("\n".join(cleaned_lines).strip())

final_text = "\n\n---\n\n".join(parts).strip() + "\n"

OUT.write_text(final_text, encoding="utf-8")

print("=" * 80)
print("Clean thesis build complete")
print("=" * 80)
print(f"Saved to: {OUT}")
print(f"Lines: {len(final_text.splitlines())}")
print(f"Words: {len(WORD_RE.findall(final_text))}")
print(f"Draft mentions: {final_text.lower().count('draft')}")
print(f"Bad glued headings '# Chapter': {len(BAD_GLUED_HEADING_RE.findall(final_text))}")
