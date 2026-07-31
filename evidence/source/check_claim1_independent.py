"""Independent matrix checker for the claim-1 counterexample."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def check() -> dict:
    points = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    weights = np.full(4, 0.25)
    coupling = np.array([0.5, 0.0, 0.0, 0.5])
    cost = (points[:, 0] - points[:, 1]) ** 2

    kernel = np.exp(-2j * np.pi * (points @ points.T))
    fc_at_minus_z = cost @ weights[:, None] * np.ones((1, 4))
    # The expression above is valid because every integer-grid phase is one.
    fpi = coupling @ kernel
    lhs = float(cost @ coupling)
    rhs = np.sum(weights * fc_at_minus_z.ravel() * np.conjugate(fpi))

    phi = np.array([1.0, -1.0, -1.0, 1.0])
    fphi = (weights * phi) @ kernel
    input_norm_sq = float(np.sum(weights * phi**2))
    output_norm_sq = float(np.sum(weights * np.abs(fphi) ** 2))
    residual = float(abs(rhs - lhs))

    unitary_kernel = np.exp(-1j * np.pi * (points @ points.T)) / 2.0
    density = coupling / weights
    repaired_cost = 1.0 + points[:, 0] + 2.0 * points[:, 1]
    repaired_lhs = float(repaired_cost @ coupling)
    repaired_rhs = np.sum(
        weights
        * (repaired_cost @ unitary_kernel)
        * np.conjugate(density @ unitary_kernel)
    )
    repaired_probe = np.array([1.0, -1.0, -1.0, 1.0])
    repaired_input_norm = float(np.sum(weights * repaired_probe**2))
    repaired_output_norm = float(
        np.sum(weights * np.abs(repaired_probe @ unitary_kernel) ** 2)
    )
    alternative_verified = bool(
        abs(repaired_rhs - repaired_lhs) < 1e-12
        and abs(repaired_input_norm - repaired_output_norm) < 1e-12
    )
    return {
        "checker": "independent NumPy matrix construction",
        "lhs": lhs,
        "rhs_real": float(rhs.real),
        "rhs_imag": float(rhs.imag),
        "identity_residual": residual,
        "input_norm_sq": input_norm_sq,
        "output_norm_sq": output_norm_sq,
        "isometry_residual": abs(input_norm_sq - output_norm_sq),
        "alternative": {
            "identity_residual": float(abs(repaired_rhs - repaired_lhs)),
            "isometry_residual": abs(
                repaired_input_norm - repaired_output_norm
            ),
            "verified": alternative_verified,
        },
        "agrees_falsified": residual > 0.49
        and abs(input_norm_sq - output_norm_sq) > 0.99,
        "agrees_paired": residual > 0.49
        and abs(input_norm_sq - output_norm_sq) > 0.99
        and alternative_verified,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-identity", action="store_true")
    args = parser.parse_args()
    result = check()
    if args.output:
        args.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, sort_keys=True))
    if args.require_identity:
        return 0 if math.isclose(result["identity_residual"], 0.0, abs_tol=1e-12) else 1
    return 0 if result["agrees_paired"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
