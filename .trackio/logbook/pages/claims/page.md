# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_7f1000867ff3", "created_at": "2026-07-21T20:56:24+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. The EntUCB algorithm embeds transport plans into a Hilbert space via the Fourier isometry F on L²(ℝᵈ;ϱ), reducing the bandit optimal transport problem to linear bandit estimation in that space (Section 4.1, Equation 7).
2. Theorem 5.1 bounds the entropic regret as R_T^{H,ε}(A) ≤ σ√(2T log(2/δ)) + 2Cβ_T(δ)√(T log det(...)) with probability at least 1-δ (Theorem 5.1).
3. Theorem 5.2 shows that for Lipschitz costs with an entropy penalty decaying as ε_t = αt^{-α}, EntUCB achieves sublinear regret matching classical linear-bandit rates for the Kantorovich optimal transport problem (Theorem 5.2).
4. Corollary 5.3 establishes that in finite-dimensional/discrete settings with N basis coefficients, the algorithm attains Õ(√(NT)) regret, recovering the parametric OFUL-style rate (Corollary 5.3).
5. Corollary 5.4 shows that when basis coefficients decay at rate 1-n^{-q}, regret interpolates between Õ(√T) and Õ(T) depending on the decay exponent q (Corollary 5.4).
6. The confidence sets used by the algorithm are constructed via regularized least-squares in L²(ℝᵈ;ϱ), with width controlled by the log-determinant of the design operator, mirroring the classical OFUL confidence ellipsoid construction (Equations 11-12).
