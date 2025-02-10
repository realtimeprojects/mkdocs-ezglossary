# Linking to Glossary Terms

## Basic Usage

To link to a glossary term, use the following syntax:

```markdown
See the <section:term> for more details
```

This creates a link to the term's definition in your documentation.

!!! Example

    ```markdown
    See the <demo:my_term1> for definition of term 1
    See the <demo:my term 2> for definition of term 2
    ```

    Output:
    - See the <demo:my_term1> for definition of term 1
    - See the <demo:my term 2> for definition of term 2

## Case Sensitivity
> Available since version 1.7.0

By default, term definitions and references are case-sensitive. You must use
the exact spelling in your links as used in the term definition.

To enable case-insensitive matching, set `ignore_case` to `true`:

```yaml
plugins:
    ezglossary:
        ignore_case: true
```

!!! Example
    With `ignore_case: true`, all these links point to the same term:
    ```markdown
    - <demo:my_term>
    - <demo:My_Term>
    - <demo:MY_TERM>
    ```

## Custom Link Text

By default, the term itself is used as the link text. You can override this
using the `|` modifier:

```markdown
See our <term:section|glossary sections> documentation
```

!!! Example
    ```markdown
    Learn about <demo:my_term1|our first concept>
    ```

    Output:
    - Learn about <demo:my_term1|our first concept>

!!! Note
    When using custom link text in tables, escape the `|` character:
    ```markdown
    | Description | Reference |
    |------------|-----------|
    | First term | <demo:first_term\|see details> |
    ```

## Handling Plurals
> Available since version 1.7.0

The plugin can automatically match plural forms to their singular definitions.
This is useful when you want to use the plural form in your text while linking
to the singular definition.

!!! Example
    Definition:
    ```markdown
    GPU
    :   A Graphics Processing Unit is...
    ```

    Usage:
    ```markdown
    Many <term:GPUs> support parallel processing
    ```

### Supported Languages

Plural handling is available for:
- English (en)
- Spanish (es)
- French (fr)
- German (de)

Enable plural handling in your configuration:

```yaml
plugins:
    ezglossary:
        plurals: en  # Use 'en', 'es', 'fr', or 'de'
```

### Plural Lookup Methods

#### Using the inflect Library

The [inflect library](https://github.com/jaraco/inflect) provides robust plural-to-singular
conversion for English terms:

```yaml
plugins:
    ezglossary:
        plurals: inflect
```

#### Using Built-in Rules

The plugin includes basic plural rules for supported languages:

```yaml
plugins:
    ezglossary:
        plurals: en  # or 'es', 'fr', 'de'
```

## Using Markdown Links
> Available since version 1.6.0

When <configuration:markdown_links> is enabled, the plugin also processes standard Markdown links:

```yaml
plugins:
    ezglossary:
        markdown_links: true
```

This is especially useful for:
- Terms containing Unicode characters
- Terms with emojis
- Integration with other Markdown tools

!!! Example
    ```markdown
    - See [](configuration:tooltip) for details
    - See [tooltips](configuration:tooltip) for details
    ```

    Output:
    - See [](configuration:tooltip) for details
    - See [tooltips](configuration:tooltip) for details

## Tooltips

Control whether hovering over links shows definition previews using the <configuration:tooltip> option:

```yaml
plugins:
    ezglossary:
        tooltip: short  # Options: none, short, full
```

Options:
- `none`: No tooltips (default)
- `short`: Show first line of definition
- `full`: Show complete definition

!!! Example
    With `tooltip: full`:
    
    ![Tooltip Example](../static/tooltip-full.png)

## Configuration

configuration:tooltip
:   Configure [tooltips](#tooltips) for reference links. Default: `none`

configuration:plurals
:   Configure plural handling. Options: `none` (default), `en`, `es`, `fr`, `de`, `inflect`

configuration:ignore_case
:   Enable case-insensitive term matching. Default: `false`

configuration:markdown_links
:   Enable processing of standard Markdown links. Default: `false`
