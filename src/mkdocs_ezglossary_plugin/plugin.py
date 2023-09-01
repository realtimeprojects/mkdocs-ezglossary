import logging
import re
import os
from html import parser

from mkdocs.plugins import BasePlugin, event_priority
from mkdocs import config
from mkdocs.config import config_options as co

from .glossary import Glossary

log = logging.getLogger("mkdocs.plugins.ezglossary")


class __re:
    def __init__(self):
        self.ws = r"[\n ]*"
        self.section = r"(\w+)"
        self.term = r"([\w -]+)"
        self.text = r"([^>]+)"
        self.dt = rf"<dt>{self.section}:{self.term}<\/dt>"
        self.dt_default = rf"<dt>{self.term}<\/dt>"
        self.dd = r"<dd>\n?((.|\n)+?)<\/dd>"
        self.options = r"([\w\+]+)"


_re = __re()


class GlossaryConfig(config.base.Config):
    tooltip = config.config_options.Choice(('none', 'heading', 'full'), default="none")
    inline_refs = config.config_options.Choice(('none', 'short', 'full'), default="none")
    sections = co.ListOfItems(config.config_options.Type(str), default=[])
    section_config = co.ListOfItems(config.config_options.Type(dict), default=[])
    strict = config.config_options.Type(bool, default=False)
    list_references = config.config_options.Type(bool, default=True)
    list_definitions = config.config_options.Type(bool, default=True)


class GlossaryPlugin(BasePlugin[GlossaryConfig]):
    def __init__(self):
        self._glossary = Glossary()
        self._uuid = "6251a85a-47d0-11ee-be56-0242ac120002"
        self._reflink = "6251a85a-47d0-11ee-be56-0242ac120002"

    def on_pre_build(self, config, **kwargs):
        if self.config.strict and len(self.config.sections) == 0:
            log.error("ezglossary: no sections defined, but 'strict' is true, plugin disabled")
        self._glossary.clear()

    @event_priority(5000)
    def on_page_content(self, content, page, config, files):
        content = self._find_definitions(content, page)
        content = self._register_glossary_links(content, page)
        return content

    def on_post_page(self, output, page, config):
        _dir = os.path.dirname(page.url)
        levels = len(_dir.split("/"))
        root = "../" * levels
        output = self._replace_glossary_links(output, page, root)
        output = self._replace_inline_refs(output, page, root)
        output = self._print_glossary(output, root)
        return output

    def _add_items(self, html, root, heading, entries, mode=""):
        ii = 0
        if len(entries) == 0:
            return html
        if mode == "short":
            html += "<p>"
        for (_id, data) in entries.items():
            ii += 1
            (page, desc) = data
            if mode == "short":
                html += f'<span><a title="{page.title}" href="{root}{page.url}#{_id}">[{ii}]</a></span>'
            else:
                html += f'''
                <li>
                    <a href="{root}{page.url}#{_id}">{page.title}</a>
                    <small>[{heading[:-1]}]</small>
                </li>'''
        if mode == "short":
            html += "</p>"
        return html

    def _print_glossary(self, html, root):
        def _replace(mo):
            section = mo.group(1)
            options = mo.group(2) or ""

            lr = "do_refs" in options
            if "no_refs" not in options and "do_refs" not in options:
                lr = self._get_config(section, 'list_references')

            ld = "do_defs" in options
            if "no_defs" not in options and "do_defs" not in options:
                ld = self._get_config(section, 'list_definitions')

            if not lr and not ld:
                log.warning("list_definitons and list_references disabled, summary will be empty")

            html = f'<dl class="mkdocs-glossary" id="{section}">'
            if not self._glossary.has(section=section):
                log.warning(f"no section '{section}' found in glossary")
            terms = self._glossary.terms(section)
            for term in terms:
                html += f'<dt>{term}</dt><dd><ul>'
                if ld:
                    entries = self._glossary.get(section, term, 'defs')
                    html = self._add_items(html, root, "defs", entries)
                if lr:
                    entries = self._glossary.get(section, term, 'refs')
                    html = self._add_items(html, root, "refs", entries)
                html += '</ul></dd>'
            html += "</dl>"
            return html

        regex = rf"<glossary::{_re.section}\|?{_re.options}?>"
        return re.sub(regex, _replace, html)

    def _register_glossary_links(self, output, page):
        def _replace(mo):
            section = mo.group(1)
            term = mo.group(2)
            text = mo.group(3) if mo.group(3) else term
            _id = self._glossary.add(section, term, 'refs', page)
            return f"{self._uuid}:{section}:{term}:<{text}>:{_id}"

        regex = rf"<{_re.section}:{_re.term}\|?{_re.text}?>"
        return re.sub(regex, _replace, output)

    def _replace_inline_refs(self, output, page, root):
        def _replace(mo):
            section = mo.group(1)
            term = mo.group(2)

            mode = self._get_config(section, 'inline_refs')

            entries = self._glossary.get(section, term, 'refs')
            html = ""
            if mode == "list":
                html += '<div>'
                html += '\n<ul class="ezglossary-refs">'
            html += self._add_items(html, root, "refs", entries, mode)
            if mode == "list":
                html += '</ul></div>\n'
            return html

        regex = fr"{self._reflink}:{_re.section}:{_re.term}"
        return re.sub(regex, _replace, output)

    def _replace_glossary_links(self, output, page, root):
        def _replace(mo):
            section = mo.group(1)
            term = mo.group(2)
            text = mo.group(3)
            _id = mo.group(4)
            defs = self._glossary.get(section, term, 'defs')
            if len(defs) == 0:
                log.warning(f"page '{page.url}' referenes to undefined glossary entry {section}:{term}")
                return f'<a name="{_id}">{text}</a>'
            target_id = list(defs.keys())[0]
            (target_page, desc) = defs[target_id]
            target = f"{root}{target_page.url}#{target_id}"
            return f'<a name="{_id}" title="{_html2text(desc)}" href="{target}">{text}</a>'

        regex = fr"{self._uuid}:{_re.section}:{_re.term}:<{_re.text}>:(\w+)"
        return re.sub(regex, _replace, output)

    def _find_definitions(self, content, page):
        log.debug(f"_find_definitions({page})")

        def _add_entry(section, term, desc):
            log.debug(f"found entry: {section}:{term}:{desc}")

            if self.config.tooltip == "none":
                _tooltip = ""
            if self.config.tooltip == "short":
                _tooltip = desc.split("\n")[0]
            if self.config.tooltip == "full":
                _tooltip = desc

            if section not in self.config.sections and self.config.strict:
                log.warning(f"ignoring undefined section '{section}' in glossary")
                return None

            _id = self._glossary.add(section, term, 'defs', page, _tooltip)

            inline_refs = self._get_config(section, 'inline_refs')
            reflink = f"\n{self._reflink}:{section}:{term}" if inline_refs != "none" else ""
            return f'<dt><a name="{_id}">{term}</a></dt><dd>{desc}{reflink}</dd>'

#       def _replace_default(mo):
#           section = "_"
#           term = mo.group(2)
#           _add_entry(section, term,

        def _replace(mo):
            section = mo.group(1)
            term = mo.group(2)
            desc = mo.group(3)
            rendered = _add_entry(section, term, desc)
            return rendered if rendered else mo.group()

        # regex_default = re.compile(rf"{_re.dt_default}")
        # ret = re.sub(regex_default, _replace, content)

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
    return f.text
