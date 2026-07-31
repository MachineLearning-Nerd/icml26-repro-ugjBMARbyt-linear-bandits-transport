# Claim 1 - Fourier identity

## Verdict: FALSIFIED

With uniform marginals on `{0,1}` and product reference `rho`, take the diagonal
coupling and `c(x,y)=(x-y)^2`. The coupling has the required marginals and an
`L2(rho)` density.

The direct pairing is `0`; the literal v1 Fourier inner product is `1/2`. A
norm-one zero-mean function is transformed to zero, independently contradicting
isometry.

A corrected unitary finite-group transform reproduces the pairing, but changes
the paper's normalization, frequencies, and measure representation. It is a
repair control, not evidence for the literal statement.

## Alternative verdict: VERIFIED

On uniform `Z2 x Z2`, the normalized discrete Fourier transform preserves the
`L2(rho)` norm and transport pairing when the coupling is represented by
`d pi/d rho`. Pairing residual is below `1.3e-32`; isometry residual is `0`.
An independent matrix checker reproduces both results.

Evidence: `evidence/claim_1/`.
