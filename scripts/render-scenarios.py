#!/usr/bin/env python3
"""Validate documentary scenario traceability and render its review documents."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/research"
OFFSETS = {"REF51": 17, "SDK51": 13, "WB51": 9}


def load(name):
    return json.loads((DOCS / name).read_text())


def indexed(rows, kind):
    result = {row["id"]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"Duplicate {kind} IDs")
    return result


def validate(sources, features, baseline, cases):
    source_map = indexed(sources, "source")
    feature_map = indexed(features, "feature")
    case_map = indexed(cases, "scenario")
    spec = (ROOT / "kitty-specs/wp51-parity-01M64CVY/spec.md").read_text()
    requirements = set(re.findall(r"\b(?:FR|NFR|C)-\d{3}\b", spec))
    if baseline["installation_status"] == "fingerprinted":
        if baseline["verification_status"] != "original-reference-smoke-observed":
            raise ValueError("Full reference/differential verification has not been established")
        if not re.fullmatch(r"[0-9a-f]{64}", baseline["executable_sha256"] or ""):
            raise ValueError("Fingerprint lacks an executable SHA-256")
        for field in ["displayed_version_capture", "installed_file_manifest", "environment_manifest", "printer_profile", "language_resource_profile"]:
            if not baseline[field] or not (DOCS / baseline[field]).is_file():
                raise ValueError(f"Missing reference identity artifact: {field}")
        installed = json.loads((DOCS / baseline["installed_file_manifest"]).read_text())
        exe = next(x for x in installed["files"] if x["path"].upper() == "WP51/WP.EXE")
        if exe["sha256"] != baseline["executable_sha256"]:
            raise ValueError("Executable fingerprint disagrees with installation manifest")
    elif baseline["installation_status"] != "not-acquired" or baseline["verification_status"] != "not-run":
        raise ValueError("Unknown installation/evidence state")
    for case in cases:
        if not re.fullmatch(r"CMD51-\d{3}", case["id"]):
            raise ValueError(f"Malformed scenario ID: {case['id']}")
        if case["baseline_id"] != baseline["id"]:
            raise ValueError("Scenario refers to an unknown baseline")
        if not case["feature_ids"] or set(case["feature_ids"]) - feature_map.keys():
            raise ValueError(f"Unknown/missing parent in {case['id']}")
        if not case["requirement_ids"] or set(case["requirement_ids"]) - requirements:
            raise ValueError(f"Unknown/missing requirement in {case['id']}")
        for field in ["title", "preconditions", "steps", "expected", "capture", "open_details", "source_locators"]:
            if not case[field]:
                raise ValueError(f"Missing {field} in {case['id']}")
        if case["basis"] not in {"manual-derived", "project-contract", "oracle-investigation"}:
            raise ValueError("Unknown scenario basis")
        if case["basis"] == "project-contract" and not case.get("policy_refs"):
            raise ValueError("Contract scenario lacks policy trace")
        if case["basis"] == "oracle-investigation" and case["readiness"] != "investigation":
            raise ValueError("Investigations cannot masquerade as acceptance-ready cases")
        if case["implementation_status"] != "not-implemented":
            raise ValueError("Original-reference observations cannot establish Wordling implementation")
        if case["oracle_status"] == "partially-observed":
            if baseline["installation_status"] != "fingerprinted" or not case["evidence_paths"] or not case.get("observed_scope"):
                raise ValueError("Observed case lacks fingerprinted reference and bounded evidence scope")
            for evidence in case["evidence_paths"]:
                run = json.loads((ROOT / evidence).read_text())
                if run["baseline_id"] != baseline["id"] or run["scope"] != "original-reference-only" or run["wordling_tested"]:
                    raise ValueError("Unexpected evidence scope")
                result = next(x for x in run["results"] if x["case_id"] == case["id"])
                if result["result"] != "observed-matches-smoke-expectations" or not result.get("checks") or not all(x["passed"] for x in result["checks"]):
                    raise ValueError("Observed status lacks passing bounded checks")
                for artifact in result["evidence"]:
                    path = ROOT / artifact["path"]
                    if not path.is_file() or path.stat().st_size != artifact["size"]:
                        raise ValueError(f"Missing/changed observation artifact: {path}")
                    with path.open("rb") as stream:
                        digest = hashlib.file_digest(stream, "sha256").hexdigest()
                    if digest != artifact["sha256"]:
                        raise ValueError(f"Observation checksum mismatch: {path}")
        elif case["oracle_status"] != "not-run" or case["evidence_paths"]:
            raise ValueError("Unsupported oracle status; full/differential verification is not implemented")
        for loc in case["source_locators"]:
            source = source_map[loc["source_id"]]
            if not 1 <= loc["pdf_start"] <= loc["pdf_end"] <= source["pdf_pages"]:
                raise ValueError(f"Invalid PDF locator in {case['id']}")
            if loc["source_id"] in OFFSETS:
                offset = OFFSETS[loc["source_id"]]
                if loc["printed_start"] + offset != loc["pdf_start"] or loc["printed_end"] + offset != loc["pdf_end"]:
                    raise ValueError(f"Printed/PDF mismatch in {case['id']}")
    for feature in features:
        expected = [c["id"] for c in cases if feature["id"] in c["feature_ids"]]
        if feature["command_scenario_ids"] != expected:
            raise ValueError(f"Scenario back-links disagree for {feature['id']}")
        if set(expected) - case_map.keys():
            raise ValueError("Dangling scenario reference")


def render_cases(sources, features, cases):
    source_map = indexed(sources, "source")
    feature_map = indexed(features, "feature")
    bases = Counter(c["basis"] for c in cases)
    observed = sum(c["oracle_status"] == "partially-observed" for c in cases)
    out = ["# WP 5.1 command-level scenario catalogue", "",
           "Generated from `command-scenarios.json` by `scripts/render-scenarios.py`.", "",
           f"**{len(cases)} documentary scenarios**: {bases['manual-derived']} manual-derived,",
           f"{bases['project-contract']} project-contract cases, and {bases['oracle-investigation']} explicit oracle investigation.",
           f"**{observed} cases have partial original-app observations; {len(cases) - observed} remain not run.**",
           "All Wordling implementations/differential tests remain **not implemented**. These are representative cases,",
           "not a claim that every subcommand or branch has been enumerated.", "",
           "[Reference release decision](../decisions/0001-reference-release.md) selects",
           "plain U.S. English WP 5.1 DOS dated 1992-03-09. The [installation and limits](reference-environment/README.md)",
           "are fingerprinted; bounded original-only smoke probes have begun. [Coverage matrix](scenario-coverage.md) links",
           "the parent groups; [workbook map](workbook-map.md) tracks lesson themes.", "",
           "## Procedure notation and execution contract", "",
           "- `KEY Ctrl+F8` is a chord. Commas in `KEY Home, Home, Up` mean sequential presses.",
           "- `TYPE` enters literal fixture text. `SELECT` chooses a named original menu",
           "  item using keyboard navigation; it does not imply a guessed numeric accelerator.",
           "- Begin each case with a fresh copied setup and declared fixture; restore",
           "  clock, keyboard, display, filesystem and printer/resource profiles. Use scratch",
           "  copies for destructive commands. Never operate on the immutable master fixture.",
           "- Starting states are human-readable fixture specifications. No fixture builder",
           "  for the full catalogue exists yet; `scripts/reference/smoke.py` implements a bounded subset of probes. Menu wording and unresolved prompt",
           "  responses require capture before automation; these are documentary drafts.",
           "- Record text/code cursor positions, status/prompt screens and resulting files.",
           "  For print/layout cases include resource hashes and full printer-output bytes.",
           "- Manual-derived expectations are hypotheses to test against the original.",
           "  Contract cases express stronger Wordling requirements (especially byte-identical",
           "  no-edit saves); do not invent matching original behavior. Investigation cases",
           "  intentionally have unresolved behavior and cannot count as acceptance passes.",
           "- `partially-observed` means linked original-only smoke checks were executed;",
           "  it does not mean every expected branch, byte invariant or Wordling behavior was tested.",
           "- Source locators refer to pinned source bytes. OCR has not been visually verified",
           "  for every key/menu label; named navigation avoids uncertain accelerators.", ""]
    for case in cases:
        out += [f'<a id="{case["id"].lower()}"></a>', "", f"## {case['id']}: {case['title']}", "",
                f"Parent: {', '.join(case['feature_ids'])}. Requirements: {', '.join(case['requirement_ids'])}.",
                f"Basis: **{case['basis']}**. Readiness: {case['readiness']}. Oracle: **{case['oracle_status']}**.", "",
                "**Given**", ""]
        out += [f"- {s}" for s in case["preconditions"]]
        out += ["", "**When**", ""]
        out += [f"{i}. {s}" for i, s in enumerate(case["steps"], 1)]
        out += ["", "**Then**", ""]
        out += [f"- {s}" for s in case["expected"]]
        out += ["", "**Capture / unresolved details**", ""]
        out += [f"- {s}" for s in case["capture"] + case["open_details"]]
        refs = []
        for loc in case["source_locators"]:
            source = source_map[loc["source_id"]]
            label = f"{source['id']} PDF {loc['pdf_start']}-{loc['pdf_end']}"
            if loc["printed_start"] is not None:
                label += f" (printed {loc['printed_start']}-{loc['printed_end']})"
            refs.append(f"[{label}]({source['url']}#page={loc['pdf_start']})")
        out += ["", "Sources: " + "; ".join(refs) + ".", ""]
        if case.get("policy_refs"):
            out += ["Project policy: [compatibility contract](../compatibility.md), " + ", ".join(case["policy_refs"]) + ".", ""]
        if case["evidence_paths"]:
            out += ["Observed scope: " + case["observed_scope"], ""]
            out += ["Evidence: " + ", ".join(f"[{Path(x).parent.name}]({Path(x).relative_to('docs/research').as_posix()})" for x in case["evidence_paths"]) + ".", ""]
    return "\n".join(out)


def render_coverage(features, cases):
    out = ["# Scenario-to-inventory coverage", "",
           "Generated by `scripts/render-scenarios.py`. Counts mean representative",
           "documentary cases authored, **not** subcommand completeness or tested parity.",
           "Every group still requires branch/negative-case and version reconciliation.", "",
           "| Group | Feature | Cases | Status |", "| --- | --- | --- | --- |"]
    for f in features:
        refs = [f"[{x}](command-scenarios.md#{x.lower()})" for x in f["command_scenario_ids"]]
        relevant = [c for c in cases if f["id"] in c["feature_ids"]]
        status = "investigation only" if all(c["basis"] == "oracle-investigation" for c in relevant) else "representative drafts; unverified"
        observed = sum(c["oracle_status"] == "partially-observed" for c in relevant)
        if observed:
            status = f"{observed} partial original-app observations; no Wordling verification"
        out.append(f"| {f['id']} | {f['title']} | {', '.join(refs) or 'none'} | {status} |")
    out += ["", "## Still required before completeness", "",
            "- Enumerate every macro/merge command, expression, variable and value-table option.",
            "- Expand equation commands/palette, table operations, graphic box types and imports.",
            "- Cover all printer-definition editing commands and font/resource combinations.",
            "- Cover all file conversion modes, encryption failures, networking and platform adapters.",
            "- Expand headers/footers, outline types, indices, authorities and reference error paths.",
            "- Reconcile every menu item and manual subsection against a command obligation.",
            "- Convert workbook thematic mappings into independent, step-level scenarios.",
            "- Visually check ambiguous OCR and capture exact original prompts/accelerators.",
            "- Extend the fingerprinted reference smoke observations before any full/differential verified claim.", ""]
    return "\n".join(out)


def render_workbook(features, cases, lessons, sources):
    feature_map = indexed(features, "feature")
    source_map = indexed(sources, "source")
    if [x["lesson"] for x in lessons] != list(range(1, 37)):
        raise ValueError("Workbook lesson mapping must contain each of 1..36 once")
    out = ["# Workbook lesson map", "",
           "Thematic mapping of all 36 lessons in the pinned 11/89 workbook, using",
           "its contents (WB51 PDF 4-5). These are independently worded topic labels,",
           "not copied lessons or a claim to have replayed them. Group associations are",
           "research leads and may change after step-level study. The 1989 teaching",
           "files and procedures need correction against WBC51 and the March 1992 baseline.", "",
           "Every lesson is **thematic only; step mapping incomplete; not run**.",
           "Linked command cases are candidate building blocks, not substitutes for",
           "the full lesson or evidence that every original keystroke has been covered.", "",
           "| Lesson | Theme | Source start | Parent groups | Candidate cases |",
           "| --- | --- | --- | --- | --- |"]
    for lesson in lessons:
        if set(lesson["feature_ids"]) - feature_map.keys():
            raise ValueError("Unknown workbook feature parent")
        if lesson["pdf_start"] != lesson["printed_start"] + 9:
            raise ValueError("Workbook locator offset mismatch")
        if lesson["mapping_status"] != "thematic-only" or lesson["oracle_status"] != "not-run":
            raise ValueError("Add lesson evidence before claiming step mapping or execution")
        candidates = [c["id"] for c in cases if set(c["feature_ids"]) & set(lesson["feature_ids"])]
        # Keep the table useful; the complete parent links are in scenario-coverage.md.
        links = [f"[{x}](command-scenarios.md#{x.lower()})" for x in candidates[:4]]
        if len(candidates) > 4:
            links.append("more via parent coverage")
        source = source_map[lesson["source_id"]]
        loc = f"[WB51 p. {lesson['printed_start']}; PDF {lesson['pdf_start']}]({source['url']}#page={lesson['pdf_start']})"
        out.append(f"| {lesson['lesson']} | {lesson['theme']} | {loc} | {', '.join(lesson['feature_ids'])} | {', '.join(links)} |")
    out += ["", "WBC51 PDF 1 specifically corrects file-list printing in lesson 11:",
            "the workbook teaching printer cannot print the file list. The printer-test",
            "resource and installed printer capabilities must also be declared before",
            "using printed workbook results as evidence. Later reference-manual lesson",
            "numbers are not assumed to identify the same 11/89 workbook lessons.", ""]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    sources, features = load("sources.json"), load("feature-inventory.json")
    baseline, cases = load("reference-baseline.json"), load("command-scenarios.json")
    validate(sources, features, baseline, cases)
    outputs = {"command-scenarios.md": render_cases(sources, features, cases),
               "scenario-coverage.md": render_coverage(features, cases),
               "workbook-map.md": render_workbook(features, cases, load("workbook-map.json"), sources)}
    for filename, data in outputs.items():
        path = DOCS / filename
        if args.check:
            if not path.exists() or path.read_text() != data:
                raise SystemExit(f"Stale {filename}; run scripts/render-scenarios.py")
        else:
            path.write_text(data)
    print(f"Validated {len(cases)} scenarios, {len(features)} parent groups, requirement traces, source locators and evidence states.")


if __name__ == "__main__":
    main()
