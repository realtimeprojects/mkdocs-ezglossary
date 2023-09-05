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
        templates:
        use_default: false
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
                    <dd>second term
                        this <em>text</em> is formatted
                    </dd>
                    <dt>test:third</dt>
                    <dd>
                        third term

                        detailed description of third term
                    </dd>
                </dl>
                <dl>
                    <dt>default</dt>
                    <dd>default term</dd>
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
                <p>See <test:second> for details.</p>
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

                <div id="demo">
                    <glossary::_>
                </div>

                <p>See <test:third> for details</p>
                <p>See <:default> for details</p>
            </body>
        """
    )
    return mock.Page.fromdict(_simple)


@pytest.fixture
def tablesummary():
    return mock.Page(
        file="tablesummary.md",
        title="Summary",
        ctype="html",
        content="""
            <body>
                <div id="demo">
                    <glossary::demo|theme=table>
                </div>
            </body>
        """)
