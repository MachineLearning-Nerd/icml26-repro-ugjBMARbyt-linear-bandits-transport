# Claim 3 · Decaying-entropy Kantorovich bound

## Paper contract

The v1 decaying-entropy result uses the printed regret definition together with
the exact schedule `epsilon_t = 0.5 t^{-1/2}`. At
`T=100,000,000`, `epsilon_T=0.00005`.

## Paper verdict: FALSIFIED

The genuine Kantorovich comparator of the same nonconstant 2×2 cost is `1`.
Every action sequence has literal printed regret at least `99,999,999`. The
complete theorem right-hand side is at most `582,745.7`, including confidence
terms and the full `kappa=1` approximation term `184,207.4`. The contradiction
margin is `99,417,253.3`.

| Evidence layer | Public trace | Result |
|---|---|---|
| Exact source | [Source audit](evidence/claim_3/source_audit.md) | Schedule, regret definition, theorem, and premises |
| Primary construction | [Raw result](evidence/claim_3/raw_result.json) | Lower bound `100.0M` exceeds RHS `0.583M` |
| Verdict contract | [Verdict trace](evidence/claim_3/verdict.json) | Complete literal bound fails |
| Independent implementation | [Checker output](evidence/claim_3/independent_checker_output.json) | Recomputes schedule and both sides |
| Negative control | [Mutation output](evidence/claim_3/negative_control_output.json) | Constant-schedule mutation is rejected |

## Different claim: VERIFIED

On this exact 2×2 instance, Kantorovich regret subtracting the optimum once per
round is `0` for the repeated exact optimizer. The returned plan is evaluated
directly; corrected regret and the decomposition residual are below `1e-12`.

### What changed

The replacement uses the standard per-round comparator and is explicitly
instance-specific. It retains the audited optimizer but not the printed regret
definition.

### Limitation

This finite control does not prove a general decaying-entropy regret rate.
