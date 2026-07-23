# Claim 4 method

Construct a known orthonormal basis on a uniform 3×3 discrete transport space.
The first two coefficients satisfy literal Assumption 3 at `N=2`; a third
coefficient is nonzero. The first-two-coordinate cost has the diagonal coupling
as its unique optimum, while the full cost has a cyclic coupling as its unique
optimum.

Solve both transport linear programs with SciPy HiGHS and independently
enumerate all six Birkhoff vertices. Evaluate the truncated plan under the true
cost for 4096 rounds. Including the omitted third coefficient is the negative
control and must reduce regret to zero.
