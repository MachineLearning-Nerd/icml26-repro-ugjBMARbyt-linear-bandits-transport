# Claim 3 source audit

The v1 Kantorovich regret is printed as `sum_t R_t - Kant`, subtracting one
comparator after `T` feedbacks. The proof instead sums one-step gaps, which
subtracts `T*Kant`. The exact entropy schedule is
`epsilon_t=alpha*t^{-alpha}` and the displayed approximation term depends on
`kappa`, `alpha`, and `T`.

This audit implements that schedule exactly and evaluates every RHS component,
while keeping the displayed regret definition literal.

Exact anchors are Equation (5), Theorem 5.2, Lemma D.1, Equation (29), and
the first instantaneous-regret display in Appendix D.2. For the finite
two-point marginals, Remark D.2 gives upper Rényi dimension zero. Lemma D.1
therefore gives the implemented `kappa=0+L=1`; it is not an estimated
constant.

Source provenance:

- ar5iv v1 HTML:
  `https://ar5iv.labs.arxiv.org/html/2502.07397v1`
- Fresh HTML SHA-256:
  `b8ac1371eae338c089931ad061935198b9f739b33080e88a40b2aed3e1b4d6b8`
- PDF: `https://arxiv.org/pdf/2502.07397v1`
- PDF SHA-256:
  `56a1dbed2bb2d0ee24320281cb37380cedf8f9b3be01b4366cd46a4622b86b7b`
- Fresh HTML retrieval and reread: 2026-07-31 with an explicit User-Agent.
