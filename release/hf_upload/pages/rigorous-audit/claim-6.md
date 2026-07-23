# Claim 6 - RLS confidence set

## Verdict: FALSIFIED

The diagonal and off-diagonal 2×2 couplings are both valid and have identical
literal Fourier features, yet their expected noise-free costs are `0` and `1`.
No linear predictor on the declared feature can represent both observations.

For `N=4,t=3`, printed Equation (12) also adds a 4×4 `D Lambda` operator to a
3×3 `M M*` matrix, so the expression is undefined.

A corrected observation-space OFUL formula satisfies the determinant lemma and
covers all eight Rademacher noise paths: exact coverage `1.0` at required
coverage `0.9`. A five-percent radius loses coverage. This control separates
the source contradiction from a broken RLS implementation.

Evidence: `evidence/claim_6/`.
