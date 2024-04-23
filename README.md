# mkdocs ezglossary plugin
> Glossary support for mkdocs.

## Features

-   Defining multiple glossaries
-   Linking to glossary entries in text
-   Printing a summary of your glossary with definitions and
    references anywhere in your documentation.
-   Customizable output
-   Unicode support
-   PDF support

## Documentation

-   Read the [full documentation](https://realtimeprojects.github.io/mkdocs-ezglossary)

## Prerequisites

This plugin requires the
[material definition lists](https://squidfunk.github.io/mkdocs-material/reference/lists/)
to be active or any other plugin which generates
[html description lists](https://www.w3schools.com/HTML/html_lists.asp).

## Installation

    pip install mkdocs-ezglossary-plugin

## Quickstart

### Activation

Add the following lines to your mkdocs.yml plugins section:

``` yaml
plugins:
  - search
  - ezglossary
```

### Defining glossary entries

Provided you use the material definition list, adding a glossary entry
just works by adding a definition list with section specifiers anywhere
in your documentation:

``` markdown
section:term
:   A list of specialized words with their definitions
```

### Linking to a glossary entry

You can now link to this glossary definition using the following
syntax. This will produce a link to the definition in your documentation:

``` markdown
-   See the <section:term> for details
```

### Printing a summary

Now you can place a summary of all definitions anywhere in your
documentation:

``` markdown
# Terms and Definitions

<glossary::section>
```
