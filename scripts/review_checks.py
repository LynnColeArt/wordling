#!/usr/bin/env python3
"""Run Wordling's real regression checks and emit Spec Kitty's JUnit artifact.

The declared command selects Spec Kitty's portable runner instead of its own
pytest/source-layout gate. This adapter reports subprocess outcomes; it does not
turn documentation assertions into test cases or claim WP compatibility.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import time
import xml.etree.ElementTree as ET


class Checks:
    def __init__(self, root: Path):
        self.root = root
        self.suite = ET.Element("testsuite", name="wordling-regression")
        self.failed = 0

    def run(self, name: str, command: list[str]) -> subprocess.CompletedProcess | None:
        case = ET.SubElement(self.suite, "testcase", classname="wordling.validation", name=name)
        started = time.monotonic()
        result = None
        try:
            result = subprocess.run(command, cwd=self.root, text=True, errors="replace",
                                    capture_output=True, timeout=240, check=False)
            ET.SubElement(case, "system-out").text = result.stdout
            ET.SubElement(case, "system-err").text = result.stderr
            if result.returncode:
                ET.SubElement(case, "failure", message=f"exit status {result.returncode}").text = (
                    result.stdout + result.stderr
                )
                self.failed += 1
        except (OSError, subprocess.TimeoutExpired) as error:
            ET.SubElement(case, "failure", message=type(error).__name__).text = str(error)
            self.failed += 1
        case.set("time", f"{time.monotonic() - started:.6f}")
        print(f"{'FAIL' if case.find('failure') is not None else 'PASS'} {name}", flush=True)
        return result

    def skip(self, name: str, reason: str) -> None:
        case = ET.SubElement(self.suite, "testcase", classname="wordling.validation", name=name)
        ET.SubElement(case, "skipped", message=reason)
        print(f"SKIP {name}: {reason}", flush=True)

    def write(self, output: Path) -> None:
        self.suite.set("tests", str(len(self.suite)))
        self.suite.set("failures", str(self.failed))
        self.suite.set("errors", "0")
        self.suite.set("skipped", str(sum(case.find("skipped") is not None for case in self.suite)))
        output.parent.mkdir(parents=True, exist_ok=True)
        ET.indent(self.suite)
        ET.ElementTree(self.suite).write(output, encoding="utf-8", xml_declaration=True)


def run_project_checks(root: Path, output: Path) -> int:
    checks = Checks(root)
    checks.run("inventory", [sys.executable, "scripts/render-inventory.py", "--check"])
    checks.run("scenarios", [sys.executable, "scripts/render-scenarios.py", "--check"])
    checks.run("review-adapter", [sys.executable, "-m", "unittest", "discover", "-s", "scripts",
                                  "-p", "test_review_checks.py"])
    packages = checks.run("go-package-discovery", ["go", "list", "./..."])
    go_commands = [("go-build", ["go", "build", "./..."]),
                   ("go-test", ["go", "test", "-timeout=90s", "./..."]),
                   ("go-vet", ["go", "vet", "./..."])]
    for name, command in go_commands:
        if packages is None or packages.returncode:
            checks.skip(name, "Go package discovery failed; see its failing check")
        elif not packages.stdout.strip():
            checks.skip(name, "No Go packages exist in this checkout yet")
        else:
            checks.run(name, command)
    checks.write(output)
    return 1 if checks.failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--junitxml", required=True, type=Path)
    args = parser.parse_args()
    return run_project_checks(Path(__file__).resolve().parents[1], args.junitxml)


if __name__ == "__main__":
    raise SystemExit(main())
