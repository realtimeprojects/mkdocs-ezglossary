import logging
import mock

from yaxp import xpath

from mkdocs_ezglossary_plugin.glossary import get_id

log = logging.getLogger(__name__)


def _hash(s):
    return str(hash(s))


def test_link_no_title(simple, config):
    html = mock.render_single(simple, config)

    dl = xpath.body.p.a(id=get_id("test", "third", "refs", 0),
                        title="",
                        href="../simple.md#" + get_id("test", "third", "defs", 0),
                        text="third")
    assert len(html.xpath(str(dl))) == 1


def test_link_short_title(simple, config):
    config['tooltip'] = "short"
    html = mock.render_single(simple, config)
    log.debug(html)

    dl = xpath.body.p.a(id=get_id("test", "third", "refs", 0),
                        title="third term",
                        href="../simple.md#" + get_id("test", "third", "defs", 0),
                        text="third")
    assert len(html.xpath(str(dl))) == 1


def test_link_full_title(simple, config):
    config['tooltip'] = "full"
    html = mock.render_single(simple, config)
    log.debug(html)

    dl = xpath.body.p.a(_class="mkdocs-ezglossary-link",
                        id=get_id("test", "third", "refs", 0),
                        title="*detailed description of third term",
                        href="../simple.md#" + get_id("test", "third", "defs", 0),
                        text="third")
    assert len(html.xpath(str(dl))) == 1


def test_link_replace_html(simple, config):
    config['tooltip'] = "full"
    html = mock.render_single(simple, config)
    log.debug(html)

    dl = xpath.body.p.a(id=get_id("test", "second", "refs", 0),
                        title="*this text is formatted",
                        href="../simple.md#" + get_id("test", "second", "defs", 0),
                        text="mysecond")
    assert len(html.xpath(str(dl))) == 1


def test_link_second_ref(simple, summary, config):
    config['tooltip'] = "full"
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    dl = xpath.body.p.a(id=get_id("test", "third", "refs", 1),
                        title="*third term",
                        href="../simple.md#" + get_id("test", "third", "defs", 0),
                        text="third")
    assert len(summary.xpath(str(dl))) == 1
    dl = xpath.body.p.a(id=get_id("test", "third", "refs", 2),
                        title="*third term",
                        href="../simple.md#" + get_id("test", "third", "defs", 0),
                        text="mythird")
    assert len(summary.xpath(str(dl))) == 1


def test_link_default_ref_dis(simple, summary, config):
    """ Ensure definitions for the default sections are
        ignored when the configuration `use_default` is set
        to `False`.
    """
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    dl = xpath.body.p.a(_class="mkdocs-ezglossary-link",
                        id=get_id("_", "default", "refs", 0),
                        title="",
                        href="../simple.md#" + get_id("_", "default", "defs", 0),
                        text="default")
    assert len(summary.xpath(str(dl))) == 0


def test_link_default_ref_enabled(simple, summary, config):
    """ Ensure definitions for the default sections are
        replaced when the configuration `use_default` is set
        to `True`.
    """
    config['use_default'] = True
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    dl = xpath.body.p.a(_class="mkdocs-ezglossary-link",
                        id=get_id("_", "default", "refs", 0),
                        title="",
                        href="../simple.md#" + get_id("_", "default", "defs", 0),
                        text="default")
    assert len(summary.xpath(str(dl))) == 1
    dl = xpath.body.p.a(_class="mkdocs-ezglossary-link",
                        id=get_id("_", "default2", "refs", 0),
                        title="",
                        href="../simple.md#" + get_id("_", "default2", "defs", 0),
                        text="mydef2")
    assert len(summary.xpath(str(dl))) == 1
    dl = xpath.body.p.a(_class="mkdocs-ezglossary-link",
                        id=get_id("_", "default3", "refs", 0),
                        title="",
                        href="../simple.md#" + get_id("_", "default3", "defs", 0),
                        text="mydef3")
    assert len(summary.xpath(str(dl))) == 1


def test_markdown_links_disabled(simple, summary, config):
    """ Ensure that markdown links are ignored when `markdown_links` is set to false.
    """
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    dl = xpath.body.p.a(href="test:third",
                        text="mythird")
    assert len(summary.xpath(str(dl))) == 1


def test_markdown_links_enabled(simple, summary, config):
    """ Ensure markdown links are resolved when `markdown_links` is set to true.
    """
    config['markdown_links'] = True
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    dl = xpath.body.p.a(id=get_id("test", "third", "refs", 1),
                        title="",
                        href="../simple.md#" + get_id("test", "third", "defs", 0),
                        text="third")
    assert len(summary.xpath(str(dl))) == 1
    dl = xpath.body.p.a(id=get_id("test", "third", "refs", 2),
                        title="",
                        href="../simple.md#" + get_id("test", "third", "defs", 0),
                        text="mythird")
    assert len(summary.xpath(str(dl))) == 1


def test_unicode(simple, summary, config):
    """ Unicode links are processed.
    """
    config['markdown_links'] = True
    config['use_default'] = True
    config['tooltip'] = "short"
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    dl = xpath.body.p.a(id=get_id("demo", "🚧", "refs", 0),
                        title="demo 🚧🚧🚧",
                        href="../simple.md#" + get_id("demo", "🚧", "defs", 0),
                        text="🚧")
    assert len(summary.xpath(str(dl))) == 1
    dl = xpath.body.p.a(id=get_id("_", "🚧🚧", "refs", 0),
                        title="default 🚧🚧🚧",
                        href="../simple.md#" + get_id("_", "🚧🚧", "defs", 0),
                        text="refers to 🚧")
    assert len(summary.xpath(str(dl))) == 1


def test_hyphens(simple, summary, config):
    """ Hyphens in terms are supported
    """
    config['markdown_links'] = True
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    dl = xpath.body.p.a(id=get_id("test", "hyphens-abc def", "refs", 0),
                        href="../simple.md#" + get_id("test", "hyphens-abc def", "defs", 0),
                        text="hyphens-abc def")
    assert len(summary.xpath(str(dl))) == 1
    dl = xpath.body.p.a(id=get_id("test", "hyphens-abc xyz", "refs", 0),
                        href="../simple.md#" + get_id("test", "hyphens-abc xyz", "defs", 0),
                        text="hyphens-abc xyz")
    assert len(summary.xpath(str(dl))) == 1
