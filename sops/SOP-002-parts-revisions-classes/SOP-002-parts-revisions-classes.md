---
id: SOP-002
title: Part numbering, revisions and part classes
rev: A
status: draft          # draft until released with QMS-rev A
owner: Quality lead     # a role, see roles.yaml
standard: ISO 9001:2026 # clause refs not yet checked against the purchased text
---

# SOP-002 Part numbering, revisions and part classes

Each section ends with its basis: *ISO §x.y* (required by the standard) or *minimalQMS
choice* (may be changed by teams using minimalQMS).

## 1. Purpose
To identify every part, assembly and unit, state its current revision, and set the level
of traceability according to risk.
*Basis: ISO §8.5.2, §8.4.2*

## 2. Scope
Everything that appears on a BOM: purchased parts, made parts (PCBs, printed or machined
parts, harnesses), assemblies, firmware and consumables. Also serial numbers of built units.

## 3. Part numbers
Every item on a BOM has a part number (PN). The rules, whatever the format:
- A PN identifies one item: it never changes meaning and is never reused.
- An assembly's PN shows that it is an assembly, and a custom item's PN shows that it is
  custom rather than bought, so a BOM line says by itself whether it needs its own build
  document (SOP-006) or a supplier.
- Custom PNs are scoped to the project; bought (OTS) PNs are shared across projects.
- An assembly has sub-parts or requires an assembly or modification instruction. A PCB
  ordered already assembled is an assembly.

| Type | Kept in |
|---|---|
| **OTS part** (off the shelf) | OTS library (`minimal-qms-ots-library` repo), or the product's BOM if the team keeps no library |
| **Custom part** | Product repo, in the BOM of the assembly that uses it |
| **Custom assembly** | Product repo, as the number of its build document |

The format is a team choice. The minimalQMS default (`CCC-NNNN`, `PPP-NNNN`, `PPP-A-NNNN`,
allocated with the OTS library's `new_pn.py`) is in `docs/INTERFACES.md`, "Part numbers";
the tools and agents use it. A team that uses another format records it there and adapts
the tools.
- OTS records hold where to buy: manufacturer, MPN, supplier, supplier part number, link,
  pack quantity, and the price of one piece with its date. Parts sold in packs are ordered
  in whole packs. For McMaster-Carr parts, manufacturer and MPN stay blank (McMaster hides
  them). A custom part's revision is in the BOM that uses it, and its CAD source in the
  build document's title block and make-files README; when a fabricator makes it, the BOM
  line carries the same purchasing columns.

*Basis: ISO §8.5.2. The format is a minimalQMS choice; OTS category codes are adapted from
gitplm (see NOTICE).*

## 4. Revisions
The revision is a separate field, not part of the PN: `PRX-0002` rev `B`. Revisions run
A, B, C …, omitting I, O, Q, S, X and Z.
- **Interchangeable change** (same form, fit and function): increment the revision.
- **Non-interchangeable change:** assign a new PN.
- Firmware uses its version tag (e.g. `v1.2.0`) as the revision.
- OTS parts have no internal revision; the manufacturer part number defines them. A
  replacement MPN that is not a drop-in substitute receives a new PN.

A revision change follows SOP-001: everything that cites the part (BOMs, build documents,
drawings) is updated in the same change.

A revision letter is given when the design is approved for build at G2, and becomes official
when that revision is released at G3 (section 5). Fixes found while building and testing the
first units keep the letter: rev A is what finally works, not the first attempt. The CAD tool's
own version numbers (e.g. Fusion `v31`) are not revisions: they count saves, change when
nothing a builder makes changes, and cover one file. The build document records the CAD
version each revision points to.

Each released file, output folder and git tag must identify the PN and revision it belongs
to. The default names are:
- files and folders: `<PN>_<short-name>_rev_<X>`, e.g. `PRX-0004_lid_rev_B.step`;
- tags: `<PN>-rev<X>`, e.g. `PRX-0002-revB`.

A team may use other names that meet the rule.
*Basis: ISO §8.3.6, §8.5.6, §7.5.3, §8.5.2. The interchangeability rule and letter sequence are a
minimalQMS choice based on common drafting practice. The default names are a minimalQMS
choice.*

## 5. Lifecycle
Custom parts and assemblies take their state from git, through their build document:

| State | Where it is |
|---|---|
| Draft | On a branch or in an open pull request; title blocks say "Draft". |
| Approved for build | Merged to `main` after the G2 approval, not tagged; title blocks say "Approved for build" with the approval reference. Parts may be ordered and prototype units built from it. Each build records the git commit and CAD version it was built from (SOP-006 section 5). A fix found in a prototype build is a pull request approved by the approver, with the reason in the PR and on the traveller of the build that found it; it keeps the revision letter and needs no ECR. |
| Released | Tagged `<PN>-rev<X>` at G3, once units built from it pass verification (SOP-007), with a GitHub Release carrying the build document and its appendices; title blocks say "Released" with the date, and file names add it (`docs/INTERFACES.md`). From here a change is an ECR and a new revision (SOP-001). |
| Obsolete | Superseded by a later revision or no longer in any current BOM; earlier revisions stay in their tags and releases. |

OTS parts keep a `lifecycle` column in the OTS library (`draft`, `released`, `obsolete`).
State changes follow SOP-001.
*Basis: ISO §8.5.2, §7.5.3, §8.3.4 (verification before release). Using git as the record of
state, and releasing after the first units are verified, are minimalQMS choices.*

## 6. Part classes

The class says how a part may be bought. The BOM (appendix A01) shows it in a Purchasing
column, so the purchaser knows which parts may come from anywhere:

| A01 Purchasing | Meaning |
|---|---|
| `Custom` | A custom part (PPP-NNNN), made to its design |
| `Approved supplier, exact part` | Class A |
| `Any supplier, exact part` | Class B or C, but the design depends on this exact part: a heat-set insert whose hole is drawn for it, a board the housing is built around. Marked per BOM line (`exact_part`) |
| `Any supplier, any matching part` | Class B or C: any part that matches the BOM description |

| Class | Items | Bought from |
|---|---|---|
| **A** | Parts where a wrong or fake part causes a real problem: safety (power supplies), measurement (sensors), certification (radio boards), and key components | An approved supplier (SOP-005) |
| **B** | Low-risk parts: hardware (screws, inserts, standoffs), cables, memory cards, passive adapter boards | Any supplier; the exact part where the design depends on it |
| **C** | Consumables: glue, flux, solder, zip ties | Any source |

Custom parts are made in house or by a chosen maker; the critical ones are inspected on receipt
(SOP-006 section 3). Traceability to purchases is optional (SOP-006 section 6). The class is
set per PN; when in doubt, assign A.
*Basis: ISO §8.5.2 and §8.4.2 allow traceability and control to be set by risk. The A/B/C
scheme is a minimalQMS choice.*

## 7. Serial numbers
Assemblies (`PPP-A-NNNN`) receive a serial number. Parts do not; they are traced by
purchase line or print job.
- **Format:** `<PN>-YYMMDD<letter>`, where the date is the assembly date (or the receipt
  date for purchased assemblies) and the letter counts units of that PN on that date: A,
  B … Z, then AA. Example: `PRX-A-0003-261118A`.
- **Label:** mark the serial number on the unit. Where the PN is already marked on the unit,
  the label may show only `YYMMDD<letter>`.
- **Record:** the serial number is listed in the build record (SOP-006), which links it to
  the assembly revision, its Class A purchase lines and any sub-assembly serial numbers.
  No separate form is required.
- Purchased assemblies receive their serial number at incoming inspection (SOP-006).

*Basis: ISO §8.5.2. The format is a minimalQMS choice.*

## 8. Configurations and baselines
A configuration is the set of part revisions, including software, that makes up an
assembly. The BOM of the top assembly at a given revision defines it.
- **Variants:** each variant of a product is a separate top assembly (`PPP-A-NNNN`) with its
  own BOM, in the same repo. Variants share common parts; shared parts are never
  duplicated. Variants that share little of their design are separate projects.
- **Software** that ships in the product is a custom part. Its version tag is its revision,
  and it appears on the BOM. A software update to a released product follows SOP-001.
- **Baselines:** each released configuration is tagged with its top assembly's tag (section 4,
  e.g. `PRX-A-0001-revB`). `main` holds the current approved state; branches are short-lived. A
  fix to an earlier baseline is made on a branch created from its tag.

*Basis: ISO §8.3.5, §8.5.2, §8.5.6. ISO 10007 gives guidance on configuration management.
The variant, software and tag rules are a minimalQMS choice.*

## 9. Records
- Product repo: one BOM per assembly, issued as appendix A01 of its build document
  (`03_build_package/<PN>-A01_bom_rev_<X>.csv`, source `02_design/build_document/bom.csv`),
  read from the CAD tools. Columns: ref (the callout used in the assembly instruction), PN,
  rev (custom parts), description, category (`Custom (part)`, `Custom (assembly)` or `OTS`),
  qty, unit in capitals (`EA`), and for OTS parts the manufacturer, manufacturer PN, supplier,
  supplier PN, link, price, and the unit and line cost in CAD, so the purchaser can order from it
  alone. Column names: `ref`, `internal_pn`, `rev`, `description`, `category`, `purchasing`,
  `qty`, `unit`, `manufacturer`, `manufacturer_pn`, `supplier`, `supplier_pn`, `link`,
  `unit_price`, `pack_qty`, `currency`, `unit_cost_cad`, `line_cost_cad`, `price_date`, `notes`. No
  blank cells: `-` where a field does not apply. Ordering data is copied into each
  product; the OTS library is the source when a team keeps one.
- OTS library: `parts/CCC.csv` (one file per prefix), `categories.csv` and `projects.csv`.

These records are controlled under SOP-001. CI checks that every BOM line refers to an
existing, `released` PN with a class, and that bought items have a supplier.

## Appendices
Appendices are forms and templates that belong to this SOP. They carry the SOP's revision
and change only through a revision of this SOP.

| ID | Title | File | Used in product repos as |
|---|---|---|---|
| SOP-002-A01 | Custom parts list | [SOP-002-A01-custom-parts.csv](SOP-002-A01-custom-parts.csv) | Optional: only when custom parts are shared across several assemblies |
| SOP-002-A02 | Assembly BOM | [SOP-002-A02-bom.csv](SOP-002-A02-bom.csv) | `02_design/build_document/bom.csv` (issued as appendix A01) |
