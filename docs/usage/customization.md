# Customization

ezglossary supports to customize the generated html via the jinja2
template engine.

In order to customize the generated html, add the <configuration:template>
configuration to a directory containing the jinja2 templates for each
output:

``` yaml
plugins:
    ezglossary:
        templates: docs/templates
```

The content of the templates dicrectoy should look like this:

``` text
doc/
    templates/
        links.html          # template for the reference links
        definition.html     # template for definition
        refs-short.html     # template for the references in 'short' mode
        refs-long.html      # template for the references in 'long' mode
        summary.html        # template for the summary
```

## Reference links

The `links.html` allows customization of the
[reference links](linking.md) (`<section:term>`).

The default template looks like this:

``` jinja
<a class="mkdocs-ezglossary-link"
    name="{{ target }}"
    title="{{ entry.definition }}"
    href="{{ root }}{{ entry.page.url }}#{{ entry.target }}">{{ text }}</a>
```

See [variables](#variables) for a detailed description of the variables.

## Reference list in link definition

The `refs-short.html` and `refs-long.html` render the
reference links in the [term definition](definition.md).

See the <configuration:inline_refs> configuration how to
enable the reference list in link definitions.

The default template for the short mode looks like this:

``` jinja
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

## Term definition

The `definition.html` is used for the replacement of the original
term definition.

``` jinja
<dt>
    <a name="{{ target }}">{{ term }}</a>
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

The `summary.html` renders the [summary](summary.md) output.
reference links in the [term definition](definition.md).

``` jinja
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


## Variables:

target
:   Target is the anchor to this link entry in order to
    support a direct link to this reference eitherin the
    [summary](summary.md) or in the [definition](definition.md).

entries
:   A list of [Entry][mkdocs_ezglossary_plugin.glossary.Entry] classes
    for each reference to this term. 

entry
:   A instance of the [Entry][mkdocs_ezglossary_plugin.glossary.Entry] class
    describing the definition of this term.

root
:   A prefix to the current page that contains a relative link
    to the root directory.

glossary
:   The instance of the [Glossary][mkdocs_ezglossary_plugin.glossary.Glossary]
    instance holding the complete glossary.

terms
:   The list of terms in this glossary section

text
:   The original link text

section
:   The current section for this summary

types
:   A list of types which should be displace in this summary.
    Contains one or more of this values: `refs`, `defs`.

reflink
:   A internal reference link which is used for the post-processing
    and injection of the reference links.

## Configuration

configuration:template
:   Template directory for jinja2 templates to customize the output.

    If this is set, templates are loaded from that directory, if the
    files exist.

