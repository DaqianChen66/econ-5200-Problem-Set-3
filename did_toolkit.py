"""Difference-in-differences toolkit for ECON 5200 PS3."""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def two_by_two(
    df: pd.DataFrame,
    treated: str,
    post: str,
    outcome: str
) -> float:
    """Return a simple 2x2 DiD estimate."""
    m = df.groupby([treated, post])[outcome].mean()
    return float((m[1, 1] - m[1, 0]) - (m[0, 1] - m[0, 0]))


def clean_att(
    df: pd.DataFrame,
    outcome: str,
    cohort: str,
    time: str,
    never: int = 10**9
) -> tuple[pd.DataFrame, float]:
    """Estimate ATT using never- or not-yet-treated controls."""
    rows = []

    for g in sorted(x for x in df[cohort].unique() if x < never):
        tr = df[df[cohort] == g]
        base = g - 1

        for t in range(g, int(df[time].max()) + 1):
            co = df[df[cohort] > t]

            att = (
                tr.loc[tr[time] == t, outcome].mean()
                - tr.loc[tr[time] == base, outcome].mean()
                - co.loc[co[time] == t, outcome].mean()
                + co.loc[co[time] == base, outcome].mean()
            )

            rows.append((g, t, att, (tr[time] == t).sum()))

    cells = pd.DataFrame(rows, columns=["g", "t", "att", "n"])
    overall = np.average(cells["att"], weights=cells["n"])

    return cells, float(overall)


def event_study(
    df: pd.DataFrame,
    outcome: str,
    cohort: str,
    time: str,
    unit: str,
    never: int = 10**9,
    ref_period: int = -1
) -> pd.Series:
    """Estimate a TWFE event study with one omitted reference period."""
    x = df.copy()

    x["_e"] = np.where(
        x[cohort] < never,
        x[time] - x[cohort],
        np.nan
    )

    times = sorted(int(e) for e in x["_e"].dropna().unique())
    cols = {}

    for e in times:
        if e == ref_period:
            continue

        name = f"_pre{-e}" if e < 0 else f"_post{e}"
        cols[e] = name
        x[name] = (x["_e"] == e).astype(int)

    formula = (
        f"{outcome} ~ "
        + " + ".join(cols.values())
        + f" + C({unit}) + C({time})"
    )

    fit = smf.ols(formula, data=x).fit()

    return pd.Series({
        e: 0.0 if e == ref_period else fit.params[cols[e]]
        for e in times
    })


def clustered_inference(
    df: pd.DataFrame,
    formula: str,
    treatment: str,
    cluster: str
) -> dict[str, float]:
    """Run OLS with cluster-robust standard errors."""
    fit = smf.ols(formula, data=df).fit(
        cov_type="cluster",
        cov_kwds={"groups": df[cluster]}
    )

    return {
        "estimate": float(fit.params[treatment]),
        "se": float(fit.bse[treatment]),
        "pvalue": float(fit.pvalues[treatment])
    }


def wild_cluster_bootstrap(
    df: pd.DataFrame,
    outcome: str,
    treatment: str,
    unit: str,
    time: str,
    cluster: str
) -> dict[str, float | int]:
    """Enumerate all Rademacher wild-cluster bootstrap draws."""
    restricted = smf.ols(
        f"{outcome} ~ C({unit}) + C({time})",
        data=df
    ).fit()

    fitted = restricted.fittedvalues.to_numpy()
    resid = restricted.resid.to_numpy()

    formula = f"{outcome} ~ {treatment} + C({unit}) + C({time})"

    actual = smf.ols(formula, data=df).fit(
        cov_type="cluster",
        cov_kwds={"groups": df[cluster]}
    )

    clusters = sorted(df[cluster].unique())
    t_boot = []

    for k in range(2 ** len(clusters)):
        signs = [
            1 if (k >> j) & 1 else -1
            for j in range(len(clusters))
        ]

        weights = df[cluster].map(
            dict(zip(clusters, signs))
        ).to_numpy()

        boot = df.copy()
        boot["_y"] = fitted + weights * resid

        fit = smf.ols(
            f"_y ~ {treatment} + C({unit}) + C({time})",
            data=boot
        ).fit(
            cov_type="cluster",
            cov_kwds={"groups": boot[cluster]}
        )

        t_boot.append(fit.tvalues[treatment])

    p_boot = np.mean(
        np.abs(t_boot) >= abs(actual.tvalues[treatment])
    )

    return {
        "estimate": float(actual.params[treatment]),
        "se": float(actual.bse[treatment]),
        "t_actual": float(actual.tvalues[treatment]),
        "cluster_pvalue": float(actual.pvalues[treatment]),
        "bootstrap_pvalue": float(p_boot),
        "n_vectors": len(t_boot)
    }


if __name__ == "__main__":
    test = pd.DataFrame({
        "treated": [0, 0, 1, 1],
        "post": [0, 1, 0, 1],
        "y": [1, 2, 1, 4]
    })

    assert np.isclose(
        two_by_two(test, "treated", "post", "y"),
        2.0
    )

    assert callable(clean_att)
    assert callable(event_study)
    assert callable(clustered_inference)
    assert callable(wild_cluster_bootstrap)

    print("did_toolkit checks passed.")

