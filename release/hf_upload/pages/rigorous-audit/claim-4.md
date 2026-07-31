# Claim 4 · Finite-basis equivalence

## Paper contract

The audited target is only Corollary 5.3's parenthetical assertion that its
integer-order indicator condition is equivalent to a zero coefficient tail.
It is not the broader conditional rate statement.

## Paper verdict: FALSIFIED

On a uniform 3×3 transport space, the literal integer-order condition with
`zeta(n)=1_{n>=2}` holds for a known orthonormal basis even though coefficient
three is nonzero. The claimed equivalence to a zero tail is therefore false.
The two-coordinate cost selects the diagonal plan; the full cost selects a
cyclic plan. Omitting the third coefficient loses exactly one per round:
`4096` at horizon `4096`, or `45.25 sqrt(NT)`.

| Evidence layer | Public trace | Result |
|---|---|---|
| Exact source | [Source audit](evidence/claim_4/source_audit.md) | Corollary wording and continuity boundary |
| Primary construction | [Raw result](evidence/claim_4/raw_result.json) | Admitted condition with tail `1.633` and regret `4096` |
| Verdict contract | [Verdict trace](evidence/claim_4/verdict.json) | Parenthetical equivalence fails |
| Independent implementation | [Checker output](evidence/claim_4/independent_checker_output.json) | Enumerates all six Birkhoff vertices |
| Repair control | [Control output](evidence/claim_4/negative_control_output.json) | Restoring the omitted coefficient reduces regret to `0` |

## Different claim: VERIFIED

On the same 3×3 instance, explicitly including all three nonzero coefficients
leaves a zero coefficient tail, recovers the full cyclic optimizer, and gives
zero cumulative regret. SciPy HiGHS and independent enumeration of all six
Birkhoff vertices agree.

### What changed

The replacement assumes the explicit full three-coordinate model instead of
inferring zero tail from the integer-order indicator.

### Limitation

The indicator used in the source equivalence is not continuous. This audit
does not present the broader rate as a counterexample satisfying Assumption 3's
continuity clause, and it does not dispute finite-dimensional OFUL when the
model truly has dimension `N`.
