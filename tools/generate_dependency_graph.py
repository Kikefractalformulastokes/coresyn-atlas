#!/usr/bin/env python3
"""Derive pipelines/dependency-graph.json from atlas-state.json + evidence-registry.json. Stdlib only.

Usage: python3 tools/generate_dependency_graph.py
Run from the repository root. Overwrites pipelines/dependency-graph.json.

Linking rule: an evidence item links to a component node only on an EXACT
match between the item's "branch" field and a node's "id". No fuzzy or
substring matching — an unmatched item is reported in unlinked_items rather
than guessed.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "atlas-state.json"
REGISTRY = ROOT / "evidence-registry.json"
OUT = ROOT / "pipelines" / "dependency-graph.json"


def main():
    state = json.loads(STATE.read_text())
    registry = json.loads(REGISTRY.read_text())

    nodes = state.get("nodes", [])
    edges = state.get("edges", [])
    node_ids = {n["id"] for n in nodes}

    evidence_links = []
    unlinked_items = []
    for item in registry.get("items", []):
        branch = item.get("branch")
        if branch in node_ids:
            evidence_links.append({"evidence_id": item["id"], "node_id": branch})
        else:
            unlinked_items.append({"evidence_id": item["id"], "branch_value": branch})

    out = {
        "generated_from": ["atlas-state.json", "evidence-registry.json"],
        "nodes": nodes,
        "edges": edges,
        "evidence_links": evidence_links,
        "unlinked_items": unlinked_items,
    }

    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(
        f"wrote {OUT.relative_to(ROOT)} "
        f"({len(nodes)} nodes, {len(edges)} edges, "
        f"{len(evidence_links)} linked evidence items, {len(unlinked_items)} unlinked)"
    )


if __name__ == "__main__":
    main()
