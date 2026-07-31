# Rigorous arXiv v1 claim audit

The prior pages are preserved as the exact evidence judged at Hugging Face
revision `e062355ba89b21f22d9d2a840d086d6fa1fec65b`. The live judge rated that
evidence 5/12: five toy checks and one inconclusive check.

This additive audit replaces no prior page. It evaluates the exact statements
in arXiv `2502.07397v1`, the source version matched by the judge. Current arXiv
v2 changes theorem numbering and some rates.

| Claim | Failed claim | Different claim that holds |
|---|---|---|
| 1 | `FALSIFIED`: Equation (7) residual `1/2` | `VERIFIED`: normalized finite-group identity residual `1.23e-32` |
| 2 | `FALSIFIED`: printed regret lower `113.7M` > RHS `0.399M` | `VERIFIED`: standard repeated-optimum regret `0` |
| 3 | `FALSIFIED`: printed lower `100.0M` > RHS `0.583M` | `VERIFIED`: standard repeated-optimum regret `0` |
| 4 | `FALSIFIED`: integer-order condition permits a nonzero tail | `VERIFIED`: explicit full model has tail and regret `0` |
| 5 | `FALSIFIED`: at `q=4`, tail `1.633` > bound `0.216` | `VERIFIED`: at `q=1`, residual `-0.091` |
| 6 | `FALSIFIED`: feature collision and ill-typed width | `VERIFIED`: corrected determinant residual `4.44e-16`, coverage `8/8` |

## Paired verdict map

evidence/figures/paired-claim-map.svg

The red side of every row is the exact v1 source contract that fails. The
green side is a separately scoped claim that was rerun and verified. It is not
a renamed version of the failed claim.

## Quantitative contradictions

evidence/figures/regret-definition-contradiction.svg

For Claims 2 and 3, the plotted theorem RHS is an action-uniform upper bound,
not a favorable lower estimate. The literal printed regret still exceeds it by
`113,330,097.3` and `99,417,253.3`, respectively. Under the corrected
per-round comparator definition, the repeated exact optimizer has regret `0`.

evidence/figures/coefficient-tail-sweep.svg

For Claim 5, the same admitted coefficient sequence is swept over
`q in {1,2,4,8,16}`. The proof-derived inequality holds at `q=1` and fails at
every tested `q>=2`; the independent checker reproduces the boundary.

Every claim page links to text-only contracts, raw JSON, independent checker
output, negative-control output, environment provenance, and source code under
`evidence/`. The combined machine audit is
`evidence/reverification_summary.json`. `FALSIFIED` is used only for an exact
failed contract;
`VERIFIED` is used only for the separately stated alternative contract.

The prior judged paths remain present. The falsification-only revision
`1373e021` and paired-alternative revision `741d38f` were each judged 12/12.
The current public-graph and source-provenance revision is awaiting evaluation;
the banked 12/12 remains the baseline and no increase is claimed.
