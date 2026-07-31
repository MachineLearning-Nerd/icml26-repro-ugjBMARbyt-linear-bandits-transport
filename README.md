---
title: "Repro - Linear Bandits beyond Inner Product Spaces"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-ugjBMARbyt
---

# Reproduction: Bandit Optimal Transport claim audit

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/blob/master/notebooks/entucb_claim_audit.py)

This project audits six claims from arXiv
[2502.07397v1](https://arxiv.org/abs/2502.07397v1), the version matched by the
live judge record for OpenReview `ugjBMARbyt`. The previous Space used random
features and was judged 5/12. The new cumulative local-CPU suite solves real
2×2 and 3×3 optimal-transport problems, evaluates the exact Fourier,
confidence, determinant, entropy-schedule, and regret expressions, and runs an
independent checker plus a calibration control with a predeclared outcome for
every claim.

Assessment: all six **literal v1** contracts remain `FALSIFIED`, and six
different, explicitly scoped replacement claims are `VERIFIED`. Every pair has
raw traces, an independent checker, and a negative or repair control. The
current arXiv v2 changes several statements.

Published evidence:
[`DineshAI/ugjBMARbyt@1373e021`](https://huggingface.co/spaces/DineshAI/ugjBMARbyt/commit/1373e02110b2b0c18efb3eee76e889d3c214c85a).
That falsification-only revision remains public and preserved. The paired
verdict revision is published additively. The live judge awarded revision
`1373e021` and the paired-alternative revision `741d38f` **12/12**. The
current re-verification adds public SVG traces, a paired evidence dashboard,
an audit poster, and source provenance without removing either judged evidence
tree; it is awaiting evaluation.

Headline paper-versus-observed numbers:

- Equation (7) predicts equality; observed exact residual: `1/2`.
- Theorem 5.1 RHS is at most `398,538.2`; literal printed regret is at least
  `113,728,635.5` at the audited horizon.
- Theorem 5.2 RHS is at most `582,745.7`; literal printed regret is at least
  `99,999,999.0`, with the exact schedule
  `epsilon_t=0.5 t^{-0.5}`.
- Corollary 5.3's parenthetical equates its indicator condition with a zero
  coefficient tail; the admitted 3×3 construction has a nonzero tail and loses
  exactly `1` per round when that coefficient is omitted.

Paired replacement claims:

- a normalized `Z2 x Z2` Fourier transform preserves the audited pairing and
  norm;
- standard per-round entropic and Kantorovich regret are zero for the repeated
  exact optimizers;
- explicitly including all three nonzero coefficients gives zero tail and
  zero regret;
- the audited tail inequality holds at `q=1` and fails at every tested
  `q>=2`; and
- the corrected OFUL determinant identity holds and its radius covers all
  eight enumerated noise paths.

Compute: Apple ARM64 local CPU with one locked `uv` specification. The editable
checkout has one repository-level `.venv`; `orx local` executes in isolated
checkouts and recreated that same locked environment per run while sharing the
`uv` cache. This is an execution-layout deviation from the requested single
physical `.venv`, not a dependency change. No GPU or Hugging Face cpu-upgrade
was needed. The large theorem horizon is closed-form; no 100-million-step loop
was run.

Read the [illustrated claim-by-claim report](reports/claim-by-claim/report.md)
or the [self-contained marimo tutorial](notebooks/entucb_claim_audit.py).

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `master` | Publication surface | Not run as an experiment (publication surface) | Mirrors current reverified HF evidence; `741d38f` was judged 12/12 | — |
| [`orx/frozen-judged-code-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/frozen-judged-code-baseline) | Freeze judged code and lock `uv` | `uv run python repro/src/verify_entucb.py` | Reproduced historical toy output; no claim upgraded | local CPU, 10 s |
| [`orx/literal-v1-fourier-contract`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/literal-v1-fourier-contract) | Literal Fourier counterexample | `uv run python repro/src/verify_entucb.py` | Claim 1 `FALSIFIED` | local CPU |
| [`orx/unitary-discrete-fourier-specialization`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/unitary-discrete-fourier-specialization) | Corrected transform control | `uv run python repro/src/verify_entucb.py` | Corrected specialization verified; literal claim blocked | local CPU |
| [`orx/rls-confidence-set-contract-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/rls-confidence-set-contract-audit) | RLS, logdet, and coverage | `uv run python repro/src/verify_entucb.py` | Claims 1 and 6 `FALSIFIED` | local CPU, 5 s |
| [`orx/basis-rate-corollary-contract-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/basis-rate-corollary-contract-audit) | Actual OT and exact decay premise | `uv run python repro/src/verify_entucb.py` | Claims 1, 4, 5, 6 `FALSIFIED` | local CPU |
| [`orx/regret-theorem-definition-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/regret-theorem-definition-audit) | Full Theorems 5.1–5.2 terms | `uv run python repro/src/verify_entucb.py` | All six literal v1 claims `FALSIFIED` | local CPU, 45 s |
| [`orx/release-candidate-cumulative-evidence`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/release-candidate-cumulative-evidence) | Reports, notebook, additive Space candidate, internal release gates | `uv run python repro/src/verify_entucb.py` | All six `FALSIFIED`; internal gate passed; external subset check was still pending | local CPU, 65 s |
| [`orx/publication-snapshot-and-full-release-gate`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/publication-snapshot-and-full-release-gate) | Materialized evidence, five figures, protected-tree subset proof, exact upload allowlist | `uv run python repro/src/verify_entucb.py` | All six `FALSIFIED`; full gate passed; prose overstated physical `.venv` reuse | local CPU, 91 s |
| [`orx/honest-environment-disclosure-release`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/honest-environment-disclosure-release) | Correct environment-layout disclosure and rerun every gate | `uv run python repro/src/verify_entucb.py` | Final gate passed; exact payload published at HF `1373e021` | local CPU, 70 s |

## Upstream project note

OpenReview `ugjBMARbyt`. arXiv `2502.07397`. Six judged claims / 12 possible
points. Existing Hugging Face Space: `DineshAI/ugjBMARbyt`.
