# Claim 5 · Coefficient-decay interpolation

## Paper contract

The v1 proof replaces an `l1` coefficient tail by an expression derived from
an `L2` norm and an `l1` head under Assumption 3. That step is used to obtain
the interpolation rate.

## Paper verdict: FALSIFIED

At `q=4`, an admitted finite sequence has coefficient tail `1.632993` after
order two, while the proof-derived upper bound is `0.215502`; the residual is
`1.417491`. Separately,
`gamma_1=3` and `gamma_n=0.1/(sqrt(n) log(n+1))` is in `l2` and satisfies
Assumption 3 for every positive `q`, but its `l1` tail diverges. The premise
does not encode the tail decay used by the proof.

| Evidence layer | Public trace | Result |
|---|---|---|
| Exact source | [Source audit](evidence/claim_5/source_audit.md) | Proof step, assumption, and quantifiers |
| Primary construction | [Raw result](evidence/claim_5/raw_result.json) | `q=4` residual `1.417491`; divergent `l1` control |
| Verdict contract | [Verdict trace](evidence/claim_5/verdict.json) | Proof-derived universal implication fails |
| Independent implementation | [Checker output](evidence/claim_5/independent_checker_output.json) | Recomputes all finite sweep values |
| Negative control | [Mutation output](evidence/claim_5/negative_control_output.json) | Requiring the false `q=4` inequality exits nonzero |

## Different claim: VERIFIED

For the same audited finite coefficient sequence, the paper-derived tail
inequality holds at the scoped boundary `q=1`, with residual `-0.091020`. It
fails at every tested `q in {2,4,8,16}`. Independent arithmetic reproduces the
boundary.

### What changed

The replacement fixes one sequence and one exponent (`q=1`); it removes the
paper's universal interpolation conclusion.

### Limitation

This boundary check is not a repaired decay theorem. It states only the exact
finite inequality that the trace verifies.
