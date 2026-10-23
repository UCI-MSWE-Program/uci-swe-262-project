"""Demonstrate Tag.find_parent() on an HTML/XML file.

Usage: python3 task5.py <input.html|input.xml>

Task 5: locate a tag of interest, then use find_parent() to inspect its
immediate parent, walk the whole ancestor chain, find the nearest
enclosing <section>, and find the nearest ancestor that carries an id.
"""

import argparse
import typing

import bs4


def describe(tag: bs4.Tag | None) -> str | None:
    """Return a short one-line description of a tag, or None."""
    if tag is None:
        return None
    if tag.get('id'):
        return f'<{tag.name} id="{tag["id"]}">'
    if tag.get('class'):
        return f'<{tag.name} class="{" ".join(tag["class"])}">'
    return f'<{tag.name}>'


def main() -> None:
    """Run the find_parent() demo from the command line."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Demonstrate find_parent().')
    parser.add_argument('input', help='HTML or XML file to parse')
    args: argparse.Namespace = parser.parse_args()

    handle: typing.TextIO
    with open(args.input, encoding='utf-8') as handle:
        markup: str = handle.read()
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(
        markup, 'xml' if args.input.endswith('.xml') else 'lxml')

    target: bs4.Tag | None = (
        soup.find('b') or soup.find('p') or soup.find('a'))
    if target is None:
        print('No <b>, <p>, or <a> tag found in the document.')
        return
    print(f'Target tag: {describe(target)}')
    print(f'Text:       {target.get_text(strip=True)[:60]}')

    immediate: bs4.Tag | None = target.find_parent()
    print(f'\nImmediate parent (find_parent()): {describe(immediate)}')

    print('\nFull ancestor chain (repeated find_parent()):')
    current: bs4.Tag | None = target
    while current is not None:
        print(f'  {describe(current)}')
        current = current.find_parent()

    section: bs4.Tag | None = target.find_parent('section')
    if section is not None:
        print(f'\nNearest enclosing <section> '
              f'(find_parent("section")): {describe(section)}')
        heading: bs4.Tag | None = section.find('h2')
        if heading is not None:
            print(f'Section heading: {heading.get_text(strip=True)}')
    else:
        print('\nNo enclosing <section> found (find_parent("section")).')

    ancestor_with_id: bs4.Tag | None = target.find_parent(id=True)
    if ancestor_with_id is not None:
        print(f'\nNearest ancestor carrying an id '
              f'(find_parent(id=True)): {describe(ancestor_with_id)}')


if __name__ == '__main__':
    main()
