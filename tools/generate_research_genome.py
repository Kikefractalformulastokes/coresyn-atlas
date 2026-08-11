#!/usr/bin/env python3
"""Derive pipelines/research-genome.json from evidence-registry.json. Stdlib only.

Usage: python3 tools/generate_research_genome.py
Run from the repository root. Overwrites pipelines/research-genome.json.

The status -> publication-chain-stage mapping is documented in
ATLAS_1_1_DESIGN.md section 3 and mirrored here. A status with no documented
mapping is reported as stage "UNMAPPED" rather than defaulted or guessed.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "evidence-registry.json"
OUT = ROOT / "pipelines" / "research-genome.json"

MAPPING_TABLE_VERSION = "2026-08-04-v1"

PUBLICATION_CHAIN = [
    "Paper", "Reproduction", "Stress test", "Improvement",
    "Evidence", "External validation", "Publication", "SEO", "Product",
]

# Documented in ATLAS_1_1_DESIGN.md section 3. Intentionally incomplete:
# the registry currently contains only early-chain evidence.
STATUS_TO_STAGE = {
    "VERIFIED_DOCUMENT": "Reproduction",
    "INTERNALLY_REPRODUCED": "Reproduction",
}


def main():
    registry = json.loads(REGISTRY.read_text())

    items_out = []
    for item in registry.get("items", []):
        status = item.get("status", "UNKNOWN")
        stage = STATUS_TO_STAGE.get(status, "UNMAPPED")
        items_out.append({
            "evidence_id": item["id"],
            "registry_status": status,
            "stage": stage,
        })

    out = {
        "generated_from": "evidence-registry.json",
        "publication_chain": PUBLICATION_CHAIN,
        "mapping_table_version": MAPPING_TABLE_VERSION,
        "items": items_out,
    }

    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    unmapped = sum(1 for i in items_out if i["stage"] == "UNMAPPED")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(items_out)} items, {unmapped} unmapped)")


if __name__ == "__main__":
    main()
