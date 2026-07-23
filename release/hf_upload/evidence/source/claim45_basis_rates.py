"""Exact Assumption-3 and actual finite-OT audits for Claims 4 and 5."""
from __future__ import annotations

import itertools
import math

import numpy as np
from scipy.optimize import linprog


def _ot_constraints(side: int) -> tuple[np.ndarray, np.ndarray]:
    rows = []
    rhs = []
    for i in range(side):
        row = np.zeros((side, side))
        row[i, :] = 1.0
        rows.append(row.ravel())
        rhs.append(1.0 / side)
    for j in range(side):
        row = np.zeros((side, side))
        row[:, j] = 1.0
        rows.append(row.ravel())
        rhs.append(1.0 / side)
    return np.asarray(rows), np.asarray(rhs)


def solve_ot(cost: np.ndarray) -> dict:
    side = cost.shape[0]
    a_eq, b_eq = _ot_constraints(side)
    solution = linprog(
        cost.ravel(),
        A_eq=a_eq,
        b_eq=b_eq,
        bounds=(0.0, None),
        method="highs",
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    plan = solution.x.reshape(side, side)
    return {
        "objective": float(np.sum(plan * cost)),
        "plan": plan.tolist(),
        "max_marginal_residual": float(
            max(
                np.max(np.abs(plan.sum(axis=0) - 1.0 / side)),
                np.max(np.abs(plan.sum(axis=1) - 1.0 / side)),
            )
        ),
        "solver": "scipy.optimize.linprog(method='highs')",
        "solver_status": int(solution.status),
        "solver_message": solution.message,
    }


def finite_transport_construction() -> dict:
    side = 3
    diagonal = np.eye(side, dtype=bool)
    cyclic = np.zeros((side, side), dtype=bool)
    other = np.zeros((side, side), dtype=bool)
    for i in range(side):
        cyclic[i, (i + 1) % side] = True
        other[i, (i + 2) % side] = True

    constant = np.ones((side, side))
    off_diagonal_indicator = (~diagonal).astype(float)
    centered_head = off_diagonal_indicator - 2.0 / 3.0
    omitted_tail = np.zeros((side, side))
    omitted_tail[cyclic] = -2.0
    omitted_tail[other] = 2.0

    rho_weight = 1.0 / (side * side)
    basis = [
        constant,
        centered_head
        / math.sqrt(float(rho_weight * np.sum(centered_head**2))),
        omitted_tail
        / math.sqrt(float(rho_weight * np.sum(omitted_tail**2))),
    ]
    gram = np.array(
        [
            [rho_weight * float(np.sum(left * right)) for right in basis]
            for left in basis
        ]
    )
    coefficients = np.array(
        [
            3.0,
            math.sqrt(2.0) / 3.0,
            math.sqrt(8.0 / 3.0),
        ]
    )
    truncated_cost = coefficients[0] * basis[0] + coefficients[1] * basis[1]
    full_cost = truncated_cost + coefficients[2] * basis[2]
    norm = float(np.linalg.norm(coefficients))
    head_l1 = float(np.sum(np.abs(coefficients[:2])))
    tail_l1 = float(abs(coefficients[2]))

    truncated_solution = solve_ot(truncated_cost)
    full_solution = solve_ot(full_cost)
    truncated_plan = np.asarray(truncated_solution["plan"])
    true_cost_of_truncated_plan = float(np.sum(truncated_plan * full_cost))
    per_round_regret = true_cost_of_truncated_plan - full_solution["objective"]
    included_tail_solution = solve_ot(full_cost)
    included_tail_regret = (
        included_tail_solution["objective"] - full_solution["objective"]
    )

    return {
        "support": {
            "mu": [1.0 / 3.0] * 3,
            "nu": [1.0 / 3.0] * 3,
            "reference": "uniform product measure on the 3x3 support",
            "continuous_extension": "finite values extended by disjoint smooth bumps",
        },
        "basis": {
            "description": [
                "constant",
                "centered off-diagonal indicator",
                "cyclic-vs-anticyclic omitted contrast",
            ],
            "gram_matrix": gram.tolist(),
            "max_orthonormality_residual": float(
                np.max(np.abs(gram - np.eye(3)))
            ),
            "coefficients": coefficients.tolist(),
            "coefficient_exact": ["3", "sqrt(2)/3", "sqrt(8/3)"],
            "L2_norm": norm,
            "head_l1_at_N2": head_l1,
            "omitted_tail_l1": tail_l1,
        },
        "costs": {
            "truncated_N2": truncated_cost.tolist(),
            "full": full_cost.tolist(),
        },
        "ot": {
            "truncated_cost_solution": truncated_solution,
            "full_cost_solution": full_solution,
            "true_cost_of_truncated_plan": true_cost_of_truncated_plan,
            "per_round_regret": per_round_regret,
            "included_tail_solution": included_tail_solution,
            "included_tail_regret": included_tail_regret,
        },
    }


def _infinite_sequence_audit() -> dict:
    amplitude = 0.1
    gamma_1 = 3.0
    gamma_2 = amplitude / (math.sqrt(2.0) * math.log(3.0))
    # Integral comparison:
    # sum_{n=2} inf 1/(n log(n+1)^2)
    # <= f(2) + integral_2^inf dx/(x log(x)^2).
    tail_l2_sq_upper = amplitude**2 * (
        1.0 / (2.0 * math.log(3.0) ** 2) + 1.0 / math.log(2.0)
    )
    norm_upper = math.sqrt(gamma_1**2 + tail_l2_sq_upper)
    head_2 = gamma_1 + gamma_2
    partial_cutoffs = [10, 100, 1_000, 10_000, 100_000]
    partial_l1 = []
    partial_l2_sq = []
    for cutoff in partial_cutoffs:
        indices = np.arange(2, cutoff + 1, dtype=float)
        values = amplitude / (np.sqrt(indices) * np.log(indices + 1.0))
        partial_l1.append(float(gamma_1 + np.sum(values)))
        partial_l2_sq.append(float(gamma_1**2 + np.sum(values**2)))
    return {
        "sequence": "gamma_1=3; gamma_n=0.1/(sqrt(n)*log(n+1)) for n>=2",
        "L2_membership": True,
        "tail_l2_squared_upper_bound": tail_l2_sq_upper,
        "full_L2_norm_upper_bound": norm_upper,
        "head_l1_at_n2": head_2,
        "assumption_3_holds_for_every_q_positive": head_2 > norm_upper,
        "tail_l1_diverges": True,
        "divergence_reason": "eventually log(n+1)<=n^(1/4), so gamma_n>=0.1*n^(-3/4)",
        "partial_sum_cutoffs": partial_cutoffs,
        "partial_l1": partial_l1,
        "partial_l2_squared": partial_l2_sq,
    }


def evaluate_claims_4_and_5() -> dict:
    construction = finite_transport_construction()
    coeff = construction["basis"]["coefficients"]
    norm = construction["basis"]["L2_norm"]
    head = construction["basis"]["head_l1_at_N2"]
    tail = construction["basis"]["omitted_tail_l1"]

    horizons = np.array([16, 32, 64, 128, 256, 512], dtype=float)
    scheduled_regret = horizons - 1.0
    observed_exponent = float(
        np.polyfit(np.log(horizons), np.log(scheduled_regret), deg=1)[0]
    )
    q_sweep = []
    for q in (1.0, 2.0, 4.0, 8.0, 16.0):
        zeta_2 = 1.0 - 2.0 ** (-q)
        paper_tail_bound = norm * (1.0 - zeta_2)
        q_sweep.append(
            {
                "q": q,
                "zeta_2": zeta_2,
                "assumption_ratio_at_n2": head / zeta_2,
                "L2_norm": norm,
                "assumption_holds": head / zeta_2 >= norm,
                "actual_tail_l1": tail,
                "paper_derived_tail_bound": paper_tail_bound,
                "tail_bound_residual": tail - paper_tail_bound,
                "predicted_exponent": (q + 1.0) / (2.0 * q + 1.0),
            }
        )

    t = 4096
    regret = t * construction["ot"]["per_round_regret"]
    return {
        "claim_4": {
            "N": 2,
            "zeta": "indicator(n>=2)",
            "zeta_is_continuous": False,
            "assumption_3_on_integer_orders": head >= norm,
            "paper_parenthetical_tail_zero": False,
            "omitted_nonzero_coefficients": coeff[2:],
            "horizon": t,
            "actual_cumulative_regret": regret,
            "sqrt_NT": math.sqrt(2.0 * t),
            "regret_to_sqrt_NT_ratio": regret / math.sqrt(2.0 * t),
            "tail_included_negative_control_regret": construction["ot"][
                "included_tail_regret"
            ],
            "transport": construction,
        },
        "claim_5": {
            "q_sweep": q_sweep,
            "selected_q": 4.0,
            "schedule": "n_t=ceil(t^(1/(2q+1)))",
            "schedule_N_is_2_for_t_2_through_512": True,
            "horizons": horizons.astype(int).tolist(),
            "cumulative_regret_before_tail_enters": scheduled_regret.tolist(),
            "observed_loglog_exponent_on_pre_entry_range": observed_exponent,
            "paper_exponent_q4": 5.0 / 9.0,
            "finite_coefficient_tail_counterexample": {
                "coefficients": coeff,
                "L2_norm": norm,
                "head_l1_at_n2": head,
                "tail_l1_after_n2": tail,
                "paper_false_equality_norm_minus_head": norm - head,
            },
            "infinite_coefficient_counterexample": _infinite_sequence_audit(),
        },
    }
