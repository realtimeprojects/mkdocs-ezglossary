# EZGlossary Plugin Development Guide

## Architecture Overview

This is a **MkDocs plugin** that processes glossary terms in markdown files, converting them to interactive HTML elements. The core workflow:

1. **Term Discovery**: Plugin scans for `section:term` patterns in `<dt>` elements during `on_page_content` 
2. **Glossary Building**: Terms stored in `Glossary` class with section-based organization
3. **Link Processing**: Text content gets term references replaced with HTML links during `on_page_content`
4. **Template Rendering**: Jinja2 templates in `src/mkdocs_ezglossary_plugin/templates/` generate final HTML

## Key Components

### Core Classes (`src/mkdocs_ezglossary_plugin/`)

- **`plugin.py`**: Main `GlossaryPlugin` class - MkDocs plugin entry point with event handlers
- **`glossary.py`**: `Glossary` and `Entry` classes - term storage and retrieval with UUID-based IDs
- **`template.py`**: Jinja2 template loading with custom template directory support
- **`plurals.py`**: Language-specific plural/singular mapping dictionaries

### ID Generation Pattern

All glossary entries use **deterministic MD5 hashes** via `get_id()` function:
- Definitions: `md5(f"{section.lower()}:{term.lower()}")`
- References: `md5(f"{section.lower()}:{term.lower()}:ref:{index}")`

This ensures consistent IDs across builds for stable linking.

### Term Matching Logic

**Critical**: The plugin supports three plural modes:
- `none`: Exact term matching only
- `en`: Built-in English plural rules in `plurals.py`
- `inflect`: Python inflect library for advanced pluralization

Case sensitivity controlled by `ignore_case` config option affects ALL matching operations.

## Development Workflows

### Testing
```bash
# Run all tests
tox

# Run specific test file
pytest tests/test_glossary.py

# Run tests with verbose output
pytest -v tests/
```

### Project Structure
- **Source**: `src/mkdocs_ezglossary_plugin/` (not root-level package)
- **Entry Point**: `setup.cfg` defines plugin as `ezglossary = mkdocs_ezglossary_plugin.plugin:GlossaryPlugin`
- **Templates**: Jinja2 files in `src/mkdocs_ezglossary_plugin/templates/`

### Plugin Configuration Pattern

The plugin uses `GlossaryConfig` class inheriting from `config.base.Config` with these key options:
- `sections`: List of allowed glossary sections (when `strict=True`)
- `section_config`: Per-section configuration overrides
- `templates`: Custom template directory path
- `exclude_from_search`: Hide glossary content from MkDocs search

## Project-Specific Patterns

### Regular Expression Usage

The plugin uses a centralized `__re` class in `plugin.py` defining reusable patterns:
```python
self.dt = rf"<dt>(<.*>)?{self.section}:{self.term}(<.*>)?<\/dt>"
```

### Template Variable Conventions

Templates expect these specific variables:
- `target`: Anchor ID for the element
- `term`: The glossary term text
- `definition`: Term definition content
- `reflink`: Generated reference link HTML
- `fmt_pre`/`fmt_post`: Formatting wrapper HTML

### UUID Handling

The plugin uses fixed UUIDs for internal operations:
```python
self._uuid = "6251a85a-47d0-11ee-be56-0242ac120002"
self._reflink = "886d7696-137e-4a59-a39d-6f7d311d5bd1"
```

### Error Handling Pattern

The plugin follows MkDocs conventions:
- Use `log = logging.getLogger("mkdocs.plugins.ezglossary")` 
- Log errors with descriptive context
- Gracefully degrade when optional features fail

## Testing Conventions

### Fixture Structure (`tests/conftest.py`)

Tests use YAML-based config fixtures and mock objects:
```python
@pytest.fixture
def config():
    _default = """
        strict: false
        ignore_case: false
        plurals: "none"
    """
```

### Test Organization

- `test_glossary.py`: Core `Glossary` class functionality
- `test_*`: Feature-specific test files
- `conftest.py`: Shared fixtures and mock objects
- `mock.py`: Mock MkDocs objects for testing

When modifying the glossary logic, always run plural-related tests as they have complex edge cases around language-specific rules.