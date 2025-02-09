# mkdocs-ezglossary-plugin

> A powerful glossary plugin for MkDocs

## Features

- Multiple glossary sections
- Case-sensitive and case-insensitive term matching
- Rich text formatting in definitions
- Reference tracking and linking
- Customizable summaries
- Unicode support
- PDF export support
- Custom templates via Jinja2
- Plural forms support (English)

## Documentation

📚 Read the [full documentation](https://realtimeprojects.github.io/mkdocs-ezglossary)

## Prerequisites

This plugin requires one of:
- [Material for MkDocs definition lists](https://squidfunk.github.io/mkdocs-material/reference/lists/) (recommended)
- Any plugin that generates [HTML description lists](https://www.w3schools.com/HTML/html_lists.asp)

## Installation

```bash
pip install mkdocs-ezglossary-plugin
```

## Quick Start

### 1. Enable the Plugin

Add ezglossary to your mkdocs.yml:

```yaml
plugins:
  - search
  - ezglossary
```

### 2. Define Terms

Add glossary terms anywhere in your documentation:

```markdown
section:term
:   A list of specialized words with their definitions
```

### 3. Link to Terms

Reference terms in your documentation:

```markdown
See the <glossary:term> for more details.
```

### 4. Create a Summary

Generate a summary of all terms:

```markdown
# Glossary

<glossary::glossary>
```

## Configuration

Basic configuration options:

```yaml
plugins:
  - ezglossary:
      # Case-insensitive term matching
      ignore_case: true
      
      # Show references in definitions
      inline_refs: short  # none, short, list
      
      # Enable plural forms (English)
      plurals: en  # none, en
      
      # Custom templates directory
      templates: docs/templates
```

See the [configuration documentation](https://realtimeprojects.github.io/mkdocs-ezglossary/configuration) for all options.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

`mkdocs-ezglossary-plugin` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
