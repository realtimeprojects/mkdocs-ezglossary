# Linking to a glossary entry

## Basic

Link to this glossary definition using the following
syntax. This will produce a link to the definition in your documentation:

``` markdown
-   See the <section:term> for details
```

!!! Example

    Link to the previously defined `glossary` term in the `term` section:

    ``` markdown
    -   See the <demo:my_term1> for definition of term 1
    -   See the <demo:my term 2> for definition of term 2
    ```

    -   See the <demo:my_term1> for definition of term 1
    -   See the <demo:my term 2> for definition of term 1

## Individual reference texts

By default the <term:term> is used as text for the link, however,
you can override the term using the `|` modifier:

!!! Example

    ``` markdown
    -   You can define multiple <term:section|glossary sections>
    ```

    -   You can define multiple <term:section|glossary sections>

## Tooltips

The <configuration:tooltip> configuration allows you to control wether
tooltips should be desplayed with a preview on the definition:

```markdown
plugins:
    search
    ezglossary:
        - tooltips: [none, heading, full]
```

Options:

none
:   Tooltips are disabled

heading
:   The <term:reference> link shows the first line of the definition as a tooltip
    (link title)

full
:   The reference link shows the full definition as a tooltip.

!!! Example

    ```markdown
    plugins:
        search
        ezglossary:
            - tooltips: full
    ```

    !!! Quote "Active tooltips"

        ![](../static/tooltip-full.png)


## Configuration

configuration:tooltip
:   Configure [tooltips](#tooltips) for reference links. Default is `none`.
