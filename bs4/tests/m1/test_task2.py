"""Unit tests for task2.py (list every hyperlink)."""

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (INPUT_FILES, SMALL_INPUTS, build_soup, read_input,  # noqa: E402
                     run_task, run_task_on_path)

LINK_COUNT_RE = re.compile(r'Found (\d+) hyperlink\(s\):')


class Task2Tests(unittest.TestCase):
    def test_list_links_each_input(self):
        for name in INPUT_FILES:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task2.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    self.assertIn('hyperlink(s):', proc.stdout)

    def test_link_counts_and_targets(self):
        for name in SMALL_INPUTS:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task2.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    links = build_soup(read_input(name), name).find_all('a')
                    match = LINK_COUNT_RE.search(proc.stdout)
                    self.assertIsNotNone(match, proc.stdout)
                    self.assertEqual(int(match.group(1)), len(links))
                    for link in links:
                        href = link.get('href', '(no href)')
                        self.assertIn(f'<a href="{href}">', proc.stdout)

    def test_link_without_href(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / 'nohref.html'
            f.write_text('<html><body><a>plain</a></body></html>',
                         encoding='utf-8')
            proc = run_task_on_path('task2.py', f)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn('Found 1 hyperlink(s):', proc.stdout)
            self.assertIn('<a href="(no href)">plain</a>', proc.stdout)


if __name__ == '__main__':
    unittest.main()
