"""Generate the report's evidence-bearing figures from verifier JSON."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


COLORS = {
    "ink": "#172033",
    "red": "#b42318",
    "orange": "#d97706",
    "blue": "#2563eb",
    "green": "#15803d",
    "pale": "#f5f7fb",
}


def _load(root: Path, claim: int, name: str) -> dict:
    path = root / ".openresearch" / "artifacts" / f"claim_{claim}" / name
    return json.loads(path.read_text(encoding="utf-8"))


def _finish(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def make_all_figures(root: Path) -> list[str]:
    out = root / "reports" / "claim-by-claim" / "images"
    out.mkdir(parents=True, exist_ok=True)
    verdicts = {i: _load(root, i, "verdict.json") for i in range(1, 7)}

    fig, axes = plt.subplots(2, 3, figsize=(13, 6.8))
    metrics = [
        ("1 · Fourier identity", "Eq. 7 residual", verdicts[1]["equation_7_absolute_residual"]),
        ("2 · Entropic bound", "violation margin", verdicts[2]["violation_margin"]),
        ("3 · Decaying entropy", "violation margin", verdicts[3]["violation_margin"]),
        ("4 · Finite basis", "true regret / round", verdicts[4]["actual_ot_per_round_regret"]),
        ("5 · Decay premise", "tail-bound residual", verdicts[5]["finite_tail_bound_residual"]),
        ("6 · Confidence set", "feedback gap", verdicts[6]["different_expected_feedback_gap"]),
    ]
    for ax, (title, label, value) in zip(axes.flat, metrics):
        ax.set_facecolor(COLORS["pale"])
        ax.text(0.05, 0.80, title, transform=ax.transAxes, fontsize=13, weight="bold")
        ax.text(
            0.05,
            0.52,
            "FALSIFIED",
            transform=ax.transAxes,
            fontsize=18,
            weight="bold",
            color=COLORS["red"],
        )
        shown = f"{value:,.3g}"
        ax.text(0.05, 0.27, f"{label}: {shown}", transform=ax.transAxes, fontsize=11)
        ax.text(0.05, 0.08, "independent checker + negative control", transform=ax.transAxes, fontsize=8.5)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#d4d9e2")
    fig.suptitle(
        "Literal arXiv v1 contracts: six reproducible contradictions",
        fontsize=19,
        weight="bold",
        color=COLORS["ink"],
    )
    fig.text(
        0.5,
        0.01,
        "These are source-version verdicts, not a live judge score.",
        ha="center",
        fontsize=10,
        color="#596273",
    )
    headline = out / "headline_claims.png"
    _finish(fig, headline)

    raw1 = _load(root, 1, "raw_result.json")
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
    for ax, key, title in (
        (axes[0], "rho", "Reference ρ"),
        (axes[1], "pi", "Diagonal coupling π"),
        (axes[2], "cost_values", "Cost c(x,y)=(x−y)²"),
    ):
        values = np.asarray(raw1["construction"][key]).reshape(2, 2)
        image = ax.imshow(values, cmap="Blues", vmin=0)
        for (i, j), value in np.ndenumerate(values):
            ax.text(j, i, f"{value:g}", ha="center", va="center", fontsize=13)
        ax.set_title(title, weight="bold")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        fig.colorbar(image, ax=ax, fraction=0.046)
    fig.suptitle(
        "Equation (7): valid transport pairing 0, proposed Fourier pairing 1/2",
        fontsize=16,
        weight="bold",
    )
    fig.text(
        0.5,
        -0.02,
        "All phases equal one on the stated integer support; the transform also maps a norm-1 zero-mean function to zero.",
        ha="center",
        fontsize=9.5,
    )
    fourier = out / "fourier_counterexample.png"
    _finish(fig, fourier)

    labels = ["Theorem 5.1", "Theorem 5.2"]
    lower = np.array([verdicts[2]["printed_regret_lower"], verdicts[3]["printed_regret_lower"]])
    upper = np.array([verdicts[2]["theorem_rhs_upper"], verdicts[3]["theorem_rhs_upper"]])
    x = np.arange(2)
    fig, ax = plt.subplots(figsize=(8.5, 4.7))
    width = 0.34
    ax.bar(x - width / 2, lower, width, label="literal printed regret lower bound", color=COLORS["red"])
    ax.bar(x + width / 2, upper, width, label="complete RHS upper bound", color=COLORS["blue"])
    ax.set_yscale("log")
    ax.set_xticks(x, labels)
    ax.set_ylabel("value at T = 100,000,000 (log scale)")
    ax.set_title("Even an action-uniform RHS upper bound is orders of magnitude smaller", weight="bold")
    ax.legend(frameon=False)
    for i in range(2):
        ax.text(i, lower[i] * 1.12, f"{lower[i]/upper[i]:.0f}×", ha="center", color=COLORS["red"], weight="bold")
    ax.grid(axis="y", which="both", alpha=0.2)
    theorem = out / "theorem_bounds.png"
    _finish(fig, theorem)

    raw4 = _load(root, 4, "raw_result.json")
    transport = raw4["transport"]
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.9))
    arrays = [
        (transport["costs"]["truncated_N2"], "N=2 truncated cost"),
        (transport["ot"]["truncated_cost_solution"]["plan"], "plan selected at N=2"),
        (transport["ot"]["full_cost_solution"]["plan"], "true optimal plan"),
    ]
    for ax, (array, title) in zip(axes, arrays):
        values = np.asarray(array)
        image = ax.imshow(values, cmap="coolwarm")
        for (i, j), value in np.ndenumerate(values):
            ax.text(j, i, f"{value:.2g}", ha="center", va="center", fontsize=10)
        ax.set_title(title, weight="bold")
        ax.set_xticks(range(3))
        ax.set_yticks(range(3))
        fig.colorbar(image, ax=ax, fraction=0.046)
    fig.suptitle(
        "Corollary 5.3 premise admits an omitted direction that changes the OT optimum",
        fontsize=15.5,
        weight="bold",
    )
    fig.text(
        0.5,
        -0.02,
        "The prescribed N=2 plan loses exactly 1 per round under the full cost; including coefficient 3 gives zero regret.",
        ha="center",
        fontsize=9.5,
    )
    basis = out / "basis_ot.png"
    _finish(fig, basis)

    raw5 = _load(root, 5, "raw_result.json")
    raw6 = _load(root, 6, "raw_result.json")
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4))
    qrows = raw5["q_sweep"]
    qs = [row["q"] for row in qrows]
    actual = [row["actual_tail_l1"] for row in qrows]
    claimed = [row["paper_derived_tail_bound"] for row in qrows]
    axes[0].plot(qs, actual, "o-", color=COLORS["red"], label="actual admitted tail")
    axes[0].plot(qs, claimed, "o-", color=COLORS["blue"], label="proof's claimed upper bound")
    axes[0].set_xscale("log", base=2)
    axes[0].set_yscale("log")
    axes[0].set_xlabel("q")
    axes[0].set_ylabel("tail after n=2")
    axes[0].set_title("Assumption 3 does not imply its tail bound", weight="bold")
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=0.2)

    contradiction = raw6["transport_model_contradiction"]
    axes[1].bar(
        ["feature distance", "expected-feedback gap"],
        [contradiction["maximum_feature_difference"], contradiction["mean_gap"]],
        color=[COLORS["blue"], COLORS["red"]],
    )
    axes[1].set_ylim(0, 1.15)
    axes[1].set_title("Identical features, incompatible feedback", weight="bold")
    axes[1].text(
        0.5,
        0.76,
        "corrected OFUL control:\nexact coverage = 1.0\nrequired = 0.9",
        transform=axes[1].transAxes,
        ha="center",
        fontsize=11,
        bbox={"boxstyle": "round", "facecolor": COLORS["pale"], "edgecolor": "#d4d9e2"},
    )
    fig.suptitle("Rate-premise and confidence-model diagnostics", fontsize=16, weight="bold")
    diagnostics = out / "confidence_decay.png"
    _finish(fig, diagnostics)

    paths = [headline, fourier, theorem, basis, diagnostics]
    return [str(path.relative_to(root)) for path in paths]
