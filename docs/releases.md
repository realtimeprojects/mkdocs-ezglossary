# Release Notes

## v2.0.0
| ~2025-02-10~

-   Fix #24: Show all references in glossary (summary) when `ignore_case=true`.
-   Fix #25: Fix #25: make template file path relative to mkdocs.yml

!!! Note

    This version required major refactorying of the `Glossary` class.
    The interface to it changed. You may need to update your custom templates
    in order to work.

## v1.7.1
| ~2024-10-11~

-   Fix #22: Plural configuration did not work.

## v1.7.0
| ~2024-10-10~

-   Glossary: Add section and term as attributes of Entry
-   Links: Add name attribute containing "{section:term}"
-   Fix html entity handling.
-   Basic support of [handling plurals](usage/linking.md#handling-plurals). See
    also [#18](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/18)
-   Fix #21: Support [ignoring case for terms](usage/linking.md#case-sensitivity)
-   Fix #20: Usage of `tooltip:short`
-   Fix #19: Usage of `inline_refs:list`

## v1.6.10
| ~2024-05-08~

-   Fix handling of non-existing canonica_url.

## v1.6.9
| ~2024-05-08~

-   Fixed: [#16](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/16):
    Relative links not working on ReadTheDocs. 

## v1.6.8
| ~2024-04-24~

-   Fixed: [#15](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/15):
    Links to undefined glossary entries are displayed.

## v1.6.7
| ~2024-04-23~

-   Fixed: [#14](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/14):
    Add `&` to [list of unsupported characters for terms and section](usage/definition.md#limitations)
    to handle html-entity-encoded mailto links.

## v1.6.6
| ~2024-04-23~

-   Fixed: [#14](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/14):
    Add `@` to [list of unsupported characters for terms and section](usage/definition.md#limitations).

## v1.6.5
| ~2024-04-23~

-   Fixed: [#13](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/13):
    Support [html entities](usage/definition.md#limitations) in sections and terms.

## v1.6.4
| ~2024-04-23~

-   Fixed: [#12](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/12):
    Support [unicode characters](usage/linking.md#using-markdown-links) for terms.

## v1.6.3
| ~2024-04-22~

-   Fixed: [#11](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/11):
    Glossary entries with hyphens lead to errors.

## v1.6.2
| ~2024-04-22~

-   Removed debug warnings in logging

## v1.6.1
| ~2024-04-16~

-   Fixed: [#10](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/10):
    Links in PDF exports are not working
-   Removed debug warnings in logging

## v1.6.0
| ~2024-04-15~

-   Fixed: [#7](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/7):
    Support [markdown links](usage/linking.md) for linking of unicode characters and support for emojis.

## v1.5.9
| ~2024-04-15~

-   Fixed: [#8](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/8):
    typo on documentation for <configuration:tooltip> configuration.
-   Fixed: [#9](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/9):
    Handling linking with individual text in tables 
-   Fixed: [#9](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/9):
    Handling summaries with options in tables 
-   Fixed `no_defs`/`no_refs`/`do_defs`/`do_refs` handling in default summary theme

## v1.5.8
| ~2024-03-08~

-   Fixed typo in README.md

## v1.5.7
| ~2023-11-27~

-   Fixed: [#3](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/3)
    (Support formatting of definitions)

## v1.5.6
| ~2023-11-22~

-   Fixed: [#4](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/4)
    (Links to default section not working)

## v1.5.5
| ~2023-09-29~

-   Fix doc errors in README.md

## v1.5.4
| ~2023-09-06~

-   Fix anchor lookup for page references

## v1.5.3
| ~2023-09-06~

-   Fix error in summary-detailed template.

## v1.5.2
| ~2023-09-06~

-   Fix project description and keywords

## v1.5.1
| ~2023-09-05~

-   Directly link definition to term in summary
-   summary theme "detailed": Safe output for definition
-   summary theme "table": Safe output for definition

-   Add "[table](usage/summary.md#themes)" summary theme
## v1.5.0
| ~2023-09-05~

-   Add "[table](usage/summary.md#themes)" summary theme

## v1.4.0
| ~2023-09-04~

-   Support [page references](usage/pagerefs.md)
-   Support [themes for summary](usage/summary.md#themes)
-   Add [Glossary.definition()][mkdocs_ezglossary_plugin.glossary.Glossary.definition]

## v1.3.1
| ~2023-09-03~

-   Fix reference counter for short list

## v1.3.0
| ~2023-09-03~

-   Support [default sections](usage/default.md)

## v1.2.2
| ~2023-09-02~

-   Fix project long description

## v1.2.1
| ~2023-09-02~

-   Optimize reference list output for definition.

## v1.2.0
| ~2023-09-02~

-   Support [customizable output](usage/customization.md)

~
## v1.1.2
| ~2023-09-01~

-   fix html syntax for summary
-   add section id to summary data list

## v1.1.1
| ~2023-09-01~

-   reduce log noise
-   fix html output for inline refs
-   rename <configuration:inline_refs> value "off" to "none"

## v1.1.0
| ~2023-08-31~

-   support whitespaces and dashes in terms.
-   add <configuration:list_definitions> configuration to
    disable listing definitions in summary.
-   Support overriding <configuration:list_definitions> and
    <configuration:list_references> using `[no|do]_[refs|defs]`
    as summary modifier. See 
    [documentation](https://realtimeprojects.github.io/mkdocs-ezglossary/usage/summary#overriding-the-output-behaviour).
-   Support per-section definition of <configuration:list_definitions> and
    <configuration:list_references>
-   Support inline references in term definitions


## v1.0.4
| ~2023-08-31~

-   Fix: individual link text only allowed single words.

## v1.0.3
| ~2023-08-31~

-   Documentation added

## v1.0.2
| ~2023-08-31~

-   Fix README.md

## v1.0.1
| ~2023-08-31~

-   Remove noise outupt

## v1.0.0
| ~2023-08-31~

-   Initial release
