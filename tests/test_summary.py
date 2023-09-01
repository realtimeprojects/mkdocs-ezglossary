import logging

from lxml import etree
from yaxp import xpath as xp

import mock

log = logging.getLogger(__name__)


def test_summary(simple, summary, config):
    config['inline_refs'] = "short"
    pages = mock.render([simple, summary], config)
    summary = pages["summary.md"]
    log.debug(summary)
    tree = etree.fromstring(summary)

    dl = xp.dl(_class="mkdocs-glossary", _id="test")
    assert len(tree.xpath(str(dl))) == 1
