# Claim 3 source audit

The v1 Kantorovich regret is printed as `sum_t R_t - Kant`, subtracting one
comparator after `T` feedbacks. The proof instead sums one-step gaps, which
subtracts `T*Kant`. The exact entropy schedule is
`epsilon_t=alpha*t^{-alpha}` and the displayed approximation term depends on
`kappa`, `alpha`, and `T`.

This audit implements that schedule exactly and evaluates every RHS component,
while keeping the displayed regret definition literal.
