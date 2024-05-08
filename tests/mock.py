from lxml import etree
import logging

from mkdocs_ezglossary_plugin.plugin import GlossaryPlugin

log = logging.getLogger()


class Config(dict):
    def __getattr__(self, name):
        return self.get(name)


class Page:
    def __init__(self, title: str, file: str, content: str, ctype="html", meta={}):
        self.file = file
        self.title = title
        self.content = content
        self.ctype = ctype
        self.meta = meta

    @property
    def url(self):
        return self.file

    @property
    def canonical_url(self):
        return f"/{self.file.rsplit('.', maxsplit=1)[0]}/"

    @staticmethod
    def fromdict(data: dict):
        return Page(data['title'], data['file'], data['html'])

    def __repr__(self):
        return f"Page({self.title}, {self.file})"


def render_single(page, config):
    return render([page], config)[page.url]


def render(pages, config):
    parser = etree.XMLParser(recover=True)
    files = []
    results = {}
    plugin = GlossaryPlugin()
    plugin.config = config
    plugin.on_pre_build(config)
    for page in pages:
        if page.ctype == "markdown":
            results[page.url] = plugin.on_page_markdown(page.content, page, config, files)
    for page in pages:
        if page.ctype == "html":
            results[page.url] = plugin.on_page_content(page.content, page, config, files)
    for page in pages:
        if page.ctype == "html":
            results[page.url] = plugin.on_post_page(results[page.url], page, config)
    for page in pages:
        fp = open(page.url + "." + page.ctype, "w", encoding="utf-8")
        fp.write(results[page.url])
        fp.close()
        log.debug(f"--- >>> {page.url}")
        log.debug(results[page.url])
        log.debug(f"--- <<< {page.url}")
        if page.ctype == "html":
            results[page.url] = etree.fromstring(results[page.url], parser=parser)
    return results
