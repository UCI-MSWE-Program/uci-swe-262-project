"""Print every tag that carries an id attribute, using one API call.

Usage: python3 task4.py <input.html|input.xml>

Task 4: soup.find_all(id=True) matches every tag that has an id
attribute in a single search call.
"""

import argparse
import typing

import bs4


def main() -> None:
    """Run the id-tag-listing task from the command line."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='List tags with an id.')
    parser.add_argument('input', help='HTML or XML file to parse')
    args: argparse.Namespace = parser.parse_args()

    handle: typing.TextIO
    with open(args.input, encoding='utf-8') as handle:
        soup: bs4.BeautifulSoup = bs4.BeautifulSoup(
            handle.read(), 'xml' if args.input.endswith('.xml') else 'lxml',
            parse_only=bs4.SoupStrainer(id=True))

    tags: bs4.ResultSet = soup.find_all(id=True)
    print(f'Found {len(tags)} tag(s) with an id attribute:')
    for tag in tags:
        print(f'  <{tag.name} id="{tag["id"]}">')


if __name__ == '__main__':
    main()
