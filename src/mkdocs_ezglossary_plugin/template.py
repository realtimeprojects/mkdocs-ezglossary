import os

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

import logging

env = Environment(
    loader=PackageLoader("mkdocs_ezglossary_plugin"),
    autoescape=select_autoescape()
)


def load(file, config):
    logging.error(f"--* {config}")
    if not config.templates:
        return env.get_template(file)
    if not os.path.exists(os.path.join(config.templates, file)):
        return env.get_template(file)

    templateLoader = FileSystemLoader(searchpath=config.templates)
    templateEnv = Environment(loader=templateLoader)
    return templateEnv.get_template(file)
