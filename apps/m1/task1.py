"""Read an HTML/XML file into a tree and write it back, prettified.

Usage: python3 task1.py <input.html|input.xml> [output]

Task 1: parse a file given on the command line into a BeautifulSoup tree,
then write the tree back to disk as a prettified file using
soup.prettify().
"""

import argparse
import os
import time
import typing

import bs4


def make_soup(markup: str, path: str) -> tuple[bs4.BeautifulSoup, str]:
    """Build a BeautifulSoup tree with the best available parser.

    Args:
        markup: The file contents as a string.
        path: The input file path, used to detect XML documents.

    Returns:
        A tuple of (soup, parser_name).
    """
    if path.endswith('.xml'):
        return bs4.BeautifulSoup(markup, 'xml'), 'xml'
    try:
        return bs4.BeautifulSoup(markup, 'lxml'), 'lxml'
    except bs4.FeatureNotFound:
        return bs4.BeautifulSoup(markup, 'html.parser'), 'html.parser'


def main() -> None:
    """Run the prettify task from the command line."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Prettify an HTML/XML file.')
    parser.add_argument('input', help='HTML or XML file to parse')
    parser.add_argument('output', nargs='?', help='Pretty output file path')
    args: argparse.Namespace = parser.parse_args()

    start: float = time.perf_counter()
    input_handle: typing.TextIO
    with open(args.input, encoding='utf-8') as input_handle:
        markup: str = input_handle.read()
    soup: bs4.BeautifulSoup
    parser_name: str
    soup, parser_name = make_soup(markup, args.input)
    parse_seconds: float = time.perf_counter() - start
    pretty: str = soup.prettify()

    output_path: str
    if args.output is None:
        stem: str
        extension: str
        stem, extension = os.path.splitext(args.input)
        output_path = f'{stem}_pretty{extension}'
    else:
        output_path = args.output
    output_handle: typing.TextIO
    with open(output_path, 'w', encoding='utf-8') as output_handle:
        output_handle.write(pretty)

    print(f'parser: {parser_name}')
    print(f'input:  {args.input} ({os.path.getsize(args.input):,} bytes)')
    print(f'output: {output_path} ({os.path.getsize(output_path):,} bytes)')
    print(f'time:   parse {parse_seconds:.2f} s, prettify+write '
          f'{time.perf_counter() - start - parse_seconds:.2f} s, total '
          f'{time.perf_counter() - start:.2f} s')


if __name__ == '__main__':
    main()
