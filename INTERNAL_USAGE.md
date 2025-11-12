# Internal Use Instructions for mkdocs-ezglossary-plugin

This document provides instructions for using this modified mkdocs-ezglossary plugin internally at Simspace.

## Overview

This is a fork of the [mkdocs-ezglossary plugin](https://github.com/realtimeprojects/mkdocs-ezglossary) with additional functionality for section-specific search exclusion. The plugin allows you to exclude specific glossary sections from appearing in MkDocs search results while keeping them visible in the documentation.

## New Features

- **Section-specific search exclusion**: Configure individual glossary sections to be excluded from search indexing
- **Backward compatibility**: All existing functionality preserved
- **Generic implementation**: Works with any user-defined glossary sections

## Installation for Internal Projects

### Using uv (Recommended)

Add this to your `pyproject.toml` dependencies:

```toml
dependencies = [
    "mkdocs-ezglossary-plugin @ git+ssh://git@github.com/Simspace/mkdocs-ezglossary-sim.git@v2.1.0",
    # ... other dependencies
]
```

Or for development dependencies:

```toml
[project.optional-dependencies]
dev = [
    "mkdocs-ezglossary-plugin @ git+ssh://git@github.com/Simspace/mkdocs-ezglossary-sim.git@v2.1.0",
    # ... other dev dependencies  
]
```

Then install with:
```bash
uv sync
```

### Using pip

```bash
pip install git+ssh://git@github.com/Simspace/mkdocs-ezglossary-sim.git@v2.1.0
```

### GitHub Actions Setup

For CI/CD workflows, you'll need to set up SSH key access. Add a secret called `GH_SSH_KEY_FOR_EZGLOSSARY` to your repository with an SSH private key that has access to this repository.

Example workflow step:
```yaml
- name: Setup SSH key for private repos
  uses: webfactory/ssh-agent@v0.9.0
  with:
    ssh-private-key: ${{ secrets.GH_SSH_KEY_FOR_EZGLOSSARY }}

- name: Install dependencies
  run: |
    uv sync
```

## Configuration

### Basic Configuration

```yaml
plugins:
  - ezglossary:
      sections: [main, internal, roles, deprecated]
```

### Section-Specific Search Exclusion

To exclude specific sections from search results:

```yaml
plugins:
  - ezglossary:
      sections: [main, internal, roles, deprecated]
      section_config:
        - name: internal
          exclude_from_search: true
        - name: deprecated  
          exclude_from_search: true
```

### Global Search Exclusion

To exclude all glossary content from search:

```yaml
plugins:
  - ezglossary:
      exclude_from_search: true
```

## Version Management

This project uses semantic versioning with git tags. Available versions:

- `v2.1.0` - Current version with section-specific exclude_from_search functionality
- Use `@main` for the latest development version (not recommended for production)

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone git@github.com:Simspace/mkdocs-ezglossary-sim.git
cd mkdocs-ezglossary-sim

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Install dependencies
uv sync --dev

# Run tests
uv run pytest
uv run tox
```

### Making Changes

1. Create a feature branch
2. Make your changes
3. Run tests: `uv run pytest`
4. Update version in `pyproject.toml` if needed
5. Create a pull request

### Creating a New Release

1. Update version in `pyproject.toml`
2. Commit the version change
3. Create and push a git tag:
   ```bash
   git tag v2.2.0
   git push origin v2.2.0
   ```
4. Projects can then reference the new version

## Support

For issues or questions:
- Create an issue in this repository
- Contact the maintainer: stephanie.fuller@simspace.com

## License

MIT License - see LICENSE file for details.