# Glossary Summary

## Basic Usage

To create a summary of all definitions and references for a glossary section,
add a summary tag anywhere in your documentation:

```markdown
# Terms and Definitions

<glossary::demo>
```

!!! Example

    Let's generate a summary for the section `demo`:

    ```markdown
    # Demo Terms

    <glossary::demo>
    ```

    This will produce the following summary, containing links to all definitions
    and references of terms in your documentation:

    !!! Quote "Output"

        <glossary::demo>

## Customizing Output

You can override the default behavior for `list_definitions` and
`list_references` by adding modifiers to the glossary reference:

```markdown
<glossary::demo|no_refs>
```

!!! Note

    When using modifiers in tables, you need to escape the `|` character:

    ```markdown
    | Column 1                  | Column 2 |
    |---------------------------|----------|
    | <glossary:demo\|no_refs> | ...      |
    ```

### Available Modifiers

#### `no_refs`
>   Exclude reference links from the summary.
    
```markdown
<glossary::demo|no_refs>
```

!!! Quote "Output"

    <glossary::demo|no_refs>

#### `no_defs`
>   Exclude definitions from the summary.

```markdown
<glossary::demo|no_defs>
```

!!! Quote "Output"

    <glossary::demo|no_defs>

#### `do_defs` and `do_refs`
>   Explicitly include definitions and/or references.

```markdown
<glossary::demo|do_defs+do_refs>
```

!!! Quote "Output"

    <glossary::demo|do_defs+do_refs>

## Configuration

configuration:list_definitions
:   Controls whether definitions appear in the summary. Default is `true`.

=== "Global Configuration"

    ```yaml
    plugins:
        - search
        - ezglossary:
            - list_definitions: false
    ```

=== "Section-specific Configuration"

    ```yaml
    plugins:
        - search
        - ezglossary:
            sections:
                demo
            section_config:
                - name: demo
                  list_references = true

            - list_definitions: false
    ```

configuration:list_references
:   Controls whether references appear in the summary. Default is `true`.

=== "Global Configuration"

    ```yaml
    plugins:
        - ezglossary:
            - list_references: false
    ```

=== "Section-specific Configuration"

    ```yaml
    plugins:
        - search
        - ezglossary:
            sections:
                demo
            section_config:
                - name: demo
                  list_references = true

            - list_references: false
    ```

## Themes

You can customize the summary appearance by passing a `theme` option:

```markdown
<glossary::demo|theme=detailed>
```

The theme option loads a custom Jinja template named `summary-<theme>.html`.

!!! Example

    This theme shows the term definitions in the glossary:

    !!! Quote "Output"

        <glossary::demo|theme=detailed>

### Available Themes

detailed
:   Displays the term definition in the summary.

table
:   Presents the summary in a tabular format.

## Further Reading

- See [sections](sections.md) documentation for section configuration details.
- Check [customization](customization.md) for creating custom summary templates.
