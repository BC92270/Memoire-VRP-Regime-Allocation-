from __future__ import annotations

from pathlib import Path
import re


ROOT = Path("thesis/latex")

SECTIONS = [
    ROOT / "sections/00_abstract.tex",
    ROOT / "sections/01_introduction.tex",
    ROOT / "sections/02_literature_review.tex",
    ROOT / "sections/03_data_methodology.tex",
    ROOT / "sections/04_empirical_results.tex",
    ROOT / "sections/05_robustness.tex",
    ROOT / "sections/06_conclusion.tex",
]

MAIN = ROOT / "main.tex"
BIB = ROOT / "references.bib"
LOG = ROOT / "main.log"


errors: list[str] = []
warnings: list[str] = []


# ============================================================
# Files
# ============================================================

for path in [MAIN, BIB, *SECTIONS]:
    if not path.exists():
        errors.append(
            f"Missing required file: {path}"
        )


texts = {}

for path in SECTIONS:
    if path.exists():
        texts[path] = path.read_text(
            encoding="utf-8"
        )

combined = "\n".join(
    texts.values()
)


# ============================================================
# Placeholders / stale conclusions
# ============================================================

forbidden = [
    "Final abstract pending",
    "Final introduction pending",
    "Final literature review pending",
    "Final methodology pending",
    "Final empirical results pending",
    "Final robustness analysis pending",
    "Final discussion and conclusion pending",
    "collapses in Europe",
    "collapses in the European",
    "-2.8511",
    "-0.3625",
    "-0.9901",
    "0.1281",
    "127 observations",
    "200 monthly observations",
    "best understood as a conditional market-state signal",
    "more useful as a regime-state variable",
    "filecite",
]

for phrase in forbidden:
    if phrase.lower() in combined.lower():
        errors.append(
            f"Stale/forbidden phrase: {phrase}"
        )


# ============================================================
# Methodological terminology
# ============================================================

dangerous = [
    "directly traded variance",
    "tradable variance swap strategy",
    "actual variance swap backtest",
    "true variance swap backtest",
]

for phrase in dangerous:
    if phrase.lower() in combined.lower():
        errors.append(
            f"Overstated terminology: {phrase}"
        )


required_global = [
    "model-based direct variance-payoff approximation",
    "not an observed return on invested capital",
    "184",
    "122",
    "232",
    "170",
    "1.019",
    "1.324",
    "82.42",
    "78.35",
    "927 basis points",
    "899 basis points",
]

for marker in required_global:
    if marker.lower() not in combined.lower():
        errors.append(
            f"Missing global marker: {marker}"
        )


# ============================================================
# Timing consistency
# ============================================================

methodology = texts.get(
    ROOT / "sections/03_data_methodology.tex",
    "",
)

conclusion = texts.get(
    ROOT / "sections/06_conclusion.tex",
    "",
)

required_timing = [
    (
        methodology,
        "expands recursively",
        "HMM expanding estimation"
    ),
    (
        methodology,
        "fixed 72-month rolling training window",
        "ML rolling estimation"
    ),
    (
        methodology,
        "VRP_{t-2}",
        "High-VRP threshold t-2"
    ),
    (
        methodology,
        "full absolute notional",
        "monthly roll-cost accounting"
    ),
    (
        conclusion,
        "expanding estimation history",
        "conclusion HMM/RSM timing"
    ),
    (
        conclusion,
        "fixed 72-month rolling training window",
        "conclusion ML timing"
    ),
]

for text, marker, label in required_timing:
    if marker not in text:
        errors.append(
            f"Missing timing control: {label}"
        )


# ============================================================
# Research-question consistency
# ============================================================

intro = texts.get(
    ROOT / "sections/01_introduction.tex",
    "",
)

research_fragment = (
    "Does the Variance Risk Premium create "
    "more economic value as an informational "
    "state variable"
)

if research_fragment not in intro:
    errors.append(
        "Research question missing from introduction"
    )

if research_fragment not in conclusion:
    errors.append(
        "Research question missing from conclusion"
    )


# ============================================================
# LaTeX structure
# ============================================================

all_labels: list[tuple[str, str]] = []
all_refs: list[tuple[str, str]] = []

for path, text in texts.items():
    if text.count("{") != text.count("}"):
        errors.append(
            f"Unbalanced braces: {path}"
        )

    for env in [
        "equation",
        "table",
        "tabular",
        "tabularx",
        "quote",
    ]:
        begin = text.count(
            rf"\begin{{{env}}}"
        )
        end = text.count(
            rf"\end{{{env}}}"
        )

        if begin != end:
            errors.append(
                f"{path}: {env} "
                f"{begin} begin / {end} end"
            )

    if text.count("$") % 2:
        errors.append(
            f"Odd inline $ count: {path}"
        )

    for number, line in enumerate(
        text.splitlines(),
        start=1,
    ):
        stripped = line.strip()

        if re.match(
            r"^#{1,6}\s+",
            stripped,
        ):
            errors.append(
                f"Markdown heading: "
                f"{path}:{number}"
            )

        if stripped.startswith("```"):
            errors.append(
                f"Markdown fence: "
                f"{path}:{number}"
            )

        if "S&P" in line:
            errors.append(
                f"Unescaped S&P: "
                f"{path}:{number}"
            )

        if (
            len(stripped) >= 2
            and set(stripped) == {"="}
        ):
            errors.append(
                f"Repeated '=' corruption: "
                f"{path}:{number}"
            )

        if (
            len(stripped) >= 2
            and set(stripped) == {"-"}
        ):
            errors.append(
                f"Repeated '-' corruption: "
                f"{path}:{number}"
            )

    for label in re.findall(
        r"\\label\{([^}]+)\}",
        text,
    ):
        all_labels.append(
            (label, str(path))
        )

    for ref in re.findall(
        r"\\(?:ref|eqref|autoref)\{([^}]+)\}",
        text,
    ):
        all_refs.append(
            (ref, str(path))
        )


label_names = [
    label
    for label, _ in all_labels
]

duplicates = sorted({
    label
    for label in label_names
    if label_names.count(label) > 1
})

for label in duplicates:
    errors.append(
        f"Duplicate label: {label}"
    )

label_set = set(label_names)

for ref, path in all_refs:
    if ref not in label_set:
        errors.append(
            f"Undefined internal reference "
            f"{ref} in {path}"
        )


# ============================================================
# Citation keys vs bibliography
# ============================================================

bib_text = (
    BIB.read_text(
        encoding="utf-8"
    )
    if BIB.exists()
    else ""
)

bib_keys = set(
    re.findall(
        r"@\w+\{([^,]+),",
        bib_text,
    )
)

citation_keys: set[str] = set()

citation_pattern = re.compile(
    r"\\(?:textcite|parencite|cite|autocite)"
    r"(?:\[[^\]]*\])?"
    r"(?:\[[^\]]*\])?"
    r"\{([^}]+)\}"
)

for text in texts.values():
    for group in citation_pattern.findall(text):
        for key in group.split(","):
            citation_keys.add(
                key.strip()
            )

missing_bib = sorted(
    citation_keys - bib_keys
)

for key in missing_bib:
    errors.append(
        f"Citation key absent from bibliography: {key}"
    )


# ============================================================
# Compilation log / page limit
# ============================================================

page_count = None

if not LOG.exists():
    errors.append(
        "main.log missing"
    )
else:
    log = LOG.read_text(
        encoding="utf-8",
        errors="replace",
    )

    page_matches = re.findall(
        r"MAIN_THESIS_PAGES=(\d+)",
        log,
    )

    if not page_matches:
        errors.append(
            "MAIN_THESIS_PAGES absent from main.log"
        )
    else:
        page_count = int(
            page_matches[-1]
        )

        if page_count > 35:
            errors.append(
                f"University page limit exceeded: "
                f"{page_count}/35"
            )

    log_errors = [
        "undefined citations",
        "citation undefined",
        "undefined references",
        "empty bibliography",
        "please rerun biber",
    ]

    for phrase in log_errors:
        if phrase in log.lower():
            errors.append(
                f"LaTeX log issue: {phrase}"
            )


# ============================================================
# Size / section overview
# ============================================================

word_counts = {}

for path, text in texts.items():
    word_counts[path.name] = len(
        text.split()
    )


# ============================================================
# Output
# ============================================================

print("=" * 100)
print("FINAL LATEX THESIS AUDIT")
print("=" * 100)

print()
print("SECTION WORD COUNTS")
print("-" * 100)

for filename, words in word_counts.items():
    print(
        f"{filename:<32} "
        f"{words:>7}"
    )

print("-" * 100)

print(
    f"{'TOTAL':<32} "
    f"{sum(word_counts.values()):>7}"
)

print()

if page_count is not None:
    print(
        f"MAIN THESIS PAGES: "
        f"{page_count} / 35"
    )
    print(
        f"PAGE MARGIN: "
        f"{35 - page_count}"
    )

print()
print(
    f"CITATION KEYS USED: "
    f"{len(citation_keys)}"
)
print(
    f"BIBLIOGRAPHY ENTRIES: "
    f"{len(bib_keys)}"
)

print()
print("WARNINGS")
print("-" * 100)

if warnings:
    for warning in warnings:
        print(
            "WARNING —",
            warning,
        )
else:
    print("None")

print()
print("ERRORS")
print("-" * 100)

if errors:
    for error in errors:
        print(
            "ERROR —",
            error,
        )

    print()
    print("=" * 100)
    print("FINAL LATEX THESIS AUDIT FAILED")
    print("=" * 100)

    raise SystemExit(1)

print("None")
print()
print("=" * 100)
print("FINAL LATEX THESIS AUDIT PASSED")
print("=" * 100)
