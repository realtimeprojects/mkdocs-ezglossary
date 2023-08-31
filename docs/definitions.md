# Definitions

terms:term
:   A term is a definition of a word in your glossary.

    The same term can be defined in multiple <terms:sections>

terms:section
:   ezglossary supports adding terms to different sections. This
    allows defining multiple glossaries and printing individual
    <term:summaries> for each section

terms:summary
:   The summary is a list of all defined terms in a <term:section>.
    
    It contains links to their <term:definitions> and <term:references>.

terms:definition
:   The definition of a term in a definition lists.

    The ezglossary plugin hooks in the html generation process,
    and looks for definition lists. In case it identifies
    a 

terms:reference
:   The reference is a place in your documentation where you
    refer to a term by placing a [link](usage.md#linking-to-a-glossary-entry).

## Summary

<glossary::terms>
