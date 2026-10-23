"""Unit tests for task5.py (demonstrate find_parent())."""

import sys
import tempfile
import unittest
from pathlib import Path

import bs4

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (INPUT_FILES, SMALL_INPUTS, build_soup, load_task,  # noqa: E402
                     read_input, run_task)


class Task5Tests(unittest.TestCase):
    def test_find_parent_each_input(self):
        for name in INPUT_FILES:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task5.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    self.assertTrue(
                        'Target tag:' in proc.stdout
                        or 'No <b>, <p>, or <a> tag found' in proc.stdout,
                        proc.stdout)

    def test_find_parent_matches_direct_computation(self):
        task5 = load_task('task5')
        for name in SMALL_INPUTS:
            with self.subTest(input=name):
                soup = build_soup(read_input(name), name)
                target = soup.find('b') or soup.find('p') or soup.find('a')
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task5.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    if target is None:
                        self.assertIn(
                            'No <b>, <p>, or <a> tag found', proc.stdout)
                        continue
                    self.assertIn(f'Target tag: {task5.describe(target)}',
                                  proc.stdout)
                    self.assertIn(
                        f'Text:       {target.get_text(strip=True)[:60]}',
                        proc.stdout)
                    self.assertIn(
                        'Immediate parent (find_parent()): '
                        f'{task5.describe(target.find_parent())}',
                        proc.stdout)
                    section = target.find_parent('section')
                    if section is not None:
                        self.assertIn(
                            'Nearest enclosing <section> '
                            f'(find_parent("section")): '
                            f'{task5.describe(section)}',
                            proc.stdout)
                    else:
                        self.assertIn(
                            'No enclosing <section> found', proc.stdout)
                    ancestor = target.find_parent(id=True)
                    if ancestor is not None:
                        self.assertIn(
                            'Nearest ancestor carrying an id '
                            f'(find_parent(id=True)): '
                            f'{task5.describe(ancestor)}',
                            proc.stdout)

    def test_describe(self):
        task5 = load_task('task5')
        soup = bs4.BeautifulSoup(
            '<div id="x"></div><div class="a b"></div><div></div>', 'lxml')
        divs = soup.find_all('div')
        self.assertEqual(task5.describe(divs[0]), '<div id="x">')
        self.assertEqual(task5.describe(divs[1]), '<div class="a b">')
        self.assertEqual(task5.describe(divs[2]), '<div>')
        self.assertIsNone(task5.describe(None))


if __name__ == '__main__':
    unittest.main()
