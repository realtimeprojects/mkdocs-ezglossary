# Sections

## Overview

The key feature of ezglossary is that you can define multiple
<term:section|glossary sections>. Like described in the [definition](definition.md) documentation,
every <term:term> is assigned to a section.

This allows [printing individual summaries](summary.md) for each <term:section>.

## Predefining sections

By default, you don't need to predefine the sections you use in your documentation.
However, in order to avoid spelling errors, you can enable the <configuration:strict> mode

If strict mode is activated, you also need to configure <configuration:sections>.

## Configuration

configuration:strict
:   If set to `true`, ezglossary prints warnings if you - define a - or - refer to -
    a term for a undefined section:

    ``` markdown
    plugins:
        - search
        - ezglossary:
            strict: true
    ```

configuration:sections
:   Defines a list of sections that are recognized by ezglossary.

    If <configuration:strict> mode is enabled, only <term:definition|definitions>
    and <term:reference|references> for a defined sections are processed by ezglossary:

    ``` markdown
    plugins:
        - search
        - ezglossary:
            strict: true
            sections:
                - terms
                - configuration
                - demo
    ```

