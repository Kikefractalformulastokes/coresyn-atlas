#!/usr/bin/env python3
"""Registry Guardian — consistency checks across Atlas registries. Stdlib only.

Single responsibility, per ATLAS_1_1_GOVERNANCE_INFRA.md: detect duplicate
ids, cross-registry id collisions, dangling references and dangling paths.
It generates no science and approves nothing; it only reports and, for new
findings, appends OPEN entries to registry/conflict_registry.json.

Usage: python3 tools/registry_guardian.py
Exit code 0 if no OPEN/UNDER_REVIEW conflicts remain after this run, 1
otherwise. A nonzero exit is meant to block a merge per PROTOCOL.md
section 11.3 — the merge gate already requires the change to be reviewed;
this gives that review a concrete, mechanical pass/fail signal.
"""
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(relpath):
    path = ROOT / relpath
    if not path.exists():
        return None, path
    return json.loads(path.read_text()), path


def conflict_id(kind, involved_ids):
    digest = hashlib.sha256(f"{kind}:{'|'.join(sorted(involved_ids))}".encode()).hexdigest()[:12]
    return f"conf-{kind.lower().replace('_', '-')}-{digest}"


def find_duplicate_ids(items, id_field, source_label):
    seen = {}
    conflicts = []
    for item in items:
        val = item.get(id_field)
        if val in seen:
            conflicts.append({
                "type": "DUPLICATE_ID",
                "involved_ids": [val],
                "description": f"id '{val}' appears more than once in {source_label}",
            })
        seen[val] = True
    return conflicts


def check():
    conflicts = []

    evidence, _ = load("evidence-registry.json")
    atlas_state, _ = load("atlas-state.json")
    agents, _ = load("registry/agent_registry.json")
    capabilities, _ = load("registry/capability_registry.json")
    projects, _ = load("registry/project_registry.json")
    people, _ = load("registry/person_registry.json")
    master, _ = load("registry/master_registry.json")

    node_ids = [n["id"] for n in atlas_state.get("nodes", [])] if atlas_state else []
    evidence_ids = [i["id"] for i in evidence.get("items", [])] if evidence else []
    agent_ids = [a["agent_id"] for a in agents.get("agents", [])] if agents else []
    capability_ids = [c["id"] for c in capabilities.get("capabilities", [])] if capabilities else []
    project_ids = [p["id"] for p in projects.get("projects", [])] if projects else []
    person_ids = [p["id"] for p in people.get("people", [])] if people else []

    if evidence:
        conflicts += find_duplicate_ids(evidence["items"], "id", "evidence-registry.json")
    if agents:
        conflicts += find_duplicate_ids(agents["agents"], "agent_id", "registry/agent_registry.json")
    if capabilities:
        conflicts += find_duplicate_ids(capabilities["capabilities"], "id", "registry/capability_registry.json")
    if projects:
        conflicts += find_duplicate_ids(projects["projects"], "id", "registry/project_registry.json")
    if people:
        conflicts += find_duplicate_ids(people["people"], "id", "registry/person_registry.json")

    # cross-namespace collisions: an id must not be reused across evidence / agent / project / person ids
    namespaces = {
        "evidence-registry.json": set(evidence_ids),
        "registry/agent_registry.json": set(agent_ids),
        "registry/project_registry.json": set(project_ids),
        "registry/person_registry.json": set(person_ids),
    }
    ns_names = list(namespaces.keys())
    for i in range(len(ns_names)):
        for j in range(i + 1, len(ns_names)):
            a_name, b_name = ns_names[i], ns_names[j]
            overlap = namespaces[a_name] & namespaces[b_name]
            for val in overlap:
                conflicts.append({
                    "type": "ID_NAMESPACE_COLLISION",
                    "involved_ids": [val],
                    "description": f"id '{val}' is used in both {a_name} and {b_name}",
                })

    # every project's atlas_domain_ref (kind=ATLAS_DOMAIN_REF) must resolve to a real atlas-state.json node
    if projects and atlas_state:
        node_set = set(node_ids)
        for p in projects["projects"]:
            ref = p.get("atlas_domain_ref")
            if ref and ref not in node_set:
                conflicts.append({
                    "type": "MASTER_REGISTRY_DANGLING_REF",
                    "involved_ids": [p["id"], ref],
                    "description": f"project '{p['id']}' has atlas_domain_ref='{ref}', which is not a known atlas-state.json node id",
                })

    # every person's agent_registry_ref must resolve to a real agent
    if people and agents:
        agent_set = set(agent_ids)
        for p in people["people"]:
            ref = p.get("agent_registry_ref")
            if ref and ref not in agent_set:
                conflicts.append({
                    "type": "MASTER_REGISTRY_DANGLING_REF",
                    "involved_ids": [p["id"], ref],
                    "description": f"person '{p['id']}' has agent_registry_ref='{ref}', which is not a known agent_id",
                })

    # every agent capability must exist in the capability registry
    if agents and capabilities:
        cap_set = set(capability_ids)
        for a in agents["agents"]:
            for cap in a.get("capabilities", []):
                if cap not in cap_set:
                    conflicts.append({
                        "type": "MASTER_REGISTRY_DANGLING_REF",
                        "involved_ids": [a["agent_id"], cap],
                        "description": f"agent '{a['agent_id']}' claims capability '{cap}', which is not defined in registry/capability_registry.json",
                    })
            instance_of = a.get("instance_of")
            if instance_of and instance_of not in set(agent_ids):
                conflicts.append({
                    "type": "MASTER_REGISTRY_DANGLING_REF",
                    "involved_ids": [a["agent_id"], instance_of],
                    "description": f"agent '{a['agent_id']}' has instance_of='{instance_of}', which is not a known agent_id",
                })

    # every path master_registry.json lists must exist on disk
    if master:
        for reg in master.get("registries", []):
            for key in ("path", "schema"):
                val = reg.get(key)
                if val and not (ROOT / val).exists():
                    conflicts.append({
                        "type": "MASTER_REGISTRY_DANGLING_REF",
                        "involved_ids": [reg["name"], val],
                        "description": f"master_registry.json entry '{reg['name']}' references {key}='{val}', which does not exist on disk",
                    })

    return conflicts


def reconcile_conflict_registry(found):
    data, path = load("registry/conflict_registry.json")
    if data is None:
        data = {"conflicts": []}

    existing_signatures = {
        (c["type"], tuple(sorted(c["involved_ids"]))) for c in data["conflicts"]
    }

    today = date.today().isoformat()
    added = 0
    for c in found:
        sig = (c["type"], tuple(sorted(c["involved_ids"])))
        if sig in existing_signatures:
            continue
        data["conflicts"].append({
            "conflict_id": conflict_id(c["type"], c["involved_ids"]),
            "type": c["type"],
            "detected_at": today,
            "detected_by": "tools/registry_guardian.py",
            "involved_ids": c["involved_ids"],
            "description": c["description"],
            "state": "OPEN",
        })
        added += 1

    if added:
        path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n")

    open_count = sum(1 for c in data["conflicts"] if c["state"] in ("OPEN", "UNDER_REVIEW"))
    return added, open_count


def main():
    found = check()
    added, open_count = reconcile_conflict_registry(found)
    print(f"registry_guardian: {len(found)} conflict(s) found this run, {added} newly logged, {open_count} OPEN/UNDER_REVIEW total")
    for c in found:
        print(f"  [{c['type']}] {c['description']}")
    if open_count:
        raise SystemExit(1)
    print("registry_guardian: clean — no blocking conflicts")


if __name__ == "__main__":
    main()
