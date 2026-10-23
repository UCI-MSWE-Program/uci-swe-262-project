"""Unit tests for task6.py (rename <b> tags to <blockquote>)."""

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (INPUT_FILES, SMALL_INPUTS, build_soup, read_input,  # noqa: E402
                     run_task)

RENAME_COUNT_RE = re.compile(r'Renamed (\d+) <b> tag\(s\) to <blockquote>\.')


class Task6Tests(unittest.TestCase):
    def test_rename_b_tags_each_input(self):
        for name in INPUT_FILES:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task6.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    self.assertIn('<b> tag(s) to <blockquote>', proc.stdout)
                    self.assertIn('Wrote modified tree to', proc.stdout)
                    stem, suffix = name.rsplit('.', 1)
                    output = Path(tmp) / f'{stem}_task6.{suffix}'
                    self.assertTrue(output.is_file(), f'{output} not created')

    def test_rename_correctness(self):
        for name in SMALL_INPUTS:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task6.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    n_bold = len(build_soup(read_input(name), name).find_all('b'))
                    match = RENAME_COUNT_RE.search(proc.stdout)
                    self.assertIsNotNone(match, proc.stdout)
                    self.assertEqual(int(match.group(1)), n_bold)
                    stem, suffix = name.rsplit('.', 1)
                    output = Path(tmp) / f'{stem}_task6.{suffix}'
                    tree = build_soup(output.read_text(encoding='utf-8'), name)
                    self.assertEqual(len(tree.find_all('blockquote')), n_bold)
                    self.assertEqual(len(tree.find_all('b')), 0)


if __name__ == '__main__':
    unittest.main()
