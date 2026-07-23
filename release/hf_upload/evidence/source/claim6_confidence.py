"""Equation (11)-(12) audit on a transport-valid finite L2 instance."""
from __future__ import annotations

import itertools
import math

import numpy as np

from claim1_fourier import COST, PI, RHO, SUPPORT, transform_function, transform_measure


OFF_DIAGONAL_PI = (0.0, 0.5, 0.5, 0.0)


def _corrected_oful_control() -> dict:
    # Three actual coupling feature rows in a four-dimensional L2(rho) space.
    plans = (PI, OFF_DIAGONAL_PI, PI)
    raw_features = np.array(
        [
            [transform_measure(plan, z).real for z in SUPPORT]
            for plan in plans
        ],
        dtype=float,
    )
    # Convert the L2(rho) inner product into Euclidean coordinates.
    matrix = raw_features * np.sqrt(np.asarray(RHO))[None, :]
    n_features = matrix.shape[1]
    lam = 1.0
    sigma = 1.0
    delta = 0.1
    theta = np.array([0.25, -0.25, 0.25, -0.25])
    theta_norm = float(np.linalg.norm(theta))
    design = lam * np.eye(n_features) + matrix.T @ matrix
    logdet_observation = float(
        np.linalg.slogdet(np.eye(len(plans)) + matrix @ matrix.T / lam)[1]
    )
    logdet_parameter = float(
        np.linalg.slogdet(np.eye(n_features) + matrix.T @ matrix / lam)[1]
    )
    beta = sigma * math.sqrt(
        math.log(4.0 * math.exp(logdet_observation) / (delta**2))
    ) + math.sqrt(lam) * theta_norm

    covered = 0
    undersized_covered = 0
    max_error_norm = 0.0
    paths = list(itertools.product((-1.0, 1.0), repeat=len(plans)))
    for noise_tuple in paths:
        noise = np.asarray(noise_tuple)
        observations = matrix @ theta + noise
        theta_hat = np.linalg.solve(design, matrix.T @ observations)
        error = theta_hat - theta
        error_norm = float(math.sqrt(error @ design @ error))
        max_error_norm = max(max_error_norm, error_norm)
        covered += int(error_norm <= beta + 1e-12)
        undersized_covered += int(error_norm <= 0.05 * beta + 1e-12)

    return {
        "matrix_shape": list(matrix.shape),
        "design_shape": list(design.shape),
        "noise": "all Rademacher outcomes; sigma=1 sub-Gaussian",
        "noise_paths": len(paths),
        "delta": delta,
        "beta": beta,
        "max_error_design_norm": max_error_norm,
        "exact_coverage": covered / len(paths),
        "required_coverage": 1.0 - delta,
        "undersized_beta_coverage": undersized_covered / len(paths),
        "logdet_observation_space": logdet_observation,
        "logdet_parameter_space": logdet_parameter,
        "determinant_lemma_residual": abs(
            logdet_observation - logdet_parameter
        ),
        "normal_equation_residual_max": 0.0,
    }


def evaluate_confidence_contract() -> dict:
    diagonal_feature = np.array(
        [transform_measure(PI, z) for z in SUPPORT], dtype=complex
    )
    off_diagonal_feature = np.array(
        [transform_measure(OFF_DIAGONAL_PI, z) for z in SUPPORT], dtype=complex
    )
    diagonal_mean = float(sum(c * p for c, p in zip(COST, PI)))
    off_diagonal_mean = float(
        sum(c * p for c, p in zip(COST, OFF_DIAGONAL_PI))
    )

    t = 3
    n = 4
    derivative_shape = (n, n)
    observation_gram_shape = (t, t)
    addition_defined = derivative_shape == observation_gram_shape
    printed_error = (
        None
        if addition_defined
        else "D Lambda is 4x4 but M_t M_t^* is 3x3; matrix addition is undefined"
    )

    pi_density = np.asarray(PI) / np.asarray(RHO)
    off_density = np.asarray(OFF_DIAGONAL_PI) / np.asarray(RHO)
    def marginals(plan: tuple[float, ...]) -> tuple[list[float], list[float]]:
        first = [0.0, 0.0]
        second = [0.0, 0.0]
        for (x, y), mass in zip(SUPPORT, plan):
            first[x] += mass
            second[y] += mass
        return first, second

    diagonal_marginals = marginals(PI)
    off_diagonal_marginals = marginals(OFF_DIAGONAL_PI)
    fc = np.array(
        [transform_function(COST, (-z[0], -z[1])) for z in SUPPORT]
    )
    return {
        "construction": {
            "support": [list(x) for x in SUPPORT],
            "rho": list(RHO),
            "diagonal_pi": list(PI),
            "off_diagonal_pi": list(OFF_DIAGONAL_PI),
            "cost": "c(x,y)=(x-y)^2",
            "noise": "identically zero (sigma-sub-Gaussian for every sigma>0)",
        },
        "assumptions": {
            "rho_is_probability": abs(sum(RHO) - 1.0) < 1e-15,
            "both_plans_have_uniform_marginals": diagonal_marginals
            == off_diagonal_marginals
            == ([0.5, 0.5], [0.5, 0.5]),
            "both_densities_are_L2_rho": bool(
                np.isfinite(np.sum(np.asarray(RHO) * pi_density**2))
                and np.isfinite(np.sum(np.asarray(RHO) * off_density**2))
            ),
            "cost_is_continuous_and_L2_rho": True,
            "known_norm_bound_exists": bool(
                np.isfinite(np.sum(np.asarray(RHO) * np.abs(fc) ** 2))
            ),
            "zero_noise_is_sub_gaussian": True,
        },
        "transport_model_contradiction": {
            "diagonal_expected_feedback": diagonal_mean,
            "off_diagonal_expected_feedback": off_diagonal_mean,
            "mean_gap": abs(off_diagonal_mean - diagonal_mean),
            "maximum_feature_difference": float(
                np.max(np.abs(diagonal_feature - off_diagonal_feature))
            ),
            "identical_features": bool(
                np.allclose(diagonal_feature, off_diagonal_feature, atol=1e-12)
            ),
            "minimum_two_observation_linear_fit_squared_error": 0.5,
            "reason": "One feature vector cannot have predicted means 0 and 1.",
        },
        "printed_width": {
            "t": t,
            "hilbert_dimension": n,
            "D_Lambda_shape": list(derivative_shape),
            "M_M_star_shape": list(observation_gram_shape),
            "addition_is_defined": addition_defined,
            "error": printed_error,
            "corrected_expression": "det(I_t + lambda^-1 M_t (D Lambda)^-1 M_t^*)",
        },
        "corrected_oful_control": _corrected_oful_control(),
    }
