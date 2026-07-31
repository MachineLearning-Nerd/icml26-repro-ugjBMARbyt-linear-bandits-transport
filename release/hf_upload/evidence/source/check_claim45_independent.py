"""Independent permutation and Assumption-3 checker for Claims 4-5."""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np


def check() -> dict:
    diagonal = np.eye(3, dtype=bool)
    cyclic = np.zeros((3, 3), dtype=bool)
    other = np.zeros((3, 3), dtype=bool)
    for i in range(3):
        cyclic[i, (i + 1) % 3] = True
        other[i, (i + 2) % 3] = True
    head = (~diagonal).astype(float) - 2.0 / 3.0
    tail = np.zeros((3, 3))
    tail[cyclic] = -2.0
    tail[other] = 2.0
    truncated = 3.0 + head
    full = truncated + tail

    permutation_costs = []
    for permutation in itertools.permutations(range(3)):
        truncated_value = sum(truncated[i, permutation[i]] for i in range(3)) / 3
        full_value = sum(full[i, permutation[i]] for i in range(3)) / 3
        permutation_costs.append(
            {
                "permutation": list(permutation),
                "truncated": float(truncated_value),
                "full": float(full_value),
            }
        )
    truncated_min = min(item["truncated"] for item in permutation_costs)
    full_min = min(item["full"] for item in permutation_costs)
    truncated_choices = [
        item for item in permutation_costs if abs(item["truncated"] - truncated_min) < 1e-12
    ]
    full_choices = [
        item for item in permutation_costs if abs(item["full"] - full_min) < 1e-12
    ]

    coeff = np.array([3.0, math.sqrt(2.0) / 3.0, math.sqrt(8.0 / 3.0)])
    norm = float(np.linalg.norm(coeff))
    head_l1 = float(np.sum(np.abs(coeff[:2])))
    q4_bound = norm / 16.0
    q_residuals = {}
    for q in (1.0, 2.0, 4.0, 8.0, 16.0):
        q_residuals[str(int(q))] = float(
            abs(coeff[2]) - norm * 2.0 ** (-q)
        )
    result = {
        "checker": "independent enumeration of all 3! Birkhoff vertices",
        "permutation_costs": permutation_costs,
        "unique_truncated_optimum": bool(len(truncated_choices) == 1),
        "truncated_optimum": truncated_choices[0]["permutation"],
        "unique_full_optimum": bool(len(full_choices) == 1),
        "full_optimum": full_choices[0]["permutation"],
        "true_regret_of_truncated_optimum": next(
            item["full"]
            for item in permutation_costs
            if item["permutation"] == truncated_choices[0]["permutation"]
        )
        - full_min,
        "indicator_assumption_holds": bool(head_l1 >= norm),
        "tail_is_nonzero": bool(abs(coeff[2]) > 0),
        "q4_assumption_holds": bool(
            head_l1 / (1.0 - 2.0**-4) >= norm
        ),
        "q4_actual_tail_l1": float(abs(coeff[2])),
        "q4_paper_tail_bound": q4_bound,
        "alternatives": {
            "claim_4_zero_tail_after_dimension_3": True,
            "claim_4_full_model_regret": 0.0,
            "claim_5_q_residuals": q_residuals,
            "claim_5_q1_holds": q_residuals["1"] <= 0.0,
            "claim_5_tested_q_ge_2_fail": all(
                q_residuals[key] > 0.0 for key in ("2", "4", "8", "16")
            ),
        },
    }
    result["agrees_falsified"] = bool(
        result["unique_truncated_optimum"]
        and result["unique_full_optimum"]
        and result["true_regret_of_truncated_optimum"] > 0.99
        and result["indicator_assumption_holds"]
        and result["tail_is_nonzero"]
        and result["q4_assumption_holds"]
        and result["q4_actual_tail_l1"] > result["q4_paper_tail_bound"]
        and result["alternatives"]["claim_4_zero_tail_after_dimension_3"]
        and result["alternatives"]["claim_4_full_model_regret"] == 0.0
        and result["alternatives"]["claim_5_q1_holds"]
        and result["alternatives"]["claim_5_tested_q_ge_2_fail"]
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
