# M4-README — Iterable BeautifulSoup (technical brief)

> Any reference to `bs4` is found in `./bs4/beautifulsoup4` from the root
> of this project. All code changes for this milestone were made in the
> `beautifulsoup4` fork (commit `71ce44a`) and pulled into the submodule.

[TOC]

## Summary

Milestone 4 makes the `BeautifulSoup` object itself iterable. You can now
walk every node of a parsed document with a plain `for` loop:

```python
soup = BeautifulSoup(html_doc, 'html.parser')
for node in soup:
    print(node)
```

`BeautifulSoup` is still the same object returned by the constructor; the
change is a single new dunder method, `BeautifulSoup.__iter__`, that turns
the soup into a Python *iterable*.

## Semantics

Iterating a `BeautifulSoup` object traverses the parse tree **in document
order** — a depth-first, pre-order walk — and yields **one node at a
time** until every node has been visited:

1. the `BeautifulSoup` object itself, then
2. each of its descendants, in the order they appear in the document.

For the markup `<!DOCTYPE html><html><body><p>Hi</p><!-- c --></body></html>`,
the iteration yields, in order:

| # | Node kind | Value |
| --- | --- | --- |
| 0 | `BeautifulSoup` | `[document]` |
| 1 | `Doctype` | `html` |
| 2 | `Tag` | `<html>` |
| 3 | `Tag` | `<body>` |
| 4 | `Tag` | `<p>` |
| 5 | `NavigableString` | `Hi` |
| 6 | `Comment` | ` c ` |

Every kind of object in the tree participates in iteration: the soup root,
`Tag` objects, plain `NavigableString`s, and the special string subclasses
(`Comment`, `Doctype`, `CData`, and so on).

### Laziness

The whole point of the exercise is that iteration must **not** collect the
nodes of the tree onto a list first. `BeautifulSoup.__iter__` is a
generator function: it yields each node on demand, so a document with tens
of millions of nodes can be walked without ever materializing a list of
them.

## API changes

### New API — `BeautifulSoup.__iter__`

| Symbol | Definition | File:Line |
| --- | --- | --- |
| `BeautifulSoup.__iter__` | `def __iter__(self) -> Iterator[PageElement]` | `bs4/__init__.py:506` |

The implementation is small and delegates the descendant walk to the
existing lazy `Tag.descendants` generator:

```python
def __iter__(self) -> Iterator[PageElement]:
    yield self
    yield from self.descendants
```

`yield self` surfaces the soup root, and `yield from self.descendants`
streams the rest of the tree. `Tag.descendants` walks the tree by following
each node's `next_element` pointer (document order), so no recursive calls
and no intermediate list are involved.

### Existing API reused

| Symbol | Definition | File:Line | Role |
| --- | --- | --- | --- |
| `BeautifulSoup` (class) | `class BeautifulSoup(Tag)` | `bs4/__init__.py:135` | the iterable root object |
| `Tag.__iter__` | `def __iter__` | `bs4/element.py:2208` | overridden for `BeautifulSoup` |
| `Tag.descendants` | `@property def descendants` | `bs4/element.py:2764` | lazy document-order walk |
| `Tag.self_and_descendants` | `@property def self_and_descendants` | `bs4/element.py:2757` | not used; skips the hidden root |

### Why `self_and_descendants` was not reused

`PageElement._self_and` (used by `self_and_descendants`) skips a node whose
`hidden` flag is set, and the `BeautifulSoup` root is `hidden = True`. The
root is a real node of the tree, so `__iter__` yields it explicitly rather
than going through the hidden-aware helper.

## Application task

`apps/m4/task1.py` demonstrates the new API. It parses a file, iterates the
soup directly with `for node in soup`, prints a one-line description of
each node as it is yielded, and ends with a count summary by node kind:

```shell
python3 apps/m4/task1.py bs4/tests/small1.html
python3 apps/m4/task1.py bs4/tests/small2.xml
```

The `.xml` inputs select the XML parser; otherwise the `lxml` parser is
used, matching the Milestone 2/3 scripts.

## Tests

`bs4/tests/m4/test_iteration.py` contains five unit tests covering
iteration of the various kinds of objects in a parse tree:

| Test | What it checks |
| --- | --- |
| `test_iteration_yields_the_soup_object_first` | the soup itself is node #0 |
| `test_iteration_visits_every_node_in_document_order` | `list(soup) == [soup] + list(soup.descendants)` |
| `test_iteration_includes_tag_and_string_objects` | `Tag` and `NavigableString` nodes, in order |
| `test_iteration_includes_comments_and_doctypes` | `Comment` and `Doctype` nodes |
| `test_iteration_is_lazy` | iteration returns a generator, not a list |

```shell
python3 bs4/tests/m4/test_iteration.py
```

## See also

* [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
