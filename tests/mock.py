from mkdocs_ezglossary_plugin.plugin import GlossaryPlugin


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


def render(page, config):
    files = []
    plugin = GlossaryPlugin()
    plugin.config = config
    plugin.on_pre_build(config)
    html = plugin.on_page_content(page.html, page, config, files)
    return plugin.on_post_page(html, page, config)
