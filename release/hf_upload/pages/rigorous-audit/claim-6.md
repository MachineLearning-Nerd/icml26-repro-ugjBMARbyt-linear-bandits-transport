# Claim 6 · RLS confidence set

## Paper contract

The v1 model declares Fourier features for transport observations and Equation
(12) gives its confidence-width expression.

## Paper verdict: FALSIFIED

The diagonal and off-diagonal 2×2 couplings are both valid and have identical
literal Fourier features, yet their expected noise-free costs are `0` and `1`.
No linear predictor on the declared feature can represent both observations.
Independently, for `N=4,t=3`, Equation (12) adds a 4×4 `D Lambda` operator to a
3×3 `M M*` matrix, so the expression is undefined.

| Evidence layer | Public trace | Result |
|---|---|---|
| Exact source | [Source audit](evidence/claim_6/source_audit.md) | Feature declaration and Equation (12) dimensions |
| Primary construction | [Raw result](evidence/claim_6/raw_result.json) | Feature gap `0`, feedback gap `1`, 4×4 + 3×3 mismatch |
| Verdict contract | [Verdict trace](evidence/claim_6/verdict.json) | Literal linear model and width fail |
| Independent implementation | [Checker output](evidence/claim_6/independent_checker_output.json) | Reproduces collision, dimensions, and repair |
| Negative control | [Mutation output](evidence/claim_6/negative_control_output.json) | Five-percent undersized radius loses coverage |

## Different claim: VERIFIED

On the audited four-parameter, three-observation linear control, the corrected
observation-space and parameter-space log determinants agree within
`4.44e-16`. The corrected confidence radius covers all `8/8` Rademacher noise
paths, exceeding the required `0.9` coverage.

### What changed

The replacement uses a dimensionally valid observation-space formula and a
separately specified finite linear model; it does not reuse the colliding
paper feature.

### Limitation

This validates the corrected finite control, not the paper's original feature
map or a universal RLS theorem.
