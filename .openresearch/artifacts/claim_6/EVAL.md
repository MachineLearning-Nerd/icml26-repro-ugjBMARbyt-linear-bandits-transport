# Claim 6 evaluation

`FALSIFIED` requires all paper assumptions, two distinct valid transport plans
with identical declared features and expected-feedback gap greater than 0.99,
and an undefined printed Equation (12) addition for `N != t`. An independent
checker must agree.

The repaired OFUL formula must meet at least `1-delta` exact coverage over the
enumerated sub-Gaussian support and its determinant-lemma residual must be below
`1e-12`. This repair control prevents a coding failure from being mistaken for
a source failure. The undersized-radius negative control must fail coverage.
