# Claim 3 method

Use the same nonconstant 2×2 cost and solve the genuine Kantorovich LP. Its
minimum is one, so every valid action sequence has printed zero-noise regret at
least `T-1`. The finite support has upper Rényi dimension zero and the exact
support Lipschitz constant is one, giving `kappa=1`.

Set `alpha=1/2`; calculate schedule anchors through
`T=100,000,000`, including `epsilon_T=0.00005`. Add the complete v1
approximation term to the action-uniform confidence-bound upper bound. A
constant-epsilon schedule is the negative control and must be rejected.
