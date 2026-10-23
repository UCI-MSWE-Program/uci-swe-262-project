"""Unit tests for task3.py (list all tags and summarize) on the largest inputs."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import run_task  # noqa: E402


class Task3Tests(unittest.TestCase):
    def _run_and_report(self, name):
        returncode, seconds, peak_kib, stderr = run_task('task3.py', name)
        if seconds is not None and peak_kib is not None:
            print(f'{name}: {seconds:.2f}s, '
                  f'peak RSS {peak_kib / 1024 ** 2:.2f} GiB')
        else:
            print(f'{name}: did not complete')
        self.assertIsNotNone(seconds, 'missing ELAPSED_SECONDS in output')
        self.assertIsNotNone(peak_kib, 'missing PEAK_RSS_KIB in output')
        self.assertEqual(
            returncode, 0,
            f'task3.py failed on {name} (memory limit or crash):\n{stderr}')

    def test_giga_html(self):
        self._run_and_report('giga.html')

    def test_medium1_html(self):
        self._run_and_report('medium1.html')

if __name__ == '__main__':
    unittest.main()
