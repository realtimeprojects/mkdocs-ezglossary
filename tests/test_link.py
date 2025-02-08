import logging

from yaxp import xpath

from mkdocs_ezglossary_plugin.glossary import get_id

import mock
from test_helpers import has_link

log = logging.getLogger(__name__)


def _hash(s):
    return str(hash(s))


def test_link_no_title(simple, config):
    html = mock.render_single(simple, config)
    
    assert has_link(
        page=html,
        section="test",
        term="third",
        title="",
        href="../simple.md",
        text="third"
    )


def test_link_case_sensitive(simple, config):
    html = mock.render_single(simple, config)
    
    # Should not find link when case doesn't match and ignore_case is False
    assert not has_link(
        page=html,
        section="test",
        term="First",  # Capital F
        title="",
        href="../simple.md",
        text="First"
    )


def test_link_ignore_case(simple, config):
    config['ignore_case'] = True
    html = mock.render_single(simple, config)
    
    # Should find link when ignore_case is True, regardless of case
    assert has_link(
        page=html,
        section="test",
        term="first",
        title="",
        href="../simple.md",
        text="First"
    )


def test_link_with_title(simple, config):
    config['tooltip'] = 'full'  # Enable tooltips
    html = mock.render_single(simple, config)
    
    assert has_link(
        page=html,
        section="test",
        term="third",
        title="third term",
        href="../simple.md",
        text="third"
    )


def test_link_with_spaces(simple, summary, config):
    summary = mock.render([simple, summary], config)['summary.md']
    
    assert has_link(
        page=summary,
        section="test",
        term="hyphens-abc xyz",
        title="",
        href="../simple.md",
        text="hyphens-abc xyz"
    )


def test_unicode_links(simple, summary, config):
    summary = mock.render([simple, summary], config)['summary.md']
    
    assert has_link(
        page=summary,
        section="demo",
        term="🚧",
        title="",
        href="../simple.md",
        text="🚧"
    )


def test_plural_links(simple, summary, config):
    config['plurals'] = 'en'
    summary = mock.render([simple, summary], config)['summary.md']

    # Test various plural forms
    # Format: (section, plural, singular, index)
    test_cases = [
        ("plurals", "GPUs", "GPU", 0),
        ("plurals", "geese", "goose", 0),
        ("plurals", "children", "child", 0),
        ("plurals", "cities", "city", 0),
        # 2 definitions exist: potato and potatoes, in this case, the plural is used
        ("plurals", "potatoes", "potatoes", 0),
        ("plurals", "grandchildren", "grandchild", 1),
    ]

    for section, plural, singular, index in test_cases:
        assert has_link(
            page=summary,
            section=section,
            term=plural,
            title="",
            href="../simple.md",
            text=plural,
            destination=singular,
            index=index
        ), f"Failed to find link for plural '{plural}' (singular: '{singular}')"


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

    assert has_link(
        page=summary,
        section="test",
        term="third",
        title="third term",
        href="../simple.md",
        text="third",
        destination="third",
        index=1
    )
    assert has_link(
        page=summary,
        section="test",
        term="third",
        title="third term",
        href="../simple.md",
        text="mythird",
        destination="third",
        index=2
    )


def test_link_default_ref_dis(simple, summary, config):
    """ Ensure definitions for the default sections are
        ignored when the configuration `use_default` is set
        to `False`.
    """
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    assert not has_link(
        page=summary,
        section="_",
        term="default",
        title="",
        href="../simple.md",
        text="default",
        destination="default"
    )


def test_link_default_ref_enabled(simple, summary, config):
    """ Ensure definitions for the default sections are
        replaced when the configuration `use_default` is set
        to `True`.
    """
    config['use_default'] = True
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    assert has_link(
        page=summary,
        section="_",
        term="default",
        title="",
        href="../simple.md",
        text="default",
        destination="default"
    )
    assert has_link(
        page=summary,
        section="_",
        term="default2",
        title="",
        href="../simple.md",
        text="mydef2",
        destination="default2"
    )
    assert has_link(
        page=summary,
        section="_",
        term="default3",
        title="",
        href="../simple.md",
        text="mydef3",
        destination="default3"
    )


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

    assert has_link(
        page=summary,
        section="test",
        term="third",
        title="",
        href="../simple.md",
        text="third",
        destination="third",
        index=1
    )
    assert has_link(
        page=summary,
        section="test",
        term="third",
        title="",
        href="../simple.md",
        text="mythird",
        destination="third",
        index=2
    )


def test_unicode(simple, summary, config):
    """ Unicode links are processed.
    """
    config['markdown_links'] = True
    config['use_default'] = True
    config['tooltip'] = "short"
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    assert has_link(
        page=summary,
        section="demo",
        term="🚧",
        title="demo 🚧🚧🚧",
        href="../simple.md",
        text="🚧",
        destination="🚧"
    )
    assert has_link(
        page=summary,
        section="_",
        term="🚧🚧",
        title="default 🚧🚧🚧",
        href="../simple.md",
        text="refers to 🚧",
        destination="🚧🚧"
    )


def test_plurals_inflect(simple, summary, config):
    """ Plurals are mapped to singulars
    """
    config['tooltip'] = "full"
    config['plurals'] = 'inflect'
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    assert has_link(
        page=summary,
        section='plurals',
        term='children',
        title='children definition',
        href='../simple.md',
        text='children',
        destination='child'
    )
    assert has_link(
        page=summary,
        section='plurals',
        term='geese',
        title='goose definition',
        href='../simple.md',
        text='geese',
        destination='goose'
    )


def test_plurals_en(simple, summary, config):
    """ Plurals are mapped to singulars
    """
    config['tooltip'] = "full"
    config['plurals'] = 'en'
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    assert has_link(
        page=summary,
        section='plurals',
        term='children',
        title='children definition',
        href='../simple.md',
        text='children',
        destination='child'
    )
    assert has_link(
        page=summary,
        section='plurals',
        term='geese',
        title='goose definition',
        href='../simple.md',
        text='geese',
        destination='goose'
    )
    assert has_link(
        page=summary,
        section='plurals',
        term='grandchildren',
        title='grandchild definition',
        href='../simple.md',
        text='grandchildren',
        destination='grandchild',
        index=1
    )


def test_plural_priority(simple, summary, config):
    """ If the plural term is defined, this should be used in priority
    """
    config['tooltip'] = "full"
    config['plurals'] = 'en'
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    assert has_link(
        page=summary,
        section='plurals',
        term='potatoes',
        title='potatoes definition',
        href='../simple.md',
        text='potatoes',
        destination='potatoes'
    )


def test_plurals_disabled(simple, summary, config):
    """ Plurals are not mapped to singulars, if not enabled
    """
    config['tooltip'] = "full"
    summary = mock.render([simple, summary], config)['summary.md']
    log.debug(summary)

    assert not has_link(
        page=summary,
        section='plurals',
        term='children',
        title='children definition',
        href='simple.md',
        text='children',
        destination='child'
    )

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
