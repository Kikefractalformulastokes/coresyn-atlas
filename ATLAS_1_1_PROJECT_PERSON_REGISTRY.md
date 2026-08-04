# Atlas 1.1 — Project Registry, Person Registry, Reviewer Registry

**Status:** DESIGN — not merged. Stacked on `design/atlas-1.1-registry-guardian` (PR #7), which is itself stacked on `design/atlas-1.1-pipelines` (PR #6). Neither earlier PR is touched by this one.
**Prompted by:** founder review of PR #7, which drew a distinction this design had collapsed: *"Agent Registry ≠ Knowledge Registry."* Agent Registry (PR #7) should hold only agents; entities like projects and people need their own registries with their own status vocabulary, so a claim this session can't verify has somewhere honest to live besides "silently absent" or "asserted as fact."

## What changed in the thinking

PR #7's Agent Registry correctly refused to seed `Node02`/`Matmerize`/`Kroon`/`NashGate` — no evidence, no entry. The founder's response agreed with that refusal but pointed out the fix isn't to keep refusing forever: it's to give unverified-but-referenced entities a *type-correct* home with an honest status, distinct from where verified agents live. That's what this PR adds.

## An important existing-data finding, checked before writing anything

`atlas-state.json` already has 26 nodes representing CoreSyn's internal research domains and products (`core`, `k3`, `temporal`, `ccfa001`, `materials`, `risk`, `aerospace`, ...). A naive Project Registry would have duplicated a large fraction of that data under new ids — precisely the "two competing truths" problem Registry Guardian exists to prevent. So Project Registry here does **not** re-list those 26 domains. It covers only what `atlas-state.json` doesn't:

1. **Delivery repositories** this session worked in directly (`kind: REPOSITORY`) — `coresyn-atlas`, `riesgodeobra-site`, `coresyn-alpha-gate`, `coresyn-lab`, `coresyn-core-aero-001-verifier`, `Nsmds`. Where one of these corresponds to an existing `atlas-state.json` node (e.g. `riesgodeobra-site` ↔ node `risk`; `coresyn-core-aero-001-verifier` ↔ node `aerospace`), the entry cross-references it via `atlas_domain_ref` rather than restating the node's data.
2. **One explicit cross-reference entry** (`kind: ATLAS_DOMAIN_REF`) for node `materials` — included specifically because of point 3 below, not as a general pattern (the other 25 nodes are not individually mirrored here; `atlas-state.json` stays their one source of truth).
3. **Externally-referenced, unverified project claims** (`kind: EXTERNAL_CLAIM_UNVERIFIED`) — `CRM CFD` (also referenced as CRM/DPW6, CRM Cycle 006-008b), `Matmerize`, `NashGate`. Each gets the founder's own suggested status vocabulary (`SOURCE_NOT_INGESTED` / `NOT_VERIFIED_IN_THIS_SCOPE`), which — as specified — asserts neither existence nor non-existence. For `Matmerize` specifically, the entry notes an **unconfirmed hypothesis**: the name resembles `atlas-state.json`'s real `materials` node (Materials Intelligence, status "reingesta de evidencia pendiente"). That's flagged as a possible mix-up, not asserted as the same project — the two entries are deliberately not merged.

## Person Registry

**File:** `registry/person_registry.json`. Two entries: `person-enrique` (`status: VERIFIED`, cross-referenced to Agent Registry's `enrique` via `agent_registry_ref` rather than duplicated as separate unlinked data) and `person-kroon` (`status: UNVERIFIED_IN_THIS_SCOPE`, per the same founder-specified vocabulary, with the same three-way search — GitHub, Drive, local branches — coming up empty).

**Schema:** `schemas/person-registry.schema.json`. `roles` is a controlled vocabulary (currently `FOUNDER`, `REVIEWER`); Reviewer Registry is derived by filtering on it.

## Reviewer Registry — a deliberate reconciliation, not a literal third file

The founder's list named three deliverables: Project Registry, Person Registry, Reviewer Registry. A literal fourth hand-maintained registry for "known reviewers" would duplicate Person Registry (a reviewer is also a person) — the exact anti-pattern this whole design track exists to avoid. So Reviewer Registry here is **derived**, the same pattern as PR #6's Registry Index/Dependency Graph/Research Genome: `tools/generate_reviewer_registry.py` filters `person_registry.json` for `roles` containing `REVIEWER` and writes `registry/reviewer_registry.json`. Currently 0 entries — nobody in Person Registry has that role yet, and none is fabricated to make the file look populated.

This is explicitly **not** the same thing as `pipelines/reviewer-pipeline.json` (PR #6), which tracks review *requests* and their disposition per `PROTOCOL.md` section 9. Reviewer Registry answers "who could review"; Reviewer Pipeline answers "what was sent and what happened." Keeping them separate means identity data and request/disposition data never share one source of truth — if this reconciliation isn't what you had in mind, it's a two-line schema change to make it a hand-maintained file instead; flagging the substitution here rather than silently deciding it.

## Master Registry update

`registry/master_registry.json` gains three entries (`project_registry`, `person_registry` as `CANONICAL`; `reviewer_registry` as `DERIVED`) and drops `project_registry` from `not_yet_implemented` (now built). `human_approval_gate` stays deferred, same reasoning as PR #7.

## Registry Guardian extended

`tools/registry_guardian.py` now also: checks duplicate ids within the two new registries; generalizes the cross-namespace collision check from the evidence/agent pair (PR #7) to all four id namespaces (evidence, agent, project, person) pairwise; validates every `atlas_domain_ref` resolves to a real `atlas-state.json` node; validates every `agent_registry_ref` resolves to a real agent. All of these passed clean on this data (0 collisions — ids were deliberately prefixed `proj-`/`person-` to avoid accidental overlap with `enrique` et al.).

## The new conflict type, and why Guardian now correctly exits 1

`schemas/conflict-registry.schema.json` gains `EXTERNAL_CLAIM_UNVERIFIED`: *"another node/party reported an entity this node could not independently verify... never auto-resolved."* Five entries were added by hand to `registry/conflict_registry.json` — **not** by the Guardian script, because "someone claimed X" isn't something a consistency checker can detect; it's information from this conversation, logged deliberately rather than only living in chat history:

- `conf-ext-claim-crm-cfd`, `conf-ext-claim-matmerize`, `conf-ext-claim-nashgate` (projects), `conf-ext-claim-kroon` (person), `conf-ext-claim-node02` (an agent-shaped claim with no registry home at all — `node02` is recorded as a bare label precisely because it doesn't resolve to anything, in Agent Registry or otherwise).

All five are `state: UNDER_REVIEW`, matching the founder's instruction that these are never auto-resolved. **This means `python3 tools/registry_guardian.py` now exits 1** on this branch — five real open items, not a bug. That's the intended mechanical signal for `PROTOCOL.md` section 11.3's merge gate: these five need either independently-checkable evidence or an explicit founder disposition (`RESOLVED`/`WONT_FIX`) before this branch's conflict count reaches zero. Verification below documents both the exit-1 state (current) and that no *new*, undocumented conflicts exist beyond these five.

## Delivery

Single pull request, branch `design/atlas-1.1-project-person-registry`, stacked on PR #7. No file from PR #6 or PR #7 is modified except `registry/master_registry.json` (extending the index, expected as new registries appear) and `CHANGELOG.md` (same append pattern as before). Not merged as part of this delivery.
