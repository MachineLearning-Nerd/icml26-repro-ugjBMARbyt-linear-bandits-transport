# Claim 6 source audit

ArXiv v1 Equations (9)--(12) define regularized least squares in
`L2(rho)`, the feature operator `M_t`, the design operator
`M_t^* M_t + lambda D Lambda`, and a log-determinant confidence radius.
The model is explicitly justified using the v1 Fourier identity.

There are two literal obligations:

1. actual transport feedback must be a linear functional of the declared
   Fourier action feature; and
2. Equation (12) must add operators on the same space.

The source uses `D Lambda + lambda^-1 M_t M_t^*`. For a finite Hilbert space
of dimension `N`, these have shapes `N x N` and `t x t`, respectively, so the
printed addition is not generally defined. The corrected observation-space
form inserts `I_t` and `(D Lambda)^-1`.
