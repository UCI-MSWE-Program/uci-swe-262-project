# Milestone 1: Beautiful Soup 4 Exercise

A suite of eight command-line programs that exercise the
[Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) HTML/XML
parsing library. Each program takes an HTML or XML file as a command-line
argument, builds a parse tree, performs one task, and (for tasks 1, 6, and 7)
writes the modified tree back to disk. Task 8 edits the given document.

[TOC]

## Environment

*   Python 3.14.7
*   Beautiful Soup 4.15.0 (installed with `pip`)

## How to run

```shell
python3 task1.py input.html [output]
python3 task2.py input.html
python3 task3.py input.html
python3 task4.py input.html
python3 task5.py input.html
python3 task6.py input.html [output]
python3 task7.py input.html [class_attribute1] [class_attribute2] [-o output]
python3 task8.py input.html signed_by
```

Every script accepts `.xml` files too; the XML parser is selected
automatically. When no output path is given, tasks 1, 6, and 7 write next to
the input file with a `_pretty`, `_task6`, or `_task7` suffix; task 8 signs
the input file in place.

`task7.py` takes two optional class parameters:

*   `class_attribute1` (optional, defaults to `test`) is added to every
    `<p>` tag, keeping existing classes.
*   `class_attribute2` (optional) is removed from every `<p>` tag first; the
    special value `*` clears all existing classes instead.
*   The modified tree is written to `-o output` if given, otherwise next to
    the input file with a `_task7` suffix.

```shell
python3 task7.py input.html             # <p class="liquid"> -> <p class="liquid test">
python3 task7.py input.html money        # <p class="liquid"> -> <p class="liquid money">
python3 task7.py input.html money liquid # <p class="liquid"> -> <p class="money">
python3 task7.py input.html world "*"    # <p class="liquid money"> -> <p class="world">
```

`task8.py` signs the document in place:

*   First signing: inserts
    `<!-- Created by <signed_by>. At <timestamp> -->` at the top of the
    document (right after the DOCTYPE for HTML, after the XML declaration on
    the second line for XML, or at the very top when the document has no
    DOCTYPE).
*   Later signings: appends
    `<!-- Modified by <signed_by>. At <timestamp> -->` on the line after the
    previous signature.

## The eight tasks

| File | Task | Main API used |
| --- | --- | --- |
| `task1.py` | Read a file into a tree and write the tree back to disk as a prettified file. | `BeautifulSoup(...)`, `soup.prettify()` |
| `task2.py` | Print all hyperlinks, with `href` and link text. | `soup.find_all('a')` |
| `task3.py` | Print all tags in the document (and a count summary). | `soup.find_all()` |
| `task4.py` | Print all tags that have an `id` attribute, in a single API call. | `soup.find_all(id=True)` |
| `task5.py` | Use `find_parent()` meaningfully: immediate parent, full ancestor chain, nearest enclosing `<section>`, nearest ancestor with an `id`. | `tag.find_parent()`, `tag.find_parent('section')`, `tag.find_parent(id=True)` |
| `task6.py` | Change all `<b>` tags to `<blockquote>` and write the tree to a file. | `soup.find_all('b')`, `tag.name = 'blockquote'` |
| `task7.py` | Add a class to every `<p>` tag (optionally removing another class, or clearing all classes with `*`, first) and write the tree to a file. | `soup.find_all('p')`, `tag.get('class')`, `tag['class']` |
| `task8.py` | Sign the document: insert a `Created by` (or `Modified by`) comment after the XML declaration or DOCTYPE and write the signed tree back to the file. | `bs4.Comment`, `soup.find(...)`, `soup.insert()` |

## Test corpus

`tests/` holds a corpus of 10 HTML/XML files used to exercise every task
(small, medium, large, very large, and deeply nested documents), plus the
two GB-scale experiment inputs:

| File | Kind | Size (KiB) |
| --- | --- | --- |
| `tests/small1.html` | small HTML | 0.46 |
| `tests/small2.xml` | small XML | 0.42 |
| `tests/medium1.html` | medium HTML | 282 |
| `tests/medium2.xml` | medium XML | 414 |
| `tests/large1.html` | large HTML | 2,801 |
| `tests/large2.html` | large HTML | 6,985 |
| `tests/very_large.html` | very large HTML | 70,297 |
| `tests/nested.html` | very nested HTML | 27 (1,000 nested `<div>` levels) |
| `tests/giga.html` | GB-scale experiment (synthetic HTML) | 1,049,806 |
| `tests/enwiki-20151002-pages-meta-current23.xml` | GB-scale experiment (real Wikipedia dump) | 6,078,948 |

The Wikipedia dump, `tests/enwiki-20151002-pages-meta-current23.xml`,
can be downloaded from [Internet Archive][enwiki-dump].

[enwiki-dump]: https://archive.org/download/enwiki-20151002/enwiki-20151002-pages-meta-current23.xml-p018225001p020925000.bz2

## Very large file experiment

The five largest inputs were run through `task1.py` under `/usr/bin/time`
to record wall-clock time and peak resident memory (RSS). Peak RSS grows
roughly linearly with input size, at roughly 17-27x the file size:

| Input | Size (KiB) | Peak RSS (KiB) | RSS / size | Time (s) |
| --- | --- | --- | --- | --- |
| `tests/large1.html` | 2,801 | 75,824 | 27.1x | 0.54 |
| `tests/large2.html` | 6,985 | 153,584 | 22.0x | 1.32 |
| `tests/very_large.html` | 70,297 | 1,255,348 | 17.9x | 14.45 |
| `tests/giga.html` | 1,049,806 | 18,346,856 | 17.5x | 228.68 |
| `tests/enwiki-20151002-pages-meta-current23.xml` | 6,078,948 | 56,724,436 | n/a | 150.32 |

The `enwiki` run was killed by the OS out-of-memory killer (signal 9)
after 150.32 s, when RSS reached 56,724,436 KiB (~54 GiB).

### Why peak memory is far larger than the file

`task1.py` is a whole-document tool, and several full copies of the
document coexist in memory at peak:

1.  Raw markup: the entire file is read into a single Python `str` that
    stays alive (the tree's text nodes are slices into it).
2.  lxml tree: the lxml parser builds its own C-backed tree of Python
    objects, which remains as the backing store for the soup tree.
3.  BeautifulSoup tree: every element, text node, comment, and attribute
    becomes a `bs4.element.Tag` or `NavigableString` object with dicts
    and parent/sibling pointers. The hundreds of bytes of per-node
    overhead dwarf the source text, so a dump with tens of millions of
    nodes dominates RSS.
4.  Prettified output: `soup.prettify()` materializes the entire
    reformatted document as a new string, ~20% larger than the input
    (1.07 GB in, 1.29 GB out for `giga.html`).

### Why the enwiki run failed

Extrapolating the 17-27x scaling, the 6.2 GB Wikipedia dump would need on
the order of 100+ GB of RAM. The machine ran out of memory at ~54 GiB,
and the OS killed the process before parsing finished.

### Do the task1 results apply to the other tasks?

Yes, with one caveat. All eight tasks share the identical bottleneck: the
entire file is read into one `str` and a full parse tree is built, which
costs 17-27x the file size and dominates peak RSS in every task. The
enwiki failure happened during parsing, before `prettify()` even ran, and
the parse phase is byte-for-byte identical across all tasks. Any file
that runs out of memory while `task1.py` parses will therefore fail every
other task at the same point.

The caveat is that `prettify()` adds one extra ~1.2x copy of the document
that tasks 2-5 never make, while `task3.py`'s bare `soup.find_all()`
materializes a list of every tag. A file that fails only at the very last
prettify step might barely work in `task2.py`, `task4.py`, or `task5.py`.
Because the parse tree dwarfs these extras (17-27x versus ~1.2x), a
`task1.py` failure is a strong indicator that the other tasks will fail
too, but strictly confirming it means running `task3.py` against the same
file and checking that it dies at the same stage.

## See also

* [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
