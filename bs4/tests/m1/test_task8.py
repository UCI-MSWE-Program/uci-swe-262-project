"""Unit tests for task8.py (sign a document in place)."""

import sys
import tempfile
import unittest
from pathlib import Path

import bs4

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (INPUT_FILES, copy_input, load_task,  # noqa: E402
                     run_task, run_task_on_path)


class Task8Tests(unittest.TestCase):
    def test_sign_each_input(self):
        for name in INPUT_FILES:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task8.py', name, tmp, 'student')
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    self.assertIn('Signed: Created by student', proc.stdout)
                    self.assertIn('Wrote signed tree back to', proc.stdout)
                    signed = (Path(tmp) / name).read_text(encoding='utf-8')
                    self.assertIn('Created by student', signed)

    def test_sign_then_resign(self):
        with tempfile.TemporaryDirectory() as tmp:
            copied = copy_input('small1.html', tmp)
            first = run_task_on_path('task8.py', copied, 'alice')
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertIn('Signed: Created by alice', first.stdout)
            second = run_task_on_path('task8.py', copied, 'bob')
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn('Signed: Modified by bob', second.stdout)
            content = copied.read_text(encoding='utf-8')
            self.assertIn('Created by alice', content)
            self.assertIn('Modified by bob', content)

    def test_make_comment_and_is_signature(self):
        task8 = load_task('task8')
        comment = task8.make_comment('Created', 'alice', '2026-10-23 08:42 PM')
        self.assertIsInstance(comment, bs4.Comment)
        self.assertIn('Created by alice', str(comment))
        self.assertTrue(task8.is_signature(comment))
        self.assertFalse(task8.is_signature(bs4.Comment('  random note ')))
        self.assertFalse(task8.is_signature(
            bs4.NavigableString('Created by x. At 2026-10-23 08:42 PM')))


if __name__ == '__main__':
    unittest.main()
