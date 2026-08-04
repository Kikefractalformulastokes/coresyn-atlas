# Atlas 1.1 — Governance Infrastructure (Registry Guardian et al.)

**Status:** DESIGN — not merged, not authoritative until a founder-approved pull request lands it on `main`.
**Governed by:** `PROTOCOL.md` v1.0, sections 1-11. Adds no new role, evidence status, or lifecycle exception.
**Relationship to PR #6 (`ATLAS_1_1_DESIGN.md`):** this branch is stacked on `design/atlas-1.1-pipelines` and does not modify any file from that PR. It adds five new pieces the founder asked for after reviewing PR #6: Registry Guardian, Agent Registry, Capability Registry, Conflict Registry, Master Registry. Nothing scientific — `evidence-registry.json` and `atlas-state.json` are read, never written, by everything below.

## Why these five

PR #6 gave Atlas a way to derive read-views (Registry Index, Dependency Graph, Research Genome) and to track new activity (Scientific/Reviewer/Commercial Pipelines) — but nothing in it could tell you *who* is allowed to do what, or notice when two registries disagree. That's the gap this PR closes.

## A note on scope — what is and isn't seeded here

The founder's review of PR #6 referenced entities (`Node02`, `Matmerize`, `Kroon`, `NashGate`, a CRM/DPW6 agent mesh) that do not appear anywhere in this repository, in `evidence-registry.json`, or in any artifact this session has independently verified. Earlier in this session, exhaustive searches (GitHub `search_repositories`, Google Drive `search_files`, all reachable local branches) for exactly these terms returned zero matches. Consistent with that, and with `PROTOCOL.md` section 7 ("statistical duplicates... are not counted" / evidence discipline generally), **`registry/agent_registry.json` below contains only entities this session can source to a real reference**: the four roles `PROTOCOL.md` section 1 already defines (Enrique, CoreSyn Scientific Brain, Atlas, CMOS), plus the one concrete session identity this session itself operated under and disclosed throughout (`CODEX-EVIDENCE-EXECUTOR-01`, now committed at `governance/CODEX_EVIDENCE_EXECUTOR_ROLE.json`).

If real evidence for any other agent surfaces — a repository, a hash-verified handoff package, anything independently checkable — it gets added the same way `CORE-AERO-001` was: its own branch, its own PR, verified before it's proposed. Not seeded here on description alone. This is the exact failure mode Registry Guardian exists to prevent (competing, unverifiable "truths" entering a canonical registry) — so it would be self-defeating to seed the Agent Registry with unverified agents in the same PR that introduces the tool meant to catch that.

## 1. Capability Registry

**Purpose:** a fixed vocabulary of capability flags, each with a plain-language meaning and a risk tier, so an Agent Registry entry can't just declare an arbitrary string as a "capability."

**File:** `registry/capability_registry.json` — 13 capabilities seeded, spanning the founder's examples (`CAN_EXECUTE_PYTHON`, `CAN_MERGE_PR`, `CAN_PUBLISH`, `CAN_WRITE_CANONICAL_REGISTRY`, `CAN_TAKE_EXTERNAL_ACTION`, `CAN_WRITE_EXTERNAL_STORAGE`) plus governance-authority capabilities needed to represent `PROTOCOL.md` section 1's human/role split (`AUTHORIZE_MERGE`, `AUTHORIZE_COMMERCIAL_MOTION`, `AUTHORIZE_EXTERNAL_REVIEW_CONTRACT`, `DEFINE_CLAIM_SCOPE`, `SET_EVIDENCE_REQUIREMENTS`, `STORE_PROVENANCE`, `EXECUTE_AUTHORIZED_TASK`).

**Schema:** `schemas/capability-registry.schema.json`. New capabilities are proposed by editing this file before any agent can claim them — Registry Guardian rejects an agent entry that claims an undefined capability (see section 2).

## 2. Agent Registry

**Purpose:** one place that lists every acting role/identity, what it's allowed to do, whether it can write canonically, and whether it can act outside the repository — plus how each entry was verified.

**File:** `registry/agent_registry.json` — 5 entries: `enrique`, `coresyn-scientific-brain`, `atlas`, `cmos` (the four `PROTOCOL.md` roles), and `codex-evidence-executor-01` (`kind: SESSION_INSTANCE`, `instance_of: cmos`).

**Schema:** `schemas/agent-registry.schema.json`. Every entry states `verified_by` and `verification_method` — for the three roles beyond CMOS/Enrique, verification is currently "protocol document reference" only, and `coresyn-scientific-brain` is explicitly marked `DEFINED_NOT_YET_INSTANTIATED` because no distinct running system has been independently confirmed as an active instance of that role. That's an honest gap, not an oversight — closing it means verifying a real instance, not editing this status field.

**`writes_registry` and `external_actions` are both `false` for every entry** as of this design, including `codex-evidence-executor-01` — matching its existing disclaimers in `governance/CODEX_EVIDENCE_EXECUTOR_ROLE.json` (`canonical_write_access: false`, `external_action_access: false`).

## 3. Master Registry

**Purpose:** a pure index — file paths and their schemas — so "what registries exist" is one file, not tribal knowledge.

**File:** `registry/master_registry.json`. Lists all 11 registry/derived/scaffold files that exist after PR #6 + this PR (`evidence-registry.json`, `atlas-state.json`, the two new registries here, `conflict_registry.json`, and PR #6's five pipeline files), tagged `CANONICAL` / `DERIVED` / `TRACKING_SCAFFOLD`.

**Explicitly deferred, listed under `not_yet_implemented` rather than silently dropped:**
- `project_registry` — the founder's broader proposal (CRM, NSMDS, Matmerize, Kroon as project-level entries). Not built: no verified project-level artifact exists for most named candidates, and NSMDS/RiesgoDeObra already exist as their own repositories rather than registry rows. Building this would mean either fabricating entries for unverified projects or duplicating what already exists elsewhere — both rejected for now.
- `human_approval_gate` — not a separate file, because it would duplicate what already exists structurally: `commercial-pipeline.schema.json`'s required `founder_authorization` field (PR #6) and `PROTOCOL.md` section 11.3's merge gate already enforce it.

**Schema:** `schemas/master-registry.schema.json`. `schema` may be `null` for `evidence-registry.json`/`atlas-state.json`, which predate Atlas 1.1 and have no JSON Schema — recorded as `null`, not backfilled with a schema written after the fact to paper over the gap.

## 4. Conflict Registry

**Purpose:** where a detected inconsistency lives until it's resolved — never silently dropped, per section 7's "history is not silently rewritten."

**File:** `registry/conflict_registry.json`. **Not seeded empty by hand** — it was populated by actually running Registry Guardian (section 5) against the real repository state. That first run found one real, if mundane, conflict: `master_registry.json` referenced `registry/conflict_registry.json` before that file existed yet (a bootstrapping ordering issue in this delivery itself). The Guardian logged it, created the file as a side effect, and the entry is marked `RESOLVED` with that exact explanation — left in the ledger rather than deleted, which is the registry practicing its own no-silent-deletion rule on its first real use.

**Schema:** `schemas/conflict-registry.schema.json`.

## 5. Registry Guardian

**Purpose, and only purpose:** detect duplicate ids, cross-registry id collisions, dangling references (an agent claiming an undefined capability, an `instance_of` pointing nowhere, a `master_registry.json` path that doesn't exist on disk) and report or block. It generates no science, approves nothing, and does not itself decide a conflict's resolution — that's a human/PR action.

**Tool:** `tools/registry_guardian.py`, stdlib-only, matching the project's existing generator convention (`tools/generate_*.py` from PR #6). Checks implemented in this first version:
1. Duplicate `id`/`agent_id` within `evidence-registry.json`, `registry/agent_registry.json`, `registry/capability_registry.json`.
2. Cross-namespace collision — the same id string used as both an evidence id and an agent id.
3. Every capability an agent claims exists in the Capability Registry.
4. Every `instance_of` reference resolves to a real agent.
5. Every path/schema `master_registry.json` lists exists on disk.

**What it deliberately does not yet check** (named here rather than silently absent): hash-mismatch detection across registries — `evidence-registry.json` items don't currently carry a structured hash field (evidence hashes today live in prose inside `summary`/reproduction reports, not a dedicated field), so a real hash-mismatch check needs that field added first. Adding it is future work, not faked here with a check that can't actually fire.

**Exit behavior:** exit 1 if any `OPEN`/`UNDER_REVIEW` conflict remains after the run (new or pre-existing) — intended as the mechanical half of the `PROTOCOL.md` section 11.3 merge gate; exit 0 when clean. **Verified in this delivery:** first run found and logged the bootstrapping conflict above (exit 1); after marking it `RESOLVED`, a second run reports 0 conflicts and exits 0. Both runs' real output are in the PR verification notes, not paraphrased.

## 6. Where `CODEX_EVIDENCE_EXECUTOR_ROLE.json` ended up

This resolves a question left open since the manifest-repair delivery: the founder asked where this file should live (a `governance/` path, a third small PR, or skip it). It's now committed at `governance/CODEX_EVIDENCE_EXECUTOR_ROLE.json`, referenced from `registry/agent_registry.json`'s `codex-evidence-executor-01` entry's `source_ref`, exactly as the founder's own proposed schema anticipated (`verified_by` / `verification_method` fields pointing at real evidence rather than restating it inline).

## 7. Delivery

Single pull request, branch `design/atlas-1.1-registry-guardian`, stacked on `design/atlas-1.1-pipelines` (PR #6) because `master_registry.json` legitimately indexes files that only exist on that branch. Per the founder's explicit decision, **PR #6 stays exactly as-is (draft, unmerged)**, and this PR is also **not merged** as part of this delivery — both wait for review, and the founder's stated plan is to merge them together as Atlas 1.1 once this infrastructure is in place.
