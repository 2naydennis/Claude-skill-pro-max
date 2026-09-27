"""Known-answer tests for ultikit. Run: python3 -m unittest discover tests"""
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "skills" / "ultimate" / "scripts" / "ultikit.py"
FIX = HERE / "fixtures"


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=check)


def total(out: str) -> int:
    return int(re.search(r"total\s+(\d+)/50", out).group(1))


class Slop(unittest.TestCase):
    def test_sloppy_text_flags_patterns(self):
        out = run("slop", str(FIX / "sloppy.md")).stdout
        for flag in ("em dash", "AI word 'landscape'", "filler / chatbot residue", "serves as / stands as",
                     "shallow -ing tail", "not X but Y", "passive voice?", "bold used as decoration"):
            self.assertIn(flag, out)
        self.assertLess(total(out), 35)
        self.assertIn("revise", out)

    def test_clean_text_scores_well(self):
        out = run("slop", str(FIX / "clean.md")).stdout
        self.assertGreaterEqual(total(out), 35)
        self.assertNotIn("em dash", out)
        self.assertNotIn("AI word", out)

    def test_code_blocks_ignored(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("Run this:\n\n```\n# leverage the robust — seamless API\n```\n")
        out = run("slop", f.name).stdout
        self.assertNotIn("AI word", out)
        self.assertNotIn("em dash", out)

    def test_missing_file(self):
        r = run("slop", "does-not-exist.md", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no such file", r.stderr)


class Design(unittest.TestCase):
    def test_generic_page_flags_defaults(self):
        out = run("design", str(FIX / "generic.html")).stdout
        for flag in ("Inter as the only typeface", "AI purple/indigo gradient", "generic soft card shadow",
                     "tracked all-caps eyebrow", "arrow glued to link/button text", "tinted near-black"):
            self.assertIn(flag, out)
        self.assertIn("[ ] visible keyboard focus", out)
        self.assertIn("[ ] viewport meta", out)

    def test_careful_page_passes_floor(self):
        out = run("design", str(FIX / "careful.html")).stdout
        self.assertIn("0 default(s), 0 floor item(s) missing", out)
        self.assertIn("hover, focus-visible, active, disabled", out)


class Plan(unittest.TestCase):
    def test_creates_files_with_goal(self):
        with tempfile.TemporaryDirectory() as d:
            out = run("plan", d, "--goal", "Ship CSV export").stdout
            self.assertEqual(out.count("created"), 3)
            plan = (Path(d) / "task_plan.md").read_text()
            self.assertIn("Ship CSV export", plan)
            self.assertNotIn("{{", plan)

    def test_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "progress.md").write_text("mine")
            out = run("plan", d).stdout
            self.assertIn("kept", out)
            self.assertEqual((Path(d) / "progress.md").read_text(), "mine")
            run("plan", d, "--force")
            self.assertNotEqual((Path(d) / "progress.md").read_text(), "mine")


if __name__ == "__main__":
    unittest.main()
