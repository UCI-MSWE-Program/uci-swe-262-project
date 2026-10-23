"""Shared helpers for the milestone 1 task unit tests."""

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import bs4

ROOT = Path(__file__).resolve().parents[3]
APPS_DIR = ROOT / 'apps' / 'm1'
TESTS_DIR = ROOT / 'bs4' / 'tests'

INPUT_FILES = (
    'small1.html',
    'small2.xml',
    'medium1.html',
    'medium2.xml',
    'large1.html',
    'large2.html',
    'very_large.html',
    'nested.html',
)

SMALL_INPUTS = (
    'small1.html',
    'small2.xml',
    'medium1.html',
    'medium2.xml',
    'nested.html',
)


def copy_input(input_name, dest_dir):
    """Copy a corpus input file into dest_dir and return the new path."""
    destination = Path(dest_dir) / input_name
    shutil.copy2(TESTS_DIR / input_name, destination)
    return destination


def run_task(script, input_name, dest_dir, *extra_args):
    """Run a task script against a copy of an input file in dest_dir."""
    copied = copy_input(input_name, dest_dir)
    command = [sys.executable, str(APPS_DIR / script), str(copied), *extra_args]
    return subprocess.run(command, capture_output=True, text=True)


def run_task_on_path(script, path, *extra_args):
    """Run a task script against an existing file path (no copying)."""
    command = [sys.executable, str(APPS_DIR / script), str(path), *extra_args]
    return subprocess.run(command, capture_output=True, text=True)


def read_input(input_name):
    """Return the contents of a corpus input file as a string."""
    return (TESTS_DIR / input_name).read_text(encoding='utf-8')


def build_soup(markup, input_name):
    """Parse markup with the same parser the task scripts select."""
    parser = 'xml' if input_name.endswith('.xml') else 'lxml'
    return bs4.BeautifulSoup(markup, parser)


def load_task(name):
    """Import a task module from apps/m1 without polluting sys.path."""
    spec = importlib.util.spec_from_file_location(
        name, APPS_DIR / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
