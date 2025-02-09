# Customization

ezglossary supports customizing the generated HTML via the Jinja2
template engine.

To customize the generated HTML, add the `templates` configuration option
pointing to a directory containing the Jinja2 templates for each output:

```yaml
plugins:
    ezglossary:
        templates: docs/templates
```

The content of the templates directory should look like this:

```text
docs/
    templates/
        links.html          # template for the reference links
        definition.html     # template for term definitions
        refs-short.html     # template for references in 'short' mode
        refs-long.html      # template for references in 'long' mode
        summary.html        # template for the summary
```

## Reference Links

The `links.html` template allows customization of the
[reference links](linking.md) (`<section:term>`).

The default template looks like this:

```jinja
<a class="mkdocs-ezglossary-link"
    id="{{ target }}"
    title="{{ entry.definition }}"
    href="{{ root }}{{ entry.page.url }}#{{ entry.target }}">{{ text }}</a>
```

See [variables](#variables) for a detailed description of the available variables.

## Reference List in Term Definition

The `refs-short.html` and `refs-long.html` templates render the
reference links in the [term definition](definition.md).

See the `inline_refs` configuration option to learn how to
enable the reference list in term definitions.

The default template for the short mode looks like this:

```jinja
<div class="mkdocs-ezglossary-refs short">
    {% set counter = 0 %}
    {% for entry in entries %}
        {% set counter = counter + 1 %}
        <span>
            <a title="{{ entry.page.title }}"
               href="{{ root }}{{ entry.page.url }}#{{ entry.target }}">
                [{{ counter }}]
            </a>
        </span>    
    {% endfor %}
</div>
```

## Term Definition

The `definition.html` template is used for rendering term definitions:

```jinja
<dt>
    <a id="{{ target }}">{{ term }}</a>
</dt>
<dd>
    {{ definition|safe }}
    <br>
    {{ reflink }}
</dd>
```

!!! Note
    Use the "safe" filter to avoid HTML escaping for the
    definition content.

## Summary

The `summary.html` template renders the [summary](summary.md) output:

```jinja
<dl class="mkdocs-ezglossary-summary" id="{{ section }}">
    {% for term in terms %}
    <dt>{{term}}</dt>
    <dd>
        <ul>
            {% for type in types %}
                {% for entry in glossary.get(section, term, type) %}
                    <li>
                        <a href="{{ root }}{{ entry.page.url }}#{{ entry.target }}">{{ entry.page.title }}</a>
                        <small>[{{ type[:-1] }}]</small>
                    </li>
                {% endfor %}
            {% endfor %}
        </ul>
    </dd>
    {% endfor %}
</dl>
```

!!! Note
    Summaries support [custom themes](summary.md#themes)

## Variables

target
:   The anchor ID for this link entry, used to support direct linking from the
    [summary](summary.md) or [definition](definition.md).

entries
:   A list of [Entry][mkdocs_ezglossary_plugin.glossary.Entry] objects
    representing each reference to this term.

entry
:   An instance of [Entry][mkdocs_ezglossary_plugin.glossary.Entry]
    describing the definition of this term.

root
:   A prefix containing the relative path to the root directory.

glossary
:   The [Glossary][mkdocs_ezglossary_plugin.glossary.Glossary]
    instance holding the complete glossary.

terms
:   The list of terms in this glossary section.

text
:   The original link text.

section
:   The current section for this summary.

types
:   A list of types to display in this summary.
    Contains one or more of: `refs`, `defs`.

reflink
:   An internal reference link used for post-processing
    and injection of reference links.

## Configuration

configuration:template
:   Directory path containing Jinja2 templates for customizing the output.
    If set, templates are loaded from this directory when the files exist.
    The path is relative to the location of your mkdocs.yml file.

