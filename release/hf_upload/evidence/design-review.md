# Logbook design and evidence review

No public Hugging Face discussion or GitHub issue was present when this review
was performed on 2026-07-31. The following review therefore records the
questions a first-time reader, scientific reviewer, and visual reviewer must be
able to answer from the public logbook.

## First-time reader

- Can I immediately tell which statement failed and which different statement
  holds?
- Can I see what changed from the earlier logbook?
- Can I reach every claim and its evidence without knowing the repository?

Resolution: a new Start Here page, paired poster, claim index, and four-step
reading guide make that path explicit.

## Scientific reviewer

- Is each verdict tied to the exact arXiv v1 contract and its premises?
- Is the replacement narrower rather than a relabeled paper claim?
- Is there a raw trace, independent implementation, and calibration control?
- Are limitations stated, especially Claim 4's continuity scope?

Resolution: every claim page now uses the same contract → failure → calibration
→ replacement structure and links all five evidence layers.

## Visual reviewer

- Are falsification and verification visually distinct without relying only on
  color?
- Can the entire audit be scanned before reading details?
- Are quantitative gaps shown at a truthful scale?

Resolution: the poster labels both sides in text, the dashboard exposes the
evidence chain, and the quantitative graphs retain explicit values and units.

## Acceptance checklist

- [x] Six paper claims are labeled `FALSIFIED`.
- [x] Six different replacement claims are labeled `VERIFIED`.
- [x] Every pair has source, premises, primary trace, independent check, and
  calibration control.
- [x] Existing judged evidence remains reachable.
- [x] Final SVGs were rendered and visually inspected.
- [x] The exact public Hugging Face revision matches the verified upload.
