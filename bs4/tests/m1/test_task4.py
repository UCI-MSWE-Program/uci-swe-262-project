"""Unit tests for task4.py (list tags that carry an id)."""

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (INPUT_FILES, SMALL_INPUTS, build_soup, read_input,  # noqa: E402
                     run_task)

ID_COUNT_RE = re.compile(r'Found (\d+) tag\(s\) with an id attribute:')


class Task4Tests(unittest.TestCase):
    def test_list_id_tags_each_input(self):
        for name in INPUT_FILES:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task4.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    self.assertIn('tag(s) with an id attribute:', proc.stdout)

    def test_id_count_and_values(self):
        for name in SMALL_INPUTS:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task4.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    tags = build_soup(read_input(name), name).find_all(id=True)
                    match = ID_COUNT_RE.search(proc.stdout)
                    self.assertIsNotNone(match, proc.stdout)
                    self.assertEqual(int(match.group(1)), len(tags))
                    for tag in tags:
                        self.assertIn(f'id="{tag["id"]}"', proc.stdout)


if __name__ == '__main__':
    unittest.main()
