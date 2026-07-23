# Reproduction: Bandit Optimal Transport claim audit

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/blob/master/notebooks/entucb_claim_audit.py)

This project audits six claims from arXiv
[2502.07397v1](https://arxiv.org/abs/2502.07397v1), the version matched by the
live judge record for OpenReview `ugjBMARbyt`. The previous Space used random
features and was judged 5/12. The new cumulative local-CPU suite solves real
2×2 and 3×3 optimal-transport problems, evaluates the exact Fourier,
confidence, determinant, entropy-schedule, and regret expressions, and runs an
independent checker plus a failing control for every claim.

Assessment: all six **literal v1** contracts are `FALSIFIED`. This is not a
claim that repaired OFUL or unitary-Fourier results are false, and it is not a
new live judge score. The current arXiv v2 changes several statements.

Headline paper-versus-observed numbers:

- Equation (7) predicts equality; observed exact residual: `1/2`.
- Theorem 5.1 RHS is at most `398,538.2`; literal printed regret is at least
  `113,728,635.5` at the audited horizon.
- Theorem 5.2 RHS is at most `582,745.7`; literal printed regret is at least
  `99,999,999.0`, with the exact schedule
  `epsilon_t=0.5 t^{-0.5}`.
- Corollary 5.3 predicts a finite-basis rate; its admitted 3×3 OT instance
  loses exactly `1` per round when the nonzero tail is omitted.

Compute: Apple ARM64 local CPU, one locked repository-level `uv` environment.
No GPU and no Hugging Face cpu-upgrade were needed. The large theorem horizon
is closed-form; no 100-million-step loop was run.

Read the [illustrated claim-by-claim report](reports/claim-by-claim/report.md)
or the [self-contained marimo tutorial](notebooks/entucb_claim_audit.py).

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `master` | Publication surface | Not run as an experiment (publication surface) | Validated starting point `e8a15a8`; pending release merge | — |
| [`orx/frozen-judged-code-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/frozen-judged-code-baseline) | Freeze judged code and lock `uv` | `uv run python repro/src/verify_entucb.py` | Reproduced historical toy output; no claim upgraded | local CPU, 10 s |
| [`orx/literal-v1-fourier-contract`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/literal-v1-fourier-contract) | Literal Fourier counterexample | `uv run python repro/src/verify_entucb.py` | Claim 1 `FALSIFIED` | local CPU |
| [`orx/unitary-discrete-fourier-specialization`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/unitary-discrete-fourier-specialization) | Corrected transform control | `uv run python repro/src/verify_entucb.py` | Corrected specialization verified; literal claim blocked | local CPU |
| [`orx/rls-confidence-set-contract-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/rls-confidence-set-contract-audit) | RLS, logdet, and coverage | `uv run python repro/src/verify_entucb.py` | Claims 1 and 6 `FALSIFIED` | local CPU, 5 s |
| [`orx/basis-rate-corollary-contract-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/basis-rate-corollary-contract-audit) | Actual OT and exact decay premise | `uv run python repro/src/verify_entucb.py` | Claims 1, 4, 5, 6 `FALSIFIED` | local CPU |
| [`orx/regret-theorem-definition-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/regret-theorem-definition-audit) | Full Theorems 5.1–5.2 terms | `uv run python repro/src/verify_entucb.py` | All six literal v1 claims `FALSIFIED` | local CPU, 45 s |
| [`orx/release-candidate-cumulative-evidence`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/release-candidate-cumulative-evidence) | Reports, notebook, additive Space candidate, release gates | `uv run python repro/src/verify_entucb.py` | Pending cumulative release-gate run | local CPU |

## Upstream project note

OpenReview `ugjBMARbyt`. arXiv `2502.07397`. Six judged claims / 12 possible
points. Existing Hugging Face Space: `DineshAI/ugjBMARbyt`.
