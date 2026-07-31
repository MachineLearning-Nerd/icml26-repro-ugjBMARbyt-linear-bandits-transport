# Claim 5 source audit

The v1 proof replaces the coefficient tail by the `L2` norm minus the
cumulative coefficient `l1` head. This equality is false in general. Assumption
3 only lower-bounds the cumulative `l1` head; it neither equates total `l1` and
`l2` norms nor imposes the claimed polynomial tail.

The current v2 paper changes this part of the result, including the displayed
exponent. This experiment audits the v1 corollary selected by the live judge.

Exact anchors are Assumption 3, Corollary 5.4, Theorem E.8, Equation (42), and
the following displayed equality. The finite q-sweep checks the claimed
inequality directly. The separate infinite sequence shows the premise can hold
while the coefficient `l1` tail diverges, so the issue is not numerical
roundoff or one selected q.

Source provenance:

- ar5iv v1 HTML:
  `https://ar5iv.labs.arxiv.org/html/2502.07397v1`
- Fresh HTML SHA-256:
  `b8ac1371eae338c089931ad061935198b9f739b33080e88a40b2aed3e1b4d6b8`
- PDF: `https://arxiv.org/pdf/2502.07397v1`
- PDF SHA-256:
  `56a1dbed2bb2d0ee24320281cb37380cedf8f9b3be01b4366cd46a4622b86b7b`
- Fresh HTML retrieval and reread: 2026-07-31 with an explicit User-Agent.
