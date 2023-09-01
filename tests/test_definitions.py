import logging
import mock

from lxml import etree
from yaxp import xpath


log = logging.getLogger(__name__)


def test_default_config(simple, config):
    html = mock.render_single(simple, config)
    tree = etree.fromstring(html)
    log.debug(html)
    dl = xpath.dl()
    dl = dl.has(xpath.dt().has(xpath.a(name="test_first_defs_0", text="first")))
    dl = dl.has(xpath.dd(text="first term"))
    dl = dl.has(xpath.dt().has(xpath.a(name="test_second_defs_0", text="second")))
    dl = dl.has(xpath.dd(text="second term"))
    assert len(tree.xpath(str(dl)))

    dl = xpath.dl()
    dl = dl.has(xpath.dt().has(xpath.a(name="demo_first_defs_0", text="first")))
    dl = dl.has(xpath.dd(text="demo 1"))
    dl = dl.has(xpath.dt().has(xpath.a(name="demo_second_defs_0", text="second")))
    dl = dl.has(xpath.dd(text="demo 2"))
    assert len(tree.xpath(str(dl)))

    dl = xpath.dl()
    dl = dl.has(xpath.dd(text="*demo 2").has(xpath.a()))
    assert len(tree.xpath(str(dl))) == 0


def test_inline_refs(simple, config):
    config['inline_refs'] = "short"
    html = mock.render_single(simple, config)
    log.debug(html)
    tree = etree.fromstring(html)

    dl = xpath.dl()
    dl = dl.has(xpath.dt().has(xpath.a(name="test_first_defs_0", text="first")))
    dl = dl.has(xpath.dd(text="*first term").has(xpath.a()))
    assert len(tree.xpath(str(dl))) == 0

    dl = xpath.dl()
    dl = dl.has(xpath.dt().has(xpath.a(name="test_third_defs_0", text="third")))
    dl = dl.has(xpath.dd(text="*third term").has(xpath.a(title="Hello",
                                                         href="../simple.md#test_third_refs_0",
                                                         text="[1]")))
    assert len(tree.xpath(str(dl))) == 1
