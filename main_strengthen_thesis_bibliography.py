from pathlib import Path


BIB = Path(
    "thesis/latex/references.bib"
)

LITERATURE = Path(
    "thesis/latex/sections/"
    "02_literature_review.tex"
)

METHODOLOGY = Path(
    "thesis/latex/sections/"
    "03_data_methodology.tex"
)


bib = BIB.read_text(
    encoding="utf-8"
)

literature = LITERATURE.read_text(
    encoding="utf-8"
)

methodology = METHODOLOGY.read_text(
    encoding="utf-8"
)


# ============================================================
# NEW BIBLIOGRAPHIC ENTRIES
# ============================================================

new_entries = r"""
@article{AndersenBollerslevDieboldLabys2003,
  author  = {Andersen, Torben G. and Bollerslev, Tim and Diebold, Francis X. and Labys, Paul},
  title   = {Modeling and Forecasting Realized Volatility},
  journal = {Econometrica},
  year    = {2003},
  volume  = {71},
  number  = {2},
  pages   = {579--625},
  doi     = {10.1111/1468-0262.00418}
}

@article{JiangTian2005,
  author  = {Jiang, George J. and Tian, Yisong S.},
  title   = {The Model-Free Implied Volatility and Its Information Content},
  journal = {The Review of Financial Studies},
  year    = {2005},
  volume  = {18},
  number  = {4},
  pages   = {1305--1342},
  doi     = {10.1093/rfs/hhi027}
}

@article{Todorov2010,
  author  = {Todorov, Viktor},
  title   = {Variance Risk-Premium Dynamics: The Role of Jumps},
  journal = {The Review of Financial Studies},
  year    = {2010},
  volume  = {23},
  number  = {1},
  pages   = {345--383},
  doi     = {10.1093/rfs/hhp035}
}

@article{BollerslevGibsonZhou2011,
  author  = {Bollerslev, Tim and Gibson, Michael and Zhou, Hao},
  title   = {Dynamic Estimation of Volatility Risk Premia and Investor Risk Aversion from Option-Implied and Realized Volatilities},
  journal = {Journal of Econometrics},
  year    = {2011},
  volume  = {160},
  number  = {1},
  pages   = {235--245},
  doi     = {10.1016/j.jeconom.2010.03.033}
}

@article{BekaertHoerova2014,
  author  = {Bekaert, Geert and Hoerova, Marie},
  title   = {The VIX, the Variance Premium and Stock Market Volatility},
  journal = {Journal of Econometrics},
  year    = {2014},
  volume  = {183},
  number  = {2},
  pages   = {181--192},
  doi     = {10.1016/j.jeconom.2014.05.008}
}

@article{BollerslevMarroneXuZhou2014,
  author  = {Bollerslev, Tim and Marrone, James and Xu, Lai and Zhou, Hao},
  title   = {Stock Return Predictability and Variance Risk Premia: Statistical Inference and International Evidence},
  journal = {Journal of Financial and Quantitative Analysis},
  year    = {2014},
  volume  = {49},
  number  = {3},
  pages   = {633--661},
  doi     = {10.1017/S0022109014000453}
}

@article{AngTimmermann2012,
  author  = {Ang, Andrew and Timmermann, Allan},
  title   = {Regime Changes and Financial Markets},
  journal = {Annual Review of Financial Economics},
  year    = {2012},
  volume  = {4},
  pages   = {313--337},
  doi     = {10.1146/annurev-financial-110311-101808}
}

@article{WelchGoyal2008,
  author  = {Welch, Ivo and Goyal, Amit},
  title   = {A Comprehensive Look at The Empirical Performance of Equity Premium Prediction},
  journal = {The Review of Financial Studies},
  year    = {2008},
  volume  = {21},
  number  = {4},
  pages   = {1455--1508},
  doi     = {10.1093/rfs/hhm014}
}

@article{CampbellThompson2008,
  author  = {Campbell, John Y. and Thompson, Samuel B.},
  title   = {Predicting Excess Stock Returns Out of Sample: Can Anything Beat the Historical Average?},
  journal = {The Review of Financial Studies},
  year    = {2008},
  volume  = {21},
  number  = {4},
  pages   = {1509--1531},
  doi     = {10.1093/rfs/hhm055}
}

@article{GoyalWelchZafirov2024,
  author  = {Goyal, Amit and Welch, Ivo and Zafirov, Athanasse},
  title   = {A Comprehensive 2022 Look at the Empirical Performance of Equity Premium Prediction},
  journal = {The Review of Financial Studies},
  year    = {2024},
  volume  = {37},
  number  = {11},
  pages   = {3490--3557},
  doi     = {10.1093/rfs/hhae044}
}

@article{KandelStambaugh1996,
  author  = {Kandel, Shmuel and Stambaugh, Robert F.},
  title   = {On the Predictability of Stock Returns: An Asset-Allocation Perspective},
  journal = {The Journal of Finance},
  year    = {1996},
  volume  = {51},
  number  = {2},
  pages   = {385--424},
  doi     = {10.1111/j.1540-6261.1996.tb02689.x}
}

@article{FlemingKirbyOstdiek2001,
  author  = {Fleming, Jeff and Kirby, Chris and Ostdiek, Barbara},
  title   = {The Economic Value of Volatility Timing},
  journal = {The Journal of Finance},
  year    = {2001},
  volume  = {56},
  number  = {1},
  pages   = {329--352},
  doi     = {10.1111/0022-1082.00327}
}

@article{MoreiraMuir2017,
  author  = {Moreira, Alan and Muir, Tyler},
  title   = {Volatility-Managed Portfolios},
  journal = {The Journal of Finance},
  year    = {2017},
  volume  = {72},
  number  = {4},
  pages   = {1611--1644},
  doi     = {10.1111/jofi.12513}
}

@article{Breiman2001,
  author  = {Breiman, Leo},
  title   = {Random Forests},
  journal = {Machine Learning},
  year    = {2001},
  volume  = {45},
  pages   = {5--32},
  doi     = {10.1023/A:1010933404324}
}

@article{Kunsch1989,
  author  = {Kunsch, Hans R.},
  title   = {The Jackknife and the Bootstrap for General Stationary Observations},
  journal = {The Annals of Statistics},
  year    = {1989},
  volume  = {17},
  number  = {3},
  pages   = {1217--1241},
  doi     = {10.1214/aos/1176347265}
}

@article{PerignonEtAl2024,
  author  = {Pérignon, Christophe and Akmansoy, Olivier and Hurlin, Christophe and Dreber, Anna and Holzmeister, Felix and Huber, Jürgen and Johannesson, Magnus and Kirchler, Michael and Menkveld, Albert J. and Razen, Michael and Weitzel, Utz},
  title   = {Computational Reproducibility in Finance: Evidence from 1,000 Tests},
  journal = {The Review of Financial Studies},
  year    = {2024},
  volume  = {37},
  number  = {11},
  pages   = {3558--3593},
  doi     = {10.1093/rfs/hhae029}
}
""".strip()


new_keys = [
    "AndersenBollerslevDieboldLabys2003",
    "JiangTian2005",
    "Todorov2010",
    "BollerslevGibsonZhou2011",
    "BekaertHoerova2014",
    "BollerslevMarroneXuZhou2014",
    "AngTimmermann2012",
    "WelchGoyal2008",
    "CampbellThompson2008",
    "GoyalWelchZafirov2024",
    "KandelStambaugh1996",
    "FlemingKirbyOstdiek2001",
    "MoreiraMuir2017",
    "Breiman2001",
    "Kunsch1989",
    "PerignonEtAl2024",
]


for key in new_keys:
    if f"{{{key}," in bib:
        raise SystemExit(
            f"FAIL — bibliography key already exists: {key}"
        )


new_bib = (
    bib.rstrip()
    + "\n\n"
    + new_entries
    + "\n"
)


# ============================================================
# LITERATURE PATCH 1
# MEASUREMENT
# ============================================================

marker = (
    "The distinction between a theoretical variance risk premium "
    "and an empirical proxy is important. A volatility index is "
    "not itself a realized return on a variance-swap position. "
    "It summarizes option-implied information under a specific "
    "index methodology. Likewise, realized variance depends on "
    "sampling frequency, horizon, and annualization. Consequently, "
    "the thesis uses VIX- and VSTOXX-based measures as empirical "
    "proxies for the underlying variance-pricing mechanism rather "
    "than claiming to observe the exact contractual variance premium."
)

addition = r"""

The measurement literature makes this distinction particularly important. \textcite{AndersenBollerslevDieboldLabys2003} establish the role of high-frequency returns in constructing realized-volatility measures, while \textcite{JiangTian2005} show that model-free option-implied volatility contains substantial information about future realized volatility. \textcite{BollerslevGibsonZhou2011} combine model-free implied and realized volatility measures to estimate a time-varying volatility risk premium. These papers define a more demanding measurement benchmark than the monthly index-based proxies available in the present data set. They therefore support the economic interpretation of the implied--realized variance gap while also reinforcing the need not to treat the proxy used here as an exact observation of a contractual variance premium.
""".strip()

if literature.count(marker) != 1:
    raise SystemExit(
        "FAIL — measurement marker not found exactly once"
    )

literature = literature.replace(
    marker,
    marker + "\n\n" + addition,
    1,
)


# ============================================================
# LITERATURE PATCH 2
# JUMP / TAIL INTERPRETATION
# ============================================================

marker = (
    "\\textcite{DrechslerYaron2011} provide a complementary "
    "equilibrium interpretation. They define the variance premium "
    "using squared VIX relative to expected realized variance and "
    "show that it contains information about attitudes toward "
    "economic uncertainty. Their framework generates time variation "
    "in the premium and links that variation to return predictability. "
    "This interpretation reinforces the view that the variance premium "
    "can simultaneously represent a priced risk and a state variable."
)

addition = r"""

The downside nature of this compensation is also visible in jump risk. \textcite{Todorov2010} decomposes variance-risk-premium dynamics into diffusive and jump components and finds that the price of jump protection responds strongly to extreme market movements. This evidence is relevant for the direct-payoff channel because it emphasizes that average short-variance carry is inseparable from exposure to infrequent but potentially severe losses.
""".strip()

if literature.count(marker) != 1:
    raise SystemExit(
        "FAIL — jump-risk marker not found exactly once"
    )

literature = literature.replace(
    marker,
    marker + "\n\n" + addition,
    1,
)


# ============================================================
# LITERATURE PATCH 3
# PREDICTABILITY / INTERNATIONAL / RECENT EVIDENCE
# ============================================================

marker = (
    "The same caution applies to transformations of the premium. "
    "A raw difference and a relative implied-to-realized variance "
    "measure can encode different information when the volatility "
    "level changes. This thesis consequently treats alternative VRP "
    "transformations as competing empirical features rather than "
    "assuming ex ante that one representation is universally superior."
)

addition = r"""

Subsequent evidence also shows why predictability should not be treated as universal. \textcite{BekaertHoerova2014} show that conclusions about the predictive content of the variance premium depend materially on how conditional physical variance is estimated. Using international evidence, \textcite{BollerslevMarroneXuZhou2014} find broadly similar variance-risk-premium return-predictability patterns across several developed markets and even stronger predictability for a global VRP measure. More recently, \textcite{GoyalWelchZafirov2024} re-examine a large set of equity-premium predictors over extended samples and document substantial deterioration in many previously reported relationships. For the VRP specification of \textcite{BollerslevTauchenZhou2009}, the coefficient is no longer statistically significant in their extended-sample specification; its out-of-sample predictive evidence is weak and its investment performance is poor. These findings make cross-market comparison, genuine out-of-sample evaluation, and conservative interpretation central rather than optional features of the present design.
""".strip()

if literature.count(marker) != 1:
    raise SystemExit(
        "FAIL — predictability marker not found exactly once"
    )

literature = literature.replace(
    marker,
    marker + "\n\n" + addition,
    1,
)


# ============================================================
# LITERATURE PATCH 4
# REGIME-SWITCHING REVIEW
# ============================================================

marker = (
    "\\textcite{GuidolinTimmermann2007} provide further evidence "
    "in a stock--bond setting. Their regime-switching model "
    "identifies distinct states associated with substantially "
    "different return distributions. Optimal allocations change "
    "as investors update state probabilities, and their out-of-sample "
    "analysis supports the economic relevance of accounting for regimes."
)

addition = r"""

More broadly, \textcite{AngTimmermann2012} review the evidence on regime changes in financial markets and emphasize that regime-switching models can capture persistent shifts in means, volatilities, correlations, and other distributional features. This broader evidence supports the use of latent-state models while also cautioning against interpreting an estimated regime as a uniquely identified economic state.
""".strip()

if literature.count(marker) != 1:
    raise SystemExit(
        "FAIL — regime marker not found exactly once"
    )

literature = literature.replace(
    marker,
    marker + "\n\n" + addition,
    1,
)


# ============================================================
# LITERATURE PATCH 5
# ECONOMIC VALUE / OOS / VOLATILITY TIMING
# ============================================================

marker = (
    "\\textcite{DeMiguelGarlappiUppal2009} provide a strong "
    "benchmark for this principle. They compare fourteen portfolio "
    "models across seven empirical data sets and find that none "
    "consistently outperforms the naive \\(1/N\\) rule in Sharpe "
    "ratio, certainty-equivalent return, and turnover. Their results "
    "illustrate how estimation error can eliminate the apparent "
    "gains from more complex portfolio rules."
)

addition = r"""

The distinction between statistical predictability and economic value has a long portfolio-choice tradition. \textcite{KandelStambaugh1996} show that return-predictability evidence can matter materially for a risk-averse investor even when statistical uncertainty is substantial. At the same time, \textcite{WelchGoyal2008} document the instability of many equity-premium forecasting variables out of sample, while \textcite{CampbellThompson2008} show that economically meaningful gains can sometimes remain when economically motivated restrictions are imposed. The updated evidence of \textcite{GoyalWelchZafirov2024} reinforces the need to distinguish historical statistical significance from durable investment value.

There is also direct precedent for evaluating volatility information through portfolio outcomes rather than forecasting metrics alone. \textcite{FlemingKirbyOstdiek2001} evaluate the economic value of volatility timing and explicitly examine estimation risk and transaction costs. \textcite{MoreiraMuir2017} show that volatility-managed exposure can improve Sharpe ratios and investor utility in a broad set of portfolios. These findings motivate the risk-scaling and implementation exercises in this thesis, but they do not imply that the same gains must appear for VRP-conditioned stock--bond allocation.
""".strip()

if literature.count(marker) != 1:
    raise SystemExit(
        "FAIL — economic-value marker not found exactly once"
    )

literature = literature.replace(
    marker,
    marker + "\n\n" + addition,
    1,
)


# ============================================================
# METHODOLOGY PATCH 1
# RANDOM FOREST
# ============================================================

marker = (
    "The machine-learning layer provides a nonlinear test of the "
    "incremental information contained in VRP features. Three "
    "classifier families are considered: penalized logistic regression, "
    "Random Forest, and histogram-based Gradient Boosting. Their role "
    "is predictive rather than structural; they do not replace the "
    "economic interpretation of the variance premium. This use of "
    "flexible prediction methods is consistent with the broader "
    "asset-pricing evidence discussed by \\textcite{GuKellyXiu2020}."
)

replacement = (
    "The machine-learning layer provides a nonlinear test of the "
    "incremental information contained in VRP features. Three "
    "classifier families are considered: penalized logistic regression, "
    "Random Forest, and histogram-based Gradient Boosting. The Random "
    "Forest specification follows the ensemble-tree framework introduced "
    "by \\textcite{Breiman2001}. Their role is predictive rather than "
    "structural; they do not replace the economic interpretation of the "
    "variance premium. This use of flexible prediction methods is "
    "consistent with the broader asset-pricing evidence discussed by "
    "\\textcite{GuKellyXiu2020}."
)

if methodology.count(marker) != 1:
    raise SystemExit(
        "FAIL — ML marker not found exactly once"
    )

methodology = methodology.replace(
    marker,
    replacement,
    1,
)


# ============================================================
# METHODOLOGY PATCH 2
# BLOCK BOOTSTRAP
# ============================================================

marker = (
    "Sampling uncertainty is assessed using a paired moving-block "
    "bootstrap. Strategy and benchmark returns are resampled jointly "
    "so that cross-strategy dependence is preserved. The baseline "
    "procedure uses 2,000 bootstrap replications and six-month blocks. "
    "Welfare differences are evaluated against both the 60/40 and "
    "equal-weighted benchmarks. A strategy is classified as statistically "
    "superior only when the lower bound of the corresponding bootstrap "
    "confidence interval is above zero."
)

replacement = (
    "Sampling uncertainty is assessed using a paired moving-block "
    "bootstrap, following the block-resampling logic developed for "
    "dependent stationary observations by \\textcite{Kunsch1989}. "
    "Strategy and benchmark returns are resampled jointly so that "
    "cross-strategy dependence is preserved. The baseline procedure "
    "uses 2,000 bootstrap replications and six-month blocks. Welfare "
    "differences are evaluated against both the 60/40 and equal-weighted "
    "benchmarks. A strategy is classified as statistically superior "
    "only when the lower bound of the corresponding bootstrap confidence "
    "interval is above zero."
)

if methodology.count(marker) != 1:
    raise SystemExit(
        "FAIL — bootstrap marker not found exactly once"
    )

methodology = methodology.replace(
    marker,
    replacement,
    1,
)


# ============================================================
# METHODOLOGY PATCH 3
# REPRODUCIBILITY
# ============================================================

marker = (
    "All empirical analyses in this thesis are implemented in Python. "
    "The project repository separates data ingestion and feature "
    "construction, econometric and machine-learning models, portfolio "
    "construction, welfare analysis, robustness testing, reporting, "
    "and LaTeX production. The empirical tables and figures reported "
    "in the thesis are generated from the same codebase used to estimate "
    "the models and construct the portfolios rather than being "
    "reconstructed manually for presentation."
)

replacement = (
    "All empirical analyses in this thesis are implemented in Python. "
    "The project repository separates data ingestion and feature "
    "construction, econometric and machine-learning models, portfolio "
    "construction, welfare analysis, robustness testing, reporting, "
    "and LaTeX production. The empirical tables and figures reported "
    "in the thesis are generated from the same codebase used to estimate "
    "the models and construct the portfolios rather than being "
    "reconstructed manually for presentation. This emphasis is consistent "
    "with the reproducibility concerns documented in empirical finance "
    "by \\textcite{PerignonEtAl2024}."
)

if methodology.count(marker) != 1:
    raise SystemExit(
        "FAIL — reproducibility marker not found exactly once"
    )

methodology = methodology.replace(
    marker,
    replacement,
    1,
)


# ============================================================
# FINAL VALIDATION BEFORE ANY FILE IS WRITTEN
# ============================================================

combined_text = (
    literature
    + "\n"
    + methodology
)

for key in new_keys:
    if f"{{{key}," not in new_bib:
        raise SystemExit(
            f"FAIL — bibliography missing {key}"
        )

    if key not in combined_text:
        raise SystemExit(
            f"FAIL — new source is not cited: {key}"
        )


expected_total_entries = 25

actual_entries = new_bib.count(
    "@article{"
)

if actual_entries != expected_total_entries:
    raise SystemExit(
        "FAIL — expected "
        f"{expected_total_entries} bibliography entries, "
        f"found {actual_entries}"
    )


# ============================================================
# WRITE ONLY AFTER ALL CHECKS PASS
# ============================================================

BIB.write_text(
    new_bib,
    encoding="utf-8",
)

LITERATURE.write_text(
    literature,
    encoding="utf-8",
)

METHODOLOGY.write_text(
    methodology,
    encoding="utf-8",
)


print("=" * 88)
print("THESIS BIBLIOGRAPHY STRENGTHENING")
print("=" * 88)
print()
print(
    "PASS — 16 new academic references added"
)
print(
    "PASS — all 16 new references are cited"
)
print(
    "PASS — Literature Review strengthened"
)
print(
    "PASS — methodology citations strengthened"
)
print(
    "PASS — bibliography now contains 25 entries"
)
print()
print(
    "No empirical result or numerical conclusion "
    "was modified."
)
