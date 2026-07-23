# Claim 1 method

For the uniform Haar probability measure on `Z_2 x Z_2`, construct the
character matrix and normalize it by `1/sqrt(4)`. Transform both the continuous
cost sampled on the group and the coupling density `d pi/d rho`. Check Parseval
and the transport pairing to floating-point tolerance `1e-12`.

As a negative control, restore the paper's literal integration normalization
on the same nonzero-pairing transport problem. Its identity residual must
exceed `1.8`.
