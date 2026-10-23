"""Print every hyperlink (<a> tag) found in an HTML/XML file.

Usage: python3 task2.py <input.html|input.xml>

Task 2: list all hyperlinks in the document along with their href target
and visible link text.
"""

import argparse
import typing

import bs4


def main() -> None:
    """Run the hyperlink-listing task from the command line."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='List all hyperlinks.')
    parser.add_argument('input', help='HTML or XML file to parse')
    args: argparse.Namespace = parser.parse_args()

    handle: typing.TextIO
    with open(args.input, encoding='utf-8') as handle:
        markup: str = handle.read()
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(
        markup, 'xml' if args.input.endswith('.xml') else 'lxml')

    links: bs4.ResultSet = soup.find_all('a')
    print(f'Found {len(links)} hyperlink(s):')
    for link in links:
        href: str = link.get('href', '(no href)')
        text: str = link.get_text(strip=True)
        print(f'  <a href="{href}">{text}</a>')


if __name__ == '__main__':
    main()
