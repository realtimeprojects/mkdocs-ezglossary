# Printing a summary

## Basic

Place a <term:summary> of all definitions for a <term:section>
anywhere in your documentation:

``` markdown
# Terms and Definitions

<glossary::demo>
```

!!! Example

    Lets generate the summary for the section `term`:

    ``` markdown
    # Demo terms

    <glossary::demo>
    ```

    This will produce the following summary. Note that the summary contains
    links to all definitions (`def`) and references (`ref`) to all terms
    in your documentation:

    !!! Quote "Output"

        <glossary::demo>

## Overriding the output behaviour

Override the default values for <configuration:list_definitions> and
<configuration:list_references> by placing a modifier behind the glossary
reference:

```markdown
    <glossary::demo|no_refs>
```

=== "no_refs"

    Reference:

    ```
    <glossary::demo|no_refs>
    ```

    !!! Quote "output"

        <glossary::demo|no_refs>

=== "no_defs"

    Reference:

    ```
    <glossary::demo|no_defs>
    ```

    !!! Quote "output"

        <glossary::demo|no_defs>

=== "do_defs and do_refs"

    Reference:

    ```
    <glossary::demo|do_defs+do_refs>
    ```

    !!! Quote "output"

        <glossary::demo|do_defs+do_refs>

## Configuration

configuration:list_definitions
:   If set to `false`, definitions are not listed in the [summary](summary.md). Default
    is `true`.

    === "Global"

        ``` markdown
        plugins:
            - search
            - ezglossary:
                - list_definitions: false
        ```

    === "Per section"

        ``` markdown
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
:   If set to `false`, references are not listed in the [summary](summary.md). Default
    is `true`.

    === "Global"

        ``` markdown
        plugins:
            - search
            - ezglossary:
                - list_references: false
        ```

    === "Per section"

        ``` markdown
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

Passing a `theme` option to the `<glossary::section>` statement will
load a customized jinja template for that theme named `summary-<theme>.html`.

``` markdown
<glossary::demo|theme=detailed>
```

!!! Example

    This theme shows the term definitions in the glossary:

    !!! Quote

        <glossary::demo|theme=detailed>

Available themes are:

detailed:
:    Shows the definition of the term in the summary.

## Further reading

-   Read the [sections](sections.md) documentation to see how to configure sections.
