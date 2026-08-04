#!/usr/bin/env python3
"""Derive pipelines/registry-index.json from evidence-registry.json. Stdlib only.

Usage: python3 tools/generate_registry_index.py
Run from the repository root. Overwrites pipelines/registry-index.json.
"""
import json
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "evidence-registry.json"
OUT = ROOT / "pipelines" / "registry-index.json"


def git_commit_of(path):
    try:
        dirty = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(path.relative_to(ROOT))],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        if dirty:
            return "UNCOMMITTED"
        return subprocess.run(
            ["git", "-C", str(ROOT), "log", "-1", "--format=%H", "--", str(path.relative_to(ROOT))],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return "UNKNOWN"


def main():
    registry = json.loads(REGISTRY.read_text())
    items = registry.get("items", [])

    by_category = defaultdict(list)
    by_branch = defaultdict(list)
    by_status = defaultdict(list)
    by_visibility = defaultdict(list)

    for item in items:
        item_id = item["id"]
        by_category[item.get("category", "UNKNOWN")].append(item_id)
        by_branch[item.get("branch", "UNKNOWN")].append(item_id)
        by_status[item.get("status", "UNKNOWN")].append(item_id)
        by_visibility[item.get("visibility", "UNKNOWN")].append(item_id)

    out = {
        "generated_from": "evidence-registry.json",
        "source_version": registry.get("version", "UNKNOWN"),
        "generated_at_commit": git_commit_of(REGISTRY),
        "total_items": len(items),
        "by_category": dict(by_category),
        "by_branch": dict(by_branch),
        "by_status": dict(by_status),
        "by_visibility": dict(by_visibility),
    }

    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(items)} items indexed)")


if __name__ == "__main__":
    main()
