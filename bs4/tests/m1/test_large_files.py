"""Timing and peak-memory tests for the five largest corpus inputs.

Each test runs ``task1.py`` (parse + prettify + write) against one large
input file under a 50 GiB address-space limit and reports the wall-clock
time and peak resident-set size (RSS) of the run.

These tests are intentionally slow (minutes for the largest files) and
generate multi-gigabyte prettified outputs in a temporary directory, so
they are kept in their own module. Run them explicitly, e.g.::

    python -m unittest bs4.tests.m1.test_large_files
"""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import APPS_DIR, TESTS_DIR  # noqa: E402

MEM_LIMIT_GIB = 50
MEM_LIMIT_BYTES = MEM_LIMIT_GIB * 1024 ** 3

# Wrapper that sets the address-space limit, runs the task in a child
# process, and reports the wall-clock time and peak RSS of that child.
_WRAPPER = r'''
import resource
import subprocess
import sys
import time

task, input_path, output_path = sys.argv[1:4]
limit = int(sys.argv[4])
resource.setrlimit(resource.RLIMIT_AS, (limit, limit))

start = time.perf_counter()
proc = subprocess.run([sys.executable, task, input_path, output_path])
elapsed = time.perf_counter() - start
peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
print(f'ELAPSED_SECONDS={elapsed:.3f}')
print(f'PEAK_RSS_KIB={peak}')
sys.exit(proc.returncode)
'''

_ELAPSED_RE = re.compile(r'ELAPSED_SECONDS=([0-9.]+)')
_PEAK_RE = re.compile(r'PEAK_RSS_KIB=(\d+)')


def _run_prettify(input_name):
    """Run task1.py on input_name under the memory limit.

    Returns a (returncode, elapsed_seconds, peak_rss_kib, stderr) tuple.
    The task writes its prettified output into a temporary directory so the
    corpus directory is never modified.
    """
    input_path = TESTS_DIR / input_name
    with tempfile.TemporaryDirectory() as tmp:
        output_path = Path(tmp) / 'pretty.out'
        proc = subprocess.run(
            [sys.executable, '-c', _WRAPPER,
             str(APPS_DIR / 'task1.py'), str(input_path), str(output_path),
             str(MEM_LIMIT_BYTES)],
            capture_output=True, text=True)
    elapsed = _ELAPSED_RE.search(proc.stdout)
    peak = _PEAK_RE.search(proc.stdout)
    seconds = float(elapsed.group(1)) if elapsed else None
    peak_kib = int(peak.group(1)) if peak else None
    return proc.returncode, seconds, peak_kib, proc.stderr


class LargeFileTests(unittest.TestCase):
    def _run_and_report(self, name):
        returncode, seconds, peak_kib, stderr = _run_prettify(name)
        if seconds is not None and peak_kib is not None:
            print(f'{name}: {seconds:.2f}s, '
                  f'peak RSS {peak_kib / 1024 ** 2:.2f} GiB')
        else:
            print(f'{name}: did not complete')
        self.assertIsNotNone(seconds, 'missing ELAPSED_SECONDS in output')
        self.assertIsNotNone(peak_kib, 'missing PEAK_RSS_KIB in output')
        self.assertEqual(
            returncode, 0,
            f'task1.py exceeded the {MEM_LIMIT_GIB} GiB memory limit '
            f'or crashed:\n{stderr}')

    def test_large1_html(self):
        self._run_and_report('large1.html')

    def test_large2_html(self):
        self._run_and_report('large2.html')

    def test_very_large_html(self):
        self._run_and_report('very_large.html')

    def test_giga_html(self):
        self._run_and_report('giga.html')

    def test_enwiki_xml(self):
        self._run_and_report('enwiki-20151002-pages-meta-current23.xml')


if __name__ == '__main__':
    unittest.main()
