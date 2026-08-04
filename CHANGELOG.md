# Changelog

Prose record of governance-relevant changes to this repository. This file is hand-maintained per `PROTOCOL.md` section 11.5: after every merge that changes `evidence-registry.json` or `atlas-state.json`, this file is updated as part of closing that branch, alongside regenerating the Registry Index and Dependency Graph.

This changelog starts at the Atlas v1 freeze. Earlier history is the commit log itself (`git log`), not restated here.

## Unreleased — Atlas 1.1 design (this branch)

- **Design, not merged.** `design/atlas-1.1-pipelines` adds six subsystems on top of the existing canonical files: Registry Index, Dependency Graph, Research Genome (all three derived by stdlib-only generator scripts from `evidence-registry.json` / `atlas-state.json`), and Scientific Pipeline, Reviewer Pipeline, Commercial Pipeline (all three new empty tracking scaffolds with schemas, seeded with no entries — no history was fabricated to fill them). See `ATLAS_1_1_DESIGN.md`.
- `PROTOCOL.md` gains section 11 ("Change management"), a pure append ratifying six rules the founder set for this phase: no mixed-scope PRs, one evidence item per branch, a five-part merge gate (branch + PR + clean clone + independent re-verification + rollback instructions), Evidence Registry entry independence, mandatory post-merge regeneration of derived files, and extension discipline for new subsystems. Sections 1-10 are unchanged.
- Per explicit founder instruction, this branch is delivered as design + PR only. It is not merged as part of this delivery.

## 2026-08-02 — CORE-AERO-001 evidence registered (PR #5, open, not merged)

- Commit `042786b` on branch `feat/register-core-aero-001-evidence`. Adds one new entry to `evidence-registry.json`: `exp-core-aero-001-naca0012-liftslope`, a NACA 0012 reduced-order lift-curve-slope reproduction (`status: INTERNALLY_REPRODUCED`, `review_state: EXTERNAL_REVIEW_PENDING`), sourced from the independently-executed `coresyn-core-aero-001-verifier` packet (verified 3 times this session, identical `result.json` SHA-256 each run).
- Counters incremented: `experimental` 2 -> 3, `library` 9 -> 10.
- All validation gates passed (JSON validity, no duplicate ids, sentence-scoped blocked-claims scan, hash references). Pull request opened: https://github.com/Kikefractalformulastokes/coresyn-atlas/pull/5
- **Left open on purpose.** Founder authorization was explicit for the manifest-reconciliation merge below; it was not explicit for this one, so per the merge gate this stays `PENDING_FOUNDER_MERGE_APPROVAL`. `evidence-registry.json` on `main` still reads 9 items / `experimental: 2` / `library: 9` as of this changelog entry — the Registry Index, Dependency Graph and Research Genome example outputs shipped in this design branch reflect that unmerged `main` state, not PR #5's pending state.

## 2026-08-02 — Manifest reconciliation merged (PR #4)

- Commit `458765d` on branch `fix/atlas-manifest-reconciliation`, merged as `4ffb110`.
- Root cause: the git-committed `ATLAS_TECH_SPEC.md` (5572 bytes, hash `d2b9ba27...`) was a stale pre-2026-07-27 version; `MANIFEST.sha256` (which lives only in the Drive-hosted "CoreSyn Atlas — v1 congelado" folder, never in git) was already correct against the deployed 7291-byte version (hash `129ed94c...`). The repository was reconciled to the manifest, not the reverse.
- Verified post-merge from an independent fresh clone: all 4 manifest-scoped files re-hashed and matched `MANIFEST.sha256` exactly.
- Full audit trail: `ATLAS_1_0_FORENSIC_AUDIT.md`, `ATLAS_MANIFEST_REPAIR_EXECUTION.md`, `MANIFEST_VERIFICATION_REPORT.json`, `ROLLBACK_INSTRUCTIONS.md` (delivered to founder outside this repository; not committed here as they document a completed, already-merged action rather than living governance state).

## 2026-08-02 — Governance protocol adopted

- Commit `4e00944`: `PROTOCOL.md` v1.0 added — roles, lifecycle, minimum evidence for ACCEPTED, evidence levels E0-E5, validation-readiness distance, claims rules, contradiction handling, NS-MDS protection, external review, publication chain.

## 2026-07-24 — Atlas v1 freeze

- Commit `c2040a5`: initial frozen state, 26 nodes / 28 edges, `index.html`, `atlas-state.json`, `evidence-registry.json` (9 items at freeze).
- Commits `f2f75b2` through `051d6ef`: Pyramid Lab publication, AgentOS demo, Aerospace Atlas architecture, canonical export path fixes, validation-readiness files (CCFA001, p-Laplacian SGS), preregistered reconstruction runs (including a recorded failed run — retained per section 7, not deleted).
