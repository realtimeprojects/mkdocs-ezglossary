# Default section

With the default configuration, only references with the syntax `section:term` are recognized
and processed by ezglossary. In order to activate parsing of all term definitions,
activate the 'default' section in the configuration:

``` yaml
plugins:
    ezglossary:
        use_default: true
```

## Definition

When activated, any term definition even without section identifier is recognized
and added to the 'default' section:

``` markdown
term
: definition of term
```

!!! Example

    term1
    : definition of term1

    term2
    : definition of term1

## Linking

Links to terms in the default section can be specified with the syntax:

    <term2:>
    <default:term2>

!!! Example

    - See the <term1:> or <default:root>

## Summary

In order to print the summary for the default section, use:

``` markdown
<glossary::_>
```

!!! Example

    <glossary::_>
