#!/usr/bin/env python3
"""Fail-closed checks for the curated public release."""

from __future__ import annotations

import csv
import math
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".csv", ".py", ".yml", ".yaml", ".html", ".svg", ".txt"}
DISALLOWED_SUFFIXES = {".log", ".jsonl", ".sse", ".gguf", ".safetensors", ".pem", ".key", ".p12", ".pfx"}

PRIVATE_HOME = "/" + "home" + "/"
PRIVATE_HOST = "zai" + "server"

PATTERNS = {
    "private home path": re.compile(re.escape(PRIVATE_HOME) + r"[A-Za-z0-9._-]+/"),
    "private IPv4 address": re.compile(
        r"(?<![\d.])(?:10\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.)"
        r"\d{1,3}\.\d{1,3}(?![\d.])"
    ),
    "overlay-network IPv4 address": re.compile(
        r"(?<![\d.])100\.(?:6[4-9]|[78]\d|9\d|1[01]\d|12[0-7])"
        r"\.\d{1,3}\.\d{1,3}(?![\d.])"
    ),
    "MAC address": re.compile(
        r"(?i)(?<![0-9a-f])(?:[0-9a-f]{2}:){5}[0-9a-f]{2}(?![0-9a-f])"
    ),
    "email address": re.compile(
        r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"
    ),
    "private key marker": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "credential assignment": re.compile(
        r"(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token)"
        r"\s*[:=]\s*['\"]?[^\s,'\"}]{8,}"
    ),
    "private host label": re.compile(r"(?i)\b" + re.escape(PRIVATE_HOST) + r"\b"),
    "receipt or order identifier": re.compile(r"(?i)\b(?:order|receipt)\s*#"),
}

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")

REQUIRED = {
    "README.md",
    "LICENSE",
    "PRIVACY.md",
    "docs/REPORT.md",
    "docs/METHODOLOGY.md",
    "docs/METRICS.md",
    "docs/FAILURES.md",
    "docs/DATA-DICTIONARY.md",
    "data/gptoss-context.csv",
    "data/qwen-context.csv",
    "data/qwen-concurrency.csv",
    "data/speculative-decoding.csv",
    "data/showcase-summary.csv",
    "blog/BLOG-DRAFT.md",
    "blog/WORDPRESS-CHARTS.html",
    "blog/IMAGE-PLAN.md",
}


def candidate_files() -> list[Path]:
    command = ["git", "ls-files", "--cached", "--others", "--exclude-standard"]
    output = subprocess.check_output(command, cwd=ROOT, text=True)
    paths = []
    for line in output.splitlines():
        path = ROOT / line
        if path.is_file() and ".git" not in path.parts:
            paths.append(path)
    return sorted(paths)


def scan_privacy(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        rel = path.relative_to(ROOT)
        if path.suffix.lower() in DISALLOWED_SUFFIXES:
            errors.append(f"{rel}: disallowed raw or secret-bearing suffix")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{rel}: non-UTF-8 publication file")
            continue
        if "\r" in text:
            errors.append(f"{rel}: carriage returns are not allowed")
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{rel}:{line}: {label}")
    return errors


def validate_relative_links(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            target = target.strip()
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            clean = unquote(target.split("#", 1)[0])
            resolved = (path.parent / clean).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing relative link target: {target}")
    return errors


def read_csv(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def close(actual: float, expected: float, tolerance: float = 0.03) -> bool:
    return math.isclose(actual, expected, abs_tol=tolerance)


def validate_data() -> list[str]:
    errors: list[str] = []

    speculative = read_csv("data/speculative-decoding.csv")
    for row in speculative:
        parent = float(row["parent_tokens_s"])
        mtp = float(row["mtp_tokens_s"])
        reported = float(row["uplift_percent"])
        calculated = (mtp / parent - 1.0) * 100.0
        if not close(calculated, reported):
            errors.append(
                f"speculative uplift mismatch for {row['model']} C{row['concurrency']}: "
                f"{calculated:.2f} != {reported:.2f}"
            )

    gpt = read_csv("data/gptoss-context.csv")
    if len(gpt) != 5:
        errors.append("GPT-OSS context curve must contain five anchors")
    else:
        if not close(float(gpt[0]["decode_tokens_s"]), 83.30):
            errors.append("GPT-OSS empty-context anchor changed")
        if not close(float(gpt[-1]["decode_tokens_s"]), 34.00):
            errors.append("GPT-OSS full-context anchor changed")

    qwen = read_csv("data/qwen-kv-capacity.csv")
    if len(qwen) != 2:
        errors.append("Qwen KV table must contain BF16 and FP8 rows")
    else:
        bf16 = float(qwen[0]["reported_capacity_tokens"])
        fp8 = float(qwen[1]["reported_capacity_tokens"])
        gain = (fp8 / bf16 - 1.0) * 100.0
        if not close(gain, 96.55):
            errors.append(f"Qwen KV capacity gain mismatch: {gain:.2f}")

    outcomes = read_csv("data/capability-outcomes.csv")
    if len(outcomes) != 4:
        errors.append("Capability matrix must contain four shared tests")
    valid = {"pass", "partial", "fail"}
    for row in outcomes:
        for model, value in row.items():
            if model != "test" and value not in valid:
                errors.append(f"Invalid outcome {value!r} for {model}")

    return errors


def main() -> int:
    paths = candidate_files()
    rels = {str(path.relative_to(ROOT)) for path in paths}
    errors = [f"missing required file: {name}" for name in sorted(REQUIRED - rels)]
    errors.extend(scan_privacy(paths))
    errors.extend(validate_relative_links(paths))
    errors.extend(validate_data())

    if errors:
        print("PUBLIC RELEASE VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PUBLIC RELEASE VALIDATION PASSED: {len(paths)} files scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
