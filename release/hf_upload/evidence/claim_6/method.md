# Claim 6 method

Reuse the exact 2×2 transport problem from Claim 1. Compare the diagonal and
off-diagonal couplings. They have identical literal Fourier features on the
integer support, but the continuous ground cost has expected feedback 0 and 1.
Therefore no linear predictor using the declared feature can represent both
noise-free observations.

Independently instantiate `N=4`, `t=3`, and a quadratic regularizer. Record the
operator shapes in printed Equation (12). As a repair control, evaluate the
standard observation-space OFUL determinant and confidence radius over every
one of the `2^3` Rademacher noise paths. Verify the determinant lemma in both
spaces. A five-percent radius is the negative control and must lose coverage.
