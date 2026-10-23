# M2-README

> Any reference to `bs4` is found in `./bs4/beautifulsoup4` from the root
of this project.

A map of every Beautiful Soup API element used in Milestone 1 (tasks 1-8)
and in Part 1 of Milestone 2 (the `SoupStrainer` re-writes of `task2.py`,
`task3.py`, and `task4.py`) to its definition in the *original* Beautiful
Soup source vendored under `bs4`. Version: **4.13.0**.

All file names and line numbers refer to the original source code, *before*
any of the Milestone 2 changes were made (commit `6853b93` in the
`bs4` repository).

[TOC]

## Verification

Part 1 of Milestone 2: each `apps/m2/` script passes a
`parse_only=SoupStrainer(...)` argument to the `BeautifulSoup` constructor
instead of parsing the whole document:

| Script | Strainer | What it parses |
| --- | --- | --- |
| `task2.py` | `bs4.SoupStrainer('a')` | only `<a>` tags |
| `task3.py` | `bs4.SoupStrainer(True)` | every tag |
| `task4.py` | `bs4.SoupStrainer(id=True)` | only tags with an `id` |

*Aside from this change, all other code references BeautifulSoup 
in the same way as the m1 implementations.*

`task2.py` and `task4.py` parse a strict subset of the document.
`task3.py` must see every tag, so `SoupStrainer(True)` matches all tags
while still skipping non-tag strings.

The `parse_only` keyword is accepted by `BeautifulSoup.__init__`
(`bs4/__init__.py:214`).

Output of each `apps/m2/` script matches the corresponding un-strained
`apps/m1/` script on `small1.html`, `small2.xml`, `medium1.html`,
`medium2.xml`, and `nested.html`.

## Original source location

The relevant files are:

* `bs4/__init__.py` — `BeautifulSoup`
* `bs4/element.py` — `PageElement`, `NavigableString`,
  `Comment`, `Doctype`, `Tag`, `ResultSet`
* `bs4/filter.py` — `ElementFilter`, `SoupStrainer`
* `bs4/exceptions.py` — `FeatureNotFound`
* `bs4/builder/__init__.py` — `TreeBuilder`

## API reference

| Symbol | Definition | File:Line |
| --- | --- | --- |
| `BeautifulSoup` (class) | `class BeautifulSoup(Tag)` | `bs4/__init__.py:133` |
| `BeautifulSoup.__init__` | `def __init__` | `bs4/__init__.py:209` |
| `FeatureNotFound` (class) | `class FeatureNotFound(ValueError)` | `bs4/exceptions.py:10` |
| `ElementFilter` (class) | `class ElementFilter(object)` | `bs4/filter.py:43` |
| `SoupStrainer` (class) | `class SoupStrainer(ElementFilter)` | `bs4/filter.py:313` |
| `SoupStrainer.__init__` | `def __init__` | `bs4/filter.py:345` |
| `PageElement` (class) | `class PageElement(object)` | `bs4/element.py:346` |
| `PageElement.parent` (attribute) | `self.parent = parent` (in `PageElement.setup`) | `bs4/element.py:401` |
| `PageElement.get_text` | `def get_text` | `bs4/element.py:524` |
| `PageElement.find_parent` | `def find_parent` | `bs4/element.py:992` |
| `NavigableString` (class) | `class NavigableString(str, PageElement)` | `bs4/element.py:1274` |
| `Comment` (class) | `class Comment(PreformattedString)` | `bs4/element.py:1472` |
| `Doctype` (class) | `class Doctype(PreformattedString)` | `bs4/element.py:1486` |
| `Tag` (class) | `class Tag(PageElement)` | `bs4/element.py:1569` |
| `Tag.__init__` | `def __init__` | `bs4/element.py:1618` |
| `Tag.name` (attribute) | `self.name = name` (in `Tag.__init__`) | `bs4/element.py:1648` |
| `Tag.contents` (attribute) | `self.contents: List[PageElement] = []` (in `Tag.__init__`) | `bs4/element.py:1697` |
| `Tag.insert` | `def insert` | `bs4/element.py:1916` |
| `Tag.get` | `def get` | `bs4/element.py:2160` |
| `Tag.__getitem__` | `def __getitem__` | `bs4/element.py:2203` |
| `Tag.__setitem__` | `def __setitem__` | `bs4/element.py:2223` |
| `Tag.prettify` | `def prettify` | `bs4/element.py:2601` |
| `Tag.find` | `def find` | `bs4/element.py:2684` |
| `Tag.find_all` | `def find_all` | `bs4/element.py:2715` |
| `ResultSet` (class) | `class ResultSet(...)` | `bs4/element.py:2861` |

## Per-script breakdown

### Milestone 1 — task1.py

| Usage | Definition | File:Line |
| --- | --- | --- |
| `bs4.BeautifulSoup(markup, 'xml'\|'lxml'\|'html.parser')` | `BeautifulSoup.__init__` | `bs4/__init__.py:209` |
| `bs4.FeatureNotFound` (except clause) | `class FeatureNotFound` | `bs4/exceptions.py:10` |
| `soup.prettify()` | `Tag.prettify` (inherited by `BeautifulSoup`) | `bs4/element.py:2601` |

### Milestone 1 — task2.py

| Usage | Definition | File:Line |
| --- | --- | --- |
| `bs4.BeautifulSoup(markup, ...)` | `BeautifulSoup.__init__` | `bs4/__init__.py:209` |
| `bs4.ResultSet` (type annotation) | `class ResultSet` | `bs4/element.py:2861` |
| `soup.find_all('a')` | `Tag.find_all` | `bs4/element.py:2715` |
| `link.get('href', '(no href)')` | `Tag.get` | `bs4/element.py:2160` |
| `link.get_text(strip=True)` | `PageElement.get_text` | `bs4/element.py:524` |

### Milestone 1 — task3.py

| Usage | Definition | File:Line |
| --- | --- | --- |
| `bs4.BeautifulSoup(markup, ...)` | `BeautifulSoup.__init__` | `bs4/__init__.py:209` |
| `bs4.ResultSet` (type annotation) | `class ResultSet` | `bs4/element.py:2861` |
| `soup.find_all()` | `Tag.find_all` | `bs4/element.py:2715` |
| `tag.name` (read) | instance attribute set in `Tag.__init__` | `bs4/element.py:1648` |

### Milestone 1 — task4.py

| Usage | Definition | File:Line |
| --- | --- | --- |
| `bs4.BeautifulSoup(markup, ...)` | `BeautifulSoup.__init__` | `bs4/__init__.py:209` |
| `bs4.ResultSet` (type annotation) | `class ResultSet` | `bs4/element.py:2861` |
| `soup.find_all(id=True)` | `Tag.find_all` | `bs4/element.py:2715` |
| `tag.name` (read) | instance attribute set in `Tag.__init__` | `bs4/element.py:1648` |
| `tag["id"]` | `Tag.__getitem__` | `bs4/element.py:2203` |

### Milestone 1 — task5.py

| Usage | Definition | File:Line |
| --- | --- | --- |
| `bs4.BeautifulSoup(markup, ...)` | `BeautifulSoup.__init__` | `bs4/__init__.py:209` |
| `soup.find('b')` / `soup.find('p')` / `soup.find('a')` | `Tag.find` | `bs4/element.py:2684` |
| `tag.get('id')` / `tag.get('class')` | `Tag.get` | `bs4/element.py:2160` |
| `tag["id"]` / `tag["class"]` | `Tag.__getitem__` | `bs4/element.py:2203` |
| `tag.name` (read) | instance attribute set in `Tag.__init__` | `bs4/element.py:1648` |
| `target.get_text(strip=True)` | `PageElement.get_text` | `bs4/element.py:524` |
| `target.find_parent()` | `PageElement.find_parent` | `bs4/element.py:992` |
| `target.find_parent('section')` | `PageElement.find_parent` | `bs4/element.py:992` |
| `target.find_parent(id=True)` | `PageElement.find_parent` | `bs4/element.py:992` |
| `section.find('h2')` | `Tag.find` | `bs4/element.py:2684` |
| `heading.get_text(strip=True)` | `PageElement.get_text` | `bs4/element.py:524` |

### Milestone 1 — task6.py

| Usage | Definition | File:Line |
| --- | --- | --- |
| `bs4.BeautifulSoup(markup, ...)` | `BeautifulSoup.__init__` | `bs4/__init__.py:209` |
| `bs4.ResultSet` (type annotation) | `class ResultSet` | `bs4/element.py:2861` |
| `soup.find_all('b')` | `Tag.find_all` | `bs4/element.py:2715` |
| `tag.name = 'blockquote'` (write) | `self.name = name` (in `Tag.__init__`) | `bs4/element.py:1648` |

### Milestone 1 — task7.py

| Usage | Definition | File:Line |
| --- | --- | --- |
| `bs4.BeautifulSoup(markup, ...)` | `BeautifulSoup.__init__` | `bs4/__init__.py:209` |
| `bs4.ResultSet` (type annotation) | `class ResultSet` | `bs4/element.py:2861` |
| `soup.find_all('p')` | `Tag.find_all` | `bs4/element.py:2715` |
| `tag.get('class', [])` | `Tag.get` | `bs4/element.py:2160` |
| `tag['class'] = ' '.join(classes)` | `Tag.__setitem__` | `bs4/element.py:2223` |

### Milestone 1 — task8.py

| Usage | Definition | File:Line |
| --- | --- | --- |
| `bs4.BeautifulSoup(markup, ...)` | `BeautifulSoup.__init__` | `bs4/__init__.py:209` |
| `bs4.NavigableString` (type annotation / `isinstance`) | `class NavigableString` | `bs4/element.py:1274` |
| `bs4.Comment(...)` | `class Comment` | `bs4/element.py:1472` |
| `bs4.Doctype` (`isinstance`) | `class Doctype` | `bs4/element.py:1486` |
| `node.parent` | `self.parent = parent` (in `PageElement.setup`) | `bs4/element.py:401` |
| `parent.contents.index(node)` | `self.contents = []` (in `Tag.__init__`) | `bs4/element.py:1697` |
| `parent.insert(index, ...)` | `Tag.insert` | `bs4/element.py:1916` |
| `soup.find(string=...)` | `Tag.find` | `bs4/element.py:2684` |
| `soup.find_all(string=...)` | `Tag.find_all` | `bs4/element.py:2715` |
| `soup.insert(0, comment)` | `Tag.insert` (inherited by `BeautifulSoup`) | `bs4/element.py:1916` |

### Part 1 — task2.py (SoupStrainer)

| Usage | Definition | File:Line |
| --- | --- | --- |
| `bs4.BeautifulSoup(markup, ..., parse_only=...)` | `BeautifulSoup.__init__` | `bs4/__init__.py:209` |
| `bs4.SoupStrainer('a')` | `SoupStrainer.__init__` | `bs4/filter.py:345` |
| `bs4.ResultSet` (type annotation) | `class ResultSet` | `bs4/element.py:2861` |
| `soup.find_all('a')` | `Tag.find_all` | `bs4/element.py:2715` |
| `link.get('href', '(no href)')` | `Tag.get` | `bs4/element.py:2160` |
| `link.get_text(strip=True)` | `PageElement.get_text` | `bs4/element.py:524` |

### Part 1 — task3.py (SoupStrainer)

| Usage | Definition | File:Line |
| --- | --- | --- |
| `bs4.BeautifulSoup(markup, ..., parse_only=...)` | `BeautifulSoup.__init__` | `bs4/__init__.py:209` |
| `bs4.SoupStrainer(True)` | `SoupStrainer.__init__` | `bs4/filter.py:345` |
| `bs4.ResultSet` (type annotation) | `class ResultSet` | `bs4/element.py:2861` |
| `soup.find_all()` | `Tag.find_all` | `bs4/element.py:2715` |
| `tag.name` (read) | instance attribute set in `Tag.__init__` | `bs4/element.py:1648` |

### Part 1 — task4.py (SoupStrainer)

| Usage | Definition | File:Line |
| --- | --- | --- |
| `bs4.BeautifulSoup(markup, ..., parse_only=...)` | `BeautifulSoup.__init__` | `bs4/__init__.py:209` |
| `bs4.SoupStrainer(id=True)` | `SoupStrainer.__init__` | `bs4/filter.py:345` |
| `bs4.ResultSet` (type annotation) | `class ResultSet` | `bs4/element.py:2861` |
| `soup.find_all(id=True)` | `Tag.find_all` | `bs4/element.py:2715` |
| `tag.name` (read) | instance attribute set in `Tag.__init__` | `bs4/element.py:1648` |
| `tag["id"]` | `Tag.__getitem__` | `bs4/element.py:2203` |

## Notes

* `BeautifulSoup` subclasses `Tag`, so `find`, `find_all`, `get`,
  `insert`, `prettify`, `__getitem__`, and `__setitem__` are inherited
  from `Tag` unless `BeautifulSoup` overrides them.

* `find` and `find_all` are defined on `Tag` (`bs4/element.py:2684`
  and `:2715`). `find` calls `find_all` and returns its first result; `find_all`
  delegates to `PageElement._find_all` (`:1079`). `PageElement._find_one`
  (`:1061`) is the analogous first-result helper, but is used by `find_next`,
  `find_next_sibling`, `find_previous`, and `find_previous_sibling`, not by
  `find`. `find_parent` is defined directly on `PageElement` (`:992`).

* `tag.name`, `tag.parent`, and `tag.contents` are plain instance
  attributes, not properties or methods. They are assigned in
  `Tag.__init__` (`:1648`, `:1697`) and `PageElement.setup` (`:401`).

* `SoupStrainer` is the `ElementFilter` subclass Beautiful Soup uses
  internally for `parse_only`. Its `name`, `attrs`, `string`, and keyword
  arguments are normalized into match rules in `SoupStrainer.__init__`
  (`bs4/filter.py:345`).

* `FeatureNotFound` is imported into the `bs4` package namespace from
  `bs4.exceptions` (`bs4/exceptions.py:10`).

## See also

* [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
