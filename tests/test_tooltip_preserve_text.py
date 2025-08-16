# tests/test_tooltip_preserve_text.py
"""
Purpose
-------
Validate that `_preserve_visible_text_for_tooltip()` converts nested glossary
markers and anchors into *visible text* so tooltips render the intended words.

What it covers
--------------
1) Anchor handling:
   <a ...>TEXT</a>  ->  TEXT

2) Glossary markers:
   <section:TERM>            -> TERM
   &lt;section:TERM&gt;        -> TERM   (HTML-escaped)
   <section:>                -> section (keep tag name)

3) Idempotency:
   Applying the function twice yields the same string.

4) No-op for plain text:
   Inputs without anchors/markers are unchanged.

Why this matters
----------------
Before the fix, visible words like the referenced term label could disappear
from the tooltip (e.g., "term-a used ..." became "used ..."). These tests
guard against regressions.

How to run
----------
    pytest -q

No MkDocs/Material rendering is required; the tests exercise the helper only.
"""

import pytest
from mkdocs_ezglossary_plugin.plugin import _preserve_visible_text_for_tooltip as T

@pytest.mark.parametrize("inp, exp", [
    # 1) Anchor: keep inner text
    ('See <a href="/x">GRZ</a> docs', 'See GRZ docs'),

    # 2) Raw glossary tag: keep TERM
    ('A <general:grz> term', 'A grz term'),

    # 3) Escaped glossary tag: keep TERM
    ('A &lt;general:grz&gt; term', 'A grz term'),

    # 4) Name-only glossary tag: keep the tag name
    ('Intro <general:> section', 'Intro general section'),

    # Realistic repro from the PR description
    ('<general:term-a> used in combination with other features.',
     'term-a used in combination with other features.'),
])
def test_preserve_visible_text_parametrized(inp, exp):
    assert T(inp) == exp


def test_idempotent():
    """Running the transformer multiple times should not change the result."""
    s = "<general:grz> and <a href='/x'>docs</a>"
    once = T(s)
    twice = T(once)
    assert once == twice


def test_plain_text_is_unchanged():
    """Inputs without anchors/glossary markers should pass through untouched."""
    s = "plain text only"
    assert T(s) == s