# Claim 3 - Decaying entropy Kantorovich bound

## Verdict: FALSIFIED

The exact schedule is implemented with `alpha=1/2`:
`epsilon_t=0.5 t^{-0.5}` and `epsilon_T=0.00005` at
`T=100,000,000`. A constant-schedule mutation is rejected.

The genuine Kantorovich comparator of the nonconstant 2×2 cost is `1`.
Every action sequence therefore has literal printed regret at least
`99,999,999`. The complete theorem RHS upper bound is `582,745.7`, including
the confidence terms and the full `kappa=1` approximation term
`184,207.4`.

The contradiction is specific to the v1 displayed regret definition. The
standard per-round comparator control has zero repeated-optimum regret.

## Alternative verdict: VERIFIED

On this audited nonconstant 2x2 instance, standard Kantorovich regret
subtracting the optimum every round is zero for the repeated exact optimizer.
The returned plan is evaluated directly; corrected regret and the
printed-regret decomposition residual are both below `1e-12`.

Evidence: `evidence/claim_3/`.
