"""Literal v1 regret-definition and theorem-bound audit for Claims 2-3."""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import linprog


def _transport_lp(cost: np.ndarray) -> dict:
    a_eq = []
    b_eq = []
    for i in range(2):
        row = np.zeros((2, 2))
        row[i, :] = 1.0
        a_eq.append(row.ravel())
        b_eq.append(0.5)
    for j in range(2):
        row = np.zeros((2, 2))
        row[:, j] = 1.0
        a_eq.append(row.ravel())
        b_eq.append(0.5)
    solved = linprog(
        cost.ravel(),
        A_eq=np.asarray(a_eq),
        b_eq=np.asarray(b_eq),
        bounds=(0.0, None),
        method="highs",
    )
    if not solved.success:
        raise RuntimeError(solved.message)
    plan = solved.x.reshape(2, 2)
    return {
        "objective": float(np.sum(plan * cost)),
        "plan": plan.tolist(),
        "max_marginal_residual": float(
            max(
                np.max(np.abs(plan.sum(axis=0) - 0.5)),
                np.max(np.abs(plan.sum(axis=1) - 0.5)),
            )
        ),
        "solver": "scipy.optimize.linprog(method='highs')",
    }


def _entropy(plan: np.ndarray) -> float:
    positive = plan > 0.0
    return float(np.sum(plan[positive] * np.log(plan[positive] / 0.25)))


def _entropic_optimum(cost: np.ndarray, epsilon: float) -> dict:
    diagonal_sum = float(cost[0, 0] + cost[1, 1])
    off_diagonal_sum = float(cost[0, 1] + cost[1, 0])
    delta = diagonal_sum - off_diagonal_sum
    p = 0.5 / (1.0 + math.exp(delta / (2.0 * epsilon)))
    plan = np.array([[p, 0.5 - p], [0.5 - p, p]])
    cost_value = float(np.sum(plan * cost))
    entropy_value = _entropy(plan)
    return {
        "epsilon": epsilon,
        "plan": plan.tolist(),
        "cost": cost_value,
        "relative_entropy": entropy_value,
        "objective": cost_value + epsilon * entropy_value,
        "max_marginal_residual": float(
            max(
                np.max(np.abs(plan.sum(axis=0) - 0.5)),
                np.max(np.abs(plan.sum(axis=1) - 0.5)),
            )
        ),
        "solver": "closed-form 2x2 entropic OT stationarity equation",
    }


def _charitable_bound_upper(
    *, horizon: int, sigma: float, delta: float, lam: float, c_bound: float
) -> dict:
    dimension = 4
    logdet_beta_upper = dimension * math.log(
        1.0 + horizon / (dimension * lam)
    )
    beta_upper = sigma * math.sqrt(
        math.log(4.0 / (delta**2)) + logdet_beta_upper
    ) + math.sqrt(lam) * c_bound
    logdet_width_upper = dimension * math.log(
        1.0 + horizon / (2.0 * lam * c_bound * dimension)
    )
    noise_term = sigma * math.sqrt(2.0 * horizon * math.log(2.0 / delta))
    confidence_term = (
        2.0
        * c_bound
        * beta_upper
        * math.sqrt(horizon * logdet_width_upper)
    )
    return {
        "dimension": dimension,
        "feature_norm_upper_bound": 1.0,
        "sigma": sigma,
        "delta": delta,
        "lambda": lam,
        "C_bar": c_bound,
        "logdet_beta_upper": logdet_beta_upper,
        "beta_T_upper": beta_upper,
        "logdet_width_upper": logdet_width_upper,
        "noise_term": noise_term,
        "confidence_term": confidence_term,
        "theorem_5_1_rhs_upper": noise_term + confidence_term,
        "derivation": "rank/trace determinant bound det(I+c M*M)<=(1+cT/d)^d",
        "charitable_correction": "uses identity in the compatible space for the ill-typed printed beta determinant",
    }


def _lipschitz_constant(cost: np.ndarray) -> float:
    support = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    values = cost.ravel()
    ratios = []
    for i in range(len(support)):
        for j in range(i):
            distance = float(np.linalg.norm(support[i] - support[j]))
            ratios.append(abs(float(values[i] - values[j])) / distance)
    return max(ratios)


def evaluate_claims_2_and_3() -> dict:
    cost = np.array([[1.0, 2.0], [2.0, 1.0]])
    rho = np.full((2, 2), 0.25)
    horizon = 100_000_000
    epsilon = 0.2
    alpha = 0.5
    sigma = 1e-6
    delta = 0.05
    lam = 1.0
    c_bound = float(math.sqrt(np.sum(rho * cost**2)))

    kant = _transport_lp(cost)
    entropic = _entropic_optimum(cost, epsilon)
    bound = _charitable_bound_upper(
        horizon=horizon,
        sigma=sigma,
        delta=delta,
        lam=lam,
        c_bound=c_bound,
    )

    # The literal v1 definitions subtract one comparator value after summing T
    # feedback/objective terms. Every valid action has objective at least the
    # comparator, so these are lower bounds for any action sequence.
    entropic_printed_regret_lower = (horizon - 1) * entropic["objective"]
    kant_printed_regret_lower = (horizon - 1) * kant["objective"]

    lipschitz = _lipschitz_constant(cost)
    upper_renyi_dimension = 0.0  # finite support, as stated in the paper.
    kappa = upper_renyi_dimension + lipschitz
    approximation_term = (
        kappa
        * alpha
        / (1.0 - alpha)
        * (
            horizon ** (1.0 - alpha) * math.log(horizon)
            + alpha / (2.0**alpha) * math.log(6.0)
        )
    )
    theorem_52_upper = bound["theorem_5_1_rhs_upper"] + approximation_term
    schedule_times = [1, 2, 4, 16, 256, 65_536, horizon]
    schedule_values = [alpha * t ** (-alpha) for t in schedule_times]
    constant_schedule = [alpha for _ in schedule_times]
    schedule_max_control_error = max(
        abs(left - right) for left, right in zip(schedule_values, constant_schedule)
    )

    return {
        "construction": {
            "mu": [0.5, 0.5],
            "nu": [0.5, 0.5],
            "rho": rho.tolist(),
            "cost": cost.tolist(),
            "continuous_cost": "c(x,y)=1+(x-y)^2 on {0,1}^2",
            "noise": "identically zero",
            "horizon": horizon,
            "not_vacuous": "diagonal OT costs 1; off-diagonal OT costs 2",
        },
        "assumptions": {
            "cost_continuous_and_L2_rho": True,
            "known_C_bar_at_least_L2_norm": True,
            "zero_noise_is_sigma_squared_sub_gaussian": True,
            "sigma_strictly_positive": sigma > 0.0,
            "delta_positive": delta > 0.0,
            "lambda_positive": lam > 0.0,
            "epsilon_positive": epsilon > 0.0,
            "cost_is_Lipschitz_on_support": math.isfinite(lipschitz),
            "alpha_in_open_unit_interval": 0.0 < alpha < 1.0,
        },
        "comparators": {
            "kantorovich": kant,
            "entropic": entropic,
            "cost_L2_rho": c_bound,
            "lipschitz_constant": lipschitz,
            "upper_renyi_dimension": upper_renyi_dimension,
            "kappa": kappa,
        },
        "shared_bound_terms": bound,
        "claim_2": {
            "paper_regret_definition": "sum_t (R_t+epsilon H(pi_t|rho)) - Ent",
            "printed_regret_lower_for_every_action_sequence": entropic_printed_regret_lower,
            "theorem_rhs_upper_for_every_action_sequence": bound[
                "theorem_5_1_rhs_upper"
            ],
            "violation_margin": entropic_printed_regret_lower
            - bound["theorem_5_1_rhs_upper"],
            "corrected_repeated_optimum_regret": 0.0,
        },
        "claim_3": {
            "paper_regret_definition": "sum_t R_t - Kant",
            "alpha": alpha,
            "schedule": "epsilon_t=alpha*t^(-alpha)",
            "schedule_times": schedule_times,
            "schedule_values": schedule_values,
            "constant_schedule_negative_control_values": constant_schedule,
            "constant_schedule_max_error": schedule_max_control_error,
            "printed_regret_lower_for_every_action_sequence": kant_printed_regret_lower,
            "approximation_term": approximation_term,
            "theorem_rhs_upper_for_every_action_sequence": theorem_52_upper,
            "violation_margin": kant_printed_regret_lower - theorem_52_upper,
            "corrected_repeated_optimum_regret": 0.0,
        },
    }
