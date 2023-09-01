import logging
import mock

from lxml import etree
from yaxp import xpath


log = logging.getLogger(__name__)


def test_default_config(simple, config):
    html = mock.render(simple, config)
    tree = etree.fromstring(html)
    log.debug(html)
    cc = []
    link = xpath.a(name="test_first_defs_0", text="first")
    cc.append(f'[./dt{link}]')
    cc.append('[./dd[text()="first term"]]')
    xp = f'/dl{"".join(cc)}'
    log.debug(xp)
    assert len(tree.xpath(xp))
