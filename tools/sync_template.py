"""Copy SOP appendices into the product template, or check that the copies are current.

Usage:
    python tools/sync_template.py          # write the copies
    python tools/sync_template.py --check  # exit 1 if any copy differs (for CI)

Two kinds of copies are made into product-template/:
  1. qms/forms/ : a full copy of every appendix, so a product repo has every form it needs.
  2. starter files: records a new project starts with. CSV starters get the appendix's
     header row only; other starters are full copies.
Records with no starter (purchases, suppliers, unit history, equipment, NCs, deviations) are
created from qms/forms/ when the first one is needed; their folders do not exist until then.
Starters that need project answers (roles, plan, README, AGENTS.md) are hand-written
.jinja files in product-template/ and are not managed here.
"""
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "product-template")

# appendix file -> path in the product repo
STARTERS = {
    "SOP-001-A01-ecr-form.md": ".github/ISSUE_TEMPLATE/ecr.md",
    "SOP-001-A02-eco-pr-template.md": ".github/pull_request_template.md",
    "SOP-002-A01-custom-parts.csv": "03_build_package/parts.csv",
    "SOP-002-A02-bom.csv": "02_design/build_document/bom.csv",
    "SOP-003-A03-worklog.md": "worklog.md",
    "SOP-004-A02-gates.yaml": "00_planning/gates.yaml",
    "SOP-004-A04-risks.csv": "01_requirements/risks.csv",
    "SOP-004-A05-scorecard.csv": "00_planning/scorecard.csv",
    "SOP-006-A05-inspection-checks.csv": "02_design/build_document/inspection_checks.csv",
}


def appendices():
    return sorted(glob.glob(os.path.join(ROOT, "sops", "*", "SOP-*-A[0-9][0-9]-*")))


def starter_content(path):
    text = open(path, encoding="utf-8").read()
    if path.endswith(".csv"):
        return text.splitlines()[0] + "\n"  # header only; example rows are not copied
    return text


def planned():
    out = {}
    for src in appendices():
        name = os.path.basename(src)
        out[os.path.join("qms", "forms", name)] = open(src, encoding="utf-8").read()
        if name in STARTERS:
            out[STARTERS[name]] = starter_content(src)
    missing = set(STARTERS) - {os.path.basename(p) for p in appendices()}
    if missing:
        raise SystemExit(f"error: STARTERS lists appendices that do not exist: {sorted(missing)}")
    return out


def main(argv):
    check = "--check" in argv
    stale = []
    for rel, content in planned().items():
        dest = os.path.join(TEMPLATE, rel)
        current = open(dest, encoding="utf-8").read() if os.path.exists(dest) else None
        if current == content:
            continue
        if check:
            stale.append(rel)
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
    # forms that no longer exist as appendices
    forms_dir = os.path.join(TEMPLATE, "qms", "forms")
    expected = {os.path.basename(p) for p in appendices()}
    if os.path.isdir(forms_dir):
        for name in os.listdir(forms_dir):
            if not name.startswith("README") and name not in expected:
                if check:
                    stale.append(f"forms/{name} (no longer an appendix)")
                else:
                    os.remove(os.path.join(forms_dir, name))
    if check:
        for s in stale:
            print(f"out of date: product-template/{s}")
        print("template copies are current" if not stale else "run: python tools/sync_template.py")
        return 1 if stale else 0
    print(f"synced {len(planned())} files into product-template/")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
