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
    falsified = (
        assumptions_ok
        and result["identity"]["absolute_residual"] > 0.49
        and result["isometry"]["squared_norm_residual"] > 0.99
        and negative_record["passed"]
    )
    verdict = "FALSIFIED" if falsified else "BLOCKED"
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
    return 0 if falsified else 1


if __name__ == "__main__":
    raise SystemExit(run())
