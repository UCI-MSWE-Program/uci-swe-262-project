"""Unit tests for task1.py (prettify a file back to disk)."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (INPUT_FILES, SMALL_INPUTS, build_soup, read_input,  # noqa: E402
                     run_task)


class Task1Tests(unittest.TestCase):
    def test_prettify_each_input(self):
        for name in INPUT_FILES:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task1.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    for expected in ('parser:', 'input:', 'output:', 'time:'):
                        self.assertIn(expected, proc.stdout)
                    stem, suffix = name.rsplit('.', 1)
                    output = Path(tmp) / f'{stem}_pretty.{suffix}'
                    self.assertTrue(output.is_file(), f'{output} not created')
                    self.assertGreater(output.stat().st_size, 0)

    def test_prettify_preserves_structure(self):
        for name in SMALL_INPUTS:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task1.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    expected_parser = 'xml' if name.endswith('.xml') else 'lxml'
                    self.assertIn(f'parser: {expected_parser}', proc.stdout)
                    stem, suffix = name.rsplit('.', 1)
                    output = Path(tmp) / f'{stem}_pretty.{suffix}'
                    before = build_soup(read_input(name), name)
                    after = build_soup(output.read_text(encoding='utf-8'), name)
                    self.assertEqual(
                        [t.name for t in before.find_all()],
                        [t.name for t in after.find_all()])

    def test_prettify_explicit_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'custom_out.xml'
            proc = run_task('task1.py', 'small2.xml', tmp, str(out))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(out.is_file())
            self.assertIn('parser: xml', proc.stdout)
            self.assertIn(f'output: {out}', proc.stdout)


if __name__ == '__main__':
    unittest.main()
