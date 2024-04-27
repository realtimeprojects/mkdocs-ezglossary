# Defining glossary entries

## Basic

Provided you use the [material definition lists](https://squidfunk.github.io/mkdocs-material/reference/lists/)
adding a glossary entry just works by adding a definition list with section specifiers anywhere
in your documentation.

!!! Note
    Alternatively, you can directly use [html description lists](https://www.w3schools.com/HTML/html_lists.asp)
    in your page as well.

``` markdown
term:glossary
:   A list of specialized words with their definitions
```

`term` herby referes to the <term:section> `terms` in which this glossary
entry will be added.

!!! Example

    Define the term `glossary` in the section `term`:

    ``` markdown
    *demo:my_term1*
    :   Definition of my_term 1

    demo:my_term2
    :   Definition of my_term 2 

    *`demo:my_term2`*
    :   Definition of my_term 2 
    ```

    *demo:my_term1*
    :   Definition of my_term 1

    demo:my term 2
    :   Definition of my term 2

    *`demo:my term 3`*
    :   Definition of my term 3

## List references

By adding the configuration entry <configuration.inline_refs> to the section configuration,
you can enable displaying reference links directly to the definition of a glossary term.

This can either be done in the global definition:

```markdown
plugins:
    ezglossary:
        inline_refs: none
```

or in the section configuration:

```markdown
plugins:
    ezglossary:
        section_config:
            - name: demo
              inline_refs: short
```

## Limitations

The following characters are not allowed to be used in <term:section|sections>
and <term:term|terms>, however, you can replace them with
[html entities](https://www.freeformatter.com/html-entities.html) if you want
to use them anyway:

| Character | Replacement |
|--------------------------------|-------------|
| `#` (as first character)       | `&#35;`     |
| `&` (as first character)       | `&amp;`     |
| `/`                            | `&#47;`     | 
| `|`                            | `&#166;`    | 
| `"`                            | `&quot;`    | 
| `<`                            | `&#lt;`     | 
| `>`                            | `&#gt;`     | 
| `:`                            | `&#58;`     | 
| `@`                            | `&#64;`     | 

!!! Example

    ``` markdown
    demo:fancy&#35;definition
    :   a term using the # character

    - See <demo:fancy&#35;definition>
    ```

    !!! Output

        demo:fency&#35;definition
        :   a term using the # character

        - See <demo:fency&#35;definition>

## Configuration

configuration:inline_refs
:   defines how to display references in the <term:definition|definitions>.

    Options:

    none [default]
    :   No inline references are linked in the term definition

    short:
    :   Short references in the format `[1]` are linked in the term definition

    list:
    :   A full list of references including the page name are added to the
        term definition.
