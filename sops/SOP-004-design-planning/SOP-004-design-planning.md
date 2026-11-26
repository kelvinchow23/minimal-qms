---
id: SOP-004
title: Design and development planning
rev: A
status: draft          # draft until released with QMS-rev A
owner: Quality lead
standard: ISO 9001:2026 # clause refs not yet checked against the purchased text
---

# SOP-004 Design and development planning

Each section ends with its basis: *ISO §x.y* (required by the standard) or *minimalQMS
choice* (may be changed by teams using minimalQMS).

## 1. Purpose
To plan each product's development in stages, with gates that state what must be complete
before work proceeds.
*Basis: ISO §8.3.2*

## 2. Scope
Every product repo, from the start of a project or iteration to close-out. Day-to-day
scheduling is outside this procedure; any tool may be used.

## 3. Stages and gates
Development runs in five stages, the same for every product; the involvement level (section 3a) sets how many gates are passed in one approval. Each stage ends at a gate, where the work is approved
before the next stage starts. Gates are the stage reviews ISO 9001 refers to.

| Stage | Gate | Name | Required to pass |
|---|---|---|---|
| Scope | **G0** | Scope approved | `plan.yaml`: goal, scope, make/buy, roles, target dates |
| Requirements | **G1** | Requirements reviewed | `requirements.yaml` with a verification method for each requirement, and `risks.csv` |
| Design | **G2** | Design freeze | Build document and all its appendices exported and reviewed against requirements and risks, including the make files and BOM; parts and BOM released (SOP-002) |
| Build and verify | **G3** | Verified | Units built and tested; results show the requirements are met (SOP-006, SOP-007) |
| Release and close-out | **G4** | Released | Units released (SOP-007); lessons learned recorded, including errors made by agents; scorecard compiled (section 8) |

`gates.yaml` lists the records each gate requires. CI blocks a gate with missing records.
The gate checklists (SOP-004-A06) list the records and the questions answered at each gate.
A gate that does not apply may be skipped, with the reason stated in `plan.yaml`.
*Basis: ISO §8.3.2, §8.3.4, §8.6. The five gates are a minimalQMS choice.*

## 3a. Involvement levels
Each product chooses how much the human signs off and how much the agent does and records,
like an agent tool's permission modes. The gates are always G0 to G4; the level sets which
gates are passed together in one approval. Gates passed together share one date and one
approval reference in `plan.yaml`. The level is set per iteration in `plan.yaml`
(`involvement`), so each iteration can use a different one: for example an agent-driven first
prototype, then a human-driven iteration of the version others will build. Within an
iteration it may change between gates through a PR, for the gates not yet passed. The design controls ISO 9001 §8.3 requires (inputs, reviews,
verification, validation, controlled changes, records) are met at every level, scaled to the
product.

| | **Agent-driven** | **Balanced** | **Human-driven** |
|---|---|---|---|
| Gates passed together | **G0 + G1 + G2** in one approval of the build package, before anything is ordered; **G3 + G4** closed with one recorded line once the first unit works in its intended use | **G0 + G1**, then **G2**, then **G3 + G4** | Each gate on its own (section 3) |
| Requirements | 3 to 6 essential functions in `requirements.yaml`, each with how it is checked | Requirements and a short `risks.csv` | Full requirements, `risks.csv`, independent review |
| Design history | `worklog.md`: decisions and their reasons, written with the human as the work happens | `worklog.md` and one review record per gate (package and minutes in one file) | Review package and minutes per gate (SOP-003) |
| Build document | Instructions, A01 BOM, A02 make files, A04 traveller | The same, plus test procedures in A03 | The same, plus incoming inspection (A05) and traceability where required |
| Verification | Essential functional checks only, listed in A03 | A test for each requirement (SOP-007) | Test procedures, results and release records (SOP-007) |
| Validation | The G3 + G4 line: the first unit works in its intended use | At G3 + G4 | At G3 and G4 |
| Changes after a gate | A PR: new revision and a worklog line | ECR as a PR (SOP-001) | ECR and ECO, deviations, NCs (SOP-001, SOP-008) |

At every level the agent writes only what was discussed with the human or is in the CAD and
other sources; what was not decided is marked "not decided", never filled in. Approvals are
always the human's own words (SOP-001 section 7). `gates.yaml` lists each gate's records
and, per level, the gates passed together and the lighter records each level needs.
*Basis: ISO §8.3.2 (stages and controls set by the nature, duration and complexity of the
work), §8.3.4, §7.5.1 (documented information to the extent necessary). The three levels are
a minimalQMS choice.*

## 4. Plan
`plan.yaml` states the involvement level, the goal, scope, responsibilities (from `roles.yaml`), and for each
gate the target date, actual date and approval reference. Change a target date through a
PR with a one-line reason; earlier targets remain in the git history.
*Basis: ISO §8.3.2. Recording planned and actual dates is a minimalQMS choice.*

## 5. Requirements and risks
- `requirements.yaml`: each requirement has an ID (`REQ-nnn`), a statement, a source
  (customer, standard or internal) and a verification method (test, inspection, analysis
  or review).
- `risks.csv`: a simplified FMEA. Each line has an ID (`RISK-nnn`), the hazard or failure,
  its effect, severity and likelihood (1–5), the controls, and the requirement or test that
  verifies the controls.

Both are frozen at G1. Later changes follow SOP-001.
*Basis: ISO §8.3.3, §6.1.2. The FMEA format is a minimalQMS choice.*

## 6. Passing a gate
G0 is passed by an explicit approval (SOP-001 section 7). G1 to G4 are passed by a formal
review (SOP-003). Record the actual date and the approval reference
in `plan.yaml`.

Gates are passed in order. Several gates may be passed in quick succession, including in
one session, provided each gate's records and approval exist before work for the next gate
starts. Ideas for later gates are recorded in `worklog.md` until that gate is reached.
When verification fails, the iteration stays in the build-and-verify stage. A design
problem is corrected by a design change (SOP-001) with a review of that change, followed by
a rebuild or retest. G3 is passed only when the results meet the requirements.
*Basis: ISO §8.3.4, §8.3.5. Passing gates in quick succession is a minimalQMS choice.*

## 7. Iterations
Development repeats in iterations. Each iteration starts at G0 from the last released
revisions and passes the gates again.
- **Inputs:** lessons learned (G4), nonconformances (SOP-008), feedback from use, and open
  ECRs. G0 records which ECRs the iteration covers.
- **Scope of each gate:** only what the iteration changes. A gate the iteration does not
  affect is skipped, with the reason in `plan.yaml`. Review packages cover the changes since
  the last release.
- **Plan:** each iteration has its own `plan.yaml` entry (`iteration: n`).
- **Between iterations:** a change to a released design that does not justify an iteration
  follows SOP-001 alone (ECR, review, new revision) without gates.

*Basis: ISO §8.3.2, §8.3.6. The iteration model is a minimalQMS choice.*

## 8. Scorecard
Each iteration has a scorecard (`00_planning/scorecard.csv`, SOP-004-A05), compiled by the
agent at G4 from the time entries in `worklog.md`. For each activity it shows the agent's
time, the human's hands-on time, and the human's estimate of the time the activity would
have taken without agents. The scorecard is reviewed with the lessons learned at G4.
*Basis: minimalQMS choice. Supports ISO §9.1 (monitoring and measurement).*

## 9. Build package
The build package (`03_build_package/`) holds the design outputs needed to buy, make,
build and test the product, as one build document per in-house assembly (SOP-006 section 4),
flat, with no subfolders:
- the build document `<PN>_assembly_instructions_rev_<X>.pdf`: the assembly instruction, carrying the assembly's PN
  and revision;
- its appendices as separate files: A01 BOM for ordering (SOP-002), A02 make files (STL or 3MF
  for printed parts, PDF drawings where a dimension or finish matters, PCB fabrication and
  assembly files such as Gerbers; each with the CAD version it came from), A03 inspection and
  test procedures (SOP-006, SOP-007), A04 build traveller and A05 incoming inspection record
  (SOP-006), A06 software or firmware with its version, once released;

The make files are exported before the G2 review, so the approver reviews the actual outputs;
approval freezes those versions, and the CAD versions are marked after approval. G2 freezes
the hardware: what must be bought and made. Software and firmware that only run on the
finished unit stay a versioned draft in `02_design/software/` through G2 and are released
(appendix A06) once they pass their tests, at G3 at the latest; a change before then is a
version bump, not an assembly revision. A02 also carries a backup of the CAD in its native
format (e.g. Fusion `.f3d` for each custom part) and the top assembly as STEP, so the design
survives losing access to the CAD tool's cloud; the CAD versions are recorded in the A02
README and the review minutes. Design sources remain in `02_design/`. Large binary files are stored with Git LFS. The
package is complete when the product can be bought, made, built and tested from it alone.
It is approved at G2.
*Basis: ISO §8.3.5, §8.5.1. The folder and its contents are a minimalQMS choice.*

## Appendices
Appendices are forms and templates that belong to this SOP. They carry the SOP's revision
and change only through a revision of this SOP.

| ID | Title | File | Used in product repos as |
|---|---|---|---|
| SOP-004-A01 | Development plan | [SOP-004-A01-plan.yaml](SOP-004-A01-plan.yaml) | `00_planning/plan.yaml` |
| SOP-004-A02 | Gate requirements | [SOP-004-A02-gates.yaml](SOP-004-A02-gates.yaml) | `00_planning/gates.yaml` |
| SOP-004-A03 | Requirements | [SOP-004-A03-requirements.yaml](SOP-004-A03-requirements.yaml) | `01_requirements/requirements.yaml` |
| SOP-004-A04 | Risk list (simplified FMEA) | [SOP-004-A04-risks.csv](SOP-004-A04-risks.csv) | `01_requirements/risks.csv` |
| SOP-004-A05 | Iteration scorecard | [SOP-004-A05-scorecard.csv](SOP-004-A05-scorecard.csv) | `00_planning/scorecard.csv` |
| SOP-004-A06 | Gate checklists | [SOP-004-A06-gate-checklists.md](SOP-004-A06-gate-checklists.md) | Used by agents and reviewers; not copied |
