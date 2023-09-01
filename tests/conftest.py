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
            <body>
                <dl>
                    <dt>test:first</dt>
                    <dd>first term</dd>
                    <dt>test:second</dt>
                    <dd>second term</dd>
                    <dt>test:third</dt>
                    <dd>third term</dd>
                </dl>
                <dl>
                    <dt>demo:first</dt>
                    <dd>demo 1</dd>
                    <dt>demo:second</dt>
                    <dd>demo 2</dd>
                    <dt>demo:third</dt>
                    <dd>demo 3</dd>
                </dl>

                <p>See <test:third> for details.</p>
            </body>
        """
    )
    return mock.Page.fromdict(_simple)
