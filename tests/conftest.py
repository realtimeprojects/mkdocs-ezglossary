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
                    <dt>test:hyphens-abc def</dt>
                    <dd> hyphen abc def </dd>
                    <dt>test:hyphens-abc xyz</dt>
                    <dd> hyphen abc xyz </dd>
                </dl>
                <dl>
                    <dt>default</dt>
                    <dd>default term</dd>
                    <dt>default2</dt>
                    <dd>default2 term</dd>
                    <dt>default3</dt>
                    <dd>default3 term</dd>
                    <dt>🚧🚧</dt>
                    <dd>default 🚧🚧🚧</dd>
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
                    <dt><bold><em><code>demo:formatted</code></em></bold></dt>
                    <dd>formatted dd</dd>
                    <dt>demo:🚧</dt>
                    <dd>demo 🚧🚧🚧</dd>
                </dl>
                <dl>
                    <dt>plurals:GPU</dt>
                    <dd>GPU definition</dd>
                    <dt>plurals:potato</dt>
                    <dd>potato definition</dd>
                    <dt>plurals:potatoes</dt>
                    <dd>potatoes definition</dd>
                    <dt>plurals:goose</dt>
                    <dd>goose definition</dd>
                    <dt>plurals:goose</dt>
                    <dd>goose definition</dd>
                    <dt>plurals:city</dt>
                    <dd>city definition</dd>
                    <dt>plurals:child</dt>
                    <dd>children definition</dd>
                    <dt>plurals:grandchild</dt>
                    <dd>grandchild definition</dd>
                </dl>
                </div>

                <p>See <test:third> for details.</p>
                <p>See <test:second|mysecond> for details.</p>
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
                <p>See <test:third|mythird> for details.</p>
                <p>See <default:> for details</p>
                <p>See <default2:|mydef2> for details.</p>
                <p>See <default3:|mydef3> for details.</p>
                <p><a href="test:third">mythird</a></p>
                <p><a href="test:third"></a></p>
                <p>See <demo:🚧> for details.</p>
                <p>See <a href="🚧🚧">refers to 🚧</a> for details.</p>
                <p>See <test:hyphens-abc xyz> for details.</p>
                <p><a href="test:hyphens-abc def"></a></p>
                <p>See <plurals:GPUs> for details</p>
                <p>See <plurals:geese> for details</p>
                <p>See <plurals:children> for details</p>
                <p>See <plurals:cities> for details</p>
                <p>See <plurals:potatoes> for details</p>
                <p>See <plurals:grandchildren> for details</p>
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
