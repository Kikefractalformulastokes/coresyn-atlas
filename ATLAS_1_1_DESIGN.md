# Atlas 1.1 — Subsystem Design

**Status:** DESIGN — not merged, not authoritative until a founder-approved pull request lands it on `main`.
**Governed by:** `PROTOCOL.md` v1.0, sections 1-11. This document proposes structure only; it grants itself no authority and creates no new role, evidence status, or exception to the lifecycle in section 2.
**Relationship to Atlas 1.0:** additive. Nothing in `atlas-state.json`, `evidence-registry.json`, `ATLAS_TECH_SPEC.md` or `PROTOCOL.md` sections 1-10 is changed by this design. Atlas 1.1 is six read-oriented subsystems layered on top of the existing canonical files.

## 0. Why these six, and why derived-not-authored

Atlas 1.0 has two canonical, hand-maintained sources of truth: `evidence-registry.json` (what evidence exists) and `atlas-state.json` (what components/nodes exist and how they depend on each other). Everything below is either:

- **Derived** from those two files by a deterministic, stdlib-only script (Registry Index, Dependency Graph, Research Genome) — no new canonical data, no new claims, regenerable at any time and disposable if wrong, per section 11.5.
- **A new, currently-empty tracking surface** with a defined schema (Scientific Pipeline, Reviewer Pipeline, Commercial Pipeline) — because no machine-readable history of tasks, review requests, or commercial gates exists yet. These ship as validated-empty scaffolding, not backfilled with invented history. Populating them is future work, one real entry at a time, under section 11 rules.

No subsystem below introduces a new evidence level, a new lifecycle state, or a new claims exception. Where a subsystem needs to represent status, it reuses section 2 (`OPEN/CLAIMED/DONE/ACCEPTED/REJECTED`) and section 4 (`E0-E5`) verbatim.

## 1. Registry Index

**Purpose:** a queryable index over `evidence-registry.json` — by category, branch, status, review_state and visibility — without hand-maintaining a second copy of the registry.

**Source of truth:** `evidence-registry.json` only. The index carries no data the registry doesn't already have; it's a re-sort, not a re-statement.

**Generator:** `tools/generate_registry_index.py` (Python 3 stdlib only, matches the project's existing no-dependency convention). Reads `evidence-registry.json`, writes `pipelines/registry-index.json`.

**Schema:** `schemas/registry-index.schema.json`

**Example output (generated from `main` as of this design, 9 items, none of PR #5's pending entry included since it is unmerged):** `pipelines/registry-index.json`

**Regeneration rule:** per section 11.5, regenerate after every merge that touches `evidence-registry.json`. The script is idempotent and has no side effects beyond writing its one output file.

## 2. Dependency Graph

**Purpose:** one graph that answers "what does this evidence item or component depend on, and what depends on it" — merging `atlas-state.json`'s component graph (`nodes`/`edges`/`deps`) with the `branch` field already present on each `evidence-registry.json` item, so evidence can be traced to the component branch it supports.

**Source of truth:** `atlas-state.json` (component topology) + `evidence-registry.json` (`branch` field per item). No new edges are asserted beyond what these two files already encode.

**Generator:** `tools/generate_dependency_graph.py`. Reads both canonical files, writes `pipelines/dependency-graph.json`.

**Schema:** `schemas/dependency-graph.schema.json`

**Example output:** `pipelines/dependency-graph.json`

**Explicit limitation:** where an evidence item's `branch` value doesn't match any `atlas-state.json` node id exactly (e.g. `"science"` vs. a differently-named node), the generator records the item as `unlinked` rather than guessing a mapping. The example output below reports how many items are linked vs. unlinked on the current registry — see the `unlinked_items` field. Silent guessing would violate the no-fabrication discipline this repo has followed all session; an honest "unlinked" count is preferred to a wrong link.

## 3. Research Genome

**Purpose:** for each evidence item, where it currently sits on the section 10 publication chain (`Paper -> Reproduction -> Stress test -> Improvement -> Evidence -> External validation -> Publication -> SEO -> Product`), derived from fields already on the item (`status`, `review_state` where present, `category`) rather than a new hand-assigned field.

**Source of truth:** `evidence-registry.json`. The mapping from existing `status` strings to a publication-chain stage is a fixed, documented, non-authoritative *view* — it does not change or relabel the item's real `status`.

**Generator:** `tools/generate_research_genome.py`. Reads `evidence-registry.json`, writes `pipelines/research-genome.json`.

**Mapping table (documented, not hidden in code):**

| registry `status` (observed values) | publication-chain stage |
|---|---|
| `VERIFIED_DOCUMENT` | Reproduction |
| `INTERNALLY_REPRODUCED` | Reproduction |
| `VERIFIED_BENCHMARK_SOURCE` | `UNMAPPED` (deliberate — a benchmark source is reference input data the registry cites, not a research output moving through the chain; mapping it to a stage would misrepresent what it is) |
| (no `EXTERNAL_VALIDATION_CONFIRMED` or later status exists in the registry yet) | — |

Any `status` value not in this table is passed through as stage `UNMAPPED` rather than defaulted to a guessed stage. Running the generator against the current `main` (9 items) produces 7 items mapped to `Reproduction` and 2 `UNMAPPED` (the two NACA 0012 benchmark-source entries) — see `pipelines/research-genome.json`. Extending the table is a documentation change, reviewed like any other, not a silent default.

**Schema:** `schemas/research-genome.schema.json`

**Example output:** `pipelines/research-genome.json`

**Explicit non-claim:** this subsystem is a read-only view for tracking chain position. It does not imply, promote, or gate any item's real evidence level or lifecycle state — those remain governed solely by sections 2-4.

## 4. Scientific Pipeline

**Purpose:** machine-readable tracking of section 2's lifecycle (`OPEN -> CLAIMED -> DONE -> ACCEPTED/REJECTED`) per task/claim, so the state of in-flight work is inspectable rather than only living in conversation history.

**Source of truth:** none yet. No machine-readable task ledger currently exists for Atlas — section 2 has governed real work (e.g. the manifest reconciliation, the CORE-AERO-001 evidence proposal) but only as narrative in pull requests and audit reports, never as structured records. This subsystem is new tracking infrastructure, not a derivation.

**Schema:** `schemas/scientific-pipeline.schema.json` — one record per task: `task_id`, `claim` (falsifiable, scoped per section 3.1), `state` (section 2's five values, nothing else), `owner_role` (one of section 1's roles), `evidence_refs` (links into `evidence-registry.json` `id`s once they exist), `state_history` (append-only, timestamped, never overwritten — mirrors section 7's "history is not silently rewritten").

**Seed file:** `pipelines/scientific-pipeline.json` ships with `"tasks": []`. It is **not** backfilled with the manifest-reconciliation or CORE-AERO-001 work retroactively, because doing so would mean inventing `task_id`s and timestamps for events that were never recorded in this structured form as they happened — that's fabrication of history, which section 7 and this session's own discipline both rule out. The `CHANGELOG.md` (below) covers that retroactive record honestly, in prose, sourced from the actual merged/opened pull requests.

**Adoption path:** the next task opened under this protocol is the first real entry. No entry is added except by a pull request that also does the work it describes.

## 5. Reviewer Pipeline

**Purpose:** tracking for section 9's external review process — bounded packages sent to a reviewer, the precise question asked, conflicts declared, package hash, rerun logs, and disposition.

**Source of truth:** none yet — no external review has been sent for any Atlas evidence item as of this design (every item in the registry is `status: INTERNALLY_REPRODUCED` / `VERIFIED_DOCUMENT`, i.e. pre-external-review per section 4's E2/E3).

**Schema:** `schemas/reviewer-pipeline.schema.json` — one record per review request: `request_id`, `evidence_ids` (the bounded set of registry items sent), `question` (the precise, bounded question per section 9 — never "review everything"), `package_hash`, `reviewer_identity`, `sent_date`, `disposition` (`PENDING`/`ACCEPTED`/`REJECTED`/`WITHDRAWN`), `rerun_log_ref`, `conflicts_declared`.

**Seed file:** `pipelines/reviewer-pipeline.json` ships with `"requests": []`, for the same reason as the Scientific Pipeline: no real request has happened yet in this structured form.

**Governance note:** per section 9, any reviewer contract, exclusivity, IP assignment or payment term still requires Enrique's explicit authorization regardless of what this pipeline tracks — the schema has an `authorization_ref` field precisely so that link is always recorded, never implicit.

## 6. Commercial Pipeline

**Purpose:** tracking for section 10's final two stages (`SEO -> Product`) and the founder-authorization gate that section 9 already requires before anything commercial happens — so a claim's commercial state is inspectable and can never silently run ahead of its evidence state.

**Source of truth:** none yet — no Atlas evidence item has reached `External validation` in the section 10 chain (see the Research Genome mapping table above: nothing maps past `Reproduction` today), so nothing is eligible to enter this pipeline yet.

**Schema:** `schemas/commercial-pipeline.schema.json` — one record per commercial motion: `motion_id`, `evidence_ids`, `publication_chain_stage_required` (must be `External validation`, `Publication`, `SEO` or `Product` — the schema rejects earlier stages), `founder_authorization` (required object: `authorized_by`, `date`, `scope` — absent means blocked), `state`.

**Hard gate, enforced at the schema level, not just by convention:** `schemas/commercial-pipeline.schema.json` marks `founder_authorization` as `required`. A commercial-pipeline record with no founder authorization is schema-invalid, not merely discouraged — mirroring section 9's "requires Enrique's explicit authorization" as a structural constraint instead of a promise.

**Seed file:** `pipelines/commercial-pipeline.json` ships with `"motions": []`.

## 7. What this design deliberately does not do

- It does not merge anything automatically. Every file below lands only via a pull request, reviewed like any other change under section 11.
- It does not touch `evidence-registry.json` or `atlas-state.json` content — the two generators read them, nothing writes to them.
- It does not modify `PROTOCOL.md` sections 1-10. Section 11 is a pure append.
- It does not backfill history into the three new empty pipelines. `CHANGELOG.md` is the honest, prose record of what already happened; the pipelines start clean.
- It does not invent a mapping, a link, or a stage for data the canonical files don't support (see the `unlinked_items` and `UNMAPPED` handling above).

## 8. Delivery

All of the above ships as a single pull request against `coresyn-atlas` on branch `design/atlas-1.1-pipelines`, because everything in it is governance/design-layer (section 11.1's mixed-scope rule concerns manifest / evidence-registry / governance PRs — this PR touches none of `evidence-registry.json`'s content and none of the frozen manifest's four files). Per the founder's explicit instruction, this pull request is **not merged** as part of this delivery.
