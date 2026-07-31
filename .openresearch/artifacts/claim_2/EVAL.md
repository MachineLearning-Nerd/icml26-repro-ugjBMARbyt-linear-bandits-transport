# Claim 2 evaluation

`FALSIFIED` requires all theorem assumptions, a valid entropic OT solution, a
printed-regret lower bound exceeding the action-uniform RHS upper bound by more
than 90 million, independent agreement, and zero corrected regret for a
repeated optimal action. Any missing condition exits nonzero.

The paired alternative is `VERIFIED` only when the repeated optimizer's
objective is recomputed from its plan, standard per-round-comparator regret is
below `1e-12`, the printed-regret decomposition residual is below `1e-12`, and
the independent checker agrees.
