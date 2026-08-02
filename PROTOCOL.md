# CoreSyn Atlas — Evidence and Validation Protocol

**Protocol version:** 1.0  
**Adopted:** 2026-08-02  
**Status:** Governance protocol created after the Atlas v1 freeze; this is not represented as a recovered historical file.

## 1. Roles
- Enrique retains human values, disclosure choices, commercial decisions and final authorization.
- CoreSyn Scientific Brain determines scientific priority, claim boundaries and evidence requirements.
- Atlas stores graph, provenance, contradictions and handoffs.
- CMOS executes authorized tasks and records evidence.
- The executor never approves its own work.

## 2. Lifecycle
`OPEN -> CLAIMED -> DONE -> ACCEPTED / REJECTED`

- OPEN: scoped, not completed.
- CLAIMED: assigned for execution; no promotion follows.
- DONE: artifacts exist and are inspectable; review remains pending.
- ACCEPTED: an independent reviewer confirms all applicable evidence gates.
- REJECTED: evidence fails, is incomplete, contradicts the claim or violates governance. Rejection evidence is retained.

DONE is not ACCEPTED. Dogfooding, author rerun, internal QA or an AI-generated certificate is not external validation.

## 3. Minimum evidence for ACCEPTED
1. Exact falsifiable claim and scope.
2. Source and data provenance.
3. Explicit licenses or rights status.
4. Frozen code and data identifiers.
5. Environment or executable lock.
6. SHA-256 manifest.
7. Deterministic tests and raw logs.
8. Declared baselines and configurations.
9. Metrics with uncertainty or sensitivity analysis.
10. Null tests, ablations and known falsifiers.
11. Limitations, failure registry and contrary evidence.
12. Bounded reproduction instructions.
13. Independent reviewer identity, date, method and disposition.
14. Inspectable evidence linking the disposition to the frozen package.

Any missing applicable item blocks ACCEPTED.

## 4. Evidence levels
- E0 Claim only.
- E1 Artifact present, evidence chain incomplete.
- E2 Internal reproduction with frozen hashes and limitations.
- E3 Internal stress evidence: baselines, uncertainty, null tests and failure analysis.
- E4 Independent reproduction or bounded specialist review.
- E5 Public/community acceptance where applicable.

Atlas labels must never imply E4 or E5 without a linked external artifact.

## 5. Validation-readiness distance
- 0: only independent reproduction/review remains.
- 1: one internal evidence class or transfer defect remains.
- 2: multiple internal package gaps remain.
- 3: benchmark or reproducibility work is incomplete.
- 4: evidence is mainly narrative, planned or early recovery.
- 5: source artifacts or provenance are absent.

Intensive validator outreach is frozen until distance 0, except a bounded routing or feasibility inquiry that cannot promote the claim.

## 6. Claims
Permitted wording must identify the actual level: internally reproduced, internally benchmarked, sent for bounded independent review, external reproduction pending, research only, or protocol-ready/experiment pending.

Prohibited without linked evidence: validated or certified by an institution, institution endorsement, production-ready, clinically validated, regulator-ready, manufacturer partnership, portfolio-wide validation, or solution of an open prize problem.

## 7. Contradictions and corrections
- Contrary evidence is never deleted.
- Reconstructed artifacts never inherit the identity or hash of missing originals.
- Corrections create new versions and provenance records; history is not silently rewritten.
- Statistical duplicates, repeated seeds or correlated conditions are not counted as independent observations.
- Counts and states use canonical machine-readable exports and an explicit counting convention.

## 8. NS-MDS and sensitive research
NS-MDS is protected methodological IP. Public records may use only: multiscale, direct/inverse operators, reproduction, closure, audit, uncertainty and baselines.

Never publish formulas, prompts, weights, keys, private data, proprietary implementation or prize-problem proof kernels. Cross-domain transfer requires benchmark, null test, ablation, sensitivity, physical constraints, reproducibility and independent review.

## 9. External review
A reviewer or umbrella institution receives a bounded package and a precise question, not a request for a generic portfolio seal. Conflicts, package hash, rerun logs and disposition are recorded. Contracts, exclusivity, IP assignment, payments and legal declarations require Enrique's explicit authorization.

## 10. Publication chain
`Paper -> Reproduction -> Stress test -> Improvement -> Evidence -> External validation -> Publication -> SEO -> Product`

A later stage cannot imply completion of an earlier gate.
