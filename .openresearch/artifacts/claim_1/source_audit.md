# Claim 1 source audit

The judged statement is from arXiv v1, Section 4.1, Equation (7), under
Assumption 1. The v1 source defines a reference probability measure `rho`,
defines the function transform by integrating against that same `rho`, asserts
that this operator is an isometry on `L2(rho)`, and then uses this assertion to
identify the transport duality pairing with an `L2(rho)` inner product.

The appendix repeats the arbitrary-`rho` transform in its Fourier and
Plancherel statements. Classical Plancherel instead uses Haar/Lebesgue measure,
so the arbitrary probability reference measure cannot be silently replaced in
the contract.

Exact source provenance:

- PDF: `https://arxiv.org/pdf/2502.07397v1`
- PDF SHA-256:
  `56a1dbed2bb2d0ee24320281cb37380cedf8f9b3be01b4366cd46a4622b86b7b`
- Source archive: `https://export.arxiv.org/e-print/2502.07397v1`
- Source archive SHA-256:
  `a0aacd1eef4f15691ab0bd6dca092a58da3bad467827c3f1d53d4d7ff899e06a`
- Retrieved: 2026-07-23 with an explicit audit User-Agent.

This check evaluates the literal v1 operator. The corrected unitary finite
Fourier transform is a separate sibling experiment and is not evidence for
the literal statement.
