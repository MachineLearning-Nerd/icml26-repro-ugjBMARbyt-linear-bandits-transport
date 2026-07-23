# Claim 5 - Coefficient-decay interpolation

## Verdict: FALSIFIED

At `q=4`, a sequence satisfying literal Assumption 3 has coefficient tail
`1.632993` after order two. The v1 proof asserts an upper bound `0.215502`;
the residual is `1.417491`.

Separately, the sequence
`gamma_1=3`,
`gamma_n=0.1/(sqrt(n) log(n+1))`
is in `l2` and satisfies Assumption 3 for every positive `q`, but its `l1` tail
diverges. The premise therefore does not encode the decay used in the proof.

The finite pre-entry schedule slope is diagnostic only; the verdict rests on
the exact premise-to-tail counterexamples.

Evidence: `evidence/claim_5/`.
