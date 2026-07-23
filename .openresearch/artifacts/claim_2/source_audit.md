# Claim 2 source audit

The v1 definition is printed as the sum of `T` noisy entropic objectives minus
one entropic optimum. The proof later defines one-step regret and states that
its sum equals the printed regret, which would instead subtract the optimum
`T` times. This audit treats the displayed definition literally.

The bound computation includes `sigma`, `C_bar`, `beta_T`, and both
log-determinants. Because printed Equation (12) is ill-typed, the experiment
uses the charitable compatible-space identity and then an action-uniform
rank/trace upper bound. A violation of this larger RHS is stronger than one
based on a favorable action sequence.
