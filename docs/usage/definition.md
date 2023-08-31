# Defining glossary entries

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
    demo:my_term1
    :   Definition of my_term1
    ```

    demo:my_term1
    :   Definition of my_term1

    demo:my term 2
    :   Definition of my term 2


