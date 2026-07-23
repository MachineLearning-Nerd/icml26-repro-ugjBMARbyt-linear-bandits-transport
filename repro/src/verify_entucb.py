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
from claim45_basis_rates import evaluate_claims_4_and_5
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
    claim45 = evaluate_claims_4_and_5()
    independent45_path = (
        ROOT
        / ".openresearch"
        / "artifacts"
        / "claim_4"
        / "independent_checker_output.json"
    )
    independent45_path.parent.mkdir(parents=True, exist_ok=True)
    independent45 = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("check_claim45_independent.py")),
            "--output",
            str(independent45_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if independent45.returncode != 0:
        print(independent45.stdout)
        print(independent45.stderr, file=sys.stderr)
        raise RuntimeError("independent claims 4-5 checker disagreed with the evidence")

    claim4 = claim45["claim_4"]
    claim4_falsified = (
        claim4["assumption_3_on_integer_orders"]
        and not claim4["paper_parenthetical_tail_zero"]
        and claim4["transport"]["basis"]["max_orthonormality_residual"] < 1e-12
        and claim4["transport"]["ot"]["per_round_regret"] > 0.99
        and claim4["regret_to_sqrt_NT_ratio"] > 40.0
        and claim4["tail_included_negative_control_regret"] == 0.0
    )
    claim4_verdict = "FALSIFIED" if claim4_falsified else "BLOCKED"
    claim4_artifact = ROOT / ".openresearch" / "artifacts" / "claim_4"
    (claim4_artifact / "raw_result.json").write_text(
        json.dumps(claim4, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    claim4_negative = {
        "control": "include the omitted third basis coefficient",
        "expected_regret": 0.0,
        "observed_regret": claim4["tail_included_negative_control_regret"],
        "passed": claim4["tail_included_negative_control_regret"] == 0.0,
    }
    (claim4_artifact / "negative_control_output.json").write_text(
        json.dumps(claim4_negative, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    claim4_summary = {
        "claim_id": 4,
        "verdict": claim4_verdict,
        "assumption_3_holds": claim4["assumption_3_on_integer_orders"],
        "omitted_tail_nonzero": not claim4["paper_parenthetical_tail_zero"],
        "actual_ot_per_round_regret": claim4["transport"]["ot"][
            "per_round_regret"
        ],
        "horizon": claim4["horizon"],
        "cumulative_regret": claim4["actual_cumulative_regret"],
        "regret_to_sqrt_NT_ratio": claim4["regret_to_sqrt_NT_ratio"],
        "negative_control_failed_as_intended": claim4_negative["passed"],
        "independent_checker_exit_code": independent45.returncode,
    }
    (claim4_artifact / "verdict.json").write_text(
        json.dumps(claim4_summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    claim5 = claim45["claim_5"]
    q4 = next(item for item in claim5["q_sweep"] if item["q"] == 4.0)
    infinite = claim5["infinite_coefficient_counterexample"]
    claim5_falsified = (
        q4["assumption_holds"]
        and q4["tail_bound_residual"] > 1.4
        and infinite["L2_membership"]
        and infinite["assumption_3_holds_for_every_q_positive"]
        and infinite["tail_l1_diverges"]
    )
    claim5_verdict = "FALSIFIED" if claim5_falsified else "BLOCKED"
    claim5_artifact = ROOT / ".openresearch" / "artifacts" / "claim_5"
    claim5_artifact.mkdir(parents=True, exist_ok=True)
    (claim5_artifact / "raw_result.json").write_text(
        json.dumps(claim5, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    claim5_negative = {
        "control": "require the paper-derived q=4 tail inequality on an admitted sequence",
        "expected_exit_code": 1,
        "actual_tail_l1": q4["actual_tail_l1"],
        "claimed_upper_bound": q4["paper_derived_tail_bound"],
        "observed_exit_code": int(
            not (q4["actual_tail_l1"] <= q4["paper_derived_tail_bound"])
        ),
        "passed": q4["actual_tail_l1"] > q4["paper_derived_tail_bound"],
    }
    (claim5_artifact / "negative_control_output.json").write_text(
        json.dumps(claim5_negative, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    claim5_summary = {
        "claim_id": 5,
        "verdict": claim5_verdict,
        "q": 4.0,
        "assumption_3_holds": q4["assumption_holds"],
        "actual_tail_l1_at_n2": q4["actual_tail_l1"],
        "paper_derived_tail_bound": q4["paper_derived_tail_bound"],
        "finite_tail_bound_residual": q4["tail_bound_residual"],
        "admitted_infinite_sequence_is_L2": infinite["L2_membership"],
        "admitted_infinite_sequence_tail_l1_diverges": infinite[
            "tail_l1_diverges"
        ],
        "negative_control_failed_as_intended": claim5_negative["passed"],
        "independent_checker_exit_code": independent45.returncode,
    }
    (claim5_artifact / "verdict.json").write_text(
        json.dumps(claim5_summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    for artifact, extra in (
        (claim4_artifact, {"ot_solver": "scipy.optimize.linprog(method='highs')"}),
        (
            claim5_artifact,
            {"coefficient_partial_sum_cutoff": 100_000, "selected_q": 4.0},
        ),
    ):
        artifact_environment = dict(environment)
        artifact_environment.update(extra)
        artifact_environment["wall_seconds"] = time.perf_counter() - started
        (artifact / "environment.json").write_text(
            json.dumps(artifact_environment, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (artifact / "exact_command.txt").write_text(COMMAND + "\n", encoding="utf-8")

    print("CLAIM 4 — finite-basis rate contract")
    print(json.dumps(claim4_summary, indent=2, sort_keys=True))
    print(
        "ORX_EVAL "
        f"claim_4_verdict={claim4_verdict} "
        f"ot_gap={claim4_summary['actual_ot_per_round_regret']:.17g} "
        f"regret_sqrtNT_ratio={claim4_summary['regret_to_sqrt_NT_ratio']:.17g} "
        f"negative_control={str(claim4_negative['passed']).lower()} "
        f"git_sha={git_sha}"
    )
    print("CLAIM 5 — coefficient-decay rate contract")
    print(json.dumps(claim5_summary, indent=2, sort_keys=True))
    print(
        "ORX_EVAL "
        f"claim_5_verdict={claim5_verdict} "
        f"q=4 tail_residual={claim5_summary['finite_tail_bound_residual']:.17g} "
        f"infinite_tail_l1={str(infinite['tail_l1_diverges']).lower()} "
        f"negative_control={str(claim5_negative['passed']).lower()} "
        f"git_sha={git_sha}"
    )
    return (
        0
        if claim1_falsified
        and claim6_falsified
        and claim4_falsified
        and claim5_falsified
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(run())
