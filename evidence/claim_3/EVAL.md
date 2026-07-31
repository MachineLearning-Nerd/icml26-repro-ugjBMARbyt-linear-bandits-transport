# Claim 3 evaluation

`FALSIFIED` requires all assumptions, a valid nontrivial OT solution, the exact
decaying schedule, a printed-regret lower bound exceeding the complete RHS by
more than 90 million, and independent agreement. The constant-schedule control
must differ from the required schedule by more than 0.49.

The paired alternative is `VERIFIED` only when the repeated Kantorovich
optimizer is evaluated from its returned plan, standard per-round-comparator
regret and its printed-regret decomposition residual are below `1e-12`, and
the independent checker agrees.
