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
                <div id="test">
                <dl>
                    <dt>test:first</dt>
                    <dd>first term</dd>
                    <dt>test:second</dt>
                    <dd>second term</dd>
                    <dt>test:third</dt>
                    <dd>third term</dd>
                </dl>
                </div>
                <div id="demo">
                <dl>
                    <dt>demo:first</dt>
                    <dd>demo 1</dd>
                    <dt>demo:second</dt>
                    <dd>demo 2</dd>
                    <dt>demo:third</dt>
                    <dd>demo 3</dd>
                </dl>
                </div>

                <p>See <test:third> for details.</p>
            </body>
        """
    )
    return mock.Page.fromdict(_simple)


@pytest.fixture
def summary():
    _simple = dict(
        file="summary.md",
        title="Summary",
        html="""
            <body>
                <div id="test">
                    <glossary::test>
                </div>

                <div id="demo">
                    <glossary::demo>
                </div>
            </body>
        """
    )
    return mock.Page.fromdict(_simple)
