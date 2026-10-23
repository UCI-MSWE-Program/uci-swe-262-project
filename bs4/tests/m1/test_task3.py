"""Unit tests for task3.py (list all tags and summarize)."""

import collections
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (INPUT_FILES, SMALL_INPUTS, build_soup, read_input,  # noqa: E402
                     run_task)

TAG_COUNT_RE = re.compile(r'Found (\d+) tag\(s\) in document order:')


def parse_tag_order(stdout):
    lines = stdout.splitlines()
    start = None
    for i, line in enumerate(lines):
        if 'tag(s) in document order:' in line:
            start = i + 1
            break
    names = []
    for line in lines[start:]:
        if line.strip() == '' or line == 'Summary:':
            break
        names.append(line.strip())
    return names


def parse_summary(stdout):
    lines = stdout.splitlines()
    idx = lines.index('Summary:')
    summary = {}
    for line in lines[idx + 1:]:
        match = re.match(r'  (\S+): (\d+)$', line)
        if not match:
            continue
        summary[match.group(1)] = int(match.group(2))
    return summary


class Task3Tests(unittest.TestCase):
    def test_list_tags_each_input(self):
        for name in INPUT_FILES:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task3.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    self.assertIn('tag(s) in document order:', proc.stdout)
                    self.assertIn('Summary:', proc.stdout)

    def test_tag_order_and_summary(self):
        for name in SMALL_INPUTS:
            with self.subTest(input=name):
                with tempfile.TemporaryDirectory() as tmp:
                    proc = run_task('task3.py', name, tmp)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    tags = build_soup(read_input(name), name).find_all()
                    match = TAG_COUNT_RE.search(proc.stdout)
                    self.assertIsNotNone(match, proc.stdout)
                    self.assertEqual(int(match.group(1)), len(tags))
                    self.assertEqual(
                        parse_tag_order(proc.stdout), [t.name for t in tags])
                    self.assertEqual(
                        parse_summary(proc.stdout),
                        dict(collections.Counter(t.name for t in tags)))


if __name__ == '__main__':
    unittest.main()
