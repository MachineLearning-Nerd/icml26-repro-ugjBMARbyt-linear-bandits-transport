# Claim 1 evaluation

The verifier writes the machine result at run time. Its only full-credit
verdict is `FALSIFIED`, requiring:

1. every stated assumption to pass;
2. an Equation (7) residual greater than `0.49` (exact value `1/2`);
3. an isometry squared-norm residual greater than `0.99` (exact value `1`);
4. agreement from the independent matrix checker; and
5. failure of the deliberately false identity-required negative control.

Any missing condition exits nonzero and records `BLOCKED`, never `PASS`.

The paired alternative is `VERIFIED` only when the normalized `Z2 x Z2`
transform has pairing and isometry residuals below `1e-12`, the literal
normalization fails by more than `1.8`, and the independent checker agrees.
