# Usage

## Defining glossary entries

Provided you use the material definition list, adding a glossary entry
just works by adding a definition list with section specifiers anywhere
in your documentation:

``` markdown
term:glossary
:   A list of specialized words with their definitions
```

`term` herby referes to the <termssection> `terms` in which this glossary
entry will be added.

!!! Example

    Define the term `glossary` in the section `term`:

    ``` markdown
    term:glossary
    :   A list of specialized words with their definitions
    ```

    term:glossary
    :   A list of specialized words with their definitions

## Linking to a glossary entry

Now link to this glossary definition using the following
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

## Printing a summary

Now you can place a summary of all definitions anywhere in your
documentation:

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

    <glossary::term>

## Further reading

-   Read the [sections](sections.md) documentation to see how to configure sections.

