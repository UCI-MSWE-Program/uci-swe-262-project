"""Unit tests for task7.py (add a class to every <p> tag)."""

import sys
import tempfile
import unittest
from pathlib import Path

import bs4

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (INPUT_FILES, SMALL_INPUTS, build_soup, load_task,  # noqa: E402
                     read_input, run_task)


def classes_of(tag):
    value = tag.get('class')
    if value is None:
        return []
    return value if isinstance(value, list) else value.split()


class Task7Tests(unittest.TestCase):
    def test_add_class_each_input(self):
        for name in INPUT_FILES:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task7.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    self.assertIn('<p> tag(s)', proc.stdout)
                    self.assertIn('Wrote modified tree to', proc.stdout)
                    stem, suffix = name.rsplit('.', 1)
                    output = Path(tmp) / f'{stem}_task7.{suffix}'
                    self.assertTrue(output.is_file(), f'{output} not created')

    def test_default_add_preserves_existing_classes(self):
        for name in SMALL_INPUTS:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task7.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    before = build_soup(read_input(name), name)
                    stem, suffix = name.rsplit('.', 1)
                    output = Path(tmp) / f'{stem}_task7.{suffix}'
                    after = build_soup(output.read_text(encoding='utf-8'),
                                       name)
                    for new_p, old_p in zip(after.find_all('p'),
                                            before.find_all('p')):
                        expected = list(classes_of(old_p)) + ['test']
                        self.assertEqual(classes_of(new_p), expected)

    def test_add_and_remove(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = run_task('task7.py', 'small1.html', tmp, 'money')
            self.assertEqual(proc.returncode, 0, proc.stderr)
            output = Path(tmp) / 'small1_task7.html'
            tree = build_soup(output.read_text(encoding='utf-8'),
                              'small1.html')
            self.assertEqual([classes_of(p) for p in tree.find_all('p')],
                             [['money'], ['footer-note', 'money']])

    def test_remove_class(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = run_task('task7.py', 'small1.html', tmp, 'money',
                            'footer-note')
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn('Removed class "footer-note"', proc.stdout)
            output = Path(tmp) / 'small1_task7.html'
            tree = build_soup(output.read_text(encoding='utf-8'),
                              'small1.html')
            self.assertEqual([classes_of(p) for p in tree.find_all('p')],
                             [['money'], ['money']])

    def test_clear_all_classes(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = run_task('task7.py', 'small1.html', tmp, 'world', '*')
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn('Cleared all existing classes', proc.stdout)
            output = Path(tmp) / 'small1_task7.html'
            tree = build_soup(output.read_text(encoding='utf-8'),
                              'small1.html')
            self.assertEqual([classes_of(p) for p in tree.find_all('p')],
                             [['world'], ['world']])

    def test_explicit_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'custom_out.html'
            proc = run_task('task7.py', 'small1.html', tmp, 'money',
                            '-o', str(out))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(out.is_file())
            self.assertIn(f'Wrote modified tree to {out}', proc.stdout)

    def test_update_paragraph_classes(self):
        task7 = load_task('task7')
        soup = bs4.BeautifulSoup(
            '<p class="liquid">a</p>'
            '<p class="liquid money">b</p>'
            '<p>c</p>', 'lxml')
        ps = soup.find_all('p')
        task7.update_paragraph_classes(ps[0], 'test', None)
        self.assertEqual(classes_of(ps[0]), ['liquid', 'test'])
        task7.update_paragraph_classes(ps[1], 'money', 'liquid')
        self.assertEqual(classes_of(ps[1]), ['money'])
        task7.update_paragraph_classes(ps[2], 'test', None)
        self.assertEqual(classes_of(ps[2]), ['test'])
        task7.update_paragraph_classes(ps[1], 'world', '*')
        self.assertEqual(classes_of(ps[1]), ['world'])


def read_input_from(dest_dir, name):
    return (Path(dest_dir) / name).read_text(encoding='utf-8')


if __name__ == '__main__':
    unittest.main()
