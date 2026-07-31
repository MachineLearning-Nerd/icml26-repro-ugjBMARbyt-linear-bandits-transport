# Claim 6 source audit

ArXiv v1 Equations (9)--(12) define regularized least squares in
`L2(rho)`, the feature operator `M_t`, the design operator
`M_t^* M_t + lambda D Lambda`, and a log-determinant confidence radius.
The model is explicitly justified using the v1 Fourier identity.

There are two literal obligations:

1. actual transport feedback must be a linear functional of the declared
   Fourier action feature; and
2. Equation (12) must add operators on the same space.

The source uses `D Lambda + lambda^-1 M_t M_t^*`. For a finite Hilbert space
of dimension `N`, these have shapes `N x N` and `t x t`, respectively, so the
printed addition is not generally defined. The corrected observation-space
form inserts `I_t` and `(D Lambda)^-1`.

Exact anchors are Equations (7), (9)--(12), Proposition C.1, and Lemma C.2.
The feature-collision check attacks the declared linear observation model; the
independent shape check attacks the printed confidence width. The corrected
finite OFUL experiment is a separate positive control, not a repair silently
substituted into the paper claim.

Source provenance:

- ar5iv v1 HTML:
  `https://ar5iv.labs.arxiv.org/html/2502.07397v1`
- Fresh HTML SHA-256:
  `b8ac1371eae338c089931ad061935198b9f739b33080e88a40b2aed3e1b4d6b8`
- PDF: `https://arxiv.org/pdf/2502.07397v1`
- PDF SHA-256:
  `56a1dbed2bb2d0ee24320281cb37380cedf8f9b3be01b4366cd46a4622b86b7b`
- Fresh HTML retrieval and reread: 2026-07-31 with an explicit User-Agent.
