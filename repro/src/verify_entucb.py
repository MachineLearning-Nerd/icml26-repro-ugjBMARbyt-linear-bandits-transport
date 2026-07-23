"""Audit a corrected unitary finite Fourier specialization."""
from __future__ import annotations

import json
import os
import platform
import subprocess
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / ".openresearch" / "artifacts" / "claim_1"
COMMAND = "uv run python repro/src/verify_entucb.py"


def evaluate() -> dict:
    points = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    rho = np.full(4, 0.25)
    pi = np.array([0.5, 0.0, 0.0, 0.5])
    density = pi / rho
    cost = 1.0 + points[:, 0] + 2.0 * points[:, 1]
    characters = np.exp(-1j * np.pi * (points @ points.T))

    # U=H/sqrt(|G|) is unitary for L2 of uniform Haar probability.
    unitary = characters / np.sqrt(len(points))
    uc = cost @ unitary
    ug = density @ unitary
    lhs = float(cost @ pi)
    corrected_rhs = np.sum(rho * uc * np.conjugate(ug))

    # Literal paper normalization integrates each input against rho.
    literal_fc = (rho * cost) @ characters
    literal_fpi = pi @ characters
    literal_rhs = np.sum(rho * literal_fc * np.conjugate(literal_fpi))

    probe = np.array([1.0, -1.0, -1.0, 1.0])
    input_norm = float(np.sum(rho * np.abs(probe) ** 2))
    output_norm = float(np.sum(rho * np.abs(probe @ unitary) ** 2))
    return {
        "construction": {
            "group": "Z_2 x Z_2",
            "support": points.astype(int).tolist(),
            "rho": rho.tolist(),
            "pi": pi.tolist(),
            "density": density.tolist(),
            "continuous_cost": "c(x,y)=1+x+2y",
            "corrected_kernel": "exp(-pi*i*<x,k>)/sqrt(4)",
        },
        "corrected_specialization": {
            "transport_pairing": lhs,
            "fourier_inner_product_real": float(corrected_rhs.real),
            "fourier_inner_product_imag": float(corrected_rhs.imag),
            "identity_residual": float(abs(corrected_rhs - lhs)),
            "input_squared_norm": input_norm,
            "output_squared_norm": output_norm,
            "isometry_residual": abs(input_norm - output_norm),
        },
        "literal_normalization_negative_control": {
            "fourier_inner_product_real": float(literal_rhs.real),
            "identity_residual": float(abs(literal_rhs - lhs)),
        },
        "deviations_from_v1": [
            "frequency phase is normalized for the finite group",
            "the transform is scaled by 1/sqrt(|G|), not integration against rho",
            "pi is transformed through its density d pi/d rho",
        ],
    }


def main() -> int:
    started = time.perf_counter()
    ARTIFACT.mkdir(parents=True, exist_ok=True)
    result = evaluate()
    corrected = result["corrected_specialization"]
    passed = (
        corrected["identity_residual"] < 1e-12
        and corrected["isometry_residual"] < 1e-12
        and result["literal_normalization_negative_control"]["identity_residual"] > 1.8
    )
    result["verdict"] = {
        "claim_id": 1,
        "literal_v1_claim": "BLOCKED",
        "corrected_specialization": "VERIFIED" if passed else "BLOCKED",
        "reason": "The verified operator changes the v1 normalization and domain.",
    }
    (ARTIFACT / "raw_result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    git_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    environment = {
        "command": COMMAND,
        "git_sha": git_sha,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "logical_cpu_count": os.cpu_count(),
        "seeds": [],
        "wall_seconds": time.perf_counter() - started,
    }
    (ARTIFACT / "environment.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (ARTIFACT / "exact_command.txt").write_text(COMMAND + "\n", encoding="utf-8")
    (ARTIFACT / "negative_control_output.json").write_text(
        json.dumps(
            {
                "control": "paper's literal rho-integral normalization",
                "expected_to_fail_identity": True,
                "observed_residual": result["literal_normalization_negative_control"][
                    "identity_residual"
                ],
                "passed": result["literal_normalization_negative_control"][
                    "identity_residual"
                ]
                > 1.8,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    print(
        "ORX_EVAL "
        "claim_1_verdict=BLOCKED "
        f"corrected_specialization={'VERIFIED' if passed else 'BLOCKED'} "
        f"corrected_identity_residual={corrected['identity_residual']:.17g} "
        f"literal_negative_residual={result['literal_normalization_negative_control']['identity_residual']:.17g} "
        f"git_sha={git_sha}"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
