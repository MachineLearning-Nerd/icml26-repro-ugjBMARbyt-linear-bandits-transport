# Claim 2 - Entropic regret bound

## Verdict: FALSIFIED

V1 prints entropic regret as a sum of `T` entropic objectives minus one
entropic optimum. Its proof later sums one-step gaps, which would subtract the
optimum `T` times.

On a nonconstant 2×2 cost, the exact entropic comparator is
`1.1372863664`. At `T=100,000,000`, every action sequence has literal printed
regret at least `113,728,635.5`. A charitable action-uniform upper bound on the
complete theorem RHS is `398,538.2`.

The RHS computation includes `sigma=1e-6`, `C_bar=1.5811388301`,
`beta_T<=1.5811475200`, and the width log determinant `<=63.5323758513`.
Subtracting the comparator every round gives zero for a repeated optimal action
and removes this contradiction.

Evidence: `evidence/claim_2/`.
