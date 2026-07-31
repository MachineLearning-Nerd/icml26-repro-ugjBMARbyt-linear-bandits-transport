"""Literal finite-measure evaluation of arXiv v1 Equation (7)."""
from __future__ import annotations

import cmath
import math
from typing import Iterable

import numpy as np


SUPPORT = ((0, 0), (0, 1), (1, 0), (1, 1))
RHO = (0.25, 0.25, 0.25, 0.25)
PI = (0.5, 0.0, 0.0, 0.5)
COST = (0.0, 1.0, 1.0, 0.0)  # c(x,y) = (x-y)^2
ZERO_MEAN_FUNCTION = (1.0, -1.0, -1.0, 1.0)


def _phase(point: tuple[int, int], frequency: tuple[int, int]) -> complex:
    dot = point[0] * frequency[0] + point[1] * frequency[1]
    return cmath.exp(-2j * math.pi * dot)


def transform_function(
    values: Iterable[float], frequency: tuple[int, int]
) -> complex:
    return sum(w * v * _phase(x, frequency) for x, w, v in zip(SUPPORT, RHO, values))


def transform_measure(
    masses: Iterable[float], frequency: tuple[int, int]
) -> complex:
    return sum(m * _phase(x, frequency) for x, m in zip(SUPPORT, masses))


def _marginals(masses: tuple[float, ...]) -> tuple[list[float], list[float]]:
    first = [0.0, 0.0]
    second = [0.0, 0.0]
    for (x, y), mass in zip(SUPPORT, masses):
        first[x] += mass
        second[y] += mass
    return first, second


def evaluate_literal_counterexample() -> dict:
    left = sum(c * mass for c, mass in zip(COST, PI))
    right = sum(
        rho_z
        * transform_function(COST, (-z[0], -z[1]))
        * transform_measure(PI, z).conjugate()
        for z, rho_z in zip(SUPPORT, RHO)
    )

    phi_norm_sq = sum(w * abs(v) ** 2 for w, v in zip(RHO, ZERO_MEAN_FUNCTION))
    transformed = [transform_function(ZERO_MEAN_FUNCTION, z) for z in SUPPORT]
    transform_norm_sq = sum(w * abs(v) ** 2 for w, v in zip(RHO, transformed))
    pi_first, pi_second = _marginals(PI)
    rho_first, rho_second = _marginals(RHO)
    density = [mass / weight for mass, weight in zip(PI, RHO)]

    return {
        "construction": {
            "support": [list(x) for x in SUPPORT],
            "rho": list(RHO),
            "pi": list(PI),
            "pi_density_wrt_rho": density,
            "cost_values": list(COST),
            "continuous_cost": "c(x,y)=(x-y)^2",
            "literal_kernel": "exp(-2*pi*i*<x,z>)",
        },
        "assumptions": {
            "rho_is_probability": abs(sum(RHO) - 1.0) < 1e-15,
            "pi_is_probability": abs(sum(PI) - 1.0) < 1e-15,
            "pi_has_required_uniform_marginals": pi_first
            == rho_first
            == [0.5, 0.5]
            and pi_second == rho_second == [0.5, 0.5],
            "pi_density_is_L2_rho": math.isfinite(
                sum(w * g * g for w, g in zip(RHO, density))
            ),
            "cost_is_continuous_and_L2_rho": math.isfinite(
                sum(w * c * c for w, c in zip(RHO, COST))
            ),
        },
        "identity": {
            "left_exact": "0",
            "right_exact": "1/2",
            "left_real": left,
            "right_real": right.real,
            "right_imag": right.imag,
            "absolute_residual": abs(right - left),
        },
        "isometry": {
            "test_function": list(ZERO_MEAN_FUNCTION),
            "input_squared_norm_exact": "1",
            "output_squared_norm_exact": "0",
            "input_squared_norm": phi_norm_sq,
            "output_squared_norm": transform_norm_sq,
            "squared_norm_residual": abs(phi_norm_sq - transform_norm_sq),
        },
    }


def evaluate_unitary_specialization() -> dict:
    points = np.asarray(SUPPORT, dtype=float)
    rho = np.asarray(RHO)
    coupling = np.asarray(PI)
    density = coupling / rho
    cost = 1.0 + points[:, 0] + 2.0 * points[:, 1]
    characters = np.exp(-1j * np.pi * (points @ points.T))
    unitary = characters / math.sqrt(len(points))

    transformed_cost = cost @ unitary
    transformed_density = density @ unitary
    direct_pairing = float(cost @ coupling)
    fourier_pairing = np.sum(
        rho * transformed_cost * np.conjugate(transformed_density)
    )

    probe = np.asarray(ZERO_MEAN_FUNCTION)
    input_norm = float(np.sum(rho * np.abs(probe) ** 2))
    output_norm = float(np.sum(rho * np.abs(probe @ unitary) ** 2))

    literal_cost = (rho * cost) @ characters
    literal_coupling = coupling @ characters
    literal_pairing = np.sum(
        rho * literal_cost * np.conjugate(literal_coupling)
    )

    return {
        "claim": (
            "On uniform Z2 x Z2, the normalized discrete Fourier transform "
            "preserves the L2(rho) norm and the transport pairing when a "
            "coupling is represented by its density d pi/d rho."
        ),
        "construction": {
            "group": "Z2 x Z2",
            "rho": rho.tolist(),
            "coupling": coupling.tolist(),
            "density": density.tolist(),
            "cost": "c(x,y)=1+x+2y",
            "kernel": "exp(-pi*i*<x,k>)/sqrt(4)",
        },
        "direct_pairing": direct_pairing,
        "fourier_pairing_real": float(fourier_pairing.real),
        "fourier_pairing_imag": float(fourier_pairing.imag),
        "identity_residual": float(abs(fourier_pairing - direct_pairing)),
        "input_squared_norm": input_norm,
        "output_squared_norm": output_norm,
        "isometry_residual": abs(input_norm - output_norm),
        "literal_normalization_residual": float(
            abs(literal_pairing - direct_pairing)
        ),
        "deviations_from_failed_claim": [
            "finite-group character phase",
            "unitary 1/sqrt(4) normalization",
            "the coupling is represented by d pi/d rho",
        ],
    }
