---
id: SOP-006
title: Incoming inspection and build records
rev: A
status: draft          # draft until released with QMS-rev A
owner: Quality lead
standard: ISO 9001:2026 # clause refs not yet checked against the purchased text
---

# SOP-006 Incoming inspection and build records

Each section ends with its basis: *ISO §x.y* (required by the standard) or *minimalQMS
choice* (may be changed by teams using minimalQMS).

## 1. Purpose
To inspect critical parts on receipt and to record what went into each unit, so that any
unit can be traced to its parts and any part to the units that contain it.
*Basis: ISO §8.4.2, §8.5.1, §8.5.2*

## 2. Scope
Every build of a product: receipt of parts, assembly of units and recording of their
contents. Testing and release are covered by SOP-007.

## 3. Incoming inspection
Only **critical parts** are inspected on receipt: custom parts made by someone else (PCBs,
machined parts, outsourced prints), and parts whose failure would be unsafe or costly to find
later. They are listed with their checks in `inspection_checks.csv` (SOP-006-A05, issued in
appendix A03) and recorded on the incoming inspection record (appendix A05), one per delivery,
so all parts received together are checked and signed in one go. Other parts, bought from an
approved supplier (SOP-005), are not inspected: the build and the tests find their problems.
If an assembly has no critical parts, it has no A05.

A purchased assembly receives its serial number at receipt (SOP-002 section 7). When a part
fails, mark it, keep it apart from accepted stock, and raise an NC (SOP-008).
*Basis: ISO §8.4.2, §8.6. Classes are defined in SOP-002.*

## 4. Build document: assembly instruction, checks and traveller
Each assembly (`PPP-A-NNNN`) built in-house has a build document: its assembly instruction
(`03_build_package/<PN>_assembly_instructions_rev_<X>.pdf`, SOP-006-A04), a controlled document with the same PN and
revision as the assembly, and its appendices (SOP-004 section 9). It is written for the
person doing the work: pictures first, short text. Its sources are kept in
`02_design/build_document/` and the document is generated from them.

Three kinds of check are kept apart:
- **Incoming inspection:** on receipt of each Class A part, from its checks
  (`02_design/build_document/inspection_checks.csv`, SOP-006-A05), issued in appendix A03.
- **In-process checks:** a check at the end of each assembly step, in the instruction.
- **Final checks and tests:** after assembly; tests per SOP-007, issued in appendix A03.

Each unit is built on a **build traveller** (appendix A04): its serial number (written in by
the builder after the printed `<PN>-`), the build number (`B001` for the first build), what it
was built from (the git commit and CAD version), the assembler and the date, and a row per step check, final check and test (with a one-line brief
of the test), each with pass or fail, initials, date, comments and an NC number, ending with a
build-complete signature. Incoming inspection is not on the traveller: it is per delivery, not
per unit. If anything fails, the builder marks it, writes what they saw, stops work on that
unit or part and tells the quality lead, who raises an NC (SOP-008). The completed traveller (or a photo of it) is kept in `builds/B00n/`. Release
remains a separate decision (SOP-007).

The appendices share the build document's revision and date. Any change to any appendix is a
revision of the whole build document: its revision letter and date change on the instruction
and every appendix together (SOP-001). Every title block carries the document number
(`<PN>` for the instruction, `<PN>-A<nn>` for an appendix), revision, date, assembly name and
number, status, approval and the design source (the top assembly's CAD milestone).

All of it is a design output, approved for build at G2 and released at G3 (SOP-004). The
builder follows the instruction; a step that cannot be followed as written is recorded on the
traveller, and the design is fixed: by pull request before release, by ECR after (SOP-001).
*Basis: ISO §8.3.5 (design outputs specify production and inspection), §8.5.1 (documented
information for production)*

## 5. Opening a build
Before assembly, record in `builds/B00n/build.yaml`:
- build ID, actual start date and builder;
- assembly PN and revision, its state (approved for build, or released), the git commit
  and CAD version it was built from, and the QMS revision in use;
- configuration: the revision of every made part and the firmware version;
- serial numbers to be built (SOP-002 section 7);
- applicable deviations.

Build only from a build document approved for build or released (SOP-002 section 5). Any
other use requires a deviation.
*Basis: ISO §8.5.1, §8.5.2*

## 6. Trace record (optional)
By default a unit is traced to its design: its serial number, the build document revision,
the build configuration in `build.yaml` and its build traveller. That is enough unless
traceability to purchases is required (by a customer, a regulation or the team).

When it is required, `trace.csv` adds one row per unit per traced part: serial number, PN,
revision, quantity, purchase line(s) (`P-nnnn`; parts of one PN pooled from several purchases
list every line in the bin), and the sub-assembly's own serial number where it has one.
Parts of the same PN may be pooled from several purchases unless a batch itself matters (a lot
or date code that may need recalling); stock is labelled with the PN and its purchase lines.
*Basis: ISO 9001 §8.5.2 requires traceability only when it is a requirement; ISO 13485 makes it
one for medical devices.*

## 7. Unit history
After release, record every change to a unit in `builds/unit_history.csv` (SOP-006-A06):
serial number, date, what changed (e.g. software v1.2.0 to v1.3.0, part replaced, rework,
recalibration), the reason (ECR or NC reference) and who made the change. Per-unit settings
such as calibration values are recorded in the unit's build or history records.
Credentials are never stored in the repo.
*Basis: ISO §8.5.2, §8.5.6*

## 8. Records
`build.yaml`, `inspection.csv` and `trace.csv` in `builds/B00n/`, the assembly instructions
and the inspection checks are controlled under SOP-001. CI checks that every Class A and B line in `trace.csv` refers to an existing
purchase line, and that every Class A purchase line used has passed inspection.

## Appendices
Appendices are forms and templates that belong to this SOP. They carry the SOP's revision
and change only through a revision of this SOP.

| ID | Title | File | Used in product repos as |
|---|---|---|---|
| SOP-006-A01 | Build record header | [SOP-006-A01-build.yaml](SOP-006-A01-build.yaml) | `builds/B00n/build.yaml` |
| SOP-006-A02 | Incoming inspection record | [SOP-006-A02-inspection.csv](SOP-006-A02-inspection.csv) | `builds/B00n/inspection.csv` |
| SOP-006-A03 | Trace record | [SOP-006-A03-trace.csv](SOP-006-A03-trace.csv) | `builds/B00n/trace.csv` |
| SOP-006-A04 | Assembly instruction | [SOP-006-A04-assembly-instruction.md](SOP-006-A04-assembly-instruction.md) | `03_build_package/<PN>_assembly_instructions_rev_<X>.pdf` (generated from `02_design/build_document/`) |
| SOP-006-A05 | Incoming inspection checks | [SOP-006-A05-inspection-checks.csv](SOP-006-A05-inspection-checks.csv) | `02_design/build_document/inspection_checks.csv` (issued in appendix A03) |
| SOP-006-A06 | Unit history | [SOP-006-A06-unit-history.csv](SOP-006-A06-unit-history.csv) | `builds/unit_history.csv` |
