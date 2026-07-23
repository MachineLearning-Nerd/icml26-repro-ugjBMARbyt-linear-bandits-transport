"""Independent checker for the claim-6 structural contradictions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def check() -> dict:
    support = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    diagonal = np.array([0.5, 0.0, 0.0, 0.5])
    off_diagonal = np.array([0.0, 0.5, 0.5, 0.0])
    cost = (support[:, 0] - support[:, 1]) ** 2
    kernel = np.exp(-2j * np.pi * (support @ support.T))
    diagonal_feature = diagonal @ kernel
    off_diagonal_feature = off_diagonal @ kernel
    mean_gap = float(abs(cost @ diagonal - cost @ off_diagonal))

    m = np.ones((3, 4), dtype=float)
    d_lambda = np.eye(4)
    mm_star = m @ m.T
    result = {
        "checker": "independent transport and shape construction",
        "mean_gap": mean_gap,
        "feature_max_difference": float(
            np.max(np.abs(diagonal_feature - off_diagonal_feature))
        ),
        "features_identical": bool(
            np.allclose(diagonal_feature, off_diagonal_feature, atol=1e-12)
        ),
        "D_Lambda_shape": list(d_lambda.shape),
        "M_M_star_shape": list(mm_star.shape),
        "printed_addition_defined": d_lambda.shape == mm_star.shape,
    }
    result["agrees_falsified"] = (
        result["features_identical"]
        and result["mean_gap"] > 0.99
        and not result["printed_addition_defined"]
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check()
    if args.output:
        args.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, sort_keys=True))
    return 0 if result["agrees_falsified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
