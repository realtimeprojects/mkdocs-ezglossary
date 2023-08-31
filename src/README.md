# mkdocs glossary plugin

## Features

This plugin adds glossary support for mkdocs. It supports

-   Defining multiple glossaries
-   Linking to glossary entries in text
-   Printing a summary of your glossary with definitions and
    references anywhere in your documentation.

## Prerequisites

This plugin requires the
[material definition lists](https://squidfunk.github.io/mkdocs-material/reference/lists/)
to be active or any other plugin which generates
[html description lists](https://www.w3schools.com/HTML/html_lists.asp).

## Installation

<TBD>

## Usage

### Activation

Add the following lines to your mkdocs.yml plugins section:

``` yaml
plugins:
  - search
  - glossary
```

### Defining glossary entries

Provided you use the material definition list, adding a glossary entry
just works by adding a definition list with section specifiers anywhere
in your documentation:

``` markdown
section:term
:   My definition
```

!!! Example:

    ``` markdown
    terms:glossary
    :   A list of specialized words with their definitions
    ```

### Linking to a glossary entry

You can now link to this glossary definition using the following
syntax. This will produce a link to the definition in your documentation:

``` markdown
-   See the <section:term> for details
```

!!! Example:

    ``` markdown
    -   See the <terms:glossary> for details
    ```

### Printing a summery

Now you can place a summary of all definitions anywhere in your
documentation:

``` markdown
# Terms and Definitions

<glossary::term>
```
