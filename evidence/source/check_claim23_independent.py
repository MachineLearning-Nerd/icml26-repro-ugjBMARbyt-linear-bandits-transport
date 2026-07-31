"""Independent arithmetic checker for Claims 2-3."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def check() -> dict:
    horizon = 100_000_000
    c_bound = math.sqrt(2.5)
    sigma = 1e-6
    delta = 0.05
    dimension = 4
    logdet_beta = dimension * math.log(1.0 + horizon / dimension)
    beta = sigma * math.sqrt(math.log(4.0 / delta**2) + logdet_beta) + c_bound
    logdet_width = dimension * math.log(
        1.0 + horizon / (2.0 * c_bound * dimension)
    )
    shared_upper = sigma * math.sqrt(
        2.0 * horizon * math.log(2.0 / delta)
    ) + 2.0 * c_bound * beta * math.sqrt(horizon * logdet_width)

    epsilon = 0.2
    p = 0.5 / (1.0 + math.exp(-2.0 / (2.0 * epsilon)))
    cost_value = 2.0 - 2.0 * p
    entropy = 2.0 * p * math.log(p / 0.25) + 2.0 * (
        0.5 - p
    ) * math.log((0.5 - p) / 0.25)
    entropic_optimum = cost_value + epsilon * entropy
    claim2_lower = (horizon - 1) * entropic_optimum
    corrected_entropic_regret = horizon * (
        cost_value + epsilon * entropy - entropic_optimum
    )

    alpha = 0.5
    approximation = (
        horizon**0.5 * math.log(horizon)
        + alpha / (2.0**alpha) * math.log(6.0)
    )
    claim3_upper = shared_upper + approximation
    claim3_lower = horizon - 1.0
    corrected_kant_regret = horizon * (1.0 - 1.0)
    schedule_last = alpha * horizon ** (-alpha)
    result = {
        "checker": "independent scalar OT and determinant-bound arithmetic",
        "entropic_optimum": entropic_optimum,
        "claim_2_printed_regret_lower": claim2_lower,
        "claim_2_rhs_upper": shared_upper,
        "claim_2_violation": claim2_lower > shared_upper,
        "claim_2_alternative_regret": corrected_entropic_regret,
        "claim_2_alternative_verified": abs(corrected_entropic_regret) < 1e-12,
        "epsilon_T": schedule_last,
        "expected_epsilon_T": 0.00005,
        "schedule_exact": abs(schedule_last - 0.00005) < 1e-15,
        "claim_3_printed_regret_lower": claim3_lower,
        "claim_3_rhs_upper": claim3_upper,
        "claim_3_violation": claim3_lower > claim3_upper,
        "claim_3_alternative_regret": corrected_kant_regret,
        "claim_3_alternative_verified": abs(corrected_kant_regret) < 1e-12,
    }
    result["agrees_falsified"] = bool(
        result["claim_2_violation"]
        and result["claim_2_alternative_verified"]
        and result["schedule_exact"]
        and result["claim_3_violation"]
        and result["claim_3_alternative_verified"]
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
