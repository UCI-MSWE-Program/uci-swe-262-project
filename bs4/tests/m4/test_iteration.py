"""Unit tests for iterating directly over a BeautifulSoup object.

Milestone 4 makes the `BeautifulSoup` object itself iterable. Iterating a
soup traverses the entire parse tree in document order (a depth-first,
pre-order walk) and yields one node at a time -- the soup object first,
then every Tag, NavigableString, Comment, Doctype, and so on.

These tests verify that iteration works for the various kinds of objects
that make up a parse tree, and that the tree is streamed lazily rather
than collected onto a list first.
"""

import types
import unittest

import bs4


class SoupIterationTests(unittest.TestCase):
    """Tests for `for node in soup:` style iteration."""

    # A small document that exercises several node kinds at once: a
    # doctype, nested tags, plain text strings, and a comment.
    HTML = (
        '<!DOCTYPE html>'
        '<html><head><title>Title</title></head>'
        '<body><p>Hello <b>world</b>!</p><!-- note --></body></html>'
    )

    def _soup(self) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(self.HTML, 'html.parser')

    def test_iteration_yields_the_soup_object_first(self) -> None:
        """The first node yielded is the soup object itself."""
        soup = self._soup()
        iterator = iter(soup)
        self.assertIs(next(iterator), soup)

    def test_iteration_visits_every_node_in_document_order(self) -> None:
        """Iteration yields the soup followed by all of its descendants,
        in the same order as `soup.descendants`."""
        soup = self._soup()
        nodes = list(soup)
        self.assertEqual(nodes, [soup] + list(soup.descendants))

    def test_iteration_includes_tag_and_string_objects(self) -> None:
        """Iteration reaches every Tag and every plain-text string."""
        soup = self._soup()
        nodes = list(soup)

        tags = [n for n in nodes if isinstance(n, bs4.Tag) and n is not soup]
        self.assertEqual(
            [t.name for t in tags], [t.name for t in soup.find_all()])

        strings = [str(n) for n in nodes if type(n) is bs4.NavigableString]
        self.assertEqual(strings, ['Title', 'Hello ', 'world', '!'])

    def test_iteration_includes_comments_and_doctypes(self) -> None:
        """Iteration surfaces special string kinds: Comment and Doctype."""
        soup = self._soup()
        nodes = list(soup)

        comments = [n for n in nodes if isinstance(n, bs4.Comment)]
        self.assertEqual([str(c) for c in comments], [' note '])

        doctypes = [n for n in nodes if isinstance(n, bs4.Doctype)]
        self.assertEqual([str(d) for d in doctypes], ['html'])

    def test_iteration_is_lazy(self) -> None:
        """Iteration streams nodes without building a list up front."""
        soup = self._soup()
        iterator = iter(soup)
        self.assertIsInstance(iterator, types.GeneratorType)

        # Pulling nodes one at a time walks the tree without ever
        # materializing the whole thing.
        self.assertIs(next(iterator), soup)
        self.assertIsInstance(next(iterator), bs4.Doctype)
        self.assertEqual(next(iterator).name, 'html')


if __name__ == '__main__':
    unittest.main()
