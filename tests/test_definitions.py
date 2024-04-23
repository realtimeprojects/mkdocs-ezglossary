import logging
import mock

from yaxp import xpath

from mkdocs_ezglossary_plugin.glossary import get_id


log = logging.getLogger(__name__)


def test_default_config(simple, config):
    html = mock.render_single(simple, config)
    log.debug(html)
    dl = xpath.dl
    dl = dl.has(xpath.dt.has(xpath.a(id=get_id("test", "first", "defs", 0), text="first")))
    dl = dl.has(xpath.dd(text="first term"))
    dl = dl.has(xpath.dt.has(xpath.a(id=get_id("test", "second", "defs", 0), text="second")))
    dl = dl.has(xpath.dd(text="*second term"))
    assert len(html.xpath(str(dl)))

    dl = xpath.dl
    dl = dl.has(xpath.dt.has(xpath.a(id=get_id("demo", "first", "defs", 0), text="first")))
    dl = dl.has(xpath.dd(text="demo 1"))
    dl = dl.has(xpath.dt.has(xpath.a(id=get_id("demo", "second", "defs", 0), text="second")))
    dl = dl.has(xpath.dd(text="demo 2"))
    assert len(html.xpath(str(dl)))

    dl = xpath.dl
    dl = dl.has(xpath.dd(text="*demo 2").has(xpath.a()))
    assert len(html.xpath(str(dl))) == 0


def test_inline_refs(simple, config):
    config['inline_refs'] = "short"
    html = mock.render_single(simple, config)

    dl = xpath.dl
    dl = dl.has(xpath.dt.has(xpath.a(id=get_id("test", "first", "defs", 0), text="first")))
    dl = dl.has(xpath.dd(text="*first term").has(xpath.a()))
    assert len(html.xpath(str(dl))) == 0

    dl = xpath.dl()
    dl = dl.has(xpath.dt.has(xpath.a(id=get_id("test", "third", "defs", 0), text="third")))
    dl = dl.has(xpath.dd(text="*third term").has(xpath.a(title="Hello",
                                                         href="../simple.md#" + get_id("test", "third", "refs", 0),
                                                         text="*[1]")))
    assert len(html.xpath(str(dl))) == 1


def test_default_section(simple, config):
    config['use_default'] = True
    html = mock.render_single(simple, config)
    log.debug(html)
    dl = xpath.dl
    dl = dl.has(xpath.dt.has(xpath.a(id=get_id("_", "default", "defs", 0), text="default")))
    dl = dl.has(xpath.dd(text="default term"))
    assert len(html.xpath(str(dl)))

    dl = xpath.dl
    dl = dl.has(xpath.dt.has(xpath.a(id=get_id("demo", "first", "defs", 0), text="first")))
    dl = dl.has(xpath.dd(text="demo 1"))
    dl = dl.has(xpath.dt.has(xpath.a(id=get_id("demo", "second", "defs", 0), text="second")))
    dl = dl.has(xpath.dd(text="demo 2"))
    assert len(html.xpath(str(dl)))

    dl = xpath.dl
    dl = dl.has(xpath.dd(text="*demo 2").has(xpath.a()))
    assert len(html.xpath(str(dl))) == 0


def test_formatted_dt(simple, config):
    html = mock.render_single(simple, config)
    log.debug(html)
    dl = xpath.dl
    dl = dl.has(xpath.dt.bold.em.code.has(xpath.a(id=get_id("demo", "formatted", "defs", 0), text="formatted")))
    dl = dl.has(xpath.dd(text="formatted dd"))
    assert len(html.xpath(str(dl)))
