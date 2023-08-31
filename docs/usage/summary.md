# Printing a summary

## Basic

Place a <term:summary> of all definitions for a <term:section>
anywhere in your documentation:

``` markdown
# Terms and Definitions

<glossary::section>
```

!!! Example

    Lets generate the summary for the section `term`:

    ``` markdown
    # Terms and Definitions

    <glossary::term>
    ```

    This will produce the following summary. Note that the summary contains
    links to all definitions (`def`) and references (`ref`) to all terms
    in your documentation:

    !!! Quote "Output"

        <glossary::term>

## Configuration

configuration:list_references
:   If set to `false`, references are not listed in the [summary](summary.md). Default
    is `true`.

    ``` markdown
    plugins:
        - search
        - ezglossary:
            - list_references: false
    ```
## Further reading

-   Read the [sections](sections.md) documentation to see how to configure sections.
