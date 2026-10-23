"""Sign an HTML/XML document with a "Created by" / "Modified by" comment.

Usage: python3 task8.py <input.html|input.xml> signed_by

Task 8: exercise the comment/declaration handling and in-place tree-editing
API. If the document has not been signed before, a comment "Created by
<signed_by>. At <timestamp>" is inserted right after the XML declaration
(XML) or the DOCTYPE (HTML), or at the very top of the file when neither is
present. If the document already carries signature comments, a comment
"Modified by <signed_by>. At <timestamp>" is added on the line after the
most recent signature. The signed tree is written back to the input file.
"""

import argparse
import re
import typing
from datetime import datetime

import bs4

SIGNATURE_RE: re.Pattern[str] = re.compile(
    r'^(?:Created|Modified) by .+\. At \d{4}-\d{2}-\d{2} \d{2}:\d{2} '
    r'(?:AM|PM)$')


def is_signature(node: bs4.NavigableString) -> bool:
    """True when a comment node looks like an earlier signing comment."""
    return isinstance(node, bs4.Comment) and bool(
        SIGNATURE_RE.match(str(node).strip()))


def make_comment(verb: str, signed_by: str, timestamp: str) -> bs4.Comment:
    """Build the signature comment for this signing."""
    return bs4.Comment(f' {verb} by {signed_by}. At {timestamp} ')


def ensure_newline_after(node: bs4.NavigableString) -> None:
    """Make sure a line break follows the node on its parent.

    The XML parser strips whitespace-only text between top-level comment
    nodes, so every existing signature needs its line break restored
    before another signature is appended.
    """
    parent: bs4.Tag = node.parent
    index: int = parent.contents.index(node) + 1
    if index >= len(parent.contents) or parent.contents[index] != '\n':
        parent.insert(index, '\n')


def sign_again(comment: bs4.Comment,
               existing: list[bs4.NavigableString]) -> None:
    """Append a signature comment after the most recent one."""
    for node in existing:
        ensure_newline_after(node)
    anchor: bs4.NavigableString = existing[-1]
    parent: bs4.Tag = anchor.parent
    index: int = parent.contents.index(anchor) + 2
    parent.insert(index, comment)
    parent.insert(index + 1, '\n')


def sign_first(soup: bs4.BeautifulSoup, comment: bs4.Comment,
               is_xml: bool) -> None:
    """Place the very first signature at the top of the document.

    For HTML the comment goes on the line after the DOCTYPE, which the
    serializer already ends with a newline. For XML the comment goes on
    the second line, because the serializer emits the XML declaration
    followed by a newline ahead of the first content node.
    """
    anchor: bs4.NavigableString | None
    if is_xml:
        anchor = None
    else:
        anchor = soup.find(
            string=lambda node: isinstance(node, bs4.Doctype))
    if anchor is not None:
        parent: bs4.Tag = anchor.parent
        index: int = parent.contents.index(anchor) + 1
        parent.insert(index, comment)
        parent.insert(index + 1, '\n')
    else:
        soup.insert(0, comment)
        soup.insert(1, '\n')


def main() -> None:
    """Run the document-signing task from the command line."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Sign an HTML/XML document with a comment.')
    parser.add_argument('input', help='HTML or XML file to sign')
    parser.add_argument('signed_by', help='Name to record in the signature')
    args: argparse.Namespace = parser.parse_args()

    handle: typing.TextIO
    with open(args.input, encoding='utf-8') as handle:
        markup: str = handle.read()
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(
        markup, 'xml' if args.input.endswith('.xml') else 'lxml')

    existing: list[bs4.NavigableString] = [
        node for node in soup.find_all(string=is_signature)]
    verb: str = 'Modified' if existing else 'Created'
    timestamp: str = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    comment: bs4.Comment = make_comment(verb, args.signed_by, timestamp)

    if existing:
        sign_again(comment, existing)
    else:
        sign_first(soup, comment, args.input.endswith('.xml'))

    output_handle: typing.TextIO
    with open(args.input, 'w', encoding='utf-8') as output_handle:
        output_handle.write(str(soup))

    print(f'Signed: {verb} by {args.signed_by}. At {timestamp}')
    print(f'Wrote signed tree back to {args.input}')


if __name__ == '__main__':
    main()
