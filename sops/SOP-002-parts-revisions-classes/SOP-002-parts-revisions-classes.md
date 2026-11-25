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

| Type | Format | Kept in | Example |
|---|---|---|---|
| **OTS part** (off the shelf) | `CCC-NNNN` | OTS library (`minimal-qms-ots-library` repo) | `HWB-0001` M3x8 screws |
| **Custom part** | `PPP-NNNN` | Product repo, `03_build_package/parts.csv` | `PRX-0004` printed lid |
| **Custom assembly** | `PPP-A-NNNN` | Product repo, `03_build_package/parts.csv` | `PRX-A-0003` assembled PCB |

- `CCC` is an OTS category code; `PPP` is the project code. Both are 3 capital letters,
  registered in the OTS library, and never the same. `A` is a fixed letter that marks an
  assembly.
- An assembly has sub-parts or requires an assembly or modification instruction. A PCB
  ordered already assembled is an assembly.
- Custom parts and assemblies share one number sequence per project.
- Allocate numbers with the OTS library's `new_pn.py`. A part number never changes meaning
  and is never reused.
- OTS records hold where to buy: manufacturer, MPN, supplier, supplier part number, link,
  pack quantity, and the price of one piece with its date. Parts sold in packs are ordered
  in whole packs. For McMaster-Carr parts, manufacturer and MPN stay blank (McMaster hides
  them). Custom records hold revision, lifecycle, make method and
  source (CAD reference), plus the same purchasing columns when the part is bought from a
  fabricator.

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

A revision change follows SOP-001: everything that cites the part (`parts.csv`, BOMs,
drawings) is updated in the same change.

Each released file, output folder and git tag must identify the PN and revision it belongs
to. The default names are:
- files and folders: `<PN>_rev<X>_<short-name>`, e.g. `PRX-0004_revB_lid.step`;
- tags: `<PN>-rev<X>`, e.g. `PRX-0002-revB`.

A team may use other names that meet the rule.
*Basis: ISO §8.3.6, §8.5.6, §7.5.3, §8.5.2. The interchangeability rule and letter sequence are a
minimalQMS choice based on common drafting practice. The default names are a minimalQMS
choice.*

## 5. Lifecycle
Each PN (OTS and custom) has one lifecycle state:

| State | Meaning |
|---|---|
| `draft` | In design. Not permitted on a released BOM. |
| `released` | Approved for building or purchasing. |
| `obsolete` | Not permitted in new builds. Retained for traceability of existing units. |

State changes follow SOP-001.
*Basis: ISO §8.5.2. The three states are a minimalQMS choice.*

## 6. Part classes

The class says where a part may be bought. It is shown in the BOM (appendix A01) as a Source
column, so the purchaser knows which parts may come from anywhere.

| Class | Items | Bought from (A01 Source) |
|---|---|---|
| **A** | Parts where a wrong or fake part causes a real problem: safety (power supplies), measurement (sensors), certification (radio boards), and key components | An approved supplier (SOP-005) |
| **B** | Low-risk parts that any matching part replaces: hardware (screws, inserts, standoffs), cables, memory cards, passive adapter boards | Any source, if it matches the BOM description |
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
- Product repo `03_build_package/parts.csv`: custom parts and assemblies.
- Product repo: one BOM per assembly, issued as appendix A01 of its build document
  (`03_build_package/<PN>_rev<X>_A01_bom.csv`, source `02_design/build_document/bom.csv`),
  read from the CAD tools. Columns: ref (the callout used in the assembly instruction), PN,
  rev (custom parts), description, category (`Custom (part)`, `Custom (assembly)` or `OTS`),
  qty, unit in capitals (`EA`), and for OTS parts the manufacturer, MPN, supplier, supplier SKU,
  link and price, so the purchaser can order from it alone. Ordering data is copied into each
  product; the OTS library is the source when a team keeps one.
- OTS library: `parts/CCC.csv` (one file per prefix), `categories.csv` and `projects.csv`.

These records are controlled under SOP-001. CI checks that every BOM line refers to an
existing, `released` PN with a class, and that bought items have a supplier.

## Appendices
Appendices are forms and templates that belong to this SOP. They carry the SOP's revision
and change only through a revision of this SOP.

| ID | Title | File | Used in product repos as |
|---|---|---|---|
| SOP-002-A01 | Custom parts list | [SOP-002-A01-custom-parts.csv](SOP-002-A01-custom-parts.csv) | `03_build_package/parts.csv` |
| SOP-002-A02 | Assembly BOM | [SOP-002-A02-bom.csv](SOP-002-A02-bom.csv) | `02_design/build_document/bom.csv` (issued as appendix A01) |
