import pytest
from mkdocs_ezglossary_plugin.glossary import Glossary, Entry
from mock import Page

@pytest.fixture
def mock_page():
    return Page(
        title="Test Page",
        file="test.md",
        content="Test content",
        ctype="markdown"
    )

@pytest.fixture
def basic_glossary():
    return Glossary(ignore_case=False, plurals='none')

@pytest.fixture
def case_insensitive_glossary():
    return Glossary(ignore_case=True, plurals='none')

@pytest.fixture
def en_plural_glossary():
    return Glossary(ignore_case=False, plurals='en')

@pytest.fixture
def inflect_plural_glossary():
    return Glossary(ignore_case=False, plurals='inflect')

class TestGlossaryBasic:
    def test_empty_glossary(self, basic_glossary):
        assert basic_glossary.has('test') == False
        assert basic_glossary.terms('test') == []
        assert basic_glossary.get('test', 'term', 'refs') == []
        assert basic_glossary.definition('test', 'term') == ""

    def test_add_definition(self, basic_glossary, mock_page):
        id1 = basic_glossary.add('test', 'term1', 'defs', mock_page, 'Definition 1')
        assert basic_glossary.has('test')
        assert basic_glossary.terms('test') == ['term1']
        assert basic_glossary.definition('test', 'term1') == 'Definition 1'

    def test_add_reference(self, basic_glossary, mock_page):
        id1 = basic_glossary.add('test', 'term1', 'refs', mock_page)
        refs = basic_glossary.get('test', 'term1', 'refs')
        assert len(refs) == 1
        assert refs[0].page == mock_page

    def test_multiple_entries(self, basic_glossary, mock_page):
        # Add multiple definitions and references
        basic_glossary.add('test', 'term1', 'defs', mock_page, 'Definition 1')
        basic_glossary.add('test', 'term2', 'defs', mock_page, 'Definition 2')
        basic_glossary.add('test', 'term1', 'refs', mock_page)
        basic_glossary.add('test', 'term2', 'refs', mock_page)

        assert set(basic_glossary.terms('test')) == {'term1', 'term2'}
        assert len(basic_glossary.get('test', 'term1', 'refs')) == 1
        assert len(basic_glossary.get('test', 'term2', 'refs')) == 1

class TestGlossaryCaseSensitivity:
    def test_case_sensitive_match(self, basic_glossary, mock_page):
        basic_glossary.add('test', 'Term', 'defs', mock_page, 'Definition')
        assert basic_glossary.get('test', 'term', 'defs') == []
        assert basic_glossary.get('test', 'Term', 'defs') != []

    def test_case_insensitive_match(self, case_insensitive_glossary, mock_page):
        case_insensitive_glossary.add('test', 'Term', 'defs', mock_page, 'Definition')
        assert len(case_insensitive_glossary.get('test', 'term', 'defs')) == 1
        assert len(case_insensitive_glossary.get('test', 'TERM', 'defs')) == 1
        assert len(case_insensitive_glossary.get('test', 'Term', 'defs')) == 1

class TestGlossaryPlurals:
    def test_en_plural_rules(self, en_plural_glossary, mock_page):
        # Test cases as tuples of (singular, plural)
        test_cases = [
            ('cat', 'cats'),          # Basic 's' plural
            ('box', 'boxes'),         # 'es' plural
            ('city', 'cities'),       # 'y' to 'ies'
            ('knife', 'knives'),      # 'fe' to 'ves'
            ('child', 'children'),    # Irregular plural
            ('person', 'people'),     # Irregular plural
            ('mouse', 'mice'),        # Irregular plural
            ('tooth', 'teeth'),       # Irregular plural
        ]

        for singular, plural in test_cases:
            # Test singular->plural
            en_plural_glossary.add('test', singular, 'defs', mock_page, f'Definition of {singular}')
            plural_results = en_plural_glossary.get('test', plural, 'defs')
            assert len(plural_results) == 1, f"Failed to find plural '{plural}' for singular '{singular}'"
            
            # Clear and test plural->singular
            en_plural_glossary.clear()
            en_plural_glossary.add('test', plural, 'defs', mock_page, f'Definition of {plural}')
            singular_results = en_plural_glossary.get('test', singular, 'defs')
            assert len(singular_results) == 1, f"Failed to find singular '{singular}' for plural '{plural}'"
            en_plural_glossary.clear()

    @pytest.mark.inflect
    def test_inflect_plurals(self, inflect_plural_glossary, mock_page):
        # Test cases as tuples of (singular, plural)
        test_cases = [
            ('dog', 'dogs'),          # Regular plural
            ('church', 'churches'),    # 'es' plural
            ('baby', 'babies'),       # 'y' to 'ies'
            ('wife', 'wives'),        # 'fe' to 'ves'
            ('criterion', 'criteria'), # Latin plural
            # ('analysis', 'analyses'),  # Greek plural
            ('mouse', 'mice'),        # Irregular plural
            ('person', 'people'),     # Irregular plural
        ]

        for singular, plural in test_cases:
            # Test singular->plural
            inflect_plural_glossary.add('test', singular, 'defs', mock_page, f'Definition of {singular}')
            plural_results = inflect_plural_glossary.get('test', plural, 'defs')
            assert len(plural_results) == 1, f"Failed to find plural '{plural}' for singular '{singular}'"
            
            # Clear and test plural->singular
            inflect_plural_glossary.clear()
            inflect_plural_glossary.add('test', plural, 'defs', mock_page, f'Definition of {plural}')
            singular_results = inflect_plural_glossary.get('test', singular, 'defs')
            assert len(singular_results) == 1, f"Failed to find singular '{singular}' for plural '{plural}'"
            inflect_plural_glossary.clear()

    def test_no_plurals(self, basic_glossary, mock_page):
        # Test that plural matching is disabled when plurals='none'
        basic_glossary.add('test', 'cat', 'defs', mock_page, 'A feline animal')
        assert len(basic_glossary.get('test', 'cats', 'defs')) == 0
        
        basic_glossary.add('test', 'boxes', 'defs', mock_page, 'Multiple containers')
        assert len(basic_glossary.get('test', 'box', 'defs')) == 0

class TestGlossaryMultipleSections:
    def test_multiple_sections(self, basic_glossary, mock_page):
        # Add terms to different sections
        basic_glossary.add('animals', 'cat', 'defs', mock_page, 'A feline')
        basic_glossary.add('colors', 'red', 'defs', mock_page, 'A color')

        assert basic_glossary.has('animals')
        assert basic_glossary.has('colors')
        assert 'cat' in basic_glossary.terms('animals')
        assert 'red' in basic_glossary.terms('colors')
        assert 'cat' not in basic_glossary.terms('colors')

    def test_same_term_different_sections(self, basic_glossary, mock_page):
        # Add same term to different sections
        basic_glossary.add('section1', 'term', 'defs', mock_page, 'Definition 1')
        basic_glossary.add('section2', 'term', 'defs', mock_page, 'Definition 2')

        assert basic_glossary.definition('section1', 'term') == 'Definition 1'
        assert basic_glossary.definition('section2', 'term') == 'Definition 2'

class TestGlossaryEdgeCases:
    def test_clear_glossary(self, basic_glossary, mock_page):
        basic_glossary.add('test', 'term', 'defs', mock_page, 'Definition')
        basic_glossary.clear()
        assert not basic_glossary.has('test')
        assert basic_glossary.terms('test') == []

    def test_nonexistent_section(self, basic_glossary):
        assert basic_glossary.terms('nonexistent') == []
        assert basic_glossary.get('nonexistent', 'term', 'refs') == []
        assert basic_glossary.definition('nonexistent', 'term') == ''

    def test_whitespace_handling(self, basic_glossary, mock_page):
        basic_glossary.add('test', '  term  ', 'defs', mock_page, 'Definition')
        assert 'term' in basic_glossary.terms('test')
        assert basic_glossary.definition('test', 'term') == 'Definition' 