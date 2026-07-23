# Claim 4 - Finite-basis rate

## Verdict: FALSIFIED

The literal Assumption 3 with `zeta(n)=1_{n>=2}` holds for a known orthonormal
basis on a uniform 3×3 transport space, although coefficient three is nonzero.
Thus the paper's parenthetical equivalence with a zero tail is false.

The two-coordinate cost uniquely selects the diagonal plan. The full cost
uniquely selects a cyclic plan. SciPy HiGHS and independent enumeration of all
six Birkhoff vertices agree. The truncated plan loses exactly one per round:
`4096` at horizon `4096`, or `45.25*sqrt(NT)`. Including the omitted coefficient
gives zero regret.

This does not dispute the usual finite-dimensional OFUL rate when the model
really has dimension `N`.

Evidence: `evidence/claim_4/`.
