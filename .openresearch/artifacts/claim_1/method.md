# Claim 1 method

Use two uniform marginals on `{0,1}` and reference measure `rho` equal to their
four-point product. Let `pi` be the diagonal coupling and
`c(x,y)=(x-y)^2`.

This is a genuine transport instance:

- `pi` has both required uniform marginals;
- `d pi / d rho = (2,0,0,2)` is in `L2(rho)`;
- the polynomial cost is continuous and in `L2(rho)`.

On integer support and integer frequencies drawn from `rho`, every phase in
the paper's literal kernel is one. Direct rational arithmetic therefore gives
`<c,pi>=0` but the proposed Fourier inner product equals `1/2`. A second
zero-mean test function has input squared norm `1` and transformed squared
norm `0`, directly contradicting isometry.

The primary implementation and independent NumPy matrix implementation share
only the declared instance. The negative control mutates the checker to
require Equation (7) to hold; it must exit with status 1.
