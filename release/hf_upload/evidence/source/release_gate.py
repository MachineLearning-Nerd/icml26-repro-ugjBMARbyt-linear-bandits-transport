"""Prepare and validate the text-only additive Hugging Face upload payload."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import matplotlib.image as mpimg


TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".toml", ".lock", ".svg"}
SECRET_PATTERNS = {
    "hugging_face_token": re.compile(r"hf_[A-Za-z0-9]{20,}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _copy_text(source: Path, destination: Path) -> None:
    source.read_text(encoding="utf-8")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def _walk_logbook_files(node: dict) -> list[str]:
    paths = [node["file"]]
    for child in node.get("children", []):
        paths.extend(_walk_logbook_files(child))
    return paths


def run_release_gate(root: Path) -> dict:
    upload = root / "release" / "hf_upload"
    evidence = upload / "evidence"
    repository_evidence = root / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)

    for claim in range(1, 7):
        source_dir = root / ".openresearch" / "artifacts" / f"claim_{claim}"
        for evidence_root in (repository_evidence, evidence):
            target_dir = evidence_root / f"claim_{claim}"
            target_dir.mkdir(parents=True, exist_ok=True)
            for source in sorted(source_dir.iterdir()):
                if source.is_file() and source.suffix in TEXT_SUFFIXES:
                    _copy_text(source, target_dir / source.name)

    claim45_independent = (
        root
        / ".openresearch"
        / "artifacts"
        / "claim_4"
        / "independent_checker_output.json"
    )
    claim5_independent = (
        root
        / ".openresearch"
        / "artifacts"
        / "claim_5"
        / "independent_checker_output.json"
    )
    _copy_text(claim45_independent, claim5_independent)
    for evidence_root in (repository_evidence, evidence):
        _copy_text(
            claim5_independent,
            evidence_root / "claim_5" / claim5_independent.name,
        )

    source_files = [
        root / "repro" / "src" / "verify_entucb.py",
        root / "repro" / "src" / "claim1_fourier.py",
        root / "repro" / "src" / "claim23_regret_bounds.py",
        root / "repro" / "src" / "claim45_basis_rates.py",
        root / "repro" / "src" / "claim6_confidence.py",
        root / "repro" / "src" / "check_claim1_independent.py",
        root / "repro" / "src" / "check_claim23_independent.py",
        root / "repro" / "src" / "check_claim45_independent.py",
        root / "repro" / "src" / "check_claim6_independent.py",
        root / "repro" / "src" / "make_report_figures.py",
        root / "repro" / "src" / "make_public_evidence_svgs.py",
        root / "repro" / "src" / "release_gate.py",
        root / "pyproject.toml",
        root / "uv.lock",
    ]
    for evidence_root in (repository_evidence, evidence):
        for source in source_files:
            _copy_text(source, evidence_root / "source" / source.name)
        _copy_text(
            root / ".python-version",
            evidence_root / "source" / "python-version.txt",
        )
        _copy_text(
            root / "reports" / "claim-by-claim" / "report.md",
            evidence_root / "report" / "report.md",
        )
        _copy_text(
            root / "notebooks" / "entucb_claim_audit.py",
            evidence_root / "notebook" / "entucb_claim_audit.py",
        )
        _copy_text(
            root / "release" / "commands_executed.md",
            evidence_root / "release" / "commands_executed.md",
        )
        _copy_text(
            root / "release" / "subset_check.json",
            evidence_root / "release" / "subset_check.json",
        )
        _copy_text(
            root / "release" / "protected_judged_manifest.sha256",
            evidence_root / "release" / "protected_judged_manifest.txt",
        )

    for source in sorted((repository_evidence / "figures").glob("*.svg")):
        _copy_text(source, evidence / "figures" / source.name)
    _copy_text(
        repository_evidence / "reverification_summary.json",
        evidence / "reverification_summary.json",
    )

    for source in sorted((root / "pages").rglob("*.md")):
        _copy_text(source, upload / source.relative_to(root))

    upload_files = sorted(path for path in upload.rglob("*") if path.is_file())
    decoded = {}
    invalid_suffixes = []
    invalid_utf8 = []
    json_errors = []
    secret_hits = []
    for path in upload_files:
        relative = path.relative_to(upload).as_posix()
        if path.suffix not in TEXT_SUFFIXES:
            invalid_suffixes.append(relative)
        try:
            text = path.read_text(encoding="utf-8")
            decoded[relative] = text
        except UnicodeDecodeError:
            invalid_utf8.append(relative)
            continue
        if path.suffix == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as error:
                json_errors.append({"path": relative, "error": str(error)})
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                secret_hits.append({"path": relative, "pattern": name})

    manifest_lines = [
        f"{_sha256(path)}  {path.relative_to(upload).as_posix()}"
        for path in upload_files
    ]
    manifest_path = root / "release" / "hf_upload_manifest.sha256"
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    allowlist_path = root / "release" / "hf_upload_allowlist.txt"
    allowlist_path.write_text(
        "\n".join(path.relative_to(upload).as_posix() for path in upload_files) + "\n",
        encoding="utf-8",
    )

    protected_manifest = root / "release" / "protected_judged_manifest.sha256"
    protected_paths = {
        line.split("  ", 1)[1]
        for line in protected_manifest.read_text(encoding="utf-8").splitlines()
        if "  " in line
    }
    logbook = json.loads((upload / "logbook.json").read_text(encoding="utf-8"))
    referenced_pages = _walk_logbook_files(logbook["root"])
    upload_paths = {path.relative_to(upload).as_posix() for path in upload_files}
    missing_pages = [
        path
        for path in referenced_pages
        if path not in upload_paths and path not in protected_paths
    ]

    marimo = subprocess.run(
        [
            sys.executable,
            "-m",
            "marimo",
            "check",
            str(root / "notebooks" / "entucb_claim_audit.py"),
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )

    report = (root / "reports" / "claim-by-claim" / "report.md").read_text(
        encoding="utf-8"
    )
    image_refs = re.findall(r"!\[[^\]]*\]\((images/[^)]+)\)", report)
    bad_images = []
    for reference in image_refs:
        image_path = root / "reports" / "claim-by-claim" / reference
        try:
            image = mpimg.imread(image_path)
            if image.size == 0:
                bad_images.append(reference)
        except Exception as error:  # pragma: no cover - diagnostic path
            bad_images.append(f"{reference}: {error}")

    verdicts = {}
    alternative_verdicts = {}
    missing_evidence = []
    required_names = {
        "claim_contract.json",
        "source_audit.md",
        "method.md",
        "raw_result.json",
        "verdict.json",
        "independent_checker_output.json",
        "negative_control_output.json",
        "environment.json",
        "exact_command.txt",
        "EVAL.md",
        "limitations_and_deviations.md",
    }
    for claim in range(1, 7):
        claim_dir = root / ".openresearch" / "artifacts" / f"claim_{claim}"
        present = {path.name for path in claim_dir.iterdir() if path.is_file()}
        missing_evidence.extend(
            f"claim_{claim}/{name}" for name in sorted(required_names - present)
        )
        verdict = json.loads(
            (claim_dir / "verdict.json").read_text(encoding="utf-8")
        )
        verdicts[str(claim)] = verdict["verdict"]
        alternative_verdicts[str(claim)] = verdict.get(
            "alternative_verdict", "MISSING"
        )

    subset_path = root / "release" / "subset_check.json"
    if subset_path.exists():
        subset_check = json.loads(subset_path.read_text(encoding="utf-8"))
    else:
        subset_check = {
            "passed": False,
            "status": "pending materialized candidate comparison",
        }

    internal_ready = all(
        [
            not invalid_suffixes,
            not invalid_utf8,
            not json_errors,
            not secret_hits,
            not missing_pages,
            marimo.returncode == 0,
            len(image_refs) == 5,
            not bad_images,
            not missing_evidence,
            set(verdicts.values()) == {"FALSIFIED"},
            set(alternative_verdicts.values()) == {"VERIFIED"},
        ]
    )
    gate_ready = internal_ready and bool(subset_check.get("passed"))
    result = {
        "publication_performed": False,
        "internal_ready": internal_ready,
        "gate_ready": gate_ready,
        "claim_verdicts": verdicts,
        "alternative_claim_verdicts": alternative_verdicts,
        "upload_file_count": len(upload_files),
        "upload_manifest_sha256": _sha256(manifest_path),
        "allowlist_sha256": _sha256(allowlist_path),
        "text_only": not invalid_suffixes and not invalid_utf8,
        "invalid_suffixes": invalid_suffixes,
        "invalid_utf8": invalid_utf8,
        "json_errors": json_errors,
        "secret_hits": secret_hits,
        "logbook_missing_pages": missing_pages,
        "marimo_check_exit_code": marimo.returncode,
        "marimo_check_stdout": marimo.stdout.strip(),
        "marimo_check_stderr": marimo.stderr.strip(),
        "report_image_references": image_refs,
        "bad_images": bad_images,
        "missing_evidence": missing_evidence,
        "protected_manifest_entries": len(protected_paths),
        "subset_check": subset_check,
    }
    (root / "release" / "gate_result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result
