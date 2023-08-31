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
    -   See the <term:glossary> for the definition of the term `glossary`
    ```

    -   See the <term:glossary> for the definition of the term `glossary`

## Modifying the output

By default the <term:term> is used as text for the link, however,
you can override the term using the `|` modifier:

!!! Example

    ``` markdown
    -   You can define multiple <term:section|glossary sections>
    ```

    -   You can define multiple <term:section|glossary sections>
