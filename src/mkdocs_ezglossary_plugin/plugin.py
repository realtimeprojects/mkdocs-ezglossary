import logging
import re
import os
import html

from mkdocs.plugins import BasePlugin, event_priority
from mkdocs import config
from mkdocs.config import config_options as co

from .glossary import Glossary

log = logging.getLogger("mkdocs.plugins.ezglossary")


class __re:
    def __init__(self):
        self.section = r"(\w+)"
        self.term = r"([\w -]+)"
        self.text = r"([^>]+)"
        self.dt = rf"<dt>{self.section}:{self.term}<\/dt>"
        self.dd = r"<dd>\n?((.|\n)+?)<\/dd>"
        self.options = r"([\w\+]+)"


_re = __re()


class GlossaryConfig(config.base.Config):
    strict = config.config_options.Type(bool, default=False)
    tooltip = config.config_options.Choice(('none', 'heading', 'full'), default="none")
    sections = co.ListOfItems(co.Type(str), default=[])
    list_references = config.config_options.Type(bool, default=True)
    list_definitions = config.config_options.Type(bool, default=True)


class GlossaryPlugin(BasePlugin[GlossaryConfig]):
    def __init__(self):
        self._glossary = Glossary()
        self._uuid = "6251a85a-47d0-11ee-be56-0242ac120002"

    def on_pre_build(self, config, **kwargs):
        self.sections = self.config['sections']
        self.strict = self.config['strict']
        self.list_references = self.config['list_references']
        self.list_definitions = self.config['list_definitions']
        self.tooltip = self.config['tooltip']

        if self.strict and len(self.sections) == 0:
            log.error("ezglossary: no sections defined, but 'strict' is true, plugin disabled")
        self._glossary.clear()

    @event_priority(5000)
    def on_page_content(self, content, page, config, files):
        content = self._update_glossary(content, page)
        content = self._register_glossary_links(content, page)
        return content

    def on_post_page(self, output, page, config):
        _dir = os.path.dirname(page.url)
        levels = len(_dir.split("/"))
        root = "../" * levels
        output = self._replace_glossary_links(output, page, root)
        output = self._print_glossary(output, root)
        return output

    def _add_items(self, html, root, heading, entries):
        if len(entries) == 0:
            return html
        for (_id, data) in entries.items():
            (page, desc) = data
            html += f'''
            <li>
                <a href="{root}{page.url}#{_id}">{page.title}</a>
                <small>[{heading[:-1]}]</small>
            </li>'''
        return html

    def _print_glossary(self, html, root):
        def _replace(mo):
            section = mo.group(1)
            options = mo.group(2) or ""

            lr = "do_refs" in options
            if "no_refs" not in options and "do_refs" not in options:
                lr = self.list_references

            ld = "do_defs" in options
            if "no_defs" not in options and "do_defs" not in options:
                ld = self.list_references

            if not lr and not ld:
                log.warning("list_definitons and list_references disabled, summary will be empty")

            html = '<dl class="mkdocs-glossary">'
            if not self._glossary.has(section=section):
                log.warning(f"no section '{section}' found in glossary")
            terms = self._glossary.terms(section)
            for term in terms:
                html += f'<dt>{term}<dt><dd><ul>'
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

    def _update_glossary(self, content, page):
        def _replace(mo):
            section = mo.group(1)
            term = mo.group(2)
            if self.tooltip != "none":
                desc = mo.group(3)
            else:
                desc = ""

            _desc = desc.split("\n")[0] if self.tooltip == "heading" else desc
            if section not in self.sections and self.strict:
                log.warning(f"ignoring undefined section '{section}' [{mo.group()}] in glossary")
                return mo.group()
            _id = self._glossary.add(section, term, 'defs', page, _desc)
            if self.tooltip == "none":
                return f'<dt><a name="{_id}">{term}</a></dt>'
            return f'<dt><a name="{_id}">{term}</a></dt><dd>{desc}</dd>'

        regex_full = re.compile(rf"{_re.dt}\n*{_re.dd}", re.MULTILINE)
        regex_head = re.compile(r"<dt>(\w+)\:(\w+)\|?(\w*)?<\/dt>")
        regex = regex_head if self.tooltip == "none" else regex_full
        ret = re.sub(regex, _replace, content)
        return ret


def _html2text(content):
    class HTMLFilter(html.parser.HTMLParser):
        text = ""

        def handle_data(self, data):
            self.text += data

    f = HTMLFilter()
    f.feed(content)
    return f.text
