"""Exercise the validation adapter using real successful and failing processes."""
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from review_checks import Checks


class ReportTests(unittest.TestCase):
    def test_subprocess_failures_survive_junit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checks = Checks(root)
            checks.run("good", [sys.executable, "-c", "print('success')"])
            checks.run("bad", [sys.executable, "-c", "import sys; print('failure detail'); sys.exit(7)"])
            checks.skip("not-available", "No package yet")
            report = root / "report.xml"
            checks.write(report)
            suite = ET.parse(report).getroot()
            self.assertEqual(checks.failed, 1)
            self.assertEqual(suite.attrib["tests"], "3")
            self.assertEqual(suite.attrib["failures"], "1")
            self.assertEqual(suite.attrib["skipped"], "1")
            cases = {case.attrib["name"]: case for case in suite}
            self.assertIsNone(cases["good"].find("failure"))
            self.assertEqual(cases["bad"].find("failure").attrib["message"], "exit status 7")
            self.assertIn("failure detail", cases["bad"].find("failure").text)
            self.assertEqual(cases["not-available"].find("skipped").attrib["message"], "No package yet")

    def test_missing_executable_is_a_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checks = Checks(root)
            checks.run("missing", [str(root / "does-not-exist")])
            report = root / "report.xml"
            checks.write(report)
            suite = ET.parse(report).getroot()
            self.assertEqual(checks.failed, 1)
            self.assertEqual(suite.find("testcase/failure").attrib["message"], "FileNotFoundError")


if __name__ == "__main__":
    unittest.main()
