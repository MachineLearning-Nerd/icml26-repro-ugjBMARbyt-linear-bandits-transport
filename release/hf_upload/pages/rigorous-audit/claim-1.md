# Claim 1 · Fourier identity

## Paper contract

Equation (7) of arXiv `2502.07397v1` identifies the transport pairing with a
Fourier-space inner product for an arbitrary reference measure `rho`, and the
surrounding text treats the transform as an isometry.

## Paper verdict: FALSIFIED

On uniform `Z2 x Z2`, use the diagonal coupling and
`c(x,y)=(x-y)^2`. The coupling has the required marginals and an `L2(rho)`
density. The direct pairing is `0`, while the literal Equation (7) Fourier
inner product is `1/2`. A norm-one, zero-mean function is also transformed to
zero, producing an isometry residual of `1`.

| Evidence layer | Public trace | Result |
|---|---|---|
| Exact source | [Source audit](evidence/claim_1/source_audit.md) | Equation (7), transform definition, and premises |
| Primary construction | [Raw result](evidence/claim_1/raw_result.json) | Pairing residual `0.5`; norm residual `1` |
| Verdict contract | [Verdict trace](evidence/claim_1/verdict.json) | Literal paper claim fails |
| Independent implementation | [Checker output](evidence/claim_1/independent_checker_output.json) | Matrix calculation reproduces both failures |
| Negative control | [Mutation output](evidence/claim_1/negative_control_output.json) | Requiring the literal failed identity makes the checker exit nonzero |

## Different claim: VERIFIED

On uniform `Z2 x Z2`, the **normalized discrete Fourier transform** preserves
the `L2(rho)` norm and the transport pairing when the coupling is represented
by its density `d pi/d rho`. The pairing residual is below `1.3e-32`; the
isometry residual is `0`.

### What changed

The verified statement changes the normalization, frequency representation,
and measure representation. It is a finite-group repair control—not evidence
for the literal arbitrary-`rho` identity.

### Limitation

This verifies one exact finite-group specialization; it does not establish a
universal replacement theorem.
