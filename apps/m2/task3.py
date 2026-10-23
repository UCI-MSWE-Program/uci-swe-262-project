"""Print every tag that appears in an HTML/XML document.

Usage: python3 task3.py <input.html|input.xml>

Task 3: soup.find_all() with no arguments returns every Tag object in the
document, in document order. Each tag name is printed, followed by a
summary of how often every tag name occurs.
"""

import argparse
import collections
import typing

import bs4


def main() -> None:
    """Run the all-tags-listing task from the command line."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='List all tags.')
    parser.add_argument('input', help='HTML or XML file to parse')
    args: argparse.Namespace = parser.parse_args()

    handle: typing.TextIO
    with open(args.input, encoding='utf-8') as handle:
        soup: bs4.BeautifulSoup = bs4.BeautifulSoup(
            handle.read(), 'xml' if args.input.endswith('.xml') else 'lxml',
            parse_only=bs4.SoupStrainer(True))

    tags: bs4.ResultSet = soup.find_all()
    print(f'Found {len(tags)} tag(s) in document order:')
    for tag in tags:
        print(tag.name)

    counts: collections.Counter[str] = collections.Counter(
        tag.name for tag in tags)
    print('\nSummary:')
    for name, count in sorted(counts.items()):
        print(f'  {name}: {count}')


if __name__ == '__main__':
    main()
