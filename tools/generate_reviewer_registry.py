#!/usr/bin/env python3
"""Derive registry/reviewer_registry.json from registry/person_registry.json. Stdlib only.

Usage: python3 tools/generate_reviewer_registry.py
Run from the repository root. Overwrites registry/reviewer_registry.json.

This is WHO could review (identities with roles including REVIEWER). It is
deliberately separate from pipelines/reviewer-pipeline.json (PR #6), which
tracks WHAT review requests were sent and their disposition per PROTOCOL.md
section 9 -- identity data and request/disposition data are kept as two
sources of truth on purpose, not merged into one file.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PERSON_REGISTRY = ROOT / "registry" / "person_registry.json"
OUT = ROOT / "registry" / "reviewer_registry.json"


def main():
    people = json.loads(PERSON_REGISTRY.read_text())

    reviewers = [
        {"person_id": p["id"], "name": p["name"], "status": p["status"]}
        for p in people.get("people", [])
        if "REVIEWER" in p.get("roles", [])
    ]

    out = {
        "generated_from": "registry/person_registry.json",
        "reviewers": reviewers,
    }

    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(reviewers)} reviewer(s))")


if __name__ == "__main__":
    main()
