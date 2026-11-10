"""Walk every node of an HTML/XML document by iterating the soup object.

Usage: python3 task1.py <input.html|input.xml>

Milestone 4 makes a `BeautifulSoup` object iterable. ``for node in soup``
walks the whole parse tree in document order (a depth-first, pre-order
traversal), yielding one node at a time: the soup object first, then every
Tag, NavigableString, Comment, and Doctype. This script prints each node
as it is yielded and then summarizes the kinds of node visited.
"""

import argparse
import collections
import typing

import bs4


def describe(node: bs4.PageElement) -> str:
    """Render a single line describing a node.

    Args:
        node: Any node of the parse tree (the soup, a Tag, or a string).

    Returns:
        A string of the form '<kind>: <value>'.
    """
    if isinstance(node, bs4.BeautifulSoup):
        kind: str = 'soup'
        value: str = '[document]'
    elif isinstance(node, bs4.Tag):
        kind = 'tag'
        value = f'<{node.name}>'
    else:
        kind = type(node).__name__
        value = repr(str(node))
    return f'{kind}: {value}'


def main() -> None:
    """Run the tree-walk task from the command line."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Walk a document by iterating the soup object.')
    parser.add_argument('input', help='HTML or XML file to parse')
    args: argparse.Namespace = parser.parse_args()

    handle: typing.TextIO
    with open(args.input, encoding='utf-8') as handle:
        markup: str = handle.read()
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(
        markup, 'xml' if args.input.endswith('.xml') else 'lxml')

    counts: collections.Counter[str] = collections.Counter()
    print(f'Iterating over {args.input}:')
    for node in soup:
        counts[type(node).__name__] += 1
        print(describe(node))

    print(f'\nVisited {sum(counts.values())} node(s):')
    for kind, count in sorted(counts.items()):
        print(f'  {kind}: {count}')


if __name__ == '__main__':
    main()
