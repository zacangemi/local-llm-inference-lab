# Public-release privacy boundary

This repository is intentionally a redacted publication layer.

## Included

- Normalized benchmark and showcase measurements
- Public model identifiers and software versions
- High-level hardware specifications already disclosed in the project series
- Frozen public prompts
- Derived charts, findings, limitations, and methodology

## Excluded

- Usernames, private hostnames, home-directory paths, and device names
- Private, management, or overlay-network addresses
- MAC addresses, credentials, tokens, keys, cookies, and session material
- Exact service bindings, relay details, recovery topology, and remote-access instructions
- Receipts, order identifiers, store locations, and embedded image metadata
- Raw server logs, event streams, telemetry bundles, process lists, workspaces, and model files

Raw evidence remains offline. Public tables are transcribed from the retained source reports and checked against them before release.

## Automated checks

Run:

    python3 scripts/validate_public_release.py

The validator scans publication files for private paths, private and overlay IP ranges, MAC addresses, email addresses, credential-like assignments, known private device labels, disallowed raw-evidence extensions, and inconsistent CSV values.

The validator is a guardrail, not a claim that pattern matching can prove perfect privacy. Every public update also receives a manual diff review.

## Reporting a concern

If public material appears to expose sensitive operational data, open a GitHub security advisory or use the public contact route on https://zacharycangemi.com/.
