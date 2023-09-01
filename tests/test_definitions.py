import logging
import mock

from lxml import etree

log = logging.getLogger(__name__)


def test_default_page(simple, config):
    html = mock.render(simple, config)
    tree = etree.fromstring(html)
    log.debug(html)
    cc = []
    # cc.append('[//dt/a[@name="test_first_defs_0", @text="first"]')
    cc.append('[.//dd[text()="first term"]]')
    xp = f'/dl{"".join(cc)}'
    log.debug(xp)
    assert len(tree.xpath(xp))
