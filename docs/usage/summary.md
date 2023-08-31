# Printing a summary

Now you can place a <term:summary> of all definitions anywhere in your
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


