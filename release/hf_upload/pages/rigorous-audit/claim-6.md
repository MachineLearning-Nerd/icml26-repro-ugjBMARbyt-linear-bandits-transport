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

## Alternative verdict: VERIFIED

On the audited 4-parameter, 3-observation linear control, the corrected
observation-space and parameter-space log determinants agree within
`4.44e-16`; the confidence radius covers all `8/8` Rademacher paths. An
independent checker reproduces both facts.

Evidence: `evidence/claim_6/`.
