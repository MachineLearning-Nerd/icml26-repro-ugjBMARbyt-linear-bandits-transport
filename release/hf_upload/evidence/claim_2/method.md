# Claim 2 method

Use uniform two-point marginals and the nonconstant cost
`c(x,y)=1+(x-y)^2`. Solve its fixed-epsilon entropic OT comparator exactly.
Every admissible action has entropic objective at least this positive
comparator; therefore the printed regret is at least `(T-1) Ent` for every
possible EntUCB action sequence.

At `T=100,000,000`, compute a uniform upper bound on the theorem RHS using
feature norm at most one, dimension four, the matrix determinant lemma and the
AM-GM trace bound. Zero noise is `sigma^2`-sub-Gaussian for the declared
strictly positive `sigma=1e-6`. An independent scalar implementation repeats
the arithmetic. Subtracting the comparator every round is the corrected-regret
control.
