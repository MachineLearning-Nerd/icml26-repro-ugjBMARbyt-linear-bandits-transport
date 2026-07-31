# Provenance and limitations

- Paper contract: arXiv `2502.07397v1`.
- Fresh ar5iv v1 HTML SHA-256:
  `b8ac1371eae338c089931ad061935198b9f739b33080e88a40b2aed3e1b4d6b8`.
- V1 PDF SHA-256:
  `56a1dbed2bb2d0ee24320281cb37380cedf8f9b3be01b4366cd46a4622b86b7b`.
- Fixed command: `uv run python repro/src/verify_entucb.py`.
- Winning scientific Git commit:
  `9a0aeebd6303283e86e5b58079651ffa4e94a4ca`.
- Compute: local Apple ARM64 CPU; no GPU and no Hugging Face upgrade.
- Environment: one locked CPython 3.12 `uv` specification. The editable
  checkout has one repository-level `.venv`; isolated `orx local` run
  checkouts recreated the same locked environment while sharing the `uv`
  cache. This is a disclosed deviation from one physical `.venv` across runs.
- Seeds: none for exact constructions; all eight Rademacher paths are
  enumerated for the stochastic confidence control.

The verdicts apply to literal v1 contracts. They do not silently transfer to
current v2 or to corrected unitary-Fourier, OFUL, source-condition, or
per-round-regret statements.

The protected prior revision and its 17-file manifest are recorded on the
Prior judged revision page. The release candidate is additive and text-only.
The machine-readable subset proof and full command ledger are included under
`evidence/release/`.
