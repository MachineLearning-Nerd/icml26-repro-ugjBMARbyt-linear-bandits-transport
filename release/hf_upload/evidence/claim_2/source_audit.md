# Claim 2 source audit

The v1 definition is printed as the sum of `T` noisy entropic objectives minus
one entropic optimum. The proof later defines one-step regret and states that
its sum equals the printed regret, which would instead subtract the optimum
`T` times. This audit treats the displayed definition literally.

Exact anchors are Equation (6), Theorem 5.1, and the first two displayed
formulae in Appendix D.1. The contradiction is source-internal: Equation (6)
has one `Ent.` term outside the sum, while Appendix D.1 defines every `r_t`
with its own `-Ent.` term and then says their sum equals the same regret.

The bound computation includes `sigma`, `C_bar`, `beta_T`, and both
log-determinants. Because printed Equation (12) is ill-typed, the experiment
uses the charitable compatible-space identity and then an action-uniform
rank/trace upper bound. A violation of this larger RHS is stronger than one
based on a favorable action sequence.

Source provenance:

- ar5iv v1 HTML:
  `https://ar5iv.labs.arxiv.org/html/2502.07397v1`
- Fresh HTML SHA-256:
  `b8ac1371eae338c089931ad061935198b9f739b33080e88a40b2aed3e1b4d6b8`
- PDF: `https://arxiv.org/pdf/2502.07397v1`
- PDF SHA-256:
  `56a1dbed2bb2d0ee24320281cb37380cedf8f9b3be01b4366cd46a4622b86b7b`
- Fresh HTML retrieval and reread: 2026-07-31 with an explicit User-Agent.
