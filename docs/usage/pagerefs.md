---
terms:
  - demo: page_reference
---

# Page References

## Overview

If your page itself is a term definition, you can define the term in the page's metadata:

```markdown
---
terms:
  - <section>: <term>
---
```

When a term definition is placed in the page's metadata, the page is added to the glossary with the specified section and an empty description. This allows you to link to the page using the `<section:term>` syntax:

```markdown
- See <demo:page reference> for details
```

!!! Example

    - See <demo:page_reference> for details

## Anchors

You can refer to a title (or any other anchor in the page) in the definition:

```markdown
---
terms:
  - <section>: "<term>#anchor"
---
```

## Multiple Terms

You can define multiple terms for sections as well:

```markdown
---
terms:
  - <section>:
    - <term>
    - <term>: <anchor>
---
```

!!! Example

    ```markdown
    ---
    terms:
      - demo:
        - term1
        - term2: help
      - configuration:
        - term3
    ---
    ```

## Default Section

You can add page references to the default section:

```markdown
---
terms:
  - <term>
  - "<term>#<anchor>"
---
```

!!! Example

    ```markdown
    ---
    terms:
      - term1
      - "term2#help"
    ---
    ```

## Definitions

The page reference uses the following rules in the given order to determine the definition of the term:

1. If an [anchor definition](#anchor-definitions) is defined for the term, the anchor definition is used.
2. If a page subtitle is defined in the page metadata, the subtitle is used.
3. The page title is used.

## Anchor Definitions

Anchor definitions allow you to specify the definition for a term for page references:

```markdown
---
terms:
  ...
anchors:
  - <name>: <definition>
---
```

!!! Example

    ```markdown
    ---
    anchors:
      - help: Definition of help
    ---
    ```
