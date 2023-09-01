import pytest
import yaml

import mock


@pytest.fixture
def config():
    _default = """
        strict: false
        list_definitions: true
        list_references: true
        inline_refs: "none"
        tooltip: "none"
        sections: []
        section_config: []
    """
    config = yaml.safe_load(_default)
    return mock.Config(**config)


@pytest.fixture
def simple():
    _simple = dict(
        file="simple.md",
        title="Hello",
        html="""
            <dl>
                <dt>test:first</dt>
                <dd>first term</dd>
            </dl>
        """
    )
    return mock.Page.fromdict(_simple)
