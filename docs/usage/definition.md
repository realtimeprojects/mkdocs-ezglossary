# Defining Glossary Terms

## Basic Usage

ezglossary uses [Material definition lists](https://squidfunk.github.io/mkdocs-material/reference/lists/)
to define glossary terms. Simply add a definition list with section specifiers anywhere
in your documentation:

!!! Note
    Alternatively, you can directly use [html description lists](https://www.w3schools.com/HTML/html_lists.asp)
    in your page as well.

```markdown
term:glossary
:   A list of specialized words with their definitions
```

The format is `section:term`, where `section` specifies the glossary section
this term belongs to.

!!! Note
    You can also use [HTML description lists](https://www.w3.org/TR/html401/struct/lists.html#h-10.3)
    directly in your page.

!!! Example

    Define terms in the section `demo`:

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

## Text Formatting

You can use Markdown formatting in your definitions:

```markdown
demo:formatted_term
:   A term with **bold**, *italic*, and `code` formatting.
    
    You can even use multiple paragraphs and other Markdown elements:
    - Lists
    - Tables
    - Code blocks
```

## Reference Links

By setting `inline_refs` in your configuration, you can enable reference links
directly in term definitions:

```yaml
plugins:
    ezglossary:
        inline_refs: short  # Options: none, short, list
```

Or configure it per section:

```yaml
plugins:
    ezglossary:
        section_config:
            - name: demo
              inline_refs: short
```

## Special Characters

The following characters require special handling in section names and terms.
Replace them with their HTML entities:

| Character | HTML Entity | Usage |
|-----------|------------|-------|
| `#` (start) | `&#35;` | Section/term starting with # |
| `&` (start) | `&amp;` | Section/term starting with & |
| `/` | `&#47;` | Path separator |
| `\|` | `&#166;` | Vertical bar |
| `"` | `&quot;` | Double quote |
| `<` | `&#lt;` | Less than |
| `>` | `&#gt;` | Greater than |
| `:` | `&#58;` | Colon |
| `@` | `&#64;` | At sign |

!!! Example

    ```markdown
    demo:special&#35;term
    :   A term using the # character

    Reference: <demo:special&#35;term>
    ```

## Configuration

configuration:ignore_case
:   When enabled, terms are matched case-insensitively. Default: `false`

    ```yaml
    plugins:
        ezglossary:
            ignore_case: true
    ```

configuration:inline_refs
:   Controls how references appear in term definitions. Options:
    - `none` (default): No inline references
    - `short`: Numbered references like `[1]`
    - `list`: Full reference list with page names

    ```yaml
    plugins:
        ezglossary:
            inline_refs: short
    ```

## Further Reading

- [Linking to Terms](linking.md): Learn how to reference defined terms
- [Sections](sections.md): Organize terms in different sections
- [Summary](summary.md): Generate glossary summaries
