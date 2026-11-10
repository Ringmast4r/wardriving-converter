"""Batch-scan tests for the Universal Wardriving File Converter."""

import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "universal_wardrive_converter.py"

WIGLE_ROW = "AA:BB:CC:DD:EE:FF,HomeNet,6\n"


def run_cli(*args, cwd):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


class RecursiveSkipTestCase(unittest.TestCase):
    def test_recursive_scan_includes_converted_prefixed_sibling(self):
        # A sibling folder whose name merely starts with "converted" (e.g.
        # "converted_backup") must still be scanned. Only the real output
        # folder ("converted") may be skipped.
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            sibling = base / "converted_backup"
            sibling.mkdir()
            (sibling / "hit.csv").write_text("BSSID,SSID,Channel\n" + WIGLE_ROW)
            result = run_cli("--folder", str(base), "--recursive", cwd=str(base))
            self.assertEqual(result.returncode, 0)
            converted = list((base / "converted").glob("*_converted.csv"))
            self.assertEqual(len(converted), 1)


if __name__ == "__main__":
    unittest.main()
