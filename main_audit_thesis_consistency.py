from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys


THESIS = Path("thesis")

DOCUMENTS = {
    "abstract": (
        THESIS
        / "abstract_keywords.md"
    ),
    "introduction": (
        THESIS
        / "introduction_draft.md"
    ),
    "methodology": (
        THESIS
        / (
            "chapter_2_data_"
            "methodology_draft.md"
        )
    ),
    "results": (
        THESIS
        / (
            "chapter_3_empirical_"
            "results_draft.md"
        )
    ),
    "robustness": (
        THESIS
        / (
            "chapter_4_robustness_"
            "implementation_draft.md"
        )
    ),
    "conclusion": (
        THESIS
        / (
            "chapter_5_limitations_"
            "conclusion_draft.md"
        )
    ),
}

EMPIRICAL_PACK = (
    THESIS
    / "empirical_update_pack.md"
)

errors: list[str] = []
warnings: list[str] = []


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


def register_error(
    message: str,
) -> None:
    errors.append(message)


def register_warning(
    message: str,
) -> None:
    warnings.append(message)


def require_marker(
    label: str,
    text: str,
    marker: str,
) -> None:
    if normalize(marker) not in normalize(text):
        register_error(
            f"{label}: missing marker: "
            f"{marker}"
        )


def forbid_marker(
    label: str,
    text: str,
    marker: str,
) -> None:
    if normalize(marker) in normalize(text):
        register_error(
            f"{label}: stale or forbidden "
            f"marker: {marker}"
        )


def read_document(
    label: str,
    path: Path,
) -> str:
    if not path.exists():
        register_error(
            f"{label}: missing file: {path}"
        )
        return ""

    text = path.read_text(
        encoding="utf-8"
    )

    if not text.strip():
        register_error(
            f"{label}: empty file: {path}"
        )

    for line_number, line in enumerate(
        text.splitlines(),
        start=1,
    ):
        if line.endswith((" ", "\t")):
            register_error(
                f"{label}:{line_number}: "
                "trailing whitespace"
            )

        if "\t" in line:
            register_warning(
                f"{label}:{line_number}: "
                "tab character"
            )

    return text


texts = {
    label: read_document(
        label,
        path,
    )
    for label, path in DOCUMENTS.items()
}

if not EMPIRICAL_PACK.exists():
    register_error(
        f"Missing empirical source: "
        f"{EMPIRICAL_PACK}"
    )
    empirical_pack = ""
else:
    empirical_pack = (
        EMPIRICAL_PACK.read_text(
            encoding="utf-8"
        )
    )


STALE_MARKERS = [
    "collapses in Europe",
    "collapses in the European",
    (
        "more useful as a "
        "regime-state variable"
    ),
    (
        "more useful as a conditional "
        "market-state signal"
    ),
    (
        "best understood as a conditional "
        "market-state signal"
    ),
    (
        "Direct synthetic VRP exposure "
        "is not robust"
    ),
    (
        "when it is directly traded, "
        "or when it is used"
    ),
    "200 monthly observations",
    "127 observations",
    "-2.8511",
    "-0.3625",
    "-0.9901",
    "0.1281",
]

for label, text in texts.items():
    for marker in STALE_MARKERS:
        forbid_marker(
            label,
            text,
            marker,
        )


REQUIRED_BY_DOCUMENT = {
    "abstract": [
        (
            "model-based direct "
            "variance-payoff approximation"
        ),
        "13.08%",
        "1.324",
        (
            "bootstrap confidence "
            "intervals remain positive"
        ),
        (
            "depends critically on "
            "the payoff structure"
        ),
    ],
    "introduction": [
        (
            "signal channel and the "
            "payoff channel"
        ),
        "184",
        "122",
        "232",
        "170",
        (
            "not a reconstructed "
            "variance-swap backtest"
        ),
        (
            "depends critically on "
            "the payoff structure"
        ),
    ],
    "methodology": [
        "4,041 processed observations",
        "195 observations",
        "122 out-of-sample observations",
        "232 observations",
        "170 observations",
        (
            "21-observation "
            "realized-variance measure"
        ),
        "IV_{t-1}",
        "36-month window",
        "minimum of 24 observations",
        "25%",
        "10 basis points",
        "2,000 bootstrap replications",
        "six-month blocks",
        (
            "full absolute notional "
            "entered"
        ),
    ],
    "results": [
        "Equity–bond allocation evidence",
        (
            "Direct variance-payoff "
            "diagnostics"
        ),
        "82.42%",
        "78.35%",
        "6.23%",
        "13.08%",
        "1.324",
        "926.6",
        "898.8",
        (
            "depends critically on "
            "the payoff structure"
        ),
    ],
    "robustness": [
        (
            "Allocation-model "
            "implementation robustness"
        ),
        "Partial rebalancing",
        "25.35%",
        "9.10%",
        (
            "Direct-variance "
            "implementation framework"
        ),
        "50 basis points",
        "12 to 60 months",
        "5% notional cap",
        "Exclude all major crises",
        "141",
        "1.877",
        (
            "robust within the "
            "model-based framework"
        ),
    ],
    "conclusion": [
        "Evaluation of the hypotheses",
        "Data limitations",
        "Measurement limitations",
        (
            "Direct-payoff and "
            "capital-mapping limitations"
        ),
        "Statistical limitations",
        (
            "Cross-market interpretation "
            "limitations"
        ),
        "82.42%",
        "78.35%",
        "927 basis points",
        "899 basis points",
        (
            "Answer to the "
            "research question"
        ),
        "Contribution of the thesis",
        "Future research",
        "Final conclusion",
        (
            "does not identify a "
            "universal trading strategy"
        ),
    ],
}

for label, markers in (
    REQUIRED_BY_DOCUMENT.items()
):
    text = texts[label]

    for marker in markers:
        require_marker(
            label,
            text,
            marker,
        )


MAIN_CONCLUSION = (
    "economic value of the "
    "Variance Risk Premium depends "
    "critically on the payoff structure"
)

for label in [
    "abstract",
    "introduction",
    "results",
    "conclusion",
]:
    require_marker(
        label,
        texts[label],
        MAIN_CONCLUSION,
    )


US_WELFARE_MARKERS = [
    (
        "does not establish "
        "robust welfare dominance"
    ),
    (
        "does not establish "
        "robust investor-welfare dominance"
    ),
    (
        "neither channel establishes "
        "robust investor-welfare dominance"
    ),
]

for label in [
    "abstract",
    "results",
    "conclusion",
]:
    normalized_text = normalize(
        texts[label]
    )

    if not any(
        normalize(marker)
        in normalized_text
        for marker in US_WELFARE_MARKERS
    ):
        register_error(
            f"{label}: missing cautious "
            "United States welfare conclusion"
        )


EU_SIGNIFICANCE_MARKERS = [
    (
        "bootstrap confidence "
        "intervals remain positive"
    ),
    (
        "bootstrap-significant "
        "welfare gains"
    ),
    (
        "statistically significant"
    ),
]

for label in [
    "abstract",
    "results",
    "conclusion",
]:
    normalized_text = normalize(
        texts[label]
    )

    if not any(
        normalize(marker)
        in normalized_text
        for marker in EU_SIGNIFICANCE_MARKERS
    ):
        register_error(
            f"{label}: missing European "
            "statistical-significance conclusion"
        )


PACK_REQUIRED = [
    (
        "Equity–bond allocation "
        "evidence"
    ),
    (
        "Selected direct-variance "
        "evidence"
    ),
    (
        "Welfare evidence at "
        "gamma = 5"
    ),
    (
        "Direct-variance robustness"
    ),
    (
        "Final empirical conclusions"
    ),
    (
        "Mandatory methodological "
        "terminology"
    ),
]

for marker in PACK_REQUIRED:
    require_marker(
        "empirical_pack",
        empirical_pack,
        marker,
    )


heading_pattern = re.compile(
    r"^(?P<hashes>#+)\s+"
    r"(?P<number>\d+(?:\.\d+)+)"
    r"(?:\s+|$)"
)

for label, text in texts.items():
    for line_number, line in enumerate(
        text.splitlines(),
        start=1,
    ):
        match = heading_pattern.match(line)

        if not match:
            continue

        number = match.group("number")
        actual_level = len(
            match.group("hashes")
        )

        expected_level = (
            2 + number.count(".")
        )

        if actual_level != expected_level:
            register_error(
                f"{label}:{line_number}: "
                f"heading {number} uses "
                f"level {actual_level}; "
                f"expected level "
                f"{expected_level}"
            )


word_counts = {
    label: len(text.split())
    for label, text in texts.items()
}

minimum_words = {
    "abstract": 450,
    "introduction": 1_800,
    "methodology": 2_500,
    "results": 2_500,
    "robustness": 3_000,
    "conclusion": 4_000,
}

for label, minimum in (
    minimum_words.items()
):
    if word_counts[label] < minimum:
        register_error(
            f"{label}: only "
            f"{word_counts[label]} words; "
            f"minimum expected is {minimum}"
        )


all_headings: list[str] = []

for text in texts.values():
    all_headings.extend(
        normalize(line.strip())
        for line in text.splitlines()
        if line.startswith("#")
    )

duplicate_headings = {
    heading: count
    for heading, count
    in Counter(all_headings).items()
    if count > 1
    and not heading.startswith(
        "## 1. introduction"
    )
}

for heading, count in sorted(
    duplicate_headings.items()
):
    register_warning(
        f"Repeated heading ({count}x): "
        f"{heading}"
    )


print("=" * 100)
print("THESIS TRANSVERSAL CONSISTENCY AUDIT")
print("=" * 100)

print()
print("WORD COUNTS")
print("-" * 100)

for label, count in word_counts.items():
    print(
        f"{label:<15} {count:>7}"
    )

print(
    f"{'TOTAL':<15} "
    f"{sum(word_counts.values()):>7}"
)

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
        "THESIS TRANSVERSAL AUDIT FAILED"
    )
    print("=" * 100)
    sys.exit(1)

print(
    "THESIS TRANSVERSAL AUDIT PASSED"
)
print("=" * 100)
