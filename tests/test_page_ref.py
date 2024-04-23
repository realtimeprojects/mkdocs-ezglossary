import mock

import yaml
from yaxp import xpath as xp

from mkdocs_ezglossary_plugin.glossary import get_id

mycommand = mock.Page(
    title="My Command",
    file="mycommand.md",
    ctype="markdown",
    content="""
# Help page

## Overview

- See <cmd:help2>

## Help

## Details
""",
    meta=yaml.safe_load("""
subtitle: page subtitle
terms:
  - cmd4
  - "cmd5#world2"
  - page: cmd2
  - page: "cmd3#world"
  - page:
    - help1
    - term2: hello
    - term3: details
  - cmd:
    - help2
    - help3: help
anchors:
  - world: Description of world
    """))

commands = mock.Page(
    title="Commands",
    file="commands.md",
    content="""
<body>

    <p>See <cmd:help2>

    <glossary::page|theme=detailed>

    <glossary::cmd>

    <glossary::_>
</body>


""")


def test_page_ref_simple(config):
    pages = mock.render([mycommand, commands], config)

    dl = xp.dl(_class="#mkdocs-ezglossary-summary", _id="page")
    dl = dl.has(xp.dt.a(href="../mycommand.md#",
                        text="help1"))
    assert len(pages['commands.md'].xpath(str(dl))) == 1

    dd = xp.dd.ul.li.a(href="../commands.md#" + get_id("cmd", "help2", "refs", 0),
                       text="Commands")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="cmd")
    dl = dl.has(dd)
    dl = dl.has(xp.dt.a(text="help2"))
    assert len(pages['commands.md'].xpath(str(dl))) == 1


def test_page_ref_anchor(config):
    pages = mock.render([mycommand, commands], config)

    a = xp.a(href="../mycommand.md#hello",
             text="term2")
    dl = xp.dl(_class="#mkdocs-ezglossary-summary", _id="page")
    dl = dl.has(xp.dt.has(a))
    assert len(pages['commands.md'].xpath(str(dl))) == 1


def test_page_ref_direct(config):
    pages = mock.render([mycommand, commands], config)

    dd = xp.dd
    a = xp.a(href="../mycommand.md#",
             text="cmd2")
    dd = dd.has(xp.p(text="*page subtitle"))
    dl = xp.dl(_class="#mkdocs-ezglossary-summary", _id="page")
    dl = dl.has(xp.dt.has(a))
    dl = dl.has(dd)
    assert len(pages['commands.md'].xpath(str(dl))) == 1


def test_page_ref_direct_anchor(config):
    pages = mock.render([mycommand, commands], config)

    a = xp.a(href="../mycommand.md#world",
             text="cmd3")
    dd = xp.dd()
    dd = dd.has(xp.p(text="*Description of world"))
    dl = xp.dl(_class="#mkdocs-ezglossary-summary", _id="page")
    dl = dl.has(xp.dt.has(a))
    dl = dl.has(dd)
    assert len(pages['commands.md'].xpath(str(dl))) == 1


def test_page_ref_default_section(config):
    pages = mock.render([mycommand, commands], config)

    a = xp.a(href="../mycommand.md#",
             text="cmd4")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="_")
    dl = dl.has(xp.dt.has(a))
    assert len(pages['commands.md'].xpath(str(dl))) == 1


def test_page_ref_default_section_anchor(config):
    pages = mock.render([mycommand, commands], config)

    a = xp.a(href="../mycommand.md#world2",
             text="cmd5")
    dl = xp.dl(_class="mkdocs-ezglossary-summary", _id="_")
    dl = dl.has(xp.dt.has(a))
    assert len(pages['commands.md'].xpath(str(dl))) == 1


def test_page_ref_link(config):
    pages = mock.render([mycommand, commands], config)

    dl = xp.body.p.a(_class="mkdocs-ezglossary-link",
                     id=get_id("cmd", "help2", "refs", 0),
                     title="page subtitle",
                     href="../mycommand.md#",
                     text="help2")
    assert len(pages['commands.md'].xpath(str(dl))) == 1
