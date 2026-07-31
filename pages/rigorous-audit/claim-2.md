# Claim 2 · Entropic regret bound

## Paper contract

Equation (6) of arXiv `2502.07397v1` defines regret as a sum of `T` entropic
objectives minus **one** entropic optimum. The proof later sums one-step gaps,
which would subtract that optimum `T` times.

## Paper verdict: FALSIFIED

For the audited nonconstant 2×2 cost, the exact entropic comparator is
`1.1372863664`. At `T=100,000,000`, every action sequence therefore has literal
printed regret at least `113,728,635.5`. A deliberately generous,
action-uniform upper bound on the complete theorem right-hand side is only
`398,538.2`, leaving a contradiction margin of `113,330,097.3`.

| Evidence layer | Public trace | Result |
|---|---|---|
| Exact source | [Source audit](evidence/claim_2/source_audit.md) | Equation (6), theorem, and proof mismatch |
| Primary construction | [Raw result](evidence/claim_2/raw_result.json) | Lower bound `113.7M` exceeds RHS `0.399M` |
| Verdict contract | [Verdict trace](evidence/claim_2/verdict.json) | Complete literal bound fails |
| Independent implementation | [Checker output](evidence/claim_2/independent_checker_output.json) | Recomputes comparator, lower bound, and RHS |
| Negative control | [Mutation output](evidence/claim_2/negative_control_output.json) | Restoring one-time subtraction recreates `113.7M` regret |

## Different claim: VERIFIED

On this exact 2×2 instance, standard entropic regret that subtracts the optimum
**once per round** is `0` for the repeated exact entropic optimizer. The
optimizer objective is recomputed from its plan; both corrected regret and the
printed-regret decomposition residual are below `1e-12`.

### What changed

The replacement changes the comparator multiplicity from once overall to once
per round and limits the assertion to the audited finite instance.

### Limitation

Zero regret for this repeated optimizer is an instance control, not a proof of
the paper's full theorem under a corrected definition.
