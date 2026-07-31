# Start here: what changed, why it changed, and what proves it

The original logbook tested small simulations. Those checks were useful, but
they did not test the exact mathematical statements in arXiv `2502.07397v1`.
This additive audit does. It preserves every previously judged page while
providing six paired results:

- the paper claim, quoted and tested under its stated premises, is
  **FALSIFIED**;
- a different, narrower claim is stated explicitly and **VERIFIED**.

evidence/figures/reproduction-audit-poster.svg

## What improved

| Earlier evidence | Current evidence |
|---|---|
| Small simulation trends | Exact finite counterexamples and exhaustive controls |
| One undifferentiated `PASS` | Paired `FALSIFIED` paper claim and `VERIFIED` replacement |
| One implementation | Primary verifier plus an independent checker |
| No failure calibration | A negative or repair control with a predeclared outcome |
| Informal paper references | Exact v1 equation, theorem, corollary, and proof anchors |
| Console-oriented output | Public JSON traces, source, tables, dashboard, graphs, and poster |

evidence/figures/evidence-quality-dashboard.svg

Each green verdict is narrower than the red verdict beside it. “Premises” in
the dashboard means the exact assumptions used by that row were checked. For
Claim 4, the falsified target is only the corollary's parenthetical
indicator-to-zero-tail equivalence; the audit does not claim a counterexample
to the broader rate under the paper's continuity assumption.

## Read any claim in four steps

| Step | What to inspect | Why it matters |
|---|---|---|
| 1. Paper contract | Exact v1 source location and premises | Prevents testing a paraphrase or a newer version |
| 2. Failed trace | Raw construction and numerical/algebraic contradiction | Shows why `FALSIFIED` is warranted |
| 3. Calibration | Independent checker and negative/repair control | Detects shared bugs and vacuous verifiers |
| 4. Replacement | A separately worded, scoped statement | Shows exactly what still holds |

## Claim index

| Claim | Exact paper target that fails | Different claim that holds |
|---|---|---|
| [1 · Fourier identity](#/rigorous-claim-1) | Equation (7) with the printed transform | Normalized finite-group identity on uniform `Z2 x Z2` |
| [2 · Entropic regret](#/rigorous-claim-2) | One comparator subtracted from a `T`-round sum | Comparator subtracted once per round on the audited instance |
| [3 · Decaying entropy](#/rigorous-claim-3) | Same printed-regret mismatch under the exact schedule | Per-round Kantorovich comparator on the audited instance |
| [4 · Finite basis](#/rigorous-claim-4) | Indicator condition claimed equivalent to a zero tail | Explicit full three-coordinate model |
| [5 · Coefficient decay](#/rigorous-claim-5) | Proof-derived tail inequality at `q=4` | The same finite sequence at the scoped boundary `q=1` |
| [6 · Confidence set](#/rigorous-claim-6) | Colliding features and ill-typed Equation (12) | Corrected observation-space finite linear control |

> Scope: these are literal v1 audits and finite replacement claims. They do not
> assert that every idea in the paper is false or that a repaired theorem holds
> universally.

The machine-readable paired summary is
[`evidence/reverification_summary.json`](evidence/reverification_summary.json).
