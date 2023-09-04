---
terms:
  - demo: page_reference
---

# Page references

## Overview

In case your page itself is a term definition,
It is possible to put term definition in the page's metadata:

``` markdown
---
terms:
  - <section>: <term>
---
```

If a term definition is placed in the page`s meta data, the
page is added to the glossary with the given section with an empty
description.

This allows to link to the page using the `<section:term>` syntax:

``` markdown
-   See <demo:page reference> for details
```

!!! Example

    -   See <demo:page_reference> for details

## Anchors

It is possible to refer to an title (or any other anchor in the page)
in the definition:

``` markdown
---
terms:
  - <section>: "<term>#anchor"
---
```

## Multiple terms

It is possible to define multiple terms for sections as well:

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

## Default section

Adding page references to default the [default section](default.md):

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

The page reference uses the following rules in the given order to
determine the definition of the term:

1.   If a [anchor definition](#anchor-definitions) is defined
     for the term, the anchor definition is used
2.   If a page subtitle is defined in the page meta-data, the subtitle is used
3.   The page title is used

## Anchor definitions

The anchor definitions allow to specify the definition for a term
for page references:

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
        help: Definition of help
    ---
    ```
