import logging

from yaxp import xpath as xp

from mkdocs_ezglossary_plugin.glossary import get_id

import mock

log = logging.getLogger(__name__)


def test_summary(simple, summary, config):
    config['inline_refs'] = "short"
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]
    log.debug(summary)

    # first in test glossary
    a = xp.a(href="../simple.md#" + get_id("test", "first", "defs", 0),
             text="first")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dt.has(a))
    assert len(summary.xpath(str(dl))) == 1

    l1 = xp.a(href="../simple.md#" + get_id("test", "first", "refs", 0))
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dl.has(a))
    assert len(summary.xpath(str(dl))) == 0

    a = xp.a(href="../simple.md#" + get_id("test", "third", "defs", 0),
             text="third")
    dd = xp.dd
    l1 = xp.ul.li.a(href="../simple.md#" + get_id("test", "third", "refs", 0),
                    text="Hello")
    l2 = xp.ul.li.a(href="../summary.md#" + get_id("test", "third", "refs", 1),
                    text="Summary")
    dd = dd.has(l1)
    dd = dd.has(l2)
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dt.has(a))
    dl = dl.has(dd)
    assert len(summary.xpath(str(dl))) == 1

    a = xp.a(href="../simple.md#" + get_id("demo", "first", "defs", 0),
             text="first")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="demo")
    dl = dl.has(xp.dt.has(a))
    assert len(summary.xpath(str(dl))) == 1

    a = xp.a(href="../simple.md#" + get_id("demo", "third", "defs", 0),
             text="third")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="demo")
    dl = dl.has(xp.dt.has(a))
    assert len(summary.xpath(str(dl))) == 1

    a = xp.a(href="../simple.md#" + get_id("demo", "third", "refs", 0),
             text="third")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="demo")
    dl = dl.has(xp.dd.has(a))
    assert len(summary.xpath(str(dl))) == 0


def test_summary_noref(simple, summary, config):
    config['list_references'] = False
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]

    a = xp.a(href="../simple.md#" + get_id("test", "first", "defs", 0),
             text="first")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dt.has(a))
    assert len(summary.xpath(str(dl))) == 1

    a = xp.a(href="../simple.md#" + get_id("test", "third", "refs", 0),
             text="Hello")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="test")
    dl = dl.has(xp.dt(text="third"))
    dl = dl.has(xp.dd.has(a))
    assert len(summary.xpath(str(dl))) == 0


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
    config['use_default'] = True
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]
    log.debug(summary)

    a = xp.a(href="../simple.md#" + get_id("_", "default", "defs", 0),
             text="default")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="_")
    dl = dl.has(xp.dt.has(a))
    assert len(summary.xpath(str(dl))) == 1

    a = xp.a(href="../simple.md#" + get_id("_", "🚧🚧", "defs", 0),
             text="🚧🚧")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="_")
    dl = dl.has(xp.dt.has(a))
    assert len(summary.xpath(str(dl))) == 1


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
