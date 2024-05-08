import logging
import re
import os
from html import parser, unescape

from mkdocs.plugins import BasePlugin, event_priority
from mkdocs import config
from mkdocs.config import config_options as co

from .glossary import Glossary

from . import template

log = logging.getLogger("mkdocs.plugins.ezglossary")


class __re:
    def __init__(self):
        self.ws = r"[\n ]*"
        self.section = r"([^:<>\"\|/\@&#][^:<>\"\|/\@]*)"
        self.term = self.section
        self.text = r"([^>]+)"
        self.dt = rf"<dt>(<.*>)?{self.section}:{self.term}(<.*>)?<\/dt>"
        self.dt_default = rf"<dt>(<.*>)?{self.term}(<.*>)?<\/dt>"
        self.dd = r"<dd>\n?((.|\n)+?)<\/dd>"
        self.options = r"([\\\|\=\w\+]+)"


_re = __re()


class GlossaryConfig(config.base.Config):
    tooltip = config.config_options.Choice(('none', 'heading', 'full'), default="none")
    inline_refs = config.config_options.Choice(('none', 'short', 'full'), default="none")
    sections = co.ListOfItems(config.config_options.Type(str), default=[])
    section_config = co.ListOfItems(config.config_options.Type(dict), default=[])
    strict = config.config_options.Type(bool, default=False)
    markdown_links = config.config_options.Type(bool, default=False)
    list_references = config.config_options.Type(bool, default=True)
    list_definitions = config.config_options.Type(bool, default=True)
    use_default = config.config_options.Type(bool, default=False)
    templates = config.config_options.Type(str, default="")


class GlossaryPlugin(BasePlugin[GlossaryConfig]):
    def __init__(self):
        self._glossary = Glossary()
        self._uuid = "6251a85a-47d0-11ee-be56-0242ac120002"
        self._reflink = "886d7696-137e-4a59-a39d-6f7d311d5bd1"

    def on_pre_build(self, config, **kwargs):
        if self.config.strict and "_" not in self.config.sections:
            self.config.sections.append("_")
        if self.config.strict and len(self.config.sections) == 0:
            log.error("ezglossary: no sections defined, but 'strict' is true, plugin disabled")
        self._glossary.clear()

    def on_page_markdown(self, content, page, config, files):
        attributes = page.meta

        def _get_definition(anchor):
            anchors = attributes.get('anchors')
            if anchors:
                for anchor_def in anchors:
                    if anchor in anchor_def:
                        return anchor_def[anchor]
            if 'subtitle' in attributes:
                return attributes['subtitle']
            return page.title

        def _add2section(section, term, anchor=None):
            if not anchor:
                if "#" in term:
                    (term, anchor) = term.split("#")
                else:
                    (term, anchor) = (term, "")
            definition = _get_definition(anchor)
            log.debug(f"add2section: {section}:{term}:{anchor} -> '{definition}'")
            self._glossary.add(section,
                               term,
                               'defs',
                               page,
                               definition,
                               anchor)

        ez = attributes.get('terms')
        log.debug(ez)
        if not ez:
            return content

        for entry in ez:
            if isinstance(entry, str):
                _add2section("_", entry)
                continue

            for (section, data) in entry.items():
                if isinstance(data, str):
                    _add2section(section, data)
                    continue

                for term in data:
                    if isinstance(term, str):
                        _add2section(section, term)
                    if isinstance(term, dict):
                        for term, anchor in term.items():
                            _add2section(section, term, anchor)
        return content

    @event_priority(5000)
    def on_page_content(self, content, page, config, files):
        content = self._find_definitions(content, page)
        content = self._register_glossary_links(content, page)
        return content

    def on_post_page(self, output, page, config):
        _dir = os.path.dirname(page.url)
        levels = len(_dir.split("/"))
        if page.canonical_url.replace(config.site_url or "", "").lstrip("/").count("/") < 1:
            root = "./" * levels
        else:
            root = "../" * levels
        output = self._replace_glossary_links(output, page, root)
        output = self._replace_inline_refs(output, page, root)
        output = self._print_glossary(output, root)
        return output

    def _print_glossary(self, html, root):
        def _replace(mo):
            types = []
            section = mo.group(1)
            options = mo.group(2) or ""

            lr = "do_refs" in options
            if "no_refs" not in options and "do_refs" not in options:
                lr = self._get_config(section, 'list_references')
            if lr:
                types.append('refs')

            ld = "do_defs" in options
            if "no_defs" not in options and "do_defs" not in options:
                ld = self._get_config(section, 'list_definitions')
            if ld:
                types.append('defs')

            if len(types) == 0:
                log.warning("list_definitons and list_references disabled, summary will be empty")

            if not self._glossary.has(section=section):
                log.warning(f"no section '{section}' found in glossary")

            terms = self._glossary.terms(section)
            theme = ""
            for option in options.replace("\\|", "|").split("|"):
                if "theme" in option:
                    theme = "-" + option.split("=")[1]
            return template.render(f"summary{theme}.html",
                                   self.config,
                                   glossary=self._glossary,
                                   types=types,
                                   section=section,
                                   terms=terms,
                                   root=root)
            return html

        regex = rf"<glossary::{_re.section}\\?\|?{_re.options}?>"
        return re.sub(regex, _replace, html)

    def _register_glossary_links(self, output, page):

        def _add_link(section, term, text):
            section = "_" if (section == "default" or section is None) else section
            term = term if term else "__None__"
            text = text if text else "__None__"
            log.debug(f"glossary: found link: {section}/{term}/{text}")
            _id = self._glossary.add(section, term, 'refs', page)
            return f"{self._uuid}:{section}:{term}:<{text}>:{_id}"

        def _replace(mo):
            return _add_link(mo.group(1), mo.group(2), mo.group(4))

        def _replace_default(mo):
            return _add_link(None, mo.group(1), mo.group(3))

        def _replace_href(mo):
            return _add_link(mo.group(2), mo.group(3), mo.group(4))

        regex = rf"<{_re.section}\:{_re.term}(\\?\|({_re.text}))?>"
        output = re.sub(regex, _replace, output)
        regex = rf"<{_re.term}:(\\?\|({_re.text}))?>"
        output = re.sub(regex, _replace_default, output)

        if self.config.markdown_links:
            regex = rf'<a href="({_re.section}\:)?{_re.term}">({_re.text})?</a>'
            output = re.sub(regex, _replace_href, output)

        return output

    def _replace_inline_refs(self, output, page, root):
        def _replace(mo):
            section = mo.group(1)
            term = mo.group(2)
            log.debug(f"inline_refs: looking up: '{section}/{term}'")

            mode = self._get_config(section, 'inline_refs')

            entries = self._glossary.get(section, term, 'refs')
            return template.render(f"refs-{mode}.html",
                                   self.config,
                                   entries=entries,
                                   root=root)

        regex = fr"{self._reflink}:{_re.section}:{_re.term}"
        return re.sub(regex, _replace, output)

    def _replace_glossary_links(self, output, page, root):
        def _replace(mo):
            section = mo.group(1)
            term = unescape(mo.group(2))
            text = mo.group(3)
            _id = mo.group(4)
            defs = self._glossary.get(section, term, 'defs')

            text = term if text == "__None__" else text

            if len(defs) == 0:
                log.warning(f"page '{page.url}' refers to undefined glossary entry {section}:{term}")
                term = "" if term == "__None__" else term
                text = "" if text == "__None__" else text
                sec = f"{section}:" if section != "_" else ""
                return f'<a href="{sec}{term}">{text}</a>'

            if len(defs) > 1:
                log.warning(f"multiple definitions found for <{section}:{term}>, linking to first:")
                for _def in defs:
                    log.warning(f"\t{_def}")
            entry = defs[0]
            entry.definition = _html2text(entry.definition)
            return template.render("link.html",
                                   root=root,
                                   config=self.config,
                                   entry=entry,
                                   text=text,
                                   target=_id)

        regex = fr"{self._uuid}:{_re.section}:{_re.term}:<{_re.text}>:(\w+)"
        return re.sub(regex, _replace, output)

    def _find_definitions(self, content, page):
        log.debug(f"_find_definitions({page})")

        def _add_entry(section, term, definition, fmt_pre, fmt_post):
            term = unescape(term)
            log.debug(f"glossary: found definition: {section}:{term}:{definition} {fmt_pre}:{fmt_post}")

            if self.config.tooltip == "none":
                _tooltip = ""
            if self.config.tooltip == "short":
                _tooltip = definition.split("\n")[0]
            if self.config.tooltip == "full":
                _tooltip = definition

            if section not in self.config.sections and self.config.strict:
                log.warning(f"ignoring undefined section '{section}' in glossary")
                return None

            _id = self._glossary.add(section, term, 'defs', page, _tooltip)

            inline_refs = self._get_config(section, 'inline_refs')
            reflink = f"\n{self._reflink}:{section}:{term}" if inline_refs != "none" else ""
            return template.render("definition.html",
                                   self.config,
                                   target=_id,
                                   term=unescape(term),
                                   definition=definition,
                                   reflink=reflink,
                                   fmt_pre=fmt_pre if fmt_pre else "",
                                   fmt_post=fmt_post if fmt_post else "")

        def _replace(mo):
            fmt_pre = mo.group(1)
            section = mo.group(2)
            term = mo.group(3)
            fmt_post = mo.group(4)
            definition = mo.group(5)
            rendered = _add_entry(section, term, definition, fmt_pre, fmt_post)
            return rendered if rendered else mo.group()

        def _replace_default(mo):
            section = "_"
            fmt_pre = mo.group(1)
            term = mo.group(2)
            fmt_post = mo.group(3)
            definition = mo.group(4)
            rendered = _add_entry(section, term, definition, fmt_pre, fmt_post)
            return rendered if rendered else mo.group()

        if self.config.use_default:
            regex_dt = re.compile(rf"{_re.dt_default}{_re.ws}{_re.dd}", re.MULTILINE)
            content = re.sub(regex_dt, _replace_default, content)

        regex_dt = re.compile(rf"{_re.dt}{_re.ws}{_re.dd}", re.MULTILINE)
        ret = re.sub(regex_dt, _replace, content)
        return ret

    def _get_section_config(self, section):
        for entry in self.config.section_config:
            if entry['name'] == section:
                return entry
        return None

    def _get_config(self, section, entry):
        cfg = self._get_section_config(section)
        if not cfg or entry not in cfg:
            ret = self.config[entry]
        else:
            ret = cfg[entry]
        log.debug(f"_get_config({section}, {entry}): {ret}")
        return ret


def _html2text(content):
    class HTMLFilter(parser.HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = ""

        def handle_data(self, data):
            self.text += data

    f = HTMLFilter()
    log.debug(f"adding {content}")
    f.feed(content)
    return f.text.strip()
