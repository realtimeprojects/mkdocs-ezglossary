import logging

from yaxp import xpath as xp

from mkdocs_ezglossary_plugin.glossary import get_id

import mock

from test_helpers import has_summary_entry

log = logging.getLogger(__name__)


def test_summary(simple, summary, config):
    config['inline_refs'] = "short"
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]
    log.debug(summary)

    # first in test glossary
    assert has_summary_entry(
        page=summary,
        section="test",
        term="first",
        href="../simple.md",
        ref_text="Hello"
    )

    # Check reference to third term
    assert has_summary_entry(
        page=summary,
        section="test",
        term="third",
        href="../simple.md",
        ref_text="Hello"
    )
    
    assert has_summary_entry(
        page=summary,
        section="demo",
        term="first",
        href="../simple.md",
        ref_text="Hello"
    )
    
    assert has_summary_entry(
        page=summary,
        section="demo",
        term="third",
        href="../simple.md",
        ref_text="Hello"
    )

def test_summary_ignore_case(simple, summary, config):
    """ make sure that the summary for a term contains references to terms written in different case. """
    config['ignore_case'] = True
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]
    
    assert has_summary_entry(
        page=summary,
        section="test",
        term="first"
    )
    
    assert not has_summary_entry(
        page=summary,
        section="test",
        term="First"
    )
    

def test_summary_noref(simple, summary, config):
    config['list_references'] = False
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]

    # Check definition link exists
    assert has_summary_entry(
        page=summary,
        section="test",
        term="first",
        href="../simple.md",
        ref_text="Hello"
    )

    # Check reference link does not exist
    assert not has_summary_entry(
        page=summary,
        section="test",
        term="third",
        href="../simple.md",
        ref_text="first"
    )


def test_custom_summary(simple, summary, config):
    config['templates'] = "tests/custom"
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]

    dd = xp.dd.ul.li.a(href="../simple.md#" + get_id("test", "third", "refs", 0),
                       text="Hello")
    dl = xp.dl(_class="custom-summary", _id="test")
    dl = dl.has(xp.dt(text="third"))
    dl = dl.has(dd)
    assert len(summary.xpath(str(dl))) == 1


def test_default_summary(simple, summary, config):
    """check the usage of the default section ('_')"""
    
    config['use_default'] = True
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]
    log.debug(summary)

    assert has_summary_entry(
        page=summary,
        section="_",
        term="default",
        href="../simple.md",
        ref_text="Hello"
    )

    assert has_summary_entry(
        page=summary,
        section="_",
        term="🚧🚧",
        href="../simple.md",
        ref_text="Hello"
    )


def test_summary_table(simple, tablesummary, config):
    pages = mock.render([simple, tablesummary], config)
    summary = pages["tablesummary.md"]
    log.debug(summary)

    table = xp.div(_class="#mkdocs-ezglossary-summary").table(_id="demo")
    tr = xp.tr
    table = table.has(xp.thead.has(xp.th(text="Term"))
                      .has(xp.th(text="Definition"))
                      .has(xp.th(text="References")))
    tr = tr.has(xp.td(text="*first"))
    table.has(tr)
    assert len(summary.xpath(str(table))) == 1
