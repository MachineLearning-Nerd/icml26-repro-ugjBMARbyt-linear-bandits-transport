# Rigorous arXiv v1 claim audit

The prior pages are preserved as the exact evidence judged at Hugging Face
revision `e062355ba89b21f22d9d2a840d086d6fa1fec65b`. The live judge rated that
evidence 5/12: five toy checks and one inconclusive check.

This additive audit replaces no prior page. It evaluates the exact statements
in arXiv `2502.07397v1`, the source version matched by the judge. Current arXiv
v2 changes theorem numbering and some rates.

| Claim | Verdict | Decisive observation |
|---|---|---|
| 1 | FALSIFIED | Equation (7) gives `0` versus `1/2` on an admitted coupling |
| 2 | FALSIFIED | printed regret lower `113.7M` exceeds complete RHS upper `0.399M` |
| 3 | FALSIFIED | exact entropy schedule; printed lower `100.0M` exceeds RHS upper `0.583M` |
| 4 | FALSIFIED | admitted basis tail changes a real 3×3 OT optimum; regret `1/round` |
| 5 | FALSIFIED | admitted tail `1.633` exceeds asserted bound `0.216` |
| 6 | FALSIFIED | identical Fourier features have expected feedback `0` and `1` |

Every claim page links to text-only contracts, raw JSON, independent checker
output, negative-control output, environment provenance, and source code under
`evidence/`. `FALSIFIED` is used only for a counterexample satisfying the
literal source assumptions. Corrected controls are reported separately.

No live judge score increase is claimed by this candidate.
