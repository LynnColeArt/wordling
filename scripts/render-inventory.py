#!/usr/bin/env python3
"""Validate the research registry and render its reviewable Markdown inventory."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/research"


def render():
    sources = json.loads((DOCS / "sources.json").read_text())
    features = json.loads((DOCS / "feature-inventory.json").read_text())
    by_id = {s["id"]: s for s in sources}
    if len(by_id) != len(sources):
        raise ValueError("Duplicate source IDs")
    seen = set()
    lines = [
        "# WordPerfect 5.1 parity feature inventory", "",
        "Generated from `feature-inventory.json`; edit that registry and run",
        "`python3 scripts/render-inventory.py` to update this view.", "",
        f"Current catalogue: **{len(features)} feature groups**, all in Mission 1. These are",
        "coverage groups, not a complete command-level inventory or implementation",
        "work packages. Every group must be decomposed during section-by-section study.",
        "No feature is implemented or verified against an original executable yet.", "",
        "[Command scenarios](command-scenarios.md) provide representative command-level",
        "drafts. [Coverage matrix](scenario-coverage.md) links each parent to its cases.",
        "The presence of cases does not mean every subcommand or branch is covered.", "",
        "`indexed` means located in the manual contents or toolkit structure.",
        "`studied` means selected relevant passages were examined in this initial pass;",
        "it does not mean the entire cited range has been exhaustively studied.",
        "See findings.md for the specific studied behavior. Original-app observations",
        "are tracked at command-scenario level; no parent group is verified.",
        "Implementation and documentary status are independent.", "",
        "Page locators use the exact checksummed editions in sources.json. Printed",
        "toolkit page numbers below refer to its **WP** section only. PDF pages are",
        "one-based. Range endpoints are inclusive. OCR needs visual verification for",
        "ambiguous keystrokes, numbers and diagrams.", "",
    ]
    area = None
    for index, f in enumerate(features):
        if f["id"] in seen:
            raise ValueError(f"Duplicate feature ID: {f['id']}")
        seen.add(f["id"])
        s = by_id[f["source_id"]]
        if f["mission"] != "M1":
            raise ValueError("Parity registry may only contain M1 features")
        if f["documentary_evidence"] not in {"indexed", "studied"}:
            raise ValueError("Unsupported documentary evidence state")
        if f["implementation"] != "not-started" or f["oracle_evidence"] != "pending":
            raise ValueError("Extend the evidence schema with durable evidence before claiming progress")
        if not f["acceptance_probe"]:
            raise ValueError("Missing acceptance probe")
        refs = []
        for loc in f["locators"]:
            a, b = loc["printed_start"], loc["printed_end"]
            c, d = loc["pdf_start"], loc["pdf_end"]
            if not (1 <= a <= b and 1 <= c <= d <= s["pdf_pages"]):
                raise ValueError(f"Invalid page range: {f['id']}")
            label = str(a) if a == b else f"{a}-{b}"
            pdf = str(c) if c == d else f"{c}-{d}"
            refs.append(f"[{s['id']} pp. {label}; PDF {pdf}]({s['url']}#page={c})")
        if f["area"] != area:
            area = f["area"]
            lines.extend([f"## {area}", "", "| ID | Feature group | Manual evidence | Study | Acceptance probe |",
                          "| --- | --- | --- | --- | --- |"])
        lines.append(f"| {f['id']} | {f['title']} | {'; '.join(refs)} | {f['documentary_evidence']} | {f['acceptance_probe']} |")
        # Separate the next section cleanly; repeated blank lines are harmless.
        if index == len(features) - 1 or features[index + 1]["area"] != area:
            lines.append("")
    lines.extend([
        "## Coverage still to reconcile", "",
        "- Audit every reference chapter, appendix, menu entry, macro/merge command,",
        "  character/code table and original utility against stable inventory IDs.",
        "- Decompose compound groups into independently testable obligations; preserve",
        "  parent IDs and provenance when splitting entries.",
        "- Expand the [36-lesson thematic map](workbook-map.md) (WB51 contents, PDF 4-5)",
        "  into step-level acceptance scenarios without republishing lesson text.",
        "- Fingerprint the [selected reference release](../decisions/0001-reference-release.md), language editions, original resources,",
        "  proprietary fixture provenance and Linux platform adaptations.",
        "- Check toolkit and reference-manual release differences against the original.",
        "- No coverage percentage or parity claim until this reconciliation is complete.", "",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = render()
    target = DOCS / "feature-inventory.md"
    if args.check:
        if not target.exists() or target.read_text() != rendered:
            raise SystemExit("Inventory view is stale; run scripts/render-inventory.py")
        print("Inventory registry, source links, page ranges and generated view validated.")
    else:
        target.write_text(rendered)
        print(f"Wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
