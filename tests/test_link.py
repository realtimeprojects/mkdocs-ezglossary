import logging
import mock

from yaxp import xpath

log = logging.getLogger(__name__)


def test_link_no_title(simple, config):
    html = mock.render_single(simple, config)

    dl = xpath.body().p().a(name="test_third_refs_0",
                            title="",
                            href="../simple.md#test_third_defs_0",
                            text="third")
    assert len(html.xpath(str(dl))) == 1


def test_link_short_title(simple, config):
    config['tooltip'] = "short"
    html = mock.render_single(simple, config)
    log.debug(html)

    dl = xpath.body().p().a(name="test_third_refs_0",
                            title="third term",
                            href="../simple.md#test_third_defs_0",
                            text="third")
    assert len(html.xpath(str(dl))) == 1


def test_link_full_title(simple, config):
    config['tooltip'] = "full"
    html = mock.render_single(simple, config)
    log.debug(html)

    dl = xpath.body().p().a(name="test_third_refs_0",
                            title="*detailed description of third term",
                            href="../simple.md#test_third_defs_0",
                            text="third")
    assert len(html.xpath(str(dl))) == 1


def test_link_replace_html(simple, config):
    config['tooltip'] = "full"
    html = mock.render_single(simple, config)
    log.debug(html)

    dl = xpath.body().p().a(name="test_second_refs_0",
                            title="*this text is formatted",
                            href="../simple.md#test_second_defs_0",
                            text="second")
    assert len(html.xpath(str(dl))) == 1


def test_link_second_ref(simple, summary, config):
    config['tooltip'] = "full"
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    dl = xpath.body().p().a(name="test_third_refs_1",
                            title="*third term",
                            href="../simple.md#test_third_defs_0",
                            text="third")
    assert len(summary.xpath(str(dl))) == 1


def test_link_default_ref_disabled(simple, summary, config):
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    dl = xpath.body().p().a(name="__default_refs_0",
                            title="",
                            href="../simple.md#__default_defs_0",
                            text="default")
    assert len(summary.xpath(str(dl))) == 0


def test_link_default_ref_enabled(simple, summary, config):
    config['use_default'] = True
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    dl = xpath.body().p().a(name="__default_refs_0",
                            title="",
                            href="../simple.md#__default_defs_0",
                            text="default")
    assert len(summary.xpath(str(dl))) == 1
