# Claim-by-claim audit of Bandit Optimal Transport

![Six literal v1 claim verdicts](images/headline_claims.png)

The paper asks whether optimal-transport decisions can be learned with the same
kind of confidence geometry and regret rates as linear bandits. The original
Space answered with six small random-feature checks. The live judge correctly
classified five as toy evidence and one as inconclusive.

This reproduction audits the exact arXiv v1 statements selected by the judge,
translates every quantifier into a machine-checkable contract, and tests an
admissible counterexample alongside a distinct replacement claim. All six
literal v1 contracts are falsified, and all six replacement claims are
verified. That conclusion is narrower than “the research direction is wrong”:
several failures are source-definition or normalization errors, and the
current arXiv v2 has changed some statements.

## What was implemented

The fixed command is:

```bash
uv run python repro/src/verify_entucb.py
```

It runs one cumulative CPU suite. The important code path is:

1. construct finite probability measures and genuine coupling matrices;
2. check marginals, absolute continuity, `L2` membership, continuity or a
   continuous extension, sub-Gaussian noise, and every theorem parameter;
3. solve Kantorovich problems with SciPy HiGHS and 2×2 entropic OT in closed
   form;
4. compute the exact Fourier, RLS, confidence-radius, determinant, entropy
   schedule, and regret quantities printed in v1;
5. run an independent implementation and a deliberately failing control for
   every claim; and
6. exit nonzero unless every cumulative verdict contract is met.

The editable checkout has one repository-level CPython 3.12 `.venv`, pinned by
`pyproject.toml` and `uv.lock`. OpenResearch local jobs run from isolated
checkouts, so `uv run` recreated the same locked environment inside each run
checkout while reusing the shared `uv` cache. This deviates from the requested
single physical `.venv` across all nodes; no dependency version or command
changed. No GPU or Hugging Face upgrade was needed.

## The Fourier reduction fails on an admitted transport problem

![Fourier counterexample](images/fourier_counterexample.png)

Equation (7) defines the transform by integrating against an arbitrary
reference probability measure `rho` and calls it an `L2(rho)` isometry. On the
uniform product measure over `{0,1}²`, all literal Fourier phases are one.

Take the diagonal coupling and `c(x,y)=(x-y)²`. The coupling has the required
uniform marginals and an `L2(rho)` density. Direct transport cost is zero, but
the proposed Fourier inner product is one half. A norm-one zero-mean function
is mapped to zero, independently contradicting isometry.

A sibling experiment uses the correctly normalized unitary transform on
`Z₂×Z₂`; it reproduces the transport pairing to `1.23e-32`. It changes the
phase normalization, scaling, and measure representation, so it is a repair
control rather than evidence for v1.

## Both regret theorems conflict with the printed regret definitions

![Regret definition versus theorem bounds](images/theorem_bounds.png)

V1 prints the entropic regret as a sum of `T` objectives minus one entropic
optimum, and Kantorovich regret as a sum of `T` feedbacks minus one
Kantorovich optimum. The proofs later sum one-step gaps, which would subtract
the comparator `T` times.

The audit uses a nonconstant 2×2 cost,
`c(x,y)=1+(x-y)²`. Diagonal transport costs one and off-diagonal transport
costs two. Therefore this is not an all-actions-equal control.

| Quantity at `T=100,000,000` | Claim 2 | Claim 3 |
|---|---:|---:|
| Literal printed regret lower bound, any action sequence | 113,728,635.5 | 99,999,999.0 |
| Complete theorem RHS upper bound, any action sequence | 398,538.2 | 582,745.7 |
| Violation margin | 113,330,097.3 | 99,417,253.3 |

The RHS includes `sigma`, `C_bar`, `beta_T`, the log determinant, and—under
Theorem 5.2—the full `kappa` approximation term. The entropy schedule is
implemented exactly with `alpha=1/2`; at the final horizon,
`epsilon_T=0.00005`. A constant-schedule mutation is rejected.

When the comparator is subtracted every round, a repeated optimal action has
zero regret and the contradiction disappears. The verdict is therefore about
the literal v1 definition/theorem combination, not a claim that the standard
OFUL regret theorem is false.

## The finite-basis premise does not imply a finite model

![Actual 3x3 OT under truncated and full costs](images/basis_ot.png)

Assumption 3 lower-bounds a cumulative coefficient `l1` head divided by
`zeta(n)`. Corollary 5.3 treats `zeta(n)=1_{n≥N}` as equivalent to a zero tail.
It is not.

On a known orthonormal basis for a uniform 3×3 transport problem, the literal
integer-order assumption holds at `N=2`, yet coefficient three is nonzero. The
two-dimensional cost uniquely selects the diagonal plan; the full cost
uniquely selects a cyclic plan. HiGHS and an independent enumeration of all
six Birkhoff vertices agree. The truncated plan loses one per round, producing
regret 4096 at horizon 4096—45.25 times `sqrt(NT)`. Including the omitted
coefficient gives zero regret.

This does not dispute the conventional `sqrt(NT)` rate when the model truly is
`N`-dimensional. It falsifies the implication used by the v1 corollary.

## The decay premise does not control coefficient tails

![Coefficient-tail and confidence diagnostics](images/confidence_decay.png)

For `zeta(n)=1-n^{-q}`, the v1 proof equates an `l1` coefficient tail with the
`L2` norm minus an `l1` head. At `q=4`, an admitted finite sequence has tail
1.633 after order two; the proof asserts an upper bound 0.216.

A second exact construction uses
`gamma_1=3` and
`gamma_n=0.1/(sqrt(n) log(n+1))`. Integral comparison proves it belongs to
`l2`; its first two coefficients make Assumption 3 hold for every `q>0`; and
comparison with `n^{-3/4}` proves its `l1` tail diverges. The premise therefore
does not encode the claimed polynomial decay.

## The confidence model is internally inconsistent

The two valid 2×2 couplings in the Fourier counterexample have identical
literal action features but expected noise-free feedback zero and one. No
linear predictor on that feature can represent both observations.

Equation (12) also adds `D Lambda`, an operator on the four-dimensional
parameter space, to `M_t M_t*`, a 3×3 observation-space matrix, in the explicit
`N=4,t=3` check. The printed addition is undefined. A corrected
observation-space OFUL formula satisfies the determinant lemma and covers all
eight Rademacher noise paths (coverage 1.0 at a required 0.9); a five-percent
radius loses coverage. That isolates the source failure from the checker.

## Paired claim results

| Claim | Failed claim and trace | Different claim that holds and trace |
|---|---|---|
| 1 | `FALSIFIED`: Eq. (7) residual `1/2`; norm residual `1` | `VERIFIED`: normalized `Z2 x Z2` pairing residual `1.23e-32`; norm residual `0` |
| 2 | `FALSIFIED`: printed regret lower `113.7M` > full RHS upper `0.399M` | `VERIFIED`: repeated entropic optimizer has standard regret `0`; decomposition residual `0` |
| 3 | `FALSIFIED`: exact schedule; lower `100.0M` > RHS upper `0.583M` | `VERIFIED`: repeated Kantorovich optimizer has standard regret `0`; decomposition residual `0` |
| 4 | `FALSIFIED`: integer-order condition holds with a nonzero coefficient tail | `VERIFIED`: include all three nonzero coefficients; tail `0`, regret `0` |
| 5 | `FALSIFIED`: at `q=4`, tail `1.633` exceeds bound `0.216` | `VERIFIED`: same finite-sequence inequality holds at `q=1`; residual `-0.091` |
| 6 | `FALSIFIED`: feature collision and ill-typed printed width | `VERIFIED`: corrected determinant residual `4.44e-16`; coverage `8/8` |

These verdicts are reproducible local evidence, not a live judge score. The
earlier 96-file falsification-only payload was published as Hugging Face revision
[`1373e02110b2b0c18efb3eee76e889d3c214c85a`](https://huggingface.co/spaces/DineshAI/ugjBMARbyt/commit/1373e02110b2b0c18efb3eee76e889d3c214c85a)
and remains preserved. This paired-verdict update is additive. Until it is
evaluated, the last judged score remains 5/12.

## Provenance

The winning scientific branch is
[`orx/regret-theorem-definition-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/regret-theorem-definition-audit)
at `9a0aeebd6303283e86e5b58079651ffa4e94a4ca`. The
[`orx/honest-environment-disclosure-release`](https://github.com/MachineLearning-Nerd/icml26-repro-ugjBMARbyt-linear-bandits-transport/tree/orx/honest-environment-disclosure-release)
child contains this report, the notebook, regenerated evidence, the protected
tree comparison, the environment-layout disclosure, and the exact Space upload
manifest. Raw experiment and run identifiers remain in OpenResearch experiment
descriptions.
