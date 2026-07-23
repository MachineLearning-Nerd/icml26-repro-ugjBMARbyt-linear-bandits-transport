# Claim 5 method

Evaluate the exact `zeta(n)=1-n^{-q}` premise for
`q in {1,2,4,8,16}` on the orthonormal 3×3 OT construction. At `q=4`, the
literal assumption holds but the actual coefficient tail after order 2 exceeds
the proof's asserted bound by more than 1.4. Run the prescribed order schedule
through the interval before the omitted direction enters and solve the actual
OT problem at every distinct order.

As a second exact control, use
`gamma_1=3` and `gamma_n=0.1/(sqrt(n) log(n+1))`. An integral comparison proves
membership in `l2`; the first two coefficients already make Assumption 3 hold
for every positive `q`; comparison with `n^{-3/4}` proves its `l1` tail
diverges. Thus the premise does not encode the claimed decay at all.
