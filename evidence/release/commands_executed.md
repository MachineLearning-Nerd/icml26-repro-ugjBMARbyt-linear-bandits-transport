# Reproduction command ledger

This ledger records the commands that establish provenance, mutate experiment
state, or generate scientific/release evidence. Read-only file inspection
commands (`rg`, `sed`, `find`, and image viewers) are omitted because they do
not affect the reproduced result.

## Startup and provenance

```bash
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs 638f1957-b85c-45c0-a09d-4fb17845b64a
git branch -a
git status --short
git rev-parse HEAD
git rev-parse master
git rev-parse origin/master
df -h .
env | cut -d= -f1 | sort
```

Paper retrieval used this explicit User-Agent for every `curl` request:

```bash
curl -L --fail --user-agent 'OpenResearch-Reproduction/1.0 (claim-audit; no automated bulk access)' https://arxiv.org/pdf/2502.07397v1
curl -L --fail --user-agent 'OpenResearch-Reproduction/1.0 (claim-audit; no automated bulk access)' https://export.arxiv.org/e-print/2502.07397v1
curl -L --fail --user-agent 'OpenResearch-Reproduction/1.0 (claim-audit; no automated bulk access)' https://arxiv.org/pdf/2502.07397
curl -L --fail --user-agent 'OpenResearch-Reproduction/1.0 (claim-audit; no automated bulk access)' https://export.arxiv.org/e-print/2502.07397
curl -L --fail --user-agent 'OpenResearch-Reproduction/1.0 (claim-audit; no automated bulk access)' https://ar5iv.labs.arxiv.org/html/2502.07397
```

The verdict dataset was downloaded at revision
`049daca31e54a573b7e7da737aa08972f2cbe401` and filtered in Python with the
exact predicate:

```python
row["space_id"] == "DineshAI/ugjBMARbyt"
```

The judged Space was downloaded at the exact revision:

```text
DineshAI/ugjBMARbyt@e062355ba89b21f22d9d2a840d086d6fa1fec65b
```

## Environment and fixed command

```bash
uv lock
uv sync --locked
orx project edit 638f1957-b85c-45c0-a09d-4fb17845b64a --run-command 'uv run python repro/src/verify_entucb.py'
```

Every formal node inherited and ran exactly:

```bash
uv run python repro/src/verify_entucb.py
```

`orx local` runs from isolated Git checkouts. Consequently, `uv run` created a
locked `.venv` inside each run checkout rather than reusing the editable
checkout's physical `.venv`. All runs used the same `uv.lock`, CPython 3.12
contract, fixed command, and shared `uv` cache. This execution-layout
deviation is retained explicitly instead of being described as compliance with
the requested one-physical-venv layout.

## Experiment tree

```bash
orx create-experiment 638f1957-b85c-45c0-a09d-4fb17845b64a --title "Frozen judged-code baseline" --run-command "uv run python repro/src/verify_entucb.py"
orx exp run bb008d8c-c469-4264-86f9-c97ebed31502 --backend local
orx exp wait bb008d8c-c469-4264-86f9-c97ebed31502 --timeout 480

orx create-experiment 638f1957-b85c-45c0-a09d-4fb17845b64a --title "Literal v1 Fourier contract" --parent bb008d8c-c469-4264-86f9-c97ebed31502
orx exp run 4b6c0692-8bdc-4210-8f91-6474a3d8819e --backend local
orx exp wait 4b6c0692-8bdc-4210-8f91-6474a3d8819e --timeout 480

orx create-experiment 638f1957-b85c-45c0-a09d-4fb17845b64a --title "Unitary discrete Fourier specialization" --parent bb008d8c-c469-4264-86f9-c97ebed31502
orx exp run d449f414-67a6-46a6-aa5e-47802cf47059 --backend local
orx exp wait d449f414-67a6-46a6-aa5e-47802cf47059 --timeout 480

orx create-experiment 638f1957-b85c-45c0-a09d-4fb17845b64a --title "RLS confidence-set contract audit" --parent 4b6c0692-8bdc-4210-8f91-6474a3d8819e
orx exp run 8484698c-9ee1-4913-b1c7-263e28dfb4ed --backend local
orx exp wait 8484698c-9ee1-4913-b1c7-263e28dfb4ed --timeout 480

orx create-experiment 638f1957-b85c-45c0-a09d-4fb17845b64a --title "Basis-rate corollary contract audit" --parent 8484698c-9ee1-4913-b1c7-263e28dfb4ed
orx exp run 8e7536e3-dad7-4b78-ba41-d644e415f801 --backend local
orx exp wait 8e7536e3-dad7-4b78-ba41-d644e415f801 --timeout 480

orx create-experiment 638f1957-b85c-45c0-a09d-4fb17845b64a --title "Regret theorem definition audit" --parent 8e7536e3-dad7-4b78-ba41-d644e415f801
orx exp run b0650750-d6d2-4e8b-964d-bd6b576e9779 --backend local
orx exp wait b0650750-d6d2-4e8b-964d-bd6b576e9779 --timeout 480

orx create-experiment 638f1957-b85c-45c0-a09d-4fb17845b64a --title "Release-candidate cumulative evidence" --parent b0650750-d6d2-4e8b-964d-bd6b576e9779
orx exp run 2eb1ac00-bbdb-43d0-ba44-bcb1d9d0f9e9 --backend local
orx exp wait 2eb1ac00-bbdb-43d0-ba44-bcb1d9d0f9e9 --timeout 480

orx create-experiment 638f1957-b85c-45c0-a09d-4fb17845b64a --title "Publication snapshot and full release gate" --parent 2eb1ac00-bbdb-43d0-ba44-bcb1d9d0f9e9
```

The basis-rate node was launched twice: the first run exposed only a NumPy
Boolean JSON-serialization error, and the second reran the same fixed command
after the serialization fix.

## Evidence and release inspection

```bash
orx runs 638f1957-b85c-45c0-a09d-4fb17845b64a
orx logs <run-id>
uv run marimo check notebooks/entucb_claim_audit.py
git diff --check
git status --short
git rev-parse HEAD
```

After explicit user approval, the Hugging Face Hub Python API created one
atomic Space commit containing only the 96 manifest-verified UTF-8 paths, with
`parent_commit=e062355ba89b21f22d9d2a840d086d6fa1fec65b`. The resulting
revision was downloaded and checked against both the 96-file upload manifest
and the 112-file candidate manifest:

```text
1373e02110b2b0c18efb3eee76e889d3c214c85a
```

No delete operation, duplicate Space, GPU job, or score claim was made.

## Paired verdict release

The same fixed CPU command now requires all six literal verdicts to remain
`FALSIFIED` and all six separately stated alternatives to be `VERIFIED`.
Publication is restricted to an additive, text-only commit on the existing
Space. The exact live parent revision is downloaded again before publication;
every prior path must remain present in the candidate and final revision.
