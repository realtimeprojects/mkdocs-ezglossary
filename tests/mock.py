from lxml import etree
import logging

from mkdocs_ezglossary_plugin.plugin import GlossaryPlugin

log = logging.getLogger()


class Config(dict):
    def __getattr__(self, name):
        return self.get(name)


class Page:
    def __init__(self, title: str, file: str, html: str):
        self.file = file
        self.title = title
        self.html = html

    @property
    def url(self):
        return self.file

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
        results[page.url] = plugin.on_page_content(page.html, page, config, files)
    for page in pages:
        results[page.url] = plugin.on_post_page(results[page.url], page, config)
    for page in pages:
        fp = open(page.url + ".html", "w")
        fp.write(results[page.url])
        fp.close()
        log.debug(f"--- {page.url}")
        log.debug(results[page.url])
        log.debug("---")
        results[page.url] = etree.fromstring(results[page.url], parser=parser)
    return results
