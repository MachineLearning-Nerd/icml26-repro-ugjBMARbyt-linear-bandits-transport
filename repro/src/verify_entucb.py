"""Cumulative OpenResearch verifier for arXiv:2502.07397.

This first child audits the literal v1 Fourier contract. Later descendants add
claim checks while preserving this check and the fixed entrypoint.
"""
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

from claim1_fourier import evaluate_literal_counterexample
from claim6_confidence import evaluate_confidence_contract


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / ".openresearch" / "artifacts" / "claim_1"
COMMAND = "uv run python repro/src/verify_entucb.py"


def run() -> int:
    started = time.perf_counter()
    ARTIFACT.mkdir(parents=True, exist_ok=True)

    result = evaluate_literal_counterexample()
    (ARTIFACT / "raw_result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    independent_path = ARTIFACT / "independent_checker_output.json"
    independent = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("check_claim1_independent.py")),
            "--output",
            str(independent_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if independent.returncode != 0:
        print(independent.stdout)
        print(independent.stderr, file=sys.stderr)
        raise RuntimeError("independent claim-1 checker disagreed with the evidence")

    negative = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("check_claim1_independent.py")),
            "--require-identity",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    negative_record = {
        "control": "mutated requirement that literal Equation (7) must hold",
        "expected_exit_code": 1,
        "observed_exit_code": negative.returncode,
        "stdout": negative.stdout.strip(),
        "stderr": negative.stderr.strip(),
        "passed": negative.returncode == 1,
    }
    (ARTIFACT / "negative_control_output.json").write_text(
        json.dumps(negative_record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
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
        "processor": platform.processor(),
        "logical_cpu_count": os.cpu_count(),
        "seeds": [],
        "wall_seconds": time.perf_counter() - started,
    }
    (ARTIFACT / "environment.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (ARTIFACT / "exact_command.txt").write_text(COMMAND + "\n", encoding="utf-8")

    assumptions_ok = all(result["assumptions"].values())
    claim1_falsified = (
        assumptions_ok
        and result["identity"]["absolute_residual"] > 0.49
        and result["isometry"]["squared_norm_residual"] > 0.99
        and negative_record["passed"]
    )
    verdict = "FALSIFIED" if claim1_falsified else "BLOCKED"
    summary = {
        "claim_id": 1,
        "verdict": verdict,
        "assumptions_satisfied": assumptions_ok,
        "equation_7_left": result["identity"]["left_real"],
        "equation_7_right_real": result["identity"]["right_real"],
        "equation_7_absolute_residual": result["identity"]["absolute_residual"],
        "isometry_squared_norm_residual": result["isometry"][
            "squared_norm_residual"
        ],
        "independent_checker_exit_code": independent.returncode,
        "negative_control_failed_as_intended": negative_record["passed"],
    }
    (ARTIFACT / "verdict.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("CLAIM 1 — literal arXiv v1 Fourier contract")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(
        "ORX_EVAL "
        f"claim_1_verdict={verdict} "
        f"eq7_residual={summary['equation_7_absolute_residual']:.17g} "
        f"isometry_residual={summary['isometry_squared_norm_residual']:.17g} "
        f"negative_control={str(negative_record['passed']).lower()} "
        f"git_sha={git_sha}"
    )

    claim6_artifact = ROOT / ".openresearch" / "artifacts" / "claim_6"
    claim6_artifact.mkdir(parents=True, exist_ok=True)
    claim6 = evaluate_confidence_contract()
    (claim6_artifact / "raw_result.json").write_text(
        json.dumps(claim6, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    independent6_path = claim6_artifact / "independent_checker_output.json"
    independent6 = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("check_claim6_independent.py")),
            "--output",
            str(independent6_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if independent6.returncode != 0:
        print(independent6.stdout)
        print(independent6.stderr, file=sys.stderr)
        raise RuntimeError("independent claim-6 checker disagreed with the evidence")

    negative6 = {
        "control": "use five percent of the corrected confidence radius",
        "expected": "at least one exhaustive Rademacher path leaves the set",
        "observed_coverage": claim6["corrected_oful_control"][
            "undersized_beta_coverage"
        ],
        "passed": claim6["corrected_oful_control"]["undersized_beta_coverage"]
        < 1.0,
    }
    (claim6_artifact / "negative_control_output.json").write_text(
        json.dumps(negative6, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    claim6_falsified = (
        all(claim6["assumptions"].values())
        and claim6["transport_model_contradiction"]["identical_features"]
        and claim6["transport_model_contradiction"]["mean_gap"] > 0.99
        and not claim6["printed_width"]["addition_is_defined"]
        and claim6["corrected_oful_control"]["determinant_lemma_residual"] < 1e-12
        and claim6["corrected_oful_control"]["exact_coverage"] >= 0.9
        and negative6["passed"]
    )
    claim6_verdict = "FALSIFIED" if claim6_falsified else "BLOCKED"
    claim6_summary = {
        "claim_id": 6,
        "verdict": claim6_verdict,
        "assumptions_satisfied": all(claim6["assumptions"].values()),
        "identical_action_features": claim6["transport_model_contradiction"][
            "identical_features"
        ],
        "different_expected_feedback_gap": claim6[
            "transport_model_contradiction"
        ]["mean_gap"],
        "printed_equation_12_defined": claim6["printed_width"][
            "addition_is_defined"
        ],
        "corrected_formula_exact_coverage": claim6["corrected_oful_control"][
            "exact_coverage"
        ],
        "negative_control_failed_as_intended": negative6["passed"],
        "independent_checker_exit_code": independent6.returncode,
    }
    (claim6_artifact / "verdict.json").write_text(
        json.dumps(claim6_summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    claim6_environment = dict(environment)
    claim6_environment["wall_seconds"] = time.perf_counter() - started
    claim6_environment["exhaustive_noise_paths"] = claim6[
        "corrected_oful_control"
    ]["noise_paths"]
    (claim6_artifact / "environment.json").write_text(
        json.dumps(claim6_environment, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (claim6_artifact / "exact_command.txt").write_text(
        COMMAND + "\n", encoding="utf-8"
    )
    print("CLAIM 6 — literal confidence-set contract")
    print(json.dumps(claim6_summary, indent=2, sort_keys=True))
    print(
        "ORX_EVAL "
        f"claim_6_verdict={claim6_verdict} "
        f"feature_collision={str(claim6_summary['identical_action_features']).lower()} "
        f"feedback_gap={claim6_summary['different_expected_feedback_gap']:.17g} "
        f"eq12_defined={str(claim6_summary['printed_equation_12_defined']).lower()} "
        f"corrected_coverage={claim6_summary['corrected_formula_exact_coverage']:.17g} "
        f"negative_control={str(negative6['passed']).lower()} "
        f"git_sha={git_sha}"
    )
    return 0 if claim1_falsified and claim6_falsified else 1


if __name__ == "__main__":
    raise SystemExit(run())
