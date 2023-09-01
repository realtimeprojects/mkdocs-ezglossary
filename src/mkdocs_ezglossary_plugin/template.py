from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("mkdocs_ezglossary_plugin"),
    autoescape=select_autoescape()
)


def load(file):
    return env.get_template(file)
